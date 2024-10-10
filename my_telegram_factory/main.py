from pyrogram import Client,filters
from config import api_id, api_hash, bot_token
from database import init_db, add_bot_to_db, remove_bot_from_db, get_bots_from_db
from bot_manager import BotManager
from update_manager import UpdateManager
import logging
import os
import subprocess

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the bot...")

def main():
    init_db()  # إعداد قاعدة البيانات
    bot_manager = BotManager(api_id, api_hash)
    update_manager = UpdateManager()

    app = Client("factory_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    @app.on_message(filters.command("start"))
    async def handle_start(client, message):
        logger.info(f"Received start command from {message.from_user.id}")
        welcome_text = (
            "👋 مرحباً بكم في مصنع البوتات SB لصناعة بوتات تلغرام تعمل على فحص اليوزرات المتاحة.\n\n"
            "استخدم الأوامر في الأسفل لإنشاء بوتك الخاص:\n"
            "🔹 /create_bot - لإنشاء بوت جديد.\n"
            "🔹 /delete_bot - لحذف بوت.\n"
            "🔹 /list_bots - قائمة البوتات التي قمت بإنشائها.\n"
            "🔹 /fetch_updates - جلب التحديثات للبوتات الخاصة بك.\n"
        )
        await message.reply_text(welcome_text)  # بدون تنسيق

    @app.on_message(filters.command("create_bot"))
    async def handle_create_bot(client, message):
        logger.info(f"Received create_bot command from {message.from_user.id}")
        await message.reply_text("من فضلك أدخل توكن البوت الجديد:")
        
        @app.on_message(filters.text & filters.user(message.from_user.id))
        async def receive_token(client, msg):
            token = msg.text.strip()
            if not token:
                await msg.reply_text("يرجى إدخال توكن صالح.")
                return
            
            try:
                # تسجيل الدخول للبوت الجديد
                new_bot = Client("new_bot_session", api_id=api_id, api_hash=api_hash, bot_token=token)
                await new_bot.start()
from pyrogram import Client, filters
from config import api_id, api_hash, bot_token
from database import init_db, add_bot_to_db, remove_bot_from_db, get_bots_from_db
from bot_manager import BotManager
from update_manager import UpdateManager
import logging
import os
import subprocess

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting the bot...")

def main():
    init_db()  # إعداد قاعدة البيانات
    bot_manager = BotManager(api_id, api_hash)
    update_manager = UpdateManager()

    app = Client("factory_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    @app.on_message(filters.command("start"))
    async def handle_start(client, message):
        logger.info(f"Received start command from {message.from_user.id}")
        welcome_text = (
            "👋 مرحباً بكم في مصنع البوتات SB لصناعة بوتات تلغرام تعمل على فحص اليوزرات المتاحة.\n\n"
            "استخدم الأوامر في الأسفل لإنشاء بوتك الخاص:\n"
            "🔹 /create_bot - لإنشاء بوت جديد.\n"
            "🔹 /delete_bot - لحذف بوت.\n"
            "🔹 /list_bots - قائمة البوتات التي قمت بإنشائها.\n"
            "🔹 /fetch_updates - جلب التحديثات للبوتات الخاصة بك.\n"
        )
        await message.reply_text(welcome_text)  # بدون تنسيق

    @app.on_message(filters.command("create_bot"))
    async def handle_create_bot(client, message):
        logger.info(f"Received create_bot command from {message.from_user.id}")
        await message.reply_text("من فضلك أدخل توكن البوت الجديد:")
        
        @app.on_message(filters.text & filters.user(message.from_user.id))
        async def receive_token(client, msg):
            token = msg.text.strip()
            if not token:
                await msg.reply_text("يرجى إدخال توكن صالح.")
                return
            
            try:
                # تسجيل الدخول للبوت الجديد
                new_bot = Client("new_bot_session", api_id=api_id, api_hash=api_hash, bot_token=token)
                await new_bot.start()
                
                # حفظ معلومات البوت في قاعدة البيانات
                add_bot_to_db(token)
                
                await msg.reply_text(f"تم إنشاء بوت جديد بنجاح! توكن: {token}")
                
                # تشغيل البوت الفرعي في ملف منفصل
                with open(f"{token}.py", "w") as f:
                    f.write(f"""from pyrogram import Client
api_id = {api_id}
api_hash = "{api_hash}"
bot_token = "{token}"

app = Client("new_bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("مرحبًا بك في بوت SB لصيد اليوزرات!")

app.run()
""")
                
                logger.info(f"New bot created with token: {token}")
                await new_bot.stop()  # توقف البوت بعد إنشائه
            except Exception as e:
                await msg.reply_text(f"حدث خطأ أثناء إنشاء البوت: {e}")
        
        # إزالة هذا المعالج بعد الحصول على التوكن
        app.remove_handler(receive_token)

    @app.on_message(filters.command("delete_bot"))
    async def handle_delete_bot(client, message):
        logger.info(f"Received delete_bot command from {message.from_user.id}")
        await message.reply_text("يرجى إدخال توكن البوت الذي ترغب في حذفه:")
        
        @app.on_message(filters.text & filters.user(message.from_user.id))
        async def receive_delete_token(client, msg):
            token = msg.text.strip()
            if remove_bot_from_db(token):
                os.remove(f"{token}.py")  # حذف ملف البوت الفرعي
                await msg.reply_text("تم حذف البوت بنجاح.")
            else:
                await msg.reply_text("لم يتم العثور على بوت بهذا التوكن.")
        
        # إزالة هذا المعالج بعد الحصول على التوكن
        app.remove_handler(receive_delete_token)

    @app.on_message(filters.command("list_bots"))
    async def handle_list_bots(client, message):
        logger.info(f"Received list_bots command from {message.from_user.id}")
        bots = get_bots_from_db()  # يجب أن تكون لديك وظيفة للحصول على البوتات
        if bots:
            await message.reply_text("قائمة البوتات:\n" + "\n".join(bots))
        else:
            await message.reply_text("لا توجد بوتات مسجلة.")

    @app.on_message(filters.command("fetch_updates"))
    async def handle_fetch_updates(client, message):
        logger.info(f"Received fetch_updates command from {message.from_user.id}")
        await message.reply_text("Updating the bot... Please wait.")
        try:
            # جلب التحديثات من GitHub
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)
            if result.returncode == 0:
                await message.reply_text("Bot has been updated successfully! You may need to restart it.")
            else:
                await message.reply_text("Failed to update the bot. Please check the logs.")
                logger.error(f"Error updating bot: {result.stderr}")
        except Exception as e:
            await message.reply_text(f"An error occurred: {e}")
            logger.error(f"Error occurred while updating: {e}")

    try:
        app.run()
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()                
                # حفظ معلومات البوت في قاعدة البيانات
                add_bot_to_db(token)
                
                await msg.reply_text(f"تم إنشاء بوت جديد بنجاح! توكن: {token}")
                
                # تشغيل البوت الفرعي في ملف منفصل
                with open(f"{token}.py", "w") as f:
                    f.write(f"""from pyrogram import Client
api_id = {api_id}
api_hash = "{api_hash}"
bot_token = "{token}"

app = Client("new_bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("مرحبًا بك في بوت SB لصيد اليوزرات!")

app.run()
""")
                
                logger.info(f"New bot created with token: {token}")
                await new_bot.stop()  # توقف البوت بعد إنشائه
            except Exception as e:
                await msg.reply_text(f"حدث خطأ أثناء إنشاء البوت: {e}")
  
        # إزالة هذا المعالج بعد الحصول على التوكن
        app.remove_handler(receive_token)

    @app.on_message(filters.command("delete_bot"))
    async def handle_delete_bot(client, message):
        logger.info(f"Received delete_bot command from {message.from_user.id}")
        await message.reply_text("يرجى إدخال توكن البوت الذي ترغب في حذفه:")
        
        @app.on_message(filters.text & filters.user(message.from_user.id))
        async def receive_delete_token(client, msg):
            token = msg.text.strip()
            if remove_bot_from_db(token):
                os.remove(f"{token}.py")  # حذف ملف البوت الفرعي
                await msg.reply_text("تم حذف البوت بنجاح.")
            else:
                await msg.reply_text("لم يتم العثور على بوت بهذا التوكن.")
        
        # إزالة هذا المعالج بعد الحصول على التوكن
        app.remove_handler(receive_delete_token)

    @app.on_message(filters.command("list_bots"))
    async def handle_list_bots(client, message):
        logger.info(f"Received list_bots command from {message.from_user.id}")
        bots = get_bots_from_db()  # يجب أن تكون لديك وظيفة للحصول على البوتات
        if bots:
