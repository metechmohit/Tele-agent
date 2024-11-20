import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import CallbackQueryHandler, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
from groq import Groq
from chatgpt_md_converter import telegram_format


load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
assert TELEGRAM_TOKEN is not None
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
assert GROQ_API_KEY is not None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Bot:
    def __init__(self) -> None:
        self.app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        # self.conv = False
        self.conv = True
        self.client = Groq(api_key=GROQ_API_KEY)

        self.model = "llama3-70b-8192"
        self.system_prompt = 'You are a helpful AI assistant. For every query you are given, pretend to be an expert in the field.'

        self.app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.talk))
        self.app.add_handler(CommandHandler('start', self.start))
        self.app.add_handler(CommandHandler('choose', self.choose))
        self.app.add_handler(CallbackQueryHandler(self.button))
        self.app.add_handler(CommandHandler('switch', self.switch))
        self.app.run_polling()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        assert update.effective_chat is not None
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I'm a bot, please talk to me!"
        )

    async def switch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        assert update.effective_chat is not None
        self.conv = not self.conv

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'CONV is now {self.conv}.'
        )

    async def talk(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        assert update.effective_chat is not None
        assert update.message is not None and update.message.text is not None

        if self.conv:
            text = self.generate(update.message.text)
        else:
            text = "We are not in a conversation."
        
        print(text)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=telegram_format(text),
            # text=text,

            parse_mode=telegram.constants.ParseMode.HTML,
        )
            
    async def choose(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sends a message with three inline buttons attached."""
        assert update.message is not None

        keyboard = [
            [
                InlineKeyboardButton("LLaMA3 8b", callback_data="llama3-8b-8192"),
                InlineKeyboardButton("LLaMA3 70b", callback_data="llama3-70b-8192"),
            ],
            [
                InlineKeyboardButton("Mixtral 8x7b", callback_data="mixtral-8x7b-32768"),
                InlineKeyboardButton("Gemma 7b", callback_data="gemma-7b-it"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        assert update is not None
        query = update.callback_query
        assert query is not None
        assert query.data is not None
        await query.answer()
        self.model = query.data
        await query.edit_message_text(text=f"Current model: {query.data}")

    def generate(self, text, temperature=0.0,max_tokens=1024):
        res = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": text,
                }
            ],
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            # response_format= {"type": "json_object"}
        )
        return res.choices[0].message.content

if __name__ == '__main__':
    bot = Bot()