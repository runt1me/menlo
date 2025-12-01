#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

# Load API key from .env (same directory as script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".menlo.env"))

API_KEY = os.getenv("MENLO_API_KEY")
SERVER_URL = os.getenv("MENLO_SERVER_URL", "http://192.168.188.128:5000/push")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    if not API_KEY:
        print("Error: MENLO_API_KEY not found in .env")
        sys.exit(1)

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        headers = {"X-API-Key": API_KEY}

        # print(f"[*] Uploading {file_path} to {SERVER_URL}...")
        r = requests.post(SERVER_URL, headers=headers, files=files)

    if r.status_code != 201:
        print(f"[!] Upload failed: HTTP {r.status_code}")
        print(r.text)
        sys.exit(1)

    # print("[+] Success!")
    # print(r.json())

if __name__ == "__main__":
    main()
