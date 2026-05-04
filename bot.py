import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎬 Video yubor — men URL beraman")

@bot.message_handler(content_types=['video', 'document', 'audio', 'photo'])
def get_file_url(message):
    try:
        if message.video:
            file_id = message.video.file_id
        elif message.document:
            file_id = message.document.file_id
        elif message.audio:
            file_id = message.audio.file_id
        elif message.photo:
            file_id = message.photo[-1].file_id

        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        bot.send_message(message.chat.id, f"🔗 URL:\n{file_url}")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Xatolik")

bot.infinity_polling()
