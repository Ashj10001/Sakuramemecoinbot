from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import random

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
WEBSITE = "https://stirring-jelly-a235d8.netlify.app/"
REWARD = 0.02
ADMIN_USER_ID = "YOUR_ADMIN_USER_ID"  # Replace with your Telegram user ID

# Simulated database (replace with real database in production)
user_data = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0.0
        self.tasks_completed = 0
        self.username = ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    logger.info(f"New user: {user.full_name} (ID: {user.id})")
    
    # Initialize user in database
    if user.id not in user_data:
        user_data[user.id] = User(user.id)
        user_data[user.id].username = user.username or user.full_name
    
    # Welcome message with website link (no balance shown)
    await update.message.reply_html(
        f"🌸 <b>Welcome to Sakuramemecoin Bot, {user.first_name}!</b> 🌸\n\n"
        "🚀 Earn SMC by completing simple tasks\n\n"
        "🔹 Use /tasks to see available tasks\n"
        "🔹 Complete tasks and earn rewards\n"
        f"🌐 Visit our website: {WEBSITE}\n\n"
        "💬 Type /help for instructions"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send instructions when the command /help is issued."""
    await update.message.reply_text(
        "📘 <b>Bot Guide</b> 📘\n\n"
        "<b>Available Commands:</b>\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/tasks - View available tasks\n"
        "/complete - Mark a task as completed\n"
        "/balance - Check your SMC balance\n"
        "/website - Get our website link\n\n"
        "<b>How to Earn:</b>\n"
        "1. Use /tasks to see available tasks\n"
        "2. Complete a task\n"
        "3. Use /complete to verify\n"
        "4. Receive SMC rewards instantly!\n\n"
        f"🌐 Website: {WEBSITE}",
        parse_mode='HTML'
    )

async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available tasks to the user."""
    tasks = [
        "✅ <b>Task 1:</b> Join our Telegram channel",
        "✅ <b>Task 2:</b> Retweet our pinned tweet",
        "✅ <b>Task 3:</b> Follow us on Twitter",
        "✅ <b>Task 4:</b> Share our website with 5 friends",
        "✅ <b>Task 5:</b> Join our Discord server",
        "✅ <b>Task 6:</b> Create a meme about Sakuracoin"
    ]
    
    await update.message.reply_text(
        "📋 <b>Available Tasks:</b>\n\n" +
        "\n".join(tasks) +
        "\n\n🔹 Complete any task and use /complete to verify\n"
        f"🔹 Reward: {REWARD} SMC per task\n\n"
        "💡 You can complete multiple tasks!",
        parse_mode='HTML'
    )

async def complete_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirm task completion and send reward notification."""
    user = update.effective_user
    logger.info(f"Task completed by: {user.full_name} (ID: {user.id})")
    
    # Initialize user if not exists
    if user.id not in user_data:
        user_data[user.id] = User(user.id)
    
    # Update user balance
    user_data[user.id].balance += REWARD
    user_data[user.id].tasks_completed += 1
    
    # Send reward message
    await update.message.reply_text(
        f"🎉 <b>Congratulations!</b> 🎉\n\n"
        f"💰 <b>{REWARD} SMC</b> is on the way to your wallet!\n\n"
        "⌛ Please allow 2-3 minutes for the transaction\n"
        "🔄 Complete more tasks to earn more rewards!\n\n"
        f"🌐 Dashboard: {WEBSITE}",
        parse_mode='HTML'
    )
    
    # Notify admin (optional)
    # await context.bot.send_message(
    #     chat_id=ADMIN_USER_ID,
    #     text=f"⚠️ Task completed\nUser: {user.full_name}\nID: {user.id}\nTasks: {user_data[user.id].tasks_completed}"
    # )

async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show user's balance when requested."""
    user = update.effective_user
    
    if user.id in user_data:
        balance = user_data[user.id].balance
        tasks = user_data[user.id].tasks_completed
        await update.message.reply_text(
            f"💼 <b>Your Sakuramemecoin Balance</b> 💼\n\n"
            f"💰 <b>Total Balance:</b> {balance:.2f} SMC\n"
            f"✅ <b>Tasks Completed:</b> {tasks}\n\n"
            f"🌐 View your full dashboard: {WEBSITE}",
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            "❌ You haven't started earning yet!\n\n"
            "Use /start to begin and complete your first task to get SMC rewards."
        )

async def website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the website link."""
    await update.message.reply_text(
        f"🌐 <b>Official Website</b> 🌐\n\n"
        f"Visit our platform: {WEBSITE}\n\n"
        "🔹 Track your earnings\n"
        "🔹 View transaction history\n"
        "🔹 Discover more earning opportunities",
        parse_mode='HTML'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    user = update.effective_user
    text = update.message.text.lower()
    
    responses = [
        "🌸 Sakura season is earning season! Complete tasks with /tasks",
        "💻 Visit our website to track your earnings: " + WEBSITE,
        "💎 Each task earns you 0.02 SMC! Use /complete after finishing",
        "🚀 Ready to earn more? Check available tasks with /tasks",
        "🌐 Stay updated: " + WEBSITE
    ]
    
    if any(greet in text for greet in ["hello", "hi", "hey", "hola"]):
        await update.message.reply_text(f"👋 Hello {user.first_name}! Ready to earn some SMC?")
    elif "thank" in text:
        await update.message.reply_text("🙏 You're welcome! Keep earning with us!")
    elif "website" in text or "site" in text or "link" in text:
        await website_link(update, context)
    elif "balance" in text or "smc" in text or "earn" in text:
        await show_balance(update, context)
    elif "task" in text or "mission" in text or "job" in text:
        await show_tasks(update, context)
    elif "start" in text:
        await start(update, context)
    else:
        await update.message.reply_text(random.choice(responses))

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and send a message to the user."""
    logger.error(f"Update {update} caused error: {context.error}")
    
    if update.effective_message:
        await update.effective_message.reply_text(
            "❌ Oops! Something went wrong.\n\n"
            "Please try again later or contact support."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token("YOUR_BOT_TOKEN_HERE").build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", show_tasks))
    application.add_handler(CommandHandler("complete", complete_task))
    application.add_handler(CommandHandler("balance", show_balance))
    application.add_handler(CommandHandler("website", website_link))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
