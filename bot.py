
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deepface import DeepFace

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به RoyaBot خوش اومدی. من با دریافت عکس چهره‌ات می‌تونم تحلیل شخصیت و وضعیت روحی‌ات رو بگم.\n"
        "لطفاً عکست رو بدون عینک و نور مناسب ارسال کن.\n\n"
        "نکات عکاسی:\n"
        "- صورتت کامل داخل عکس باشه\n"
        "- روبروی دوربین بایست\n"
        "- نور طبیعی یا سفید\n"
        "- بدون فیلتر یا افکت"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_path = f"{update.message.from_user.id}.jpg"
    await file.download_to_drive(image_path)

    try:
        result = DeepFace.analyze(img_path=image_path, actions=['emotion', 'age', 'gender'], enforce_detection=False)
        msg = result[0]
        await update.message.reply_text(
            f"تحلیل چهره:\n"
            f"- جنسیت: {msg['gender']}\n"
            f"- سن تقریبی: {msg['age']}\n"
            f"- احساس غالب: {msg['dominant_emotion']}"
        )
    except Exception as e:
        await update.message.reply_text(f"خطا در تحلیل چهره: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
