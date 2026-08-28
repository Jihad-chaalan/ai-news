import { notFound } from "next/navigation";
import { getStoryById } from "@/lib/supabase-queries";
import { updateStory } from "@/app/admin/actions";
import Link from "next/link";

interface EditPageProps {
  params: Promise<{ id: string }>;
}

export default async function EditStoryPage({ params }: EditPageProps) {
  const { id } = await params;
  const story = await getStoryById(id);

  if (!story) {
    notFound();
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Edit Story</h1>
      <form action={updateStory.bind(null, id)} className="space-y-4">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title
          </label>
          <input
            type="text"
            name="title"
            id="title"
            defaultValue={story.title}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div>
          <label htmlFor="summary" className="block text-sm font-medium text-gray-700">
            Summary
          </label>
          <textarea
            name="summary"
            id="summary"
            rows={4}
            defaultValue={story.summary}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div>
          <label htmlFor="why_it_matters" className="block text-sm font-medium text-gray-700">
            Why It Matters
          </label>
          <textarea
            name="why_it_matters"
            id="why_it_matters"
            rows={2}
            defaultValue={story.why_it_matters}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div>
          <label htmlFor="key_points" className="block text-sm font-medium text-gray-700">
            Key Points (one per line)
          </label>
          <textarea
            name="key_points"
            id="key_points"
            rows={4}
            defaultValue={story.key_points.join("\n")}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
        <div className="flex gap-4">
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
          >
            Update Story
          </button>
          <Link
            href="/admin"
            className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition"
          >
            Cancel
          </Link>
        </div>
      </form>
    </div>
  );
}