AI Daily News
An AI‑powered news aggregator that automatically researches, ranks, summarises, illustrates, and publishes the 6 most important AI news stories every day at 8:00 PM.

Built with LangGraph agentic workflows, FastAPI, Next.js, and Supabase – a portfolio project showcasing advanced AI engineering and modern full‑stack development.

Features
Automated daily research – collects articles from multiple news APIs.

Semantic deduplication – clusters similar stories using embeddings and cosine similarity.

LLM‑based ranking – selects the top 6 most impactful stories.

Multi‑agent generation – creates summaries, “why it matters” blurbs, and editorial image prompts.

Fallback image generation – primary provider (Cloudflare Workers AI) with configurable fallbacks.

Supabase storage – images stored in object storage, metadata in PostgreSQL.

7‑day retention – auto‑cleans older data and images.

Dual publishing – updates a Next.js website and sends a daily briefing to Telegram.

Scheduled execution – runs daily without developer intervention.

Tech Stack
Layer Technology
Orchestration LangGraph (Python)
Backend API FastAPI (Python)
Frontend Next.js, TypeScript, Tailwind CSS
Database Supabase (PostgreSQL + Storage)
AI/LLM Configurable (OpenAI, Anthropic, etc.)
Image Gen Cloudflare Workers AI + fallbacks
Messaging Telegram Bot API
Deployment Docker, GitHub Actions
CI/CD GitHub Actions
Getting Started
Prerequisites
Docker & Docker Compose (recommended)

Or Python 3.11+ and Node.js 20+ for local development

Supabase account (free tier works)

API keys for news/LLM/image providers

Environment Variables
Copy .env.example to .env and fill in your secrets:

bash
cp .env.example .env
Key variables:

DATABASE_URL, SUPABASE_URL, SUPABASE_KEY

LLM_API_KEY (OpenAI/Anthropic)

NEWS*API_KEY*\* (NewsAPI, GNews, etc.)

CLOUDFLARE_API_KEY, CLOUDFLARE_ACCOUNT_ID

TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

FRONTEND_URL

Running with Docker (recommended)
bash
docker-compose up --build
Backend: http://localhost:8000

Frontend: http://localhost:3000

Running locally (development)
Backend:

bash
cd backend
poetry install # or pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend:

bash
cd frontend
npm install
npm run dev
Project Status
This project is under active development. See the phases plan for the incremental build roadmap.
