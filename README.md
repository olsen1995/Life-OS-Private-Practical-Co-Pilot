# 🧠 LifeOS Co-Pilot

An AI-augmented FastAPI application to help you manage daily life using modular "modes" — now powered by OpenAI and deployable on Render.

---

## 🚀 Features

- ⚡ Mode-based modular architecture (Fixit, Kitchen, Organizer, etc.)
- 🤖 AI-powered chat using OpenAI (via `/chat`)
- 🧠 Custom knowledge routing for personalized assistance
- 🧪 Pytest-integrated test suite
- 🐳 Docker-ready
- 🔐 `.env.example` for safe secret storage
- ☁️ Ready for Render deployment with `render.yaml`
- ✅ CI/CD with GitHub Actions
- 🧼 Pre-commit config with `black`, `flake8`, and `isort`

---

## 🧪 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Start the app
uvicorn main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💬 AI Chat Mode

POST to `/chat`:

```json
{
  "input": "What's in my fridge?"
}
```

Your `.env` must contain:

```env
OPENAI_API_KEY=your-key-here
```

---

## 🐳 Docker Support

```bash
docker build -t lifeos-api .
docker run -p 8000:8000 lifeos-api
```

---

## ☁️ Deploy to Render

Render auto-detects `render.yaml`:
- Click “New Web Service” → connect your GitHub repo
- Add `OPENAI_API_KEY` as an env var in the dashboard
- Deploy

---

## ✅ Pre-Commit Hooks

```bash
pip install pre-commit
pre-commit install
```

---

## 📄 License

MIT License — free to use, modify, and share.