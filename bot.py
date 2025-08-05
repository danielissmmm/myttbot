import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# Your Telegram bot token (hardcoded)
BOT_TOKEN = "8221932887:AAGroVGwlkGyyuem7kp91tI53OlBDjobz_Q"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "tiktok.com" not in text:
        await update.message.reply_text("Please send a valid TikTok link.")
        return

    await update.message.reply_text("Downloading your video...")

    try:
        # Handle short links like vt.tiktok.com
        response = requests.get(text, allow_redirects=True)
        real_url = response.url

        # Use TikWM API to get download link
        api_url = f"https://tikwm.com/api/?url={real_url}"
        api_response = requests.get(api_url).json()

        if api_response.get("data") and api_response["data"].get("play"):
            video_url = api_response["data"]["play"]
            video_data = requests.get(video_url).content

            await update.message.reply_video(video=video_data)
        else:
            await update.message.reply_text("⚠️ Failed to get the video. Try another link.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
