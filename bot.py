import os
import re
import logging
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, 
    CallbackQueryHandler, MessageHandler, Filters
)
from pymongo import MongoClient

# Configuration - Get from Render environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
GROUP_ID = os.getenv("GROUP_ID")
ADMIN_ID = os.getenv("ADMIN_ID")
MONGO_URI = os.getenv("MONGO_URI")

# Fixed URLs
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
client = MongoClient(MONGO_URI)
db = client.sakuramemecoin_bot
users = db.users

# Verification statuses
STATUS_START, STATUS_CHANNEL, STATUS_GROUP, STATUS_TWITTER, STATUS_SOL_ADDRESS = range(5)

# SOL address validation regex
SOL_REGEX = r"^[1-9A-HJ-NP-Za-km-z]{32,44}$"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    context.user_data['status'] = STATUS_START
    
    keyboard = [[InlineKeyboardButton("🌟 Start Verification", callback_data='start_verification')]]
    
    update.message.reply_text(
        f"🌸 Welcome to Sakuramemecoin Airdrop, {user.first_name}!\n\n"
        "To qualify for 0.01 SOL reward:\n\n"
        "1. Join our Telegram channel\n"
        "2. Join our Telegram group\n"
        "3. Follow our Twitter\n"
        "4. Submit your SOL address\n\n"
        "Click below to begin verification 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'start_verification':
        verify_channel(update, context)
    elif query.data == 'check_channel':
        check_channel(update, context)
    elif query.data == 'check_group':
        check_group(update, context)
    elif query.data == 'check_twitter':
        check_twitter(update, context)

def verify_channel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    context.user_data['status'] = STATUS_CHANNEL
    
    keyboard = [
        [InlineKeyboardButton("🌸 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data='check_channel')]
    ]
    
    query.edit_message_text(
        text="Step 1/4: Join our official channel 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def check_channel(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    try:
        # For now, skip actual check - implement later
        verify_group(update, context)
    except Exception as e:
        logger.error(f"Error checking channel: {e}")
        update.callback_query.answer("✅ Proceeding to next step", show_alert=True)
        verify_group(update, context)

def verify_group(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    context.user_data['status'] = STATUS_GROUP
    
    keyboard = [
        [InlineKeyboardButton("🌸 Join Group", url=GROUP_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data='check_group')]
    ]
    
    query.edit_message_text(
        text="Step 2/4: Join our community group 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def check_group(update: Update, context: CallbackContext) -> None:
    try:
        # For now, skip actual check - implement later
        verify_twitter(update, context)
    except Exception as e:
        logger.error(f"Error checking group: {e}")
        update.callback_query.answer("✅ Proceeding to next step", show_alert=True)
        verify_twitter(update, context)

def verify_twitter(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    context.user_data['status'] = STATUS_TWITTER
    
    keyboard = [
        [InlineKeyboardButton("🌸 Follow Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ I've Followed", callback_data='check_twitter')]
    ]
    
    query.edit_message_text(
        text="Step 3/4: Follow our Twitter account 👇\n\n"
             "After following, click the verification button below.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def check_twitter(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    context.user_data['status'] = STATUS_SOL_ADDRESS
    
    query.edit_message_text(
        text="Step 4/4: Submit your Solana address\n\n"
             "Please send your SOL wallet address in the following format:\n"
             "`Solana: YOUR_WALLET_ADDRESS`\n\n"
             "Example:\n"
             "`Solana: 7sPmqkM71YkGZ6J2XbkR5ZaYnXrFq2AZeQz3JmFd9XrR`\n\n"
             "⚠️ Make sure this is your mainnet SOL address!"
    )
    query.answer("Now please send your SOL address")

def handle_sol_address(update: Update, context: CallbackContext) -> None:
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
        update.message.reply_text(
            "❌ Invalid SOL address format! Please send a valid Solana mainnet address.\n"
            "Example: `Solana: 7sPmqkM71YkGZ6J2XbkR5ZaYnXrFq2AZeQz3JmFd9XrR`",
            parse_mode="Markdown"
        )
        return
    
    # Save to database
    user_data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "sol_address": sol_address,
        "completed": True,
        "reward_sent": False  # We'll mark as sent when we actually send SOL
    }
    users.update_one({"user_id": user.id}, {"$set": user_data}, upsert=True)
    
    # Notify admin
    if ADMIN_ID:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚀 New Airdrop Registration:\n\n"
                 f"User: @{user.username} ({user.first_name})\n"
                 f"SOL Address: `{sol_address}`\n",
            parse_mode="Markdown"
        )
    
    # Success message with token purchase button
    keyboard = [[InlineKeyboardButton("🚀 Buy on Pump.fun", url=PUMP_FUN_LINK)]]
    
    update.message.reply_text(
        "🎉 Congratulations! You've completed all steps for Sakuramemecoin Airdrop!\n\n"
        "💰 0.01 SOL is on its way to your wallet!\n\n"
        "Don't forget to buy our token on Pump.fun:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )
    
    # Clear user data
    context.user_data.clear()

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling update:", exc_info=context.error)

def main() -> None:
    # Persistent connection to handle Render restarts
    logger.info("Starting bot...")
    while True:
        try:
            updater = Updater(BOT_TOKEN, use_context=True)
            dp = updater.dispatcher

            # Handlers
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CallbackQueryHandler(button_handler))
            dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_sol_address))
            dp.add_error_handler(error_handler)

            updater.start_polling()
            logger.info("Bot started polling...")
            updater.idle()
        except Exception as e:
            logger.error(f"Main loop crashed: {e}")
            time.sleep(10)

if __name__ == '__main__':
    main()
