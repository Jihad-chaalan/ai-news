import { getTodayBriefing } from "@/lib/supabase-queries";
import StoryGrid from "@/components/StoryGrid";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];

export default async function HomePage() {
  const briefing = await getTodayBriefing();

  let stories: Story[] = [];
  let date: string | null = null;

  if (briefing) {
    stories = briefing.stories || [];
    date = briefing.date;
  }

  return (
    <div>
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold text-gray-900">Today&rsquo;s AI News</h1>
        {date && (
          <p className="text-gray-500 mt-2">
            {new Date(date).toLocaleDateString("en-US", {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        )}
        <p className="text-gray-600 mt-2 max-w-2xl mx-auto">
          The 6 most important AI stories, automatically researched and summarised for you.
        </p>
      </section>

      {stories.length > 0 ? (
        <StoryGrid stories={stories} date={date || undefined} />
      ) : (
        <div className="text-center py-12 text-gray-500">
          No news for today yet. Check back at 8 PM!
        </div>
      )}
    </div>
  );
}