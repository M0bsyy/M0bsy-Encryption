# M0bsy-Encryption

A secure Telegram bot that encrypts & decrypts files using AES-256 and password-wrapped master keys.

---

## 🚀 Features
- AES-256-GCM encryption
- Password-protected decryption
- XChaCha20 optional mode
- QR key export
- Owner-only decryption
- Termux, Linux, Windows supported

---

## 📌 Install (Termux / Linux)

```bash
pkg update -y

pkg install python git -y
    # Termux: or apt-get on server

git clone https://github.com/M0bsyy/M0bsy-Encryption.git

cd M0bsy-Encryption

pip install -r requirements.txt
