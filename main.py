# -*- coding: utf-8 -*-
import argparse
import hashlib
import io
import math
import os
import sys
import time
import requests

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-16"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

AUTHOR = "Baim Market"
BASE_URL = "https://sfile.co"
UPLOAD_URL = f"{BASE_URL}/upload/resume_v1_guest.php"
CHUNK_SIZE = 1024 * 1024
MAX_FILE_SIZE = 250 * 1024 * 1024

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Referer": f"{BASE_URL}/",
    "Origin": BASE_URL,
}


def log(msg: str):
    print(f"[author : {AUTHOR}] {msg}")


def compute_md5(path: str) -> str:
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def check_hash(session: requests.Session, file_hash: str, filename: str) -> dict:
    resp = session.post(
        UPLOAD_URL,
        data={
            "intent": "check-hash",
            "file_hash": file_hash,
            "file_name": filename,
        },
        headers=HEADERS,
        timeout=30,
    )

    if resp.status_code == 409:
        try:
            data = resp.json()
            data["_duplicate"] = True
            return data
        except Exception:
            return {"_duplicate": True, "raw": resp.text}

    resp.raise_for_status()

    try:
        return resp.json()
    except Exception:
        return {"raw": resp.text}


def upload_chunk(
    session: requests.Session,
    path: str,
    chunk_index: int,
    total_chunks: int,
    file_size: int,
    file_hash: str,
    filename: str,
    description: str,
    identifier: str,
) -> requests.Response:

    offset = (chunk_index - 1) * CHUNK_SIZE

    with open(path, "rb") as f:
        f.seek(offset)
        chunk_data = f.read(CHUNK_SIZE)

    params = {
        "flowChunkNumber": chunk_index,
        "flowChunkSize": CHUNK_SIZE,
        "flowCurrentChunkSize": len(chunk_data),
        "flowTotalSize": file_size,
        "flowIdentifier": identifier,
        "flowFilename": filename,
        "flowRelativePath": filename,
        "flowTotalChunks": total_chunks,
        "des": description,
        "file_hash": file_hash,
        "desired_name": filename,
    }

    files = {
        "file": (
            filename,
            chunk_data,
            "application/octet-stream"
        )
    }

    return session.post(
        UPLOAD_URL,
        data=params,
        files=files,
        headers=HEADERS,
        timeout=120,
    )


def chunk_exists(
    session: requests.Session,
    chunk_index: int,
    total_chunks: int,
    file_size: int,
    identifier: str,
    filename: str,
) -> bool:

    params = {
        "flowChunkNumber": chunk_index,
        "flowChunkSize": CHUNK_SIZE,
        "flowCurrentChunkSize": min(
            CHUNK_SIZE,
            file_size - (chunk_index - 1) * CHUNK_SIZE
        ),
        "flowTotalSize": file_size,
        "flowIdentifier": identifier,
        "flowFilename": filename,
        "flowRelativePath": filename,
        "flowTotalChunks": total_chunks,
    }

    try:
        resp = session.get(
            UPLOAD_URL,
            params=params,
            headers=HEADERS,
            timeout=15,
        )
        return resp.status_code == 200
    except Exception:
        return False


def build_identifier(filename: str, file_size: int) -> str:
    cleaned = "".join(
        c if c.isalnum() else "_"
        for c in filename
    )
    return f"{file_size}-{cleaned}"


def extract_url(payload: dict) -> str | None:
    if not isinstance(payload, dict):
        return None

    if payload.get("share_url"):
        return payload["share_url"]

    if (
        isinstance(payload.get("actions"), dict)
        and payload["actions"].get("view")
    ):
        return payload["actions"]["view"]

    if isinstance(payload.get("file"), dict):
        file_obj = payload["file"]

        if file_obj.get("download_url"):
            return file_obj["download_url"]

        if file_obj.get("short"):
            return f"{BASE_URL}/{file_obj['short']}"

    if payload.get("file_short"):
        return f"{BASE_URL}/{payload['file_short']}"

    for key in ("url", "link", "download_url"):
        val = payload.get(key)

        if isinstance(val, str) and val.startswith("http"):
            return val

    return None


def upload_file(path: str, description: str = "") -> str | None:

    if not os.path.isfile(path):
        log(f"File tidak ada: {path}")
        return None

    file_size = os.path.getsize(path)
    filename = os.path.basename(path)

    if file_size > MAX_FILE_SIZE:
        log(
            f"Ukuran file {file_size} bytes "
            f"melampaui limit 250 MB."
        )
        return None

    log(f"Target: {filename} ({file_size} bytes)")

    session = requests.Session()

    file_hash = compute_md5(path)
    log(f"MD5 hash: {file_hash}")

    hash_check = check_hash(
        session,
        file_hash,
        filename
    )

    if hash_check.get("duplicate") or hash_check.get("_duplicate"):
        log("File duplikat terdeteksi di server.")

        url = extract_url(hash_check)

        if url:
            log(f"Download URL: {url}")
            return url

        log(f"Response: {hash_check}")
        return str(hash_check)

    total_chunks = math.ceil(
        file_size / CHUNK_SIZE
    ) or 1

    identifier = build_identifier(
        filename,
        file_size
    )

    log(
        f"Mulai upload {total_chunks} chunk..."
    )

    final_url = None

    for i in range(1, total_chunks + 1):

        if chunk_exists(
            session,
            i,
            total_chunks,
            file_size,
            identifier,
            filename,
        ):
            log(
                f"Chunk {i}/{total_chunks} "
                f"dilewati (sudah ada)"
            )
            continue

        resp = upload_chunk(
            session,
            path,
            i,
            total_chunks,
            file_size,
            file_hash,
            filename,
            description,
            identifier,
        )

        if resp.status_code not in (200, 201):

            if resp.status_code >= 500:
                log(
                    f"Server error pada chunk {i}, retry..."
                )

                time.sleep(2)

                resp = upload_chunk(
                    session,
                    path,
                    i,
                    total_chunks,
                    file_size,
                    file_hash,
                    filename,
                    description,
                    identifier,
                )

            if resp.status_code not in (200, 201):
                log(
                    f"Gagal upload chunk {i}: "
                    f"HTTP {resp.status_code}"
                )
                return None

        log(
            f"Chunk {i}/{total_chunks} "
            f"terkirim (HTTP {resp.status_code})"
        )

        try:
            body = resp.json()

            found = extract_url(body)

            if found:
                final_url = found

        except Exception:

            if resp.text.strip().startswith("http"):
                final_url = resp.text.strip()

    if final_url:
        log(f"Upload selesai: {final_url}")
        return final_url

    log(
        "Upload selesai, URL tidak terbaca di response."
    )

    return None


def main():

    parser = argparse.ArgumentParser(
        description="Baim Market - Upload file ke sfile.co"
    )

    parser.add_argument(
        "file",
        help="File yang akan di-upload"
    )

    parser.add_argument(
        "description",
        nargs="?",
        default="",
        help="Deskripsi file"
    )

    args = parser.parse_args()

    result = upload_file(
        args.file,
        args.description
    )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
