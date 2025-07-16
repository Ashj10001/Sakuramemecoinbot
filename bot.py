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
PORT = int(os.getenv("PORT", "8443"))
WEBHOOK_URL = "https://sakuramemecoin-bot.onrender.com"  # Update with your Render URL

# Conversation states
JOIN_GROUP, JOIN_CHANNEL, FOLLOW_TWITTER, BUY_TOKEN = range(4)

# Airdrop links
GROUP_LINK = "https://t.me/Sakuramemecoincommunity"
CHANNEL_LINK = "https://t.me/sakuramemecoin"
TWITTER_LINK = "https://x.com/Sukuramemecoin"
PUMP_FUN_LINK = "https://pump.fun/2AXnWVULFu5kJf7Z3LA9WXxF47XLYXoNAyMQZuZjpump"

# Start command - initiates the airdrop process
async def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    welcome_message = (
        f"🌸 *Welcome to Sakura Memecoin Airdrop, {user.first_name}!* 🌸\n\n"
        "Complete these simple tasks to receive *0.02 SOL*:\n"
        "1. Join our Telegram Group\n"
        "2. Join our Telegram Channel\n"
        "3. Follow us on Twitter\n"
        "4. Buy Sakura Memecoin on Pump.fun\n\n"
        "Click the button below to get started!"
    )
    
    keyboard = [[InlineKeyboardButton("🌟 Start Airdrop 🌟", callback_data="start_airdrop")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message, 
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

# Handle the airdrop start button
async def start_airdrop(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔹 *Task 1/4: Join our Telegram Group*\n\n"
        f"Join our community: [Sakura Memecoin Group]({GROUP_LINK})\n\n"
        "Click the button below after joining!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data="joined_group")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Confirm when done:", reply_markup=reply_markup)
    return JOIN_GROUP

# Handle group join confirmation
async def joined_group(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔹 *Task 2/4: Join our Telegram Channel*\n\n"
        f"Stay updated: [Sakura Memecoin Channel]({CHANNEL_LINK})\n\n"
        "Click below after joining!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    keyboard = [[InlineKeyboardButton("✅ I've Joined", callback_data="joined_channel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Confirm when done:", reply_markup=reply_markup)
    return JOIN_CHANNEL

# Handle channel join confirmation
async def joined_channel(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔹 *Task 3/4: Follow us on Twitter*\n\n"
        f"Follow us: [Sakura Memecoin Twitter]({TWITTER_LINK})\n\n"
        "Click below after following!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    keyboard = [[InlineKeyboardButton("✅ I'm Following", callback_data="followed_twitter")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Confirm when done:", reply_markup=reply_markup)
    return FOLLOW_TWITTER

# Handle Twitter follow confirmation
async def followed_twitter(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🔹 *Task 4/4: Buy Sakura Memecoin*\n\n"
        f"Buy on Pump.fun: [Sakura Memecoin Purchase]({PUMP_FUN_LINK})\n\n"
        "Click below after purchasing!",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    
    keyboard = [[InlineKeyboardButton("✅ I've Bought Tokens", callback_data="bought_token")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Confirm your purchase:", reply_markup=reply_markup)
    return BUY_TOKEN

# Handle final confirmation and reward
async def bought_token(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🎉 *Congratulations!* 🎉\n\n"
        "You've successfully joined the Sakura Memecoin community!\n\n"
        "Your reward of *0.02 SOL* is on its way!\n\n"
        "Thank you for participating! 🌸",
        parse_mode="Markdown"
    )
    
    # Optional: Send a celebratory sticker
    await context.bot.send_sticker(
        chat_id=query.message.chat_id,
        sticker="CAACAgQAAxkBAAELV6hmDxKfQkQdNt5G9yM2X3d0cK5zIAACFAADJdPGFQABh1XQAAHrQjQE"
    )
    
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Airdrop process cancelled. Use /start to begin again whenever you're ready!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

# Main function to start the bot
def main():
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handler for the airdrop process
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            JOIN_GROUP: [CallbackQueryHandler(joined_group, pattern='^joined_group$')],
            JOIN_CHANNEL: [CallbackQueryHandler(joined_channel, pattern='^joined_channel$')],
            FOLLOW_TWITTER: [CallbackQueryHandler(followed_twitter, pattern='^followed_twitter$')],
            BUY_TOKEN: [CallbackQueryHandler(bought_token, pattern='^bought_token$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(start_airdrop, pattern='^start_airdrop$'))
    
    # Start the bot with webhook
    logger.info("Starting bot in webhook mode...")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )

if __name__ == "__main__":
    main()
