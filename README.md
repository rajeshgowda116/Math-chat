# Math AI Chatbot

A FastAPI-based mathematics tutor chatbot with a ChatGPT-style interface, animated responses, saved chat history, and dark/light mode.

## Live Demo

🚀 **Live App**: [https://math-chat-7bsv.onrender.com](https://math-chat-7bsv.onrender.com)

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

## Deploying to Render

This application includes a `render.yaml` blueprint file for easy deployment on [Render](https://render.com).

### Option 1: Automatic Blueprint Deployment (Recommended)

1. Push your repository to GitHub / GitLab.
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** and select **Blueprint**.
4. Connect your repository.
5. When prompted, enter your `GEMINI_API_KEY` under Environment Variables.
6. Click **Apply**. Render will automatically build and launch your web service.

### Option 2: Manual Web Service Setup

1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** -> **Web Service**.
3. Connect your repository.
4. Configure the service settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -k uvicorn.workers.UvicornWorker app:app` (or `uvicorn app:app --host 0.0.0.0 --port $PORT`)

5. Under **Environment Variables**, add:
   - `GEMINI_API_KEY`: Your Google Gemini API Key
   - `DATABASE_URL` *(Optional)*: URL for external/Render PostgreSQL database (defaults to local SQLite).
6. Click **Create Web Service**.

