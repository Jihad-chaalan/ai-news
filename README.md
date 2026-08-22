# AI Daily News

**AI Daily News** is a fully automated news aggregator that researches, ranks, summarises, illustrates, and publishes the **6 most important AI news stories every day at 8:00 PM**.

Built with **LangGraph** agentic workflows, **Next.js**, and **Supabase** – it demonstrates production‑grade AI orchestration, semantic deduplication, LLM‑based ranking, image generation, and multi‑channel publishing.

> **Current Status**: The backend pipeline (research → dedupe → rank → summarise → image → validate → publish) is complete and working. The Next.js frontend is under active development.

---

## ✨ Features

- **Automated daily research** – fetches from multiple news APIs (APITube, NewsData.io).
- **Semantic deduplication** – groups identical stories using embeddings + cosine similarity.
- **LLM‑based ranking** – scores stories on impact, novelty, and audience interest using Groq.
- **AI‑generated summaries** – produces concise summaries, "why it matters", and 3 key points.
- **Automated illustration** – generates editorial images via Cloudflare Workers AI (with Pollinations.ai fallback).
- **Supabase storage** – stores final briefings, stories, sources, and generated images.
- **7‑day retention** – automatically deletes older records and images.
- **Telegram publishing** – sends each story as a separate, formatted message with clickable sources.
- **Extensible design** – provider pattern for news APIs, LLMs, and image generators.

---

## 🧱 Tech Stack

| Layer                | Technology                                         |
| -------------------- | -------------------------------------------------- |
| **Orchestration**    | LangGraph (Python)                                 |
| **Backend (Agents)** | Python 3.11+, async, Pydantic                      |
| **Frontend**         | Next.js 14, TypeScript, Tailwind CSS               |
| **Database**         | Supabase (PostgreSQL + Storage)                    |
| **LLM**              | Groq (`openai/gpt-oss-120b`)                       |
| **Image Generation** | Cloudflare Workers AI + Pollinations.ai (fallback) |
| **News APIs**        | APITube, NewsData.io                               |
| **Messaging**        | Telegram Bot API                                   |
| **Deployment**       | Docker, GitHub Actions (planned)                   |
