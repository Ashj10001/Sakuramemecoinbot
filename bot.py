import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "7872973965:AAGt3KFPosFSYV1w4Ded-_tD8QtUHasei9s")
CHANNEL_LINK = "https://t.me/sakuramemecoin"
GROUP_LINK = "https://t.me/Sakuramemecoincommunity"
TWITTER_LINK = "https://x.com/Sukuramemecoin"
BUY_LINK = "https://pump.fun/coin/2AXnWVULFu5kJf7Z3LA9WXxF47XLYXoNAyMQZuZjpump"

# Conversation states
GET_WALLET = 0  # Typo fixed to GET_WALLET for consistency

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send welcome message and instructions with inline buttons"""
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("🌟 Join Channel", url=CHANNEL_LINK),
            InlineKeyboardButton("👥 Join Group", url=GROUP_LINK),
        ],
        [
            InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_LINK),
            InlineKeyboardButton("💰 Buy $SAKURA", url=BUY_LINK),
        ],
        [InlineKeyboardButton("✅ I Have Completed All Tasks", callback_data="submit_wallet")]
    ]
    
    # Fixed Markdown escaping
    await update.message.reply_text(
        f"👋 Welcome {user.mention_markdown_v2()} to the $SAKURA Airdrop Bot\\!\n\n"
        "📋 To qualify for 0\\.2 SOL airdrop:\n"
        "1\\. Join our official channel\n"
        "2\\. Join our community group\n"
        "3\\. Follow us on Twitter\n"
        "4\\. Buy $SAKURA token\n\n"
        "⬇️ Complete all tasks and click the button below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='MarkdownV2'
    )
    return GET_WALLET

async def request_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request Solana wallet address"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📥 Please send your Solana wallet address now:\n\n"
        "Example: `H1cS...g6FJ`\n"
        "_Just paste your wallet address in chat_",
        parse_mode='MarkdownV2'
    )
    return GET_WALLET

async def receive_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive wallet address and send confirmation"""
    wallet_address = update.message.text
    user = update.effective_user
    
    # Fixed Markdown escaping
    await update.message.reply_text(
        f"🎉 Congratulations {user.mention_markdown_v2()}!\n\n"
        "0\\.2 SOL is on its way to your wallet:\n"
        f"`{wallet_address}`\n\n"
        "⏳ Please allow 24\\-48 hours for the transaction to appear\n"
        "🐦 Follow us for more updates and rewards!",
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation"""
    await update.message.reply_text(
        'Operation cancelled',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot with Render-compatible configuration"""
    # Create application with workaround for Python 3.13 compatibility
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Disable job queue to fix weak reference issue
    application.job_queue = None
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GET_WALLET: [
                CallbackQueryHandler(request_wallet, pattern="^submit_wallet$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wallet)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    # Render deployment configuration
    if 'RENDER' in os.environ:
        PORT = int(os.environ.get('PORT', 10000))
        APP_NAME = os.environ.get('APP_NAME')
        
        # Set up webhook for Render
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://{APP_NAME}.onrender.com/{BOT_TOKEN}"
        )
    else:
        # Local development with polling
        application.run_polling()

if __name__ == '__main__':
    main()
