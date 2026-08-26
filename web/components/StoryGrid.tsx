import StoryCard from "./StoryCard";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];

interface StoryGridProps {
  stories: Story[];
  date?: string;
}

export default function StoryGrid({ stories, date }: StoryGridProps) {
  if (!stories || stories.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No stories available for this date.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {stories.map((story) => (
        <StoryCard key={story.id} story={story} date={date} />
      ))}
    </div>
  );
}