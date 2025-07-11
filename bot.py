import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Bot configuration
BOT_TOKEN = "7872973965:AAGt3KFPosFSYV1w4Ded-_tD8QtUHasei9s"
CHANNEL_LINK = "https://t.me/sakuramemecoin"
GROUP_LINK = "https://t.me/Sakuramemecoincommunity"
TWITTER_LINK = "https://x.com/Sukuramemecoin"
BUY_LINK = "https://pump.fun/coin/2AXnWVULFu5kJf7Z3LA9WXxF47XLYXoNAyMQZuZjpump"

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conversation states
REQUEST_WALLET, CONFIRMATION = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with task instructions"""
    user = update.effective_user
    welcome_msg = (
        f"👋 Welcome {user.mention_html()} to Sakura Meme Coin Airdrop Bot!\n\n"
        "🎌 To qualify for 0.2 SOL airdrop:\n"
        "1. Join our Official Channel\n"
        "2. Join our Telegram Group\n"
        "3. Follow our Twitter\n"
        "4. Buy $Sakura tokens\n\n"
        "⬇️ Complete the tasks below then click DONE"
    )
    
    # Create inline keyboard with task buttons
    keyboard = [
        [
            InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Join Group", url=GROUP_LINK)
        ],
        [
            InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK),
            InlineKeyboardButton("💰 Buy $Sakura", url=BUY_LINK)
        ],
        [InlineKeyboardButton("✅ DONE", callback_data="tasks_done")]
    ]
    
    await update.message.reply_html(
        welcome_msg,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )

async def handle_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle task completion callback"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✍️ Please send your Solana wallet address now:\n\n"
        "• Copy/paste your SOL address\n"
        "• Make sure it's correct!\n\n"
        "⚠️ Type /cancel if you need to restart",
        disable_web_page_preview=True
    )
    return REQUEST_WALLET

async def receive_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Process submitted wallet address"""
    wallet = update.message.text.strip()
    user = update.effective_user
    
    # Save wallet to database (optional)
    # logger.info(f"Wallet from {user.id}: {wallet}")
    
    # Send confirmation message
    await update.message.reply_html(
        f"🎉 Congratulations {user.mention_html()}!\n\n"
        "✅ Your entry has been verified!\n\n"
        "🪙 0.2 SOL is on its way to your wallet:\n"
        f"<code>{wallet}</code>\n\n"
        "⏳ Please allow 24-48 hours for the transaction\n\n"
        "🌐 Visit our community: @Sakuramemecoincommunity",
        reply_markup=ReplyKeyboardRemove(),
        disable_web_page_preview=True
    )
    return CONFIRMATION

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel current conversation"""
    await update.message.reply_text(
        "❌ Operation cancelled. Type /start to begin again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            REQUEST_WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wallet)],
            CONFIRMATION: [CommandHandler('start', start)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
    
    # Add handlers
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_done, pattern="^tasks_done$"))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
