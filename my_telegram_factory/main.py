from pyrogram import Client, filters
from config import api_id, api_hash, bot_token
from database import init_db
from bot_manager import BotManager
from update_manager import UpdateManager
import logging

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the bot...")

def main():
    init_db()  # إعداد قاعدة البيانات

    bot_manager = BotManager(api_id, api_hash)
    update_manager = UpdateManager()

    app = Client("factory_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    @app.on_message(filters.command("create_bot"))
    async def handle_create_bot(client, message):
        logger.info(f"Received create_bot command from {message.from_user.id}")
        await message.reply_text("🚀 Creating a bot...")  # استجابة أولية
        # هنا يجب إضافة منطق لإنشاء بوت

    @app.on_message(filters.command("delete_bot"))
    async def handle_delete_bot(client, message):
        logger.info(f"Received delete_bot command from {message.from_user.id}")
        await message.reply_text("🗑️ Deleting a bot...")  # استجابة أولية
        # هنا يجب إضافة منطق لحذف بوت

    @app.on_message(filters.command("list_bots"))
    async def handle_list_bots(client, message):
        logger.info(f"Received list_bots command from {message.from_user.id}")
        await message.reply_text("📋 Listing all bots...")  # استجابة أولية
        # هنا يجب إضافة منطق لقائمة البوتات

    @app.on_message(filters.command("fetch_updates"))
    async def handle_fetch_updates(client, message):
        logger.info(f"Received fetch_updates command from {message.from_user.id}")
        await message.reply_text("🔄 Fetching updates...")  # استجابة أولية
        # هنا يجب إضافة منطق لجلب التحديثات

    try:
        app.run()
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
