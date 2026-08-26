import { notFound } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { getStoryById } from "@/lib/supabase-queries";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];
type Source = Database["public"]["Tables"]["sources"]["Row"];

interface StoryWithSources extends Story {
  sources: Source[];
}

interface StoryPageProps {
  params: Promise<{ id: string }>;
}

export default async function StoryPage({ params }: StoryPageProps) {
  const { id } = await params;
  const story = await getStoryById(id) as StoryWithSources | null;

  if (!story) {
    notFound();
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Back button */}
      <Link
        href="/"
        className="inline-block mb-6 text-blue-600 hover:text-blue-800 transition-colors"
      >
        ← Back to Home
      </Link>

      {/* Image */}
      <div className="relative w-full h-80 md:h-96 bg-gray-100 rounded-xl overflow-hidden mb-6">
        {story.image_url ? (
          <Image
            src={story.image_url}
            alt={story.title}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, 800px"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            No image available
          </div>
        )}
      </div>

      {/* Title */}
      <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
        {story.title}
      </h1>

      {/* Date */}
      {story.created_at && (
        <p className="text-sm text-gray-500 mb-4">
          {new Date(story.created_at).toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}
        </p>
      )}

      {/* Summary */}
      <div className="prose prose-lg max-w-none mb-6">
        <p className="text-gray-700 leading-relaxed">{story.summary}</p>
      </div>

      {/* Why it matters */}
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-md mb-6">
        <h3 className="font-semibold text-blue-800">Why it matters</h3>
        <p className="text-gray-700">{story.why_it_matters}</p>
      </div>

      {/* Key points */}
      {story.key_points && story.key_points.length > 0 && (
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">Key points</h3>
          <ul className="list-disc pl-6 space-y-1 text-gray-700">
            {story.key_points.map((point: string, index: number) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Sources */}
      {story.sources && story.sources.length > 0 && (
        <div className="border-t border-gray-200 pt-4 mt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Sources</h3>
          <ul className="space-y-1">
            {story.sources.map((source: Source) => (
              <li key={source.id}>
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {source.publisher || source.url}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}