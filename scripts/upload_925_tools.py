#!/usr/bin/env python3
"""
NEXUS God Mode — Upload 925 tools to xAI Collection
Run on T440:
  export XAI_API_KEY="YOUR_KEY"
  export XAI_MANAGEMENT_KEY="YOUR_MGMT_KEY"
  pip install xai-sdk
  python3 upload_925_tools.py
"""
import os, time
from xai_sdk import Client

client = Client()

print("Creating collection...")
collection = client.collections.create(
    name="NEXUS_TOOLS_KB_925",
    model_name="grok-embedding-small"
)
cid = collection.collection_id
print(f"Collection: {cid}")

INPUT = os.environ.get("TOOLS_FILE", "tools_v2_deduped.jsonl")
with open(INPUT, "r") as f:
    lines = f.readlines()

print(f"Records: {len(lines)}")
CHUNK = 90
total = (len(lines) - 1) // CHUNK + 1
ok = 0

for i in range(0, len(lines), CHUNK):
    chunk = lines[i:i+CHUNK]
    idx = i // CHUNK + 1
    name = f"nexus_tools_{idx:02d}.jsonl"
    data = "".join(chunk).encode("utf-8")
    try:
        client.collections.upload_document(cid, name=name, data=data)
        ok += 1
        print(f"  [{idx}/{total}] {name} ({len(chunk)} rec) OK")
    except Exception as e:
        print(f"  [{idx}/{total}] {name} ERR {str(e)[:120]}")
    time.sleep(1.5)

print(f"\nUpload: {ok}/{total} chunks")
print(f"Collection ID: {cid}")