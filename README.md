# **Tele-Agent Bot**

Tele-Agent Bot is a versatile AI-powered Telegram bot that interacts with users by providing intelligent responses to their queries. The bot uses Groq's API and LLaMA3 models to simulate expert-level assistance in various fields.

---

## **Features**
- **Interactive Chat**: Provides responses to user queries in natural language.
- **Model Selection**: Choose from multiple AI models (LLaMA3, Mixtral, Gemma) via inline buttons.
- **Toggle Conversational Mode**: Switch between conversational and non-conversational modes.
- **Customizable Models**: Set default and dynamically selectable models for generating responses.

---

## **Commands**
1. **`/start`**  
   Initiates the bot and welcomes the user.

2. **`/choose`**  
   Displays a set of models to choose from via inline buttons.

3. **`/switch`**  
   Toggles conversational mode (ON/OFF).

4. **Message Input**  
   Sends a query directly to the bot for a response.

---

## **Setup**
### **Prerequisites**
- Python 3.10+
- Telegram Bot API Token
- Groq API Key
- `.env` file for storing API credentials.

### **Environment Variables**
Create a `.env` file in the project directory with the following variables:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
```

### **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/metechmohit/Tele-agent.git
   cd Tele-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python app.py
   ```

---

## **How to Use**
1. Open the bot on Telegram using the link below.
2. Start a conversation using `/start`.
3. Ask questions or use `/choose` to select models for specific needs.

---

## **Telegram Bot Link**
[Click Here to Use Tele-Agent Bot](https://t.me/WizWhizBot)

---

## **Dependencies**
- [Python Telegram Bot](https://python-telegram-bot.org)
- [Groq Python SDK](https://groq.com)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## **Future Enhancements**
- Add more model options.
- Implement additional commands for customization.
- Include multi-language support.

---
Let me know if you need help refining this further!
