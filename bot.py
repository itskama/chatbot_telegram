import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from utils.hf_api import question_answering, sentence_similarity, translate_text, generate_text


# ======================
# ENV
# ======================
load_dotenv()   # Render сам подставляет TELEGRAM_TOKEN + HF_TOKEN


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
        "/ask — Question Answering\n"
        "/similarity — Sentence Similarity\n"
        "/translate — Translate EN→RU\n"
        "/generate — Text Generation"
    )


# ======================
# /ask
# ======================
@dp.message(Command("ask"))
async def ask_cmd(message: types.Message):
    await message.answer(
        "📝 Send context and question separated by a line.\n\nExample:\n"
        "Context: The sky is blue.\nQuestion: What color is the sky?"
    )


@dp.message(F.text.startswith("Context:"))
async def handle_qa(message: types.Message):
    try:
        parts = message.text.split("Question:")
        context = parts[0].replace("Context:", "").strip()
        question = parts[1].strip()

        answer = question_answering(context, question)
        await message.answer(f"💡 <b>Answer:</b> {answer}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


# ======================
# /similarity
# ======================
@dp.message(Command("similarity"))
async def sim_cmd(message: types.Message):
    await message.answer("✍️ Send two sentences separated by a line break.")


@dp.message(F.text.contains("\n"))
async def handle_similarity(message: types.Message):
    try:
        s1, s2 = message.text.split("\n", 1)
        score = sentence_similarity(s1.strip(), s2.strip())
        await message.answer(f"🔍 Similarity score: {score:.3f}")
    except Exception:
        pass


# ======================
# /translate
# ======================
@dp.message(Command("translate"))
async def translate_cmd(message: types.Message):
    await message.answer("🌐 Send English text to translate into Russian.")


# ======================
# /generate
# ======================
@dp.message(Command("generate"))
async def generate_cmd(message: types.Message):
    await message.answer("🧠 Send a prompt to generate text.")


# ======================
# Debug — всё остальное
# ======================
@dp.message()
async def debug_all(message: types.Message):
    print("Incoming message:", message.text)
    await message.answer(f"You said: {message.text}")


# ======================
# MAIN
# ======================
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
