import { notFound } from "next/navigation";
import Link from "next/link";
import { getBriefingByDate } from "@/lib/supabase-queries";
import StoryGrid from "@/components/StoryGrid";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];

interface ArchiveDatePageProps {
  params: Promise<{ date: string }>;
}

export default async function ArchiveDatePage({ params }: ArchiveDatePageProps) {
  const { date } = await params;
  const briefing = await getBriefingByDate(date);

  if (!briefing) {
    notFound();
  }

  const stories: Story[] = briefing.stories || [];
  const formattedDate = new Date(date).toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <Link
        href="/archive"
        className="inline-block mb-6 text-blue-600 hover:text-blue-800 transition-colors"
      >
        ← Back to Archive
      </Link>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">
        AI News – {formattedDate}
      </h1>
      <p className="text-gray-600 mb-6">
        {stories.length} stories from this day.
      </p>

      <StoryGrid stories={stories} date={date} />
    </div>
  );
}