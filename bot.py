import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
    exit(1)

# ======================
# Command Handlers
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when /start is issued"""
    user = update.effective_user
    await update.message.reply_text(
        f"🌸 Welcome to Sakura Meme Coin Bot, {user.first_name}!\n\n"
        "I'm your gateway to the Sakura Meme Coin ecosystem.\n\n"
        "Use /help to see available commands"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help menu"""
    help_text = (
        "🌺 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help menu\n"
        "/price - Check current token price\n"
        "/buy - Purchase Sakura tokens\n"
        "/wallet - View your wallet balance\n"
        "/faq - Frequently asked questions\n\n"
        "🚀 Join our community: @SakuraMemeCoin"
    )
    await update.message.reply_text(help_text)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show current token price"""
    # In a real bot, you would fetch this from an API
    price_data = (
        "🌸 Sakura Meme Coin Price\n\n"
        "💵 Current Price: $0.0012\n"
        "📈 24h Change: +5.3%\n"
        "💼 Market Cap: $1.2M\n\n"
        "🔄 Update every 5 minutes"
    )
    await update.message.reply_text(price_data)

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user wallet balance"""
    # In a real bot, you would fetch from database
    wallet_info = (
        "👛 Your Sakura Wallet\n\n"
        "💰 Balance: 25,000 SAK\n"
        "💵 USD Value: $30.00\n\n"
        "🆔 Wallet Address: 0x742d...C8A9\n\n"
        "📥 Deposit / 📤 Withdraw using /transfer"
    )
    await update.message.reply_text(wallet_info)

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show frequently asked questions"""
    faq_text = (
        "❓ Frequently Asked Questions\n\n"
        "Q: What is Sakura Meme Coin?\n"
        "A: A community-driven meme coin with real utility.\n\n"
        "Q: How do I buy tokens?\n"
        "A: Use /buy command or visit our website.\n\n"
        "Q: Is there a staking program?\n"
        "A: Yes! Staking launches Q3 2025.\n\n"
        "🌐 Visit: sakuracoin.example.com"
    )
    await update.message.reply_text(faq_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle non-command messages"""
    text = update.message.text.lower()
    
    if any(keyword in text for keyword in ["hello", "hi", "hey"]):
        await update.message.reply_text("🌸 Konnichiwa! How can I help?")
    elif "price" in text:
        await price(update, context)
    elif "thank" in text:
        await update.message.reply_text("You're welcome! 🌸")
    else:
        await update.message.reply_text(
            "Sorry, I didn't understand that. Try /help for commands."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors"""
    logger.error(f"Update {update} caused error: {context.error}")
    await update.message.reply_text(
        "⚠️ An error occurred. Our team has been notified."
    )

# ======================
# Bot Initialization
# ======================
def main() -> None:
    """Start the bot"""
    # Create Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("wallet", wallet))
    application.add_handler(CommandHandler("faq", faq))
    
    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("🌸 Sakura Meme Coin Bot is running...")
    application.run_polling(
        poll_interval=3,
        timeout=30,
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
