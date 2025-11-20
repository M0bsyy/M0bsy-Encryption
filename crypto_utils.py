from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import os

def derive_key(master_key: str):
    return sha256(master_key.encode()).digest()

def encrypt_file(input_path, master_key):
    key = derive_key(master_key)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f:
        data = f.read()

    encrypted_data = iv + encryptor.update(data) + encryptor.finalize()
    output_path = input_path + ".enc"

    with open(output_path, 'wb') as f:
        f.write(encrypted_data)

    return output_path

def decrypt_file(input_path, master_key):
    key = derive_key(master_key)
    with open(input_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    output_path = input_path.replace(".enc", ".dec")

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

    return output_path
