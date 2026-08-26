import Image from "next/image";
import Link from "next/link";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];

interface StoryCardProps {
  story: Story;
  date?: string;
}

export default function StoryCard({ story, date }: StoryCardProps) {
  const truncatedSummary =
    story.summary.length > 120 ? story.summary.slice(0, 120) + "…" : story.summary;

  return (
    <div className="group bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col h-full">
      <div className="relative w-full h-48 bg-gray-100">
        {story.image_url ? (
          <Image
            src={story.image_url}
            alt={story.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400 text-sm">
            No image available
          </div>
        )}
      </div>
      <div className="p-4 flex flex-col flex-1">
        <h2 className="text-xl font-semibold text-gray-900 line-clamp-2 mb-1">
          {story.title}
        </h2>
        {date && <p className="text-sm text-gray-500 mb-2">{date}</p>}
        <p className="text-gray-600 text-sm flex-1 line-clamp-3">{truncatedSummary}</p>
        <Link
          href={`/story/${story.id}`}
          className="mt-4 inline-block text-blue-600 font-medium hover:text-blue-800 transition-colors"
        >
          Read more →
        </Link>
      </div>
    </div>
  );
}