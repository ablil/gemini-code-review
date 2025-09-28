import hashlib

def hash_diff(diff: str) -> str:
    return hashlib.sha256(diff.encode("utf-8")).hexdigest()
