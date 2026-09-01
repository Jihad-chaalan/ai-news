import Link from "next/link";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="text-center space-y-6">
          {/* Telegram CTA – same as About page */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-md text-left">
            <p className="text-gray-700 text-sm flex items-center gap-2">
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
                Join our channel to receive each news summary with sources directly on your phone.
              </span>
            </p>
            <a
              href="#"   // <-- Replace with your actual Telegram group link
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-2 text-blue-600 hover:underline font-medium text-sm"
            >
              Join our Telegram group →
            </a>
          </div>

          {/* Divider */}
          <div className="w-12 h-px bg-gray-300 mx-auto" />

          {/* Copyright */}
          <p className="text-sm text-gray-600">
            &copy; {year} <span className="font-medium text-gray-900">AI Daily News</span>.
            All rights reserved.
          </p>

          {/* Tech stack */}
          <p className="text-sm text-gray-500">
            Built with{" "}
                        <Link
              href="https://langchain-ai.github.io/langgraph/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline font-medium"
            >
              LangGraph
            </Link>
            ,{" "}
                        <Link
              href="https://nextjs.org"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Next.js
            </Link>
            
            , and{" "}
<Link
              href="https://supabase.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Supabase
            </Link>
          </p>
          <p className="text-xs text-gray-400">
            Orchestrated by autonomous AI agents
          </p>

          {/* Divider */}
          <div className="w-12 h-px bg-gray-300 mx-auto" />

          {/* Project info */}
          <div>
            <p className="text-sm font-semibold text-gray-900">
              Built as an AI Engineering Project
            </p>
            <p className="text-sm text-gray-600 mx-auto mt-1">
              AI Daily News is an independent project exploring how agentic AI can
              automate the complete research-to-publication workflow.
            </p>
            <p className="text-sm text-gray-600 mt-2">
              Built by <strong className="text-gray-900">Jihad Chaalan</strong>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}