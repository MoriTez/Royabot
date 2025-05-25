import logging import os from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

توکن رباتت رو اینجا بذار

TOKEN = "7984089649:AAHk_xGlOxzfH4T1-OS3QJNnNVTFPeity2I"

فعال‌کردن لاگ‌گیری برای دیباگ

logging.basicConfig( format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO )

خوش‌آمدگویی و منوی شیشه‌ای اصلی

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("ارسال عکس چهره", callback_data='send_photo')], [InlineKeyboardButton("تحلیل شخصیت", callback_data='personality')], [InlineKeyboardButton("طالع بینی و فال", callback_data='astro')], [InlineKeyboardButton("افزایش کیفیت عکس", callback_data='enhance')] ] reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text( "به RoyaBot خوش اومدی! یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=reply_markup )

رسیدگی به انتخاب‌ها از منوی شیشه‌ای

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()

if query.data == 'send_photo':
    await query.edit_message_text("لطفاً یک عکس واضح از چهره‌ات بفرست تا تحلیل کنیم!")
elif query.data == 'personality':
    await query.edit_message_text("برای تحلیل شخصیت لطفاً به چند سوال جواب بده...")
elif query.data == 'astro':
    await query.edit_message_text("تاریخ تولدت رو بفرست (مثلاً: 1372/05/21) تا طالع‌بینی بشی!")
elif query.data == 'enhance':
    await query.edit_message_text("عکست رو بفرست تا کیفیتش رو بالا ببریم!")

پردازش عکس چهره

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE): photo = update.message.photo[-1] file = await context.bot.get_file(photo.file_id) await file.download_to_drive("user_photo.jpg")

await update.message.reply_text(
    "عکس شما با موفقیت دریافت شد. در حال پردازش...\n"
    "تحلیل چهره، فرم بینی و وضعیت روحی انجام شد (نسخه آزمایشی).\n"
    "برای دریافت تحلیل کامل، عضو کانال ما شوید: @soosssis"
)

راه‌اندازی ربات

async def main(): app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("ربات روشن است و منتظر پیام‌ها...")
await app.run_polling()

if name == 'main': import asyncio asyncio.run(main())

