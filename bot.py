import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import datetime
import random

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@soosssis"  # نام کانال برای چک کردن عضویت

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# فال حافظ نمونه
HAFEZ_FAL = [
    "اگر آن ترک شیرازی به دست آرد دل ما را...",
    "الا یا ایها الساقی ادر کاسا و ناولها...",
    "دوش دیدم که ملائک در میخانه زدند...",
]

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("تحلیل چهره", callback_data='face_analysis')],
        [InlineKeyboardButton("فال حافظ", callback_data='hafez')],
        [InlineKeyboardButton("تحلیل تولد", callback_data='birthday_analysis')],
        [InlineKeyboardButton("فرم بینی", callback_data='nose_shape')],
        [InlineKeyboardButton("اطلاعات بیشتر", callback_data='more_info')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! خوش آمدید به RoyaBot\nلطفا یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=get_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'face_analysis':
        await query.edit_message_text("لطفا یک عکس از چهره خود ارسال کنید تا تحلیل شود.")
    elif query.data == 'hafez':
        await query.edit_message_text("برای گرفتن فال حافظ لطفا کلمه 'فال' را ارسال کنید.")
    elif query.data == 'birthday_analysis':
        await query.edit_message_text("لطفا تاریخ تولد خود را به صورت YYYY-MM-DD ارسال کنید.")
    elif query.data == 'nose_shape':
        await query.edit_message_text("لطفا عکس بینی خود را ارسال کنید تا فرم بینی بررسی شود.")
    elif query.data == 'more_info':
        await query.edit_message_text("ربات RoyaBot می‌تواند چهره، تولد، و فال حافظ را تحلیل کند.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id

    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
        if member.status not in ('member', 'creator', 'administrator'):
            raise Exception("عضو کانال نیست")
    except Exception:
        await update.message.reply_text(
            f"برای استفاده از این قابلیت، ابتدا باید عضو کانال {CHANNEL_USERNAME} باشید.\n"
            f"لطفا عضو کانال شوید و دوباره عکس خود را ارسال کنید."
        )
        return

    # اگر عضو بود عکس را ذخیره کن
    photos_dir = "photos"
    os.makedirs(photos_dir, exist_ok=True)

    photo_file = await update.message.photo[-1].get_file()
    file_path = os.path.join(photos_dir, f"{user.id}_{photo_file.file_id}.jpg")
    await photo_file.download_to_drive(file_path)

    await update.message.reply_text("عکس شما با موفقیت دریافت شد. در حال پردازش...")

    # تحلیل نمونه
    await update.message.reply_text("تحلیل چهره و فرم بینی شما انجام شد (نسخه نمونه).")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == 'فال':
        fal = random.choice(HAFEZ_FAL)
        await update.message.reply_text(f"فال حافظ شما:\n\n{fal}")
    elif len(text) == 10 and text[4] == '-' and text[7] == '-':
        try:
            date = datetime.datetime.strptime(text, "%Y-%m-%d").date()
            age = (datetime.date.today() - date).days // 365
            await update.message.reply_text(
                f"تحلیل تولد:\nشما {age} سال دارید.\nتاریخ تولد: {date.strftime('%Y-%m-%d')}\n"
                "شما فردی خوش‌شانس و پرانرژی هستید (نمونه تحلیل)."
            )
        except Exception:
            await update.message.reply_text("فرمت تاریخ تولد نادرست است. لطفا به صورت YYYY-MM-DD وارد کنید.")
    else:
        await update.message.reply_text(
            "دستور شناخته نشده است.\nلطفا از منوی شیشه‌ای استفاده کنید یا دستور مناسب ارسال کنید."
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("ربات در حال اجراست...")
    app.run_polling()
