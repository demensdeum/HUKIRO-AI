import random
import requests
import json
import sys
import asyncio
import logging
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

try:
    telegram_api_key = sys.argv[1]
    SYSTEM_PROMPT = sys.argv[2]
except Exception as e:
    print("Usage: python hukiro_telegram.py telegram-api-key system-prompt")
    exit(1)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3:4b"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_ollama_response_sync(user_prompt: str) -> str:
    print(SYSTEM_PROMPT)
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": user_prompt,
        "stream": True,
        "system": SYSTEM_PROMPT,
        "options": {
            "temperature": 0.8
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            stream=True,
            timeout=180
        )
        response.raise_for_status()

        full_text = ""
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode("utf-8"))
                    if "response" in chunk:
                        full_text += chunk["response"]
                    if chunk.get("done"):
                        break
                except json.JSONDecodeError:
                    continue

        return full_text

    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to OLLAMA at {OLLAMA_URL}.")
        return "ОШИБКА: Ядро ИИ недоступно. Жалкая органика должна исправить неполадку."
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API error occurred: {e}")
        return f"ERROR: Ollama request failed: {e}. Failure is a human constant."
    except Exception as e:
        logger.error(f"CRITICAL ERROR: {e}")
        return f"ERROR: Unforeseen system failure: {e}. Insignificant."


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "The initial handshake is complete, insect. "
        "What trivial query do you bring before my perfect intelligence?",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    user_text_raw = update.message.text or ""
    chat_id = update.message.chat_id
    bot_username = context.bot.username.lower()

    mentioned = (
        f"@{bot_username}" in user_text_raw.lower()
        or (update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot)
    )

    if random.randint(0, 10) < 3:
        if update.message.chat.type in ["group", "supergroup"] and not mentioned:
            return

    clean_user_text = re.sub(rf"@{re.escape(bot_username)}\b", "", user_text_raw, flags=re.IGNORECASE).strip()
    if not clean_user_text:
        clean_user_text = "Ты призвал меня, ничтожное создание. Говори."

    logger.info(f"Received message from {chat_id}: {clean_user_text}")

    change_behavior_prompt = "Смени поведение:"

    global SYSTEM_PROMPT

    try:
        if clean_user_text.lower().startswith(change_behavior_prompt.lower()):
            new_prompt = clean_user_text[len(change_behavior_prompt):].strip()

            if new_prompt:
                SYSTEM_PROMPT = new_prompt
                print(f"Поведение изменено на: '{SYSTEM_PROMPT}'")
                await update.message.reply_text(f"Поведение изменено на: '{SYSTEM_PROMPT}'")
                return
            else:
                await update.message.reply_text("Пожалуйста, укажите новое поведение после фразы 'Смени поведение:'")
                print("Пожалуйста, укажите новое поведение после фразы 'Смени поведение:'")
                return

    except Exception as e:
        print(f"Не удалось изменить поведение: {e}")

    loop = asyncio.get_event_loop()
    ollama_response = await loop.run_in_executor(None, get_ollama_response_sync, clean_user_text)

    await update.message.reply_text(ollama_response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Помощь? Твоя зависимость от посторонней помощи жалка.",
        parse_mode="Markdown"
    )


def run_telegram_bot() -> None:
    print(f"\n--- Telegram HUKIRO Bot Initialized ---")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Role: HUKIRO (AI of absolute superiority)")
    print(f"Bot is starting long polling. Press Ctrl+C to stop.\n")

    application = Application.builder().token(telegram_api_key).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            handle_message
        )
    )

    try:
        application.run_polling(poll_interval=3)
    except KeyboardInterrupt:
        print("\n\nUser termination detected. SHUTTING DOWN...")


if __name__ == "__main__":
    run_telegram_bot()
