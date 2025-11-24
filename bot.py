import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from utils.hf_api import question_answering, sentence_similarity, translate_text, generate_text

# ======================
# ENV
# ======================
load_dotenv()  # Render использует Environment Variables

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=os.getenv("TELEGRAM_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# ======================
# /start
# ======================
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Hi! I’m your AI assistant.\n\n"
        "Available commands:\n"
        "/ask <context> || <question> — Question Answering\n"
        "/similarity <sentence1> || <sentence2> — Sentence Similarity\n"
        "/translate <text> — Translate EN→RU\n"
        "/generate <prompt> — Text Generation"
    )


@dp.message(Command("ask"))
async def ask_cmd(message: types.Message):
    try:
        text = message.get_args()
        if "||" not in text:
            await message.answer("Format: /ask context || question")
            return
        context, question = text.split("||", 1)
        answer = question_answering(context.strip(), question.strip())
        await message.answer(f"💡 <b>Answer:</b> {answer}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


@dp.message(Command("similarity"))
async def sim_cmd(message: types.Message):
    try:
        text = message.get_args()
        if "||" not in text:
            await message.answer("Format: /similarity sentence1 || sentence2")
            return
        s1, s2 = text.split("||", 1)
        score = sentence_similarity(s1.strip(), s2.strip())
        await message.answer(f"🔍 Similarity score: {score:.3f}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


@dp.message(Command("translate"))
async def translate_cmd(message: types.Message):
    try:
        text = message.get_args()
        if not text:
            await message.answer("Send text to translate. Example: /translate Hello world")
            return
        result = translate_text(text.strip())
        await message.answer(f"🌐 Translation: {result}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


@dp.message(Command("generate"))
async def generate_cmd(message: types.Message):
    try:
        prompt = message.get_args()
        if not prompt:
            await message.answer("Send a prompt to generate text. Example: /generate Hello AI")
            return
        result = generate_text(prompt.strip())
        await message.answer(f"🧠 Generated: {result}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


async def main():
    print("Starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("Bot starting...")
        asyncio.run(main())
    except Exception as e:
        print("FATAL ERROR:", e)
        import traceback
        traceback.print_exc()
