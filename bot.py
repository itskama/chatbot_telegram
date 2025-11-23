import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from utils.hf_api import question_answering, sentence_similarity, translate_text, generate_text

# Загружаем переменные из .env (укажи свой путь)
load_dotenv(dotenv_path=r"C:\ml 1 sem\chatbot_telegram\.env")

# Проверяем, что токен читается
print("TELEGRAM_TOKEN =", os.getenv("TELEGRAM_TOKEN"))
print("HF_TOKEN =", os.getenv("HF_TOKEN"))

logging.basicConfig(level=logging.INFO)
load_dotenv()




bot = Bot(
    token=os.getenv("TELEGRAM_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


# /start
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


# /ask
@dp.message(Command("ask"))
async def ask_cmd(message: types.Message):
    await message.answer(
        "📝 Send context and question separated by a line.\n\nExample:\n"
        "Context: The sky is blue.\nQuestion: What color is the sky?"
    )


# QA processing
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


# /similarity
@dp.message(Command("similarity"))
async def sim_cmd(message: types.Message):
    await message.answer("✍️ Send two sentences separated by a line break.")


# similarity
@dp.message(F.text.contains("\n"))
async def handle_similarity(message: types.Message):
    try:
        s1, s2 = message.text.split("\n", 1)
        score = sentence_similarity(s1.strip(), s2.strip())
        await message.answer(f"🔍 Similarity score: {score:.3f}")
    except Exception:
        pass    # чтобы не ловить QA сообщения


# /translate
@dp.message(Command("translate"))
async def translate_cmd(message: types.Message):
    await message.answer("🌐 Send text in English to translate into Russian.")

@dp.message()
async def debug_all(message: types.Message):
    print("Пришло сообщение:", message.text)
    await message.answer(f"Вы написали: {message.text}")

