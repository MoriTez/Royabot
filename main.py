import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from features import analyze_personality, analyze_dream, zodiac_sign, generate_motivation, countdown_to_100, save_user_info

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@soosssis"
ADMINS = [7984089649]

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📷 ارسال عکس چهره", callback_data="send_photo")],
    [InlineKeyboardButton("🧠 تست شخصیت", callback_data="personality_test"),
     InlineKeyboardButton("🌙 تحلیل خواب", callback_data="dream_test")],
    [InlineKeyboardButton("🪐 طالع تولد", callback_data="zodiac"),
     InlineKeyboardButton("📜 فال روزانه", callback_data="fortune")],
    [InlineKeyboardButton("🎯 جمله انگیزشی", callback_data="motivation")]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = user.id
    await save_user_info(user, context.bot)
    await update.message.reply_text(
        f"سلام {user.first_name} 👋 به ربات Roya خوش اومدی!
از منوی زیر انتخاب کن:",
        reply_markup=keyboard
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "send_photo":
        await query.message.reply_text("لطفاً عکس چهره‌ات رو بفرست.")
    elif data == "personality_test":
        await query.message.reply_text(analyze_personality())
    elif data == "dream_test":
        await query.message.reply_text(analyze_dream())
    elif data == "zodiac":
        await query.message.reply_text("روز، ماه و سال تولدت رو اینطوری بفرست: `DD-MM-YYYY`", parse_mode="Markdown")
    elif data == "motivation":
        await query.message.reply_text(generate_motivation())
    elif data == "fortune":
        await query.message.reply_text("💫 امروزت روشنه، اتفاقات خوب در راهه!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    user = update.message.from_user
    file = await photo.get_file()
    filepath = f"photos/{user.id}.jpg"
    os.makedirs("photos", exist_ok=True)
    await file.download_to_drive(filepath)
    await update.message.reply_text("📸 عکس دریافت شد! در حال تحلیل هستیم... (نسخه کامل به‌زودی)")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        day, month, year = map(int, text.split("-"))
        zodiac, description = zodiac_sign(day, month)
        countdown = countdown_to_100(day, month, year)
        await update.message.reply_text(f"♓️ ماه تولد شما: {zodiac}
🔮 ویژگی‌ها: {description}
{countdown}")
    except:
        await update.message.reply_text("فرمت تولد اشتباهه. به صورت `DD-MM-YYYY` بفرست.", parse_mode="Markdown")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMINS:
        message = ' '.join(context.args)
        with open("data/users.txt", "r") as f:
            ids = [int(i.strip()) for i in f.readlines()]
        for uid in ids:
            try:
                await context.bot.send_message(chat_id=uid, text=message)
            except:
                continue
        await update.message.reply_text("📣 پیام تبلیغاتی ارسال شد.")
    else:
        await update.message.reply_text("⛔️ شما دسترسی ندارید.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()