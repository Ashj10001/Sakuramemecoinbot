import os
import re
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes, 
    CallbackQueryHandler, MessageHandler, filters
)

# Attempt to import MongoDB or use fallback
try:
    from pymongo import MongoClient
    MONGO_ENABLED = True
except ImportError:
    MONGO_ENABLED = False
    print("Warning: pymongo not installed. Using in-memory database")

# Configuration
BOT_TOKEN = "7872973965:AAGt3KFPosFSYV1w4Ded-_tD8QtUHasei9s"
WEBSITE_LINK = "https://stirring-jelly-a235d8.netlify.app/"
CHANNEL_LINK = "https://t.me/sakuramemecoin"
GROUP_LINK = "https://t.me/Sakuramemecoincommunity"
TWITTER_LINK = "https://x.com/Sukuramemecoin"
PUMP_FUN_LINK = "https://pump.fun/2AXnWVULFu5kJf7Z3LA9WXxF47XLYXoNAyMQZuZjpump"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database setup
if MONGO_ENABLED and "MONGO_URI" in os.environ:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client.sakuramemecoin_bot
    users = db.users
    logger.info("Using MongoDB database")
else:
    users = {}
    logger.warning("Using in-memory database - data will not persist!")

# Verification statuses
STATUS_START, STATUS_CHANNEL, STATUS_GROUP, STATUS_TWITTER, STATUS_SOL_ADDRESS = range(5)

# SOL address validation regex
SOL_REGEX = r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with join menu when the command /start is issued."""
    user = update.effective_user
    context.user_data['status'] = STATUS_START
    
    keyboard = [
        [InlineKeyboardButton("🌸 Telegram Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("🌸 Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🌸 Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("🚀 Start Verification", callback_data='start_verification')],
        [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)]
    ]
    
    await update.message.reply_html(
        f"🌸 <b>Welcome to Sakuramemecoin Airdrop, {user.first_name}!</b> 🌸\n\n"
        "To qualify for <b>0.01 SOL reward</b>:\n\n"
        "1️⃣ Join our Telegram channel\n"
        "2️⃣ Join our Telegram group\n"
        "3️⃣ Follow our Twitter\n"
        "4️⃣ Submit your SOL address\n\n"
        "<b>Click below to access all links and begin verification:</b>",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# [Rest of the code remains the same as your reference implementation]
# ... (verify_channel, check_channel, verify_group, etc.)

def save_user_data(user_id, data):
    """Save user data to MongoDB or in-memory store"""
    if MONGO_ENABLED and "MONGO_URI" in os.environ:
        users.update_one({"user_id": user_id}, {"$set": data}, upsert=True)
    else:
        users[user_id] = data

async def handle_sol_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process submitted SOL address."""
    if context.user_data.get('status') != STATUS_SOL_ADDRESS:
        return
    
    user = update.effective_user
    message = update.message.text.strip()
    
    # Extract SOL address
    if message.startswith("Solana: "):
        sol_address = message.replace("Solana: ", "")
    else:
        sol_address = message
    
    # Validate SOL address
    if not re.match(SOL_REGEX, sol_address):
        await update.message.reply_text(
            "❌ Invalid SOL address format! Please send a valid Solana mainnet address.\n"
            "Example: `Solana: 7sPmqkM71YkGZ6J2XbkR5ZaYnXrFq2AZeQz3JmFd9XrR`",
            parse_mode="Markdown"
        )
        return
    
    # Save user data
    user_data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "sol_address": sol_address,
        "completed": True,
        "reward_sent": False,
        "timestamp": time.time()
    }
    save_user_data(user.id, user_data)
    
    # Success message
    keyboard = [
        [InlineKeyboardButton("🚀 Buy on Pump.fun", url=PUMP_FUN_LINK)],
        [InlineKeyboardButton("🌐 Visit Website", url=WEBSITE_LINK)]
    ]
    
    await update.message.reply_text(
        "🎉 Congratulations! 0.01 SOL is on its way to your wallet!\n\n"
        "Don't forget to buy our token on Pump.fun:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    # Clear user data
    context.user_data.clear()

# [Rest of the code remains unchanged]

if __name__ == '__main__':
    # Create and start the bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sol_address))
    
    logger.info("Starting bot...")
    application.run_polling()
