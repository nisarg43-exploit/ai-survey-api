# AI Survey API (FastAPI + OpenAI)

This API generates two-part business responses based on survey input using GPT-4o-mini.

## 🚀 Run Locally

```bash
pip install -r requirements.txt
uvicorn api_service:app --reload
```

Then open:  
http://127.0.0.1:8000/docs

## 📦 Environment Variables

Rename `.env.template` to `.env` and add your OpenAI key:

```
OPENAI_API_KEY=sk-your-key-here
```

## 🌍 Deploy (Render or Railway)

1. Push to GitHub
2. Set `OPENAI_API_KEY` as an environment variable in the dashboard
3. Use `uvicorn api_service:app --host=0.0.0.0 --port=10000` as start command