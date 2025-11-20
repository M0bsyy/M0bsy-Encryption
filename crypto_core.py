import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def derive_key(password: str) -> bytes:
    salt = b"CHANGE_THIS_SALT"
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1
    )
    return kdf.derive(password.encode())


def encrypt_file(data: bytes, master_key: bytes, use_xchacha=False):
    nonce = os.urandom(24 if use_xchacha else 12)

    if use_xchacha:
        cipher = ChaCha20Poly1305(master_key)
    else:
        cipher = AESGCM(master_key)

    ciphertext = cipher.encrypt(nonce, data, None)
    return nonce + ciphertext


def decrypt_file(blob: bytes, password: str, wrapped_key: bytes, use_xchacha=False):
    key = derive_key(password)
    enc_key = aes_key_unwrap(key, wrapped_key)

    nonce_size = 24 if use_xchacha else 12
    nonce = blob[:nonce_size]
    ciphertext = blob[nonce_size:]

    if use_xchacha:
        cipher = ChaCha20Poly1305(enc_key)
    else:
        cipher = AESGCM(enc_key)

    return cipher.decrypt(nonce, ciphertext, None)


def wrap_key(master_key: bytes, password: str):
    key = derive_key(password)
    return aes_key_wrap(key, master_key)
