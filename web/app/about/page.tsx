import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">About AI Daily News</h1>

      <div className="prose prose-lg text-gray-700 max-w-none">
        <p className="lead">
          <strong>AI Daily News</strong> is an AI news platform that gets news through
          APIs, then filters the most important stories, extracts key points from each
          using LLMs, and publishes them with original sources – so you can read the
          full context if you want to explore further.
        </p>
                {/* Telegram channel CTA */}
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-md my-6">
          <p className="text-gray-700 text-base flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="#1D9BD9"
              className="w-5 h-5 shrink-0"
            >
              <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
            </svg>
            <span>
              <strong>Get the news daily on Telegram.</strong>{" "}
              Join our channel to receive each story directly on your phone.
            </span>
          </p>
          <a
            href="https://t.me/+R6JQYLw8FbNlYmE0"   
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-2 text-blue-600 hover:underline font-medium"
          >
            Join our Telegram group →
          </a>
        </div>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">How It Works</h2>
        <ol className="list-decimal pl-6 space-y-2">
          <li>
            <strong>Research</strong> – Fetches articles from multiple news APIs (APITube, NewsData.io)
            using AI-related keywords.
          </li>
          <li>
            <strong>Deduplication</strong> – Groups similar articles using semantic embeddings and
            cosine similarity (so you see only one story per event).
          </li>
          <li>
            <strong>Ranking</strong> – Scores each story on impact, novelty, and audience interest
            using a large language model (Groq).
          </li>
          <li>
            <strong>Summarisation</strong> – Generates a concise summary, &quot;why it matters&quot;, and 3 key
            points for each story.
          </li>
          <li>
            <strong>Illustration</strong> – Creates an editorial image prompt and generates a unique
            image using Cloudflare Workers AI (with fallback to Pollinations.ai).
          </li>
          <li>
            <strong>Validation &amp; Publishing</strong> – Validates all content, saves to a Supabase
            database, and sends each story as a separate Telegram message.
          </li>
        </ol>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Tech Stack</h2>
        <ul className="list-disc pl-6 space-y-1">
          <li>
            <strong>Orchestration</strong> – LangGraph (Python agentic workflow)
          </li>
          <li>
            <strong>Backend API</strong> – FastAPI (Python) – <em>planned</em>
          </li>
          <li>
            <strong>Frontend</strong> – Next.js 14, TypeScript, Tailwind CSS
          </li>
          <li>
            <strong>Database</strong> – Supabase (PostgreSQL + Storage)
          </li>
          <li>
            <strong>LLM</strong> – Groq (<code>openai/gpt-oss-120b</code>)
          </li>
          <li>
            <strong>Image Generation</strong> – Cloudflare Workers AI + Pollinations.ai (fallback)
          </li>
          <li>
            <strong>Messaging</strong> – Telegram Bot API
          </li>
        </ul>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Why This Project?</h2>
        <p>
          This project demonstrates production‑grade AI engineering skills, including agentic
          orchestration, semantic deduplication, LLM‑based ranking, image generation, multi‑source
          research, and end‑to‑end automation – all built with clean, modular code following SOLID
          principles.
        </p>

        <div className="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600">
            📅 <strong>Daily Schedule</strong> – The pipeline runs automatically every day at 8 PM UTC.
            <br />
            🕒 <strong>Data Retention</strong> – Only the last 7 days of news are kept; older records are
            automatically deleted.
          </p>
        </div>

        <div className="mt-8">
          <Link
            href="https://github.com/Jihad-chaalan/ai-news"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline font-medium"
          >
            View on GitHub →
          </Link>
        </div>
      </div>
    </div>
  );
}