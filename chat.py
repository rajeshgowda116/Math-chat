import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


SYSTEM_PROMPT = """
You are an expert Mathematics Tutor.

Rules:
- Answer only mathematics questions.
- Explain step by step.
- Use simple language.
- Format equations clearly.
- If the question is not about mathematics, politely refuse.
"""

def ask_math(question):
    prompt = f"{SYSTEM_PROMPT}\n\nQuestion:\n{question}"
    response = model.generate_content(prompt)
    return response.text
    response = model.generate_content(prompt)
    return response.text