AI Daily News
AI Daily News is a fully automated AI news platform that researches, ranks, summarises, illustrates, and publishes the 5 most important AI stories every day.

Built with LangGraph agentic workflows, Next.js, and Supabase – it demonstrates production‑grade AI orchestration, semantic deduplication, LLM‑based ranking, image generation, and multi‑channel publishing.

🌐 Website: [ai-daily-news.vercel.app](https://ai-news-lilac-five.vercel.app/)
📱 Telegram: Join our group https://t.me/+R6JQYLw8FbNlYmE0

✨ Features
Automated daily research – fetches from multiple news APIs (APITube, NewsData.io).

Semantic deduplication – groups identical stories using embeddings + cosine similarity.

LLM‑based ranking – scores stories on impact, novelty, and audience interest using Groq.

AI‑generated summaries – produces concise summaries, "why it matters", and 3 key points.

Automated illustration – generates editorial images via Cloudflare Workers AI (with Pollinations.ai fallback).

Supabase storage – stores final briefings, stories, sources, and generated images.

7‑day retention – automatically deletes older records and images.

Telegram publishing – sends each story as a separate, formatted message with clickable sources.

Admin panel – full CRUD operations for stories with image upload.

Extensible design – provider pattern for news APIs, LLMs, and image generators.

🧱 Tech Stack
Layer Technology
Orchestration LangGraph (Python)
Backend (Agents) Python 3.11+, async, Pydantic
Frontend Next.js 14, TypeScript, Tailwind CSS
Database Supabase (PostgreSQL + Storage)
LLM Groq (openai/gpt-oss-120b)
Image Generation Cloudflare Workers AI + Pollinations.ai (fallback)
News APIs APITube, NewsData.io
Messaging Telegram Bot API
CI/CD GitHub Actions (scheduled daily run)
Deployment Vercel (frontend), GitHub Actions (backend)
⚙️ How It Works
text
Research
↓
Deduplication
↓
Ranking
↓
Top 5 Stories
↓
┌───────────────┬────────────────┐
│ │ │
Summary Image Prompt │
│ ↓ │
│ Image Generation │
└───────────────┴────────────────┘
↓
Validation
↓
Publishing
Research – Fetches articles from multiple news APIs using AI‑related keywords.

Deduplication – Clusters similar articles using sentence‑transformers and cosine similarity.

Ranking – Scores each cluster using Groq and selects the top 5.

Summarisation – Generates a structured summary (title, summary, why it matters, key points).

Image Generation – Creates a prompt for each story, then generates and uploads an image to Supabase Storage.

Validation – Checks that all required fields are present; retries failed stories up to 3 times.

Publishing – Saves the final briefing to Supabase and sends each story as a Telegram message.

Cleanup – Deletes briefings older than 7 days and their associated images.

📂 Project Structure
text
ai-news/
├── backend/
│ ├── app/
│ │ ├── adapters/ # API providers (news, LLM, image, repository, publisher)
│ │ ├── graph/ # LangGraph nodes and workflow
│ │ ├── models/ # Pydantic models
│ │ ├── ports/ # Abstract interfaces (SOLID)
│ │ ├── services/ # Business logic (image generation, cleanup, etc.)
│ │ └── config.py # Settings loaded from .env
│ ├── tests/ # Unit and integration tests
│ └── pyproject.toml # Python dependencies (managed with uv)
├── web/ # Next.js frontend
│ ├── app/
│ ├── components/
│ └── package.json
├── .github/
│ └── workflows/
│ └── daily-run.yml # Scheduled daily pipeline
└── .env.example # Environment variables template

📅 Automation
The pipeline runs automatically every day via GitHub Actions at:

15:37 UTC (≈ 6:37 PM Lebanon time) – due to GitHub scheduler delays, it typically executes around 8 PM Lebanon time.

🌐 Frontend Pages
Page Route Description
Homepage / Latest 5 AI stories with images and summaries.
About /about Project explanation and tech stack.
Archive /archive List of available briefing dates.
Archive by Date /archive/[date] Stories from a specific date.
Story Detail /story/[id] Full story with sources and image.
Admin /admin Protected admin panel (login required).
🛠️ Admin Panel
Login – Secure login using iron-session.

Dashboard – View all stories with edit/delete options.

Add Story – Create a new story with image upload.

Edit Story – Update existing stories and images.

📱 Telegram Integration
Each story is sent as a separate Telegram message.

Messages include:

Title

Summary

Why it matters

Key points

Clickable source links

Image link

Delay between messages – 2 seconds (to avoid rate limiting).

🧹 7‑Day Retention
Briefings older than 7 days are automatically deleted.

Associated images are deleted from Supabase Storage.

Runs automatically after each publishing cycle.

🚀 Deployment
Frontend: Deployed on Vercel.

Backend: Runs via GitHub Actions (no separate server needed).

Database: Supabase (PostgreSQL + Storage).

❓ Known Issues
GitHub Actions Scheduler Delay: The cron may run 1‑2 hours late due to GitHub's free tier scheduler congestion. This is normal and doesn't affect the system – the pipeline still completes successfully.

📝 License
MIT – see LICENSE for details.

🙋‍♂️ Author
Jihad Chaalan
GitHub
LinkedIn

🔗 Links
Website: [ai-daily-news.vercel.app](https://ai-news-lilac-five.vercel.app/)

Telegram Group: Join our group https://t.me/+R6JQYLw8FbNlYmE0

GitHub: Jihad-chaalan/ai-news
