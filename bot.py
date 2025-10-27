import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from utils.hf_api import question_answering, sentence_similarity, translate_text, generate_text

load_dotenv()

from aiogram.client.bot import DefaultBotProperties

bot = Bot(
    token=os.getenv("TELEGRAM_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

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

@dp.message(Command("ask"))
async def ask_cmd(message: types.Message):
    await message.answer(
        "📝 Send context and question separated by a line.\n\nExample:\n"
        "Context: The sky is blue.\nQuestion: What color is the sky?"
    )

@dp.message(lambda msg: msg.text and msg.text.lower().startswith("context:"))
async def handle_qa(message: types.Message):
    try:
        parts = message.text.split("Question:")
        context = parts[0].replace("Context:", "").strip()
        question = parts[1].strip()
        answer = question_answering(context, question)
        await message.answer(f"💡 <b>Answer:</b> {answer}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@dp.message(Command("similarity"))
async def sim_cmd(message: types.Message):
    await message.answer("✍️ Send two sentences separated by a line break.")

@dp.message(lambda msg: "\n" in msg.text and not msg.text.lower().startswith("context:"))
async def handle_similarity(message: types.Message):
    try:
        s1, s2 = message.text.split("\n", 1)
        score = sentence_similarity(s1.strip(), s2.strip())
        await message.answer(f"🔍 Similarity score: {score:.3f}")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@dp.message(Command("translate"))
async def translate_cmd(message: types.Message):
    await message.answer("🌐 Send text in English to translate into Russian.")

@dp.message(Command("generate"))
async def generate_cmd(message: types.Message):
    await message.answer("🧠 Send a prompt to generate text.")

@dp.message(lambda msg: not msg.text.startswith("/"))
async def handle_general(message: types.Message):
    try:
        if message.reply_to_message and "🧠" in message.reply_to_message.text:
            result = generate_text(message.text)
            await message.answer(result)
        elif message.reply_to_message and "🌐" in message.reply_to_message.text:
            result = translate_text(message.text)
            await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
