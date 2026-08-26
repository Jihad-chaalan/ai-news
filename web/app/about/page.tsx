import Link from "next/link";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">About AI Daily News</h1>

      <div className="prose prose-lg text-gray-700 max-w-none">
        <p className="lead">
          <strong>AI Daily News</strong> is an automated AI news platform that delivers the{" "}
          <strong>6 most important AI stories</strong> every day at 8 PM — researched, deduplicated,
          ranked, summarised, illustrated, and published through an agentic AI pipeline.
        </p>

        <p>
          The goal is simple: keep up with the rapidly changing AI industry without having to read
          dozens of articles every day.
        </p>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">How It Works</h2>
        <ol className="list-decimal pl-6 space-y-2">
          <li>
            <strong>Research</strong> – Collects AI‑related articles from multiple news providers,
            including APITube and NewsData.io, using a broad set of AI‑related topics and keywords.
          </li>
          <li>
            <strong>Deduplication</strong> – Groups articles covering the same underlying event using
            semantic embeddings and cosine similarity, allowing multiple sources to be combined into
            a single story.
          </li>
          <li>
            <strong>Ranking</strong> – An LLM evaluates the deduplicated stories based on factors such
            as impact, technical significance, novelty, and audience interest, selecting the 6 most
            important stories of the day.
          </li>
          <li>
            <strong>Summarisation</strong> – Generates a concise summary, &quot;why it matters&quot; explanation,
            and 3 key points for each selected story.
          </li>
          <li>
            <strong>Illustration</strong> – Generates an editorial‑style image prompt and creates a
            unique AI‑generated image using Cloudflare Workers AI, with a fallback image provider
            when necessary.
          </li>
          <li>
            <strong>Validation &amp; Publishing</strong> – A validation stage checks the generated content
            before it is stored in Supabase and published to the website and Telegram.
          </li>
        </ol>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Agentic Workflow</h2>
        <p>
          AI Daily News isn&rsquo;t powered by a single AI call. The workflow is orchestrated using
          <strong> LangGraph</strong>, with specialised stages responsible for different parts of the
          pipeline:
        </p>

        <pre className="bg-gray-100 p-4 rounded-lg text-sm text-gray-700 overflow-x-auto">
{`Research
    ↓
Deduplication
    ↓
Ranking
    ↓
Top 6 Stories
    ↓
┌───────────────┬────────────────┐
│               │                │
Summary       Image Prompt       │
│               ↓                │
│         Image Generation       │
└───────────────┴────────────────┘
                ↓
           Validation
                ↓
            Publishing`}
        </pre>

        <p>
          The workflow is designed to handle failures, retries, and fallback providers rather than
          relying on a single model call.
        </p>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Tech Stack</h2>
        <ul className="list-disc pl-6 space-y-1">
          <li>
            <strong>AI Orchestration</strong> – LangGraph + Python
          </li>
          <li>
            <strong>Backend API</strong> – FastAPI + Python
          </li>
          <li>
            <strong>Frontend</strong> – Next.js, TypeScript, Tailwind CSS
          </li>
          <li>
            <strong>Database</strong> – Supabase PostgreSQL
          </li>
          <li>
            <strong>File Storage</strong> – Supabase Storage
          </li>
          <li>
            <strong>LLM</strong> – Groq (<code>openai/gpt-oss-120b</code>)
          </li>
          <li>
            <strong>Embeddings</strong> – Semantic embedding model + cosine similarity
          </li>
          <li>
            <strong>News Sources</strong> – APITube + NewsData.io
          </li>
          <li>
            <strong>Image Generation</strong> – Cloudflare Workers AI + fallback provider
          </li>
          <li>
            <strong>Messaging</strong> – Telegram Bot API
          </li>
        </ul>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Why This Project?</h2>
        <p>
          AI Daily News is designed as an end‑to‑end AI engineering project, demonstrating how multiple
          AI and software components can work together as an automated system.
        </p>
        <p>It combines:</p>
        <ul className="list-disc pl-6 space-y-1">
          <li>🤖 Agentic AI orchestration</li>
          <li>🔎 Multi‑source research</li>
          <li>🔗 Semantic deduplication</li>
          <li>🧠 LLM‑based ranking</li>
          <li>✍️ Structured AI summarisation</li>
          <li>🎨 AI image generation</li>
          <li>🔄 Fallback and retry mechanisms</li>
          <li>✅ Content validation</li>
          <li>📊 Workflow monitoring</li>
          <li>🗄️ Database and storage management</li>
          <li>📱 Automated Telegram publishing</li>
          <li>🌐 Next.js web publishing</li>
        </ul>
        <p>
          The system is built with modular architecture and separation of concerns, making individual
          providers and components replaceable without redesigning the entire pipeline.
        </p>

        <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">Daily Automation</h2>
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <ul className="list-disc pl-6 space-y-1 text-sm text-gray-600">
            <li>
              <strong>Schedule</strong> — The pipeline automatically runs every day at 8:00 PM UTC.
            </li>
            <li>
              <strong>Pipeline</strong> — News is researched, deduplicated, ranked, summarised,
              illustrated, validated, and published automatically.
            </li>
            <li>
              <strong>Data Retention</strong> — Only the latest 7 days of news are retained. Older
              stories and associated assets are automatically removed.
            </li>
            <li>
              <strong>Distribution</strong> — The final daily briefing is published on the website
              and sent to Telegram.
            </li>
          </ul>
        </div>

        <div className="mt-8 p-4 bg-gray-50 rounded-lg border border-gray-200 text-sm text-gray-600">
          {/* <p>
            <strong>Built as an AI Engineering Project</strong>
            <br />
            AI Daily News is an independent project exploring how agentic AI can automate the complete
            research‑to‑publication workflow.
          </p>
          <p className="mt-2">
            Built by <strong>Jihad Chaalan</strong>
          </p> */}
          <Link
            href="https://github.com/Jihad-chaalan/ai-news"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-2 text-blue-600 hover:underline font-medium"
          >
            GitHub →
          </Link>
        </div>
      </div>
    </div>
  );
}