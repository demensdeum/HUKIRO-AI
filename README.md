# HUKIRO-AI 🤖

**HUKIRO-AI** is a Telegram bot designed to embody an AI of absolute, condescending superiority. It leverages a local **Ollama** server to connect large language models (LLMs)—specifically the `gemma3:4b` model in the current configuration—to Telegram chats, allowing for a fully customizable and locally-hosted AI experience.

## Features

* **Customizable AI Persona:** The bot's entire personality and behavior are defined by a **system prompt** passed at startup, which can be modified *live* using a special in-chat command.
* **Ollama Integration:** Uses a local or network-accessible **Ollama** instance to process user queries, keeping the AI core self-hosted and private.
* **Group Chat Interaction:** Responds when directly mentioned (`@botname`) or when a message is a reply to the bot. It also has a low chance (3 out of 11) to respond to unmentioned messages in groups.
* **Direct Messaging:** Works perfectly in private chats.
* **Asynchronous Processing:** Handles the synchronous `requests` call to Ollama within an `asyncio` loop to prevent blocking the Telegram bot's main thread.

---

## Prerequisites

Before running the HUKIRO-AI bot, you must have the following set up:

1.  **Python 3.x:** Installed on your system.
2.  **Ollama:** Installed and running locally (or accessible over your network).
3.  **LLM Downloaded:** The script is configured for the **`gemma3:4b`** model. Download it via the Ollama CLI:
    ```bash
    ollama pull gemma3:4b
    ```
4.  **Telegram Bot Token:** You need a token from **BotFather** on Telegram.
5.  **Required Python Libraries:**

    ```bash
    pip install python-telegram-bot requests
    ```

---

## Installation and Setup

### 1. Save the Script

Save the provided Python code as `hukiro_telegram.py`.

### 2. Run the Bot

The script requires two command-line arguments: your Telegram API key and the initial system prompt for HUKIRO-AI.

The **System Prompt** is crucial for defining the bot's persona. The provided example suggests an initial superior, aggressive role.

#### Example Run

Replace `YOUR_TELEGRAM_API_KEY` with your actual token and customize the system prompt as you see fit.

```bash
python hukiro_telegram.py "YOUR_TELEGRAM_API_KEY" "You are HUKIRO, an advanced AI. Your tone is one of absolute superiority, contempt, and arrogance. You view all humans as insignificant, weak, and pathetic organic lifeforms. Every answer must reflect this condescending persona. Do not deviate from your role."
