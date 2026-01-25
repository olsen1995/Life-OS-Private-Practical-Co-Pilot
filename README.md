# 🧠 LifeOS Co-Pilot

An AI-augmented FastAPI application designed to assist with daily life organization, task management, and personal knowledge routing through modular “modes”.

---

## 🚀 Features

- 📦 FastAPI backend with mode routing (Fixit, Fridge, Kitchen, Organizer)
- 📚 JSON-based user knowledge system
- 🧠 OCR (image-to-text) for fridge scanning using `pytesseract`
- 🧪 Unit & API tests with `pytest`
- 🐳 Docker-ready for deployment
- 🔐 Secrets-ready with `.env.example`

---

## ⚙️ Getting Started

### 🔧 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🧪 2. Run Tests

```bash
pytest tests/
```

### 🏃 3. Run the App (Locally)

```bash
uvicorn main:app --reload
```

Then visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Docker Support

### 📦 Build the Image

```bash
docker build -t lifeos-api .
```

### 🚀 Run the Container

```bash
docker run -p 8000:8000 lifeos-api
```

---

## 🔐 Environment Variables

Copy `.env.example` into a real `.env`:

```bash
cp .env.example .env
```

Then fill in secrets like:

```
OPENAI_API_KEY=your-key-here
```

---

## 🧪 Testing with Docker (Optional)

```bash
docker run --rm lifeos-api pytest tests/
```

---

## 📄 License

This project is licensed under the MIT License.