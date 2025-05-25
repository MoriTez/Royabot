import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import os

# تنظیم لاگ برای خطاها و دیباگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# نام کانال شما
CHANNEL_USERNAME = "@soosssis"

# متغیرها برای ذخیره وضعیت کاربر (مثلاً آیا عکس فرستاده یا نه)
user_data = {}

# پیام خوش آمدگویی وقتی کاربر استارت میزند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data[user.id] = {"photo_received": False}
    welcome_text = f"سلام {user.first_name}! خوش آمدی به RoyaBot. لطفا یک عکس از چهره خودت بفرست تا تحلیل نمونه بگیری."
    
    # منوی شیشه‌ای پایین
    keyboard = [
        [InlineKeyboardButton("تحلیل نمونه", callback_data='sample_analysis')],
        [InlineKeyboardButton("قوانین کانال", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
        [InlineKeyboardButton("راهنما", callback_data='help')],
        [InlineKeyboardButton("تماس با ما", callback_data='contact')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "sample_analysis":
        await query.edit_message_text("برای دریافت تحلیل نمونه لطفا یک عکس از چهره خود ارسال کنید.")
    elif query.data == "help":
        await query.edit_message_text("این ربات می‌تواند چهره شما را تحلیل کند، تست روانشناسی بدهد، طالع‌بینی کند و...")
    elif query.data == "contact":
        await query.edit_message_text("برای تماس با ما، لطفا به این شماره پیام دهید: +98XXXXXXXXXX")

# هندلر دریافت عکس
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_data:
        user_data[user.id] = {"photo_received": False}
    user_data[user.id]["photo_received"] = True
    
    # ذخیره عکس در فولدر photos با نام user_id.jpg
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"photos/{user.id}.jpg"
    os.makedirs("photos", exist_ok=True)
    await photo_file.download_to_drive(photo_path)
    
    # پیام نمونه تحلیل و دعوت به کانال
    msg = ("عکس شما با موفقیت دریافت شد. در حال پردازش...\n"
           "تحلیل چهره و فرم بینی شما انجام شد (نسخه نمونه).\n\n"
           "برای دریافت تحلیل کامل، لطفا عضو کانال زیر شوید:\n"
           f"{CHANNEL_USERNAME}\n"
           "سپس دوباره عکس ارسال کنید.")
    await update.message.reply_text(msg)

# هندلر پیام‌های غیر از عکس و دستور
async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا فقط عکس چهره خود را ارسال کنید یا از منوی پایین استفاده کنید.")

def main():
    # توکن ربات خودت رو اینجا بگذار
    TOKEN = "7984089649:AAHk_xGlOxzfH4T1-OS3QJNnNVTFPeity2I"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    app.add_handler(MessageHandler(filters.ALL & (~filters.PHOTO) & (~filters.COMMAND), unknown_handler))
    
    print("ربات روشن است و منتظر پیام‌ها...")
    app.run_polling()

if __name__ == "__main__":
    main()
