from cryptography.fernet import Fernet
import os
from pathlib import Path

BASE_DIR = Path("./archivio")

def generate_key():
    return Fernet.generate_key()

def save_encrypted_file(client_name, filename, file_bytes, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(file_bytes)

    client_dir = BASE_DIR / client_name
    client_dir.mkdir(parents=True, exist_ok=True)
    encrypted_path = client_dir / f"{filename}.enc"

    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    return str(encrypted_path)

def decrypt_file(encrypted_path, key):
    cipher = Fernet(key)
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()
    return cipher.decrypt(encrypted_data)

def cleanup_client_files(client_name):
    client_dir = BASE_DIR / client_name
    if client_dir.exists():
        for file in client_dir.glob("*"):
            file.unlink()
        client_dir.rmdir()
