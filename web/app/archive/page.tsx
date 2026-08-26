import Link from "next/link";
import { getBriefingDates } from "@/lib/supabase-queries";

export default async function ArchivePage() {
  const dates = await getBriefingDates();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Archive</h1>
      <p className="text-gray-600 mb-6">
        Browse AI news from the last 7 days.
      </p>

      {dates.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          No briefings available yet. Check back after the first daily run!
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {dates.map((date) => (
            <Link
              key={date}
              href={`/archive/${date}`}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-100"
            >
              <h2 className="text-xl font-semibold text-gray-900">
                {new Date(date).toLocaleDateString("en-US", {
                  weekday: "long",
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </h2>
              <p className="text-sm text-gray-500 mt-1">View briefing →</p>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}