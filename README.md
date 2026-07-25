# Math AI Chatbot

A FastAPI-based mathematics tutor chatbot with a ChatGPT-style interface, animated responses, saved chat history, and dark/light mode.

## Features

- Math-only AI tutor responses
- ChatGPT-like typing animation
- SQLite chat history
- Sidebar with previous chats
- Open and delete saved chats
- New chat creation
- Dark mode and light mode toggle
- FastAPI backend
- Gemini API integration

## Project Structure

```text
math_chat/
├── app.py
├── chat.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── static/
│   └── style.css
└── templates/
    └── index.html
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Run The App

```bash
uvicorn app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Database

The app uses SQLite and automatically creates `math_chat.db` when it starts.

Tables:

- `chat_sessions`
- `chat_messages`

## API Endpoints

```text
GET    /
POST   /chat
POST   /chat/new
GET    /history
GET    /history/{session_id}
DELETE /history/{session_id}
```

## Notes

The chatbot is designed to answer mathematics questions only. For non-math questions, it should respond with a math-only message.
