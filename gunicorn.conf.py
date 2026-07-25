import os

# Automatically use uvicorn ASGI worker class for FastAPI
worker_class = "uvicorn.workers.UvicornWorker"

# Bind to PORT provided by Render (default 10000)
port = os.getenv("PORT", "10000")
bind = f"0.0.0.0:{port}"
