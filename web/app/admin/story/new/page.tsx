import NewStoryForm from "@/components/NewStoryForm";

export default function NewStoryPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Add New Story</h1>
      <NewStoryForm />
    </div>
  );
}