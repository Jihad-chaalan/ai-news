import { notFound } from "next/navigation";
import { getStoryById } from "@/lib/supabase-queries";
import EditStoryForm from "@/components/EditStoryForm";

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
      <EditStoryForm story={story} />
    </div>
  );
}