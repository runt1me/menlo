#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# Load API key from .env (same directory as script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".menlo.env"))

API_KEY = os.getenv("MENLO_API_KEY")

def get_menlo_servers():
    servers = []
    for key, value in os.environ.items():
        if key.startswith("MENLO_SERVER_URL"):
            servers.append(value)

    return servers

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    MENLO_SERVERS = get_menlo_servers()

    if not API_KEY:
        print("Error: MENLO_API_KEY not found in .env")
        sys.exit(1)

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        headers = {"X-API-Key": API_KEY}

        for url in MENLO_SERVERS:
            # print(f"[*] Uploading {file_path} to {url}...")
            r = requests.post(url, headers=headers, files=files)

    if r.status_code != 201:
        print(f"[!] Upload failed: HTTP {r.status_code}")
        print(r.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
