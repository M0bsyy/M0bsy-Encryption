import os
import qrcode
import tempfile
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from crypto_utils import encrypt_file, decrypt_file
from config import BOT_TOKEN, MASTER_KEY, CHAT_ID

bot = Bot(token=BOT_TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🔐 Welcome to M0bsy Encryption Bot!\nSend me a file to encrypt or decrypt.")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document
    file_path = file.get_file().download()
    update.message.reply_text("File received. Type /encrypt or /decrypt to choose an action.")
    context.user_data["file_path"] = file_path

def encrypt_command(update: Update, context: CallbackContext):
    file_path = context.user_data.get("file_path")
    if not file_path:
        update.message.reply_text("Please send a file first.")
        return
    output_file = encrypt_file(file_path, MASTER_KEY)
    bot.send_document(chat_id=update.effective_chat.id, document=open(output_file, "rb"))
    update.message.reply_text("✅ File encrypted successfully.")

def decrypt_command(update: Update, context: CallbackContext):
    file_path = context.user_data.get("file_path")
    if not file_path:
        update.message.reply_text("Please send a file first.")
        return
    output_file = decrypt_file(file_path, MASTER_KEY)
    bot.send_document(chat_id=update.effective_chat.id, document=open(output_file, "rb"))
    update.message.reply_text("✅ File decrypted successfully.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("encrypt", encrypt_command))
    dp.add_handler(CommandHandler("decrypt", decrypt_command))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
