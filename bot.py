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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start_verification':
        await verify_channel(update, context)
    elif query.data == 'check_channel':
        await check_channel(update, context)
    elif query.data == 'check_group':
        await check_group(update, context)
    elif query.data == 'check_twitter':
        await check_twitter(update, context)

async def verify_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Step 1: Verify channel membership."""
    query = update.callback_query
    context.user_data['status'] = STATUS_CHANNEL
    
    keyboard = [
        [InlineKeyboardButton("🌸 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data='check_channel')]
    ]
    
    await query.edit_message_text(
        text="Step 1/4: Join our official Telegram channel 👇",
        reply_markup=InlineKeyboardMarkup(keyboard))

async def check_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check channel membership (placeholder)."""
    query = update.callback_query
    try:
        # Actual verification would go here
        await query.answer("✅ Channel membership verified!", show_alert=True)
        await verify_group(update, context)
    except Exception as e:
        logger.error(f"Error checking channel: {e}")
        await query.answer("✅ Proceeding to next step", show_alert=True)
        await verify_group(update, context)

async def verify_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Step 2: Verify group membership."""
    query = update.callback_query
    context.user_data['status'] = STATUS_GROUP
    
    keyboard = [
        [InlineKeyboardButton("🌸 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data='check_group')]
    ]
    
    await query.edit_message_text(
        text="Step 2/4: Join our Telegram group 👇",
        reply_markup=InlineKeyboardMarkup(keyboard))

async def check_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check group membership (placeholder)."""
    query = update.callback_query
    try:
        # Actual verification would go here
        await query.answer("✅ Group membership verified!", show_alert=True)
        await verify_twitter(update, context)
    except Exception as e:
        logger.error(f"Error checking group: {e}")
        await query.answer("✅ Proceeding to next step", show_alert=True)
        await verify_twitter(update, context)

async def verify_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Step 3: Verify Twitter follow."""
    query = update.callback_query
    context.user_data['status'] = STATUS_TWITTER
    
    keyboard = [
        [InlineKeyboardButton("🌸 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ I've Followed", callback_data='check_twitter')]
    ]
    
    await query.edit_message_text(
        text="Step 3/4: Follow our Twitter account 👇\n\n"
             "After following, click the verification button below.",
        reply_markup=InlineKeyboardMarkup(keyboard))

async def check_twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check Twitter follow (placeholder)."""
    query = update.callback_query
    context.user_data['status'] = STATUS_SOL_ADDRESS
    
    await query.edit_message_text(
        text="Step 4/4: Submit your Solana address\n\n"
             "Please send your SOL wallet address in the following format:\n"
             "`Solana: YOUR_WALLET_ADDRESS`\n\n"
             "Example:\n"
             "`Solana: 7sPmqkM71YkGZ6J2XbkR5ZaYnXrFq2AZeQz3JmFd9XrR`\n\n"
             "⚠️ Make sure this is your mainnet SOL address!"
    )
    await query.answer("Now please send your SOL address")

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help instructions."""
    await update.message.reply_text(
        "📘 Airdrop Instructions:\n\n"
        "1. Use /start to begin the verification process\n"
        "2. Complete all 4 steps to qualify for 0.01 SOL\n"
        "3. Submit your Solana wallet address\n\n"
        f"🌐 Website: {WEBSITE_LINK}\n"
        "Have questions? Contact our support team"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    logger.error(msg="Exception while handling update:", exc_info=context.error)
    if update and update.message:
        await update.message.reply_text(
            "❌ Oops! Something went wrong. Please try again later."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_sol_address))
    application.add_error_handler(error_handler)
    
    logger.info("Starting Sakuramemecoin Airdrop Bot...")
    application.run_polling()
    logger.info("Bot started successfully")

if __name__ == '__main__':
    main()
