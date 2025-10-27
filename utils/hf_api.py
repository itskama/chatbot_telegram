import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

API_URLS = {
    "qa": "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2",
    "similarity": "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2",
    "translate": "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-ru",
    "generate": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
}


def query(model_key: str, payload: dict):
    response = requests.post(API_URLS[model_key], headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()


def question_answering(context, question):
    payload = {"inputs": {"context": context, "question": question}}
    result = query("qa", payload)
    return result.get("answer", "No answer found.")


def sentence_similarity(sentence1, sentence2):
    payload = {"inputs": {"source_sentence": sentence1, "sentences": [sentence2]}}
    result = query("similarity", payload)
    return result[0] if isinstance(result, list) else result


def translate_text(text):
    payload = {"inputs": text}
    result = query("translate", payload)
    return result[0]["translation_text"] if isinstance(result, list) else result


def generate_text(prompt):
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200}}
    result = query("generate", payload)
    return result[0]["generated_text"] if isinstance(result, list) else result
