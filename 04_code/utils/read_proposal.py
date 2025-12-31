
import os

file_path = "../99 Proposal.md"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        print(f.read())
else:
    print(f"File not found: {file_path}")
