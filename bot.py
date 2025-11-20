import os
import qrcode
from telegram.ext import *
from config import *
from crypto_core import *


def start(update, ctx):
    update.message.reply_text("Send a file to ENCRYPT.\nUse /decrypt <password> to decrypt.")


def encrypt_cmd(update, ctx):
    update.message.reply_text("Send the file you want to encrypt.")


def decrypt_cmd(update, ctx):
    update.message.reply_text("Send the encrypted file and use /decrypt <password>")


def send_qr(update, ctx):
    if update.effective_user.id != OWNER_ID:
        return update.message.reply_text("Not allowed.")

    img = qrcode.make(MASTER_KEY.hex())
    path = "key.png"
    img.save(path)

    update.message.reply_document(open(path, "rb"))
    os.remove(path)


def handle_file(update, ctx):
    file = update.message.document.get_file()
    data = file.download_as_bytearray()

    encrypted = encrypt_file(bytes(data), MASTER_KEY)

    filename = file.file_path.split('/')[-1] + ".enc"
    path = f"/tmp/{filename}"

    with open(path, "wb") as f:
        f.write(encrypted)

    update.message.reply_document(open(path, "rb"))
    os.remove(path)


def decrypt_file_handler(update, ctx):
    if update.effective_user.id != OWNER_ID:
        return update.message.reply_text("Only the owner can decrypt files.")

    try:
        password = ctx.args[0]
    except:
        return update.message.reply_text("Usage: /decrypt <password>")

    file = update.message.document.get_file()
    blob = file.download_as_bytearray()

    wrapped = wrap_key(MASTER_KEY, password)
    decrypted = decrypt_file(bytes(blob), password, wrapped)

    filename = file.file_path.split('/')[-1].replace(".enc", "")
    path = f"/tmp/{filename}"

    with open(path, "wb") as f:
        f.write(decrypted)

    update.message.reply_document(open(path, "rb"))
    os.remove(path)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("encrypt", encrypt_cmd))
    app.add_handler(CommandHandler("decrypt", decrypt_cmd))
    app.add_handler(CommandHandler("keyqr", send_qr))

    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    app.run_polling()


if __name__ == "__main__":
    main()
