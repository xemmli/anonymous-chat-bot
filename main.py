import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

user_pairs = {}
waiting_user = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام 👋\n"
        "به بات چت ناشناس خوش اومدی.\n\n"
        "برای شروع چت دستور /find رو بفرست\n"
        "برای قطع چت /stop"
    )

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_user
    user_id = update.message.chat_id

    if user_id in user_pairs:
        await update.message.reply_text("❗️الان توی چت هستی")
        return

    if waiting_user is None:
        waiting_user = user_id
        await update.message.reply_text("⏳ منتظر پیدا شدن طرف مقابل...")
    else:
        user_pairs[user_id] = waiting_user
        user_pairs[waiting_user] = user_id

        await context.bot.send_message(waiting_user, "✅ وصل شدی! شروع کن")
        await update.message.reply_text("✅ وصل شدی! شروع کن")

        waiting_user = None

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id in user_pairs:
        other = user_pairs[user_id]
        del user_pairs[user_id]
        del user_pairs[other]
        await context.bot.send_message(other, "❌ طرف مقابل چت رو ترک کرد")
        await update.message.reply_text("❌ چت بسته شد")
    else:
        await update.message.reply_text("❗️توی چتی نیستی")

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    if user_id in user_pairs:
        other = user_pairs[user_id]
        await context.bot.send_message(other, update.message.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay))

    app.run_polling()
      
