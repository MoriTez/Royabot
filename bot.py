import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    InputFile,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)
from datetime import datetime
from features import (
    generate_motivation,
    analyze_personality,
    analyze_dream,
    zodiac_sign,
    countdown_to_100,
)

TOKEN = "7984089649:AAHk_xGlOxzfH4T1-OS3QJNnNVTFPeity2I"

CHANNEL_USERNAME = "@soosssis"
users = {}

keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("ارسال عکس چهره", callback_data="send_photo")],
    [InlineKeyboardButton("تست شخصیت", callback_data="personality_test"),
     InlineKeyboardButton("تحلیل خواب", callback_data="dream_test")],
    [InlineKeyboardButton("فال روزانه", callback_data="fortune"),
     InlineKeyboardButton("طالع تولد", callback_data="zodiac")],
    [InlineKeyboardButton("جمله انگیزشی", callback_data="motivation")],
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users[user_id] = {"photo_sent": False}
    await update.message.reply_text(
        "به RoyaBot خوش اومدی!\nبرای شروع از منوی زیر انتخاب کن:",
        reply_markup=keyboard,
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "send_photo":
        await query.message.reply_text("لطفا یک عکس از چهره‌ات بفرست.")
    elif data == "personality_test":
        await query.message.reply_text(analyze_personality())
    elif data == "dream_test":
        await query.message.reply_text(analyze_dream())
    elif data == "fortune":
        await query.message.reply_text("فال امروزت: فرصت‌هایی در راهه، آماده باش!")
    elif data == "zodiac":
        await query.message.reply_text("روز، ماه و سال تولدت رو اینطوری بفرست: `DD-MM-YYYY`", parse_mode="Markdown")
    elif data == "motivation":
        await query.message.reply_text(generate_motivation())

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if users.get(user_id, {}).get("photo_sent"):
        await update.message.reply_text(
            "برای دریافت تحلیل کامل، عضو کانال زیر شو:\n" + CHANNEL_USERNAME,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")]
            ])
        )
        return

    photo = update.message.photo[-1]
    file = await photo.get_file()
    await file.download_to_drive("user_photo.jpg")

    users[user_id]["photo_sent"] = True

    await update.message.reply_text(
        "عکس شما با موفقیت دریافت شد. در حال پردازش...\n"
        "تحلیل چهره و فرم بینی شما انجام شد (نسخه نمونه)."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        day, month, year = map(int, text.split("-"))
        birthdate = datetime(year, month, day)
        zodiac, description = zodiac_sign(day, month)
        countdown = countdown_to_100(birthdate)
        await update.message.reply_text(
            f"ماه تولد شما: {zodiac}\nویژگی‌ها: {description}\n{countdown}"
        )
    except:
        await update.message.reply_text("فرمت تولد درست نیست. به صورت `DD-MM-YYYY` بفرست.", parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("ربات در حال اجراست...")
    app.run_polling()
