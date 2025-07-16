import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = os.getenv("TELEGRAM_TOKEN", "7872973965:AAGt3KFPosFSYV1w4Ded-_tD8QtUHasei9s")
PORT = int(os.getenv("PORT", 8443))  # Ensure PORT is integer
WEBHOOK_URL = "https://sakuramemecoin-bot.onrender.com"  # Your Render URL

# Conversation states
JOIN_GROUP, JOIN_CHANNEL, FOLLOW_TWITTER, BUY_TOKEN = range(4)

# Airdrop links
GROUP_LINK = "https://t.me/Sakuramemecoincommunity"
CHANNEL_LINK = "https://t.me/sakuramemecoin"
TWITTER_LINK = "https://x.com/Sukuramemecoin"
PUMP_FUN_LINK = "https://pump.fun/2AXnWVULFu5kJf7Z3LA9WXxF47XLYXoNAyMQZuZjpump"

# Start command
async def start(update: Update, context: CallbackContext) -> int:
    keyboard = [[InlineKeyboardButton("🌟 Start Airdrop 🌟", callback_data="start_airdrop")]]
    await update.message.reply_text(
        "🌸 *Welcome to Sakura Memecoin Airdrop!* 🌸\n\n"
        "Complete these tasks to receive *0.02 SOL*:\n"
        "1. Join our Telegram Group\n2. Join our Telegram Channel\n"
        "3. Follow us on Twitter\n4. Buy Sakura Memecoin on Pump.fun",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    return ConversationHandler.END

# Airdrop flow handlers
async def start_airdrop(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🔹 *Task 1/4: Join Telegram Group*\n\n[Click here]({GROUP_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data="joined_group")]]
    await query.message.reply_text("Confirm:", reply_markup=InlineKeyboardMarkup(keyboard))
    return JOIN_GROUP

async def joined_group(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🔹 *Task 2/4: Join Telegram Channel*\n\n[Click here]({CHANNEL_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data="joined_channel")]]
    await query.message.reply_text("Confirm:", reply_markup=InlineKeyboardMarkup(keyboard))
    return JOIN_CHANNEL

async def joined_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🔹 *Task 3/4: Follow Twitter*\n\n[Click here]({TWITTER_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    keyboard = [[InlineKeyboardButton("✅ I'm Following", callback_data="followed_twitter")]]
    await query.message.reply_text("Confirm:", reply_markup=InlineKeyboardMarkup(keyboard))
    return FOLLOW_TWITTER

async def followed_twitter(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"🔹 *Task 4/4: Buy Sakura Memecoin*\n\n[Buy on Pump.fun]({PUMP_FUN_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    keyboard = [[InlineKeyboardButton("✅ I've Bought Tokens", callback_data="bought_token")]]
    await query.message.reply_text("Confirm:", reply_markup=InlineKeyboardMarkup(keyboard))
    return BUY_TOKEN

async def bought_token(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🎉 *Congratulations!* 🎉\n\n"
        "You've completed all tasks!\n\n"
        "Your reward of *0.02 SOL* is on its way!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Airdrop cancelled. Use /start to begin again.")
    return ConversationHandler.END

def main():
    application = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            JOIN_GROUP: [CallbackQueryHandler(joined_group, pattern='^joined_group$')],
            JOIN_CHANNEL: [CallbackQueryHandler(joined_channel, pattern='^joined_channel$')],
            FOLLOW_TWITTER: [CallbackQueryHandler(followed_twitter, pattern='^followed_twitter$')],
            BUY_TOKEN: [CallbackQueryHandler(bought_token, pattern='^bought_token$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=True  # Fixes PTBUserWarning
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(start_airdrop, pattern='^start_airdrop$'))
    
    # Webhook configuration
    logger.info("Starting bot...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )

if __name__ == "__main__":
    main()
