import Link from "next/link";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="text-center space-y-4">
          {/* Copyright */}
          <p className="text-sm text-gray-600">
            &copy; {year} <span className="font-medium text-gray-900">AI Daily News</span>.
            All rights reserved.
          </p>

          {/* Tech stack */}
          <p className="text-sm text-gray-500">
            Built with{" "}
            <Link
              href="https://nextjs.org"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Next.js
            </Link>{" "}
            &amp;{" "}
            <Link
              href="https://supabase.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Supabase
            </Link>
          </p>

          {/* Divider */}
          <div className="w-12 h-px bg-gray-300 mx-auto" />

          {/* Project info */}
          <div>
            <p className="text-sm font-semibold text-gray-900">
              Built as an AI Engineering Project
            </p>
            <p className="text-sm text-gray-600 max-w mx-auto mt-1">
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