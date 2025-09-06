from telegram.ext import Updater, CommandHandler
import os

# Command handler
def start(update, context):
    update.message.reply_text("🤖 Hello! Your Railway bot is alive 🚂")

def help_command(update, context):
    update.message.reply_text("ℹ️ Available commands:\n/start - Welcome\n/help - Show this help")

if __name__ == "__main__":
    # Read bot token from environment variable
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN not set in environment variables!")

    # Create bot updater
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Start bot
    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()
