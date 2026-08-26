import Link from "next/link";

export default function NotFound() {
  return (
    <div className="text-center py-20">
      <h1 className="text-4xl font-bold text-gray-900">Story not found</h1>
      <p className="text-gray-600 mt-2">The story you are looking for does not exist.</p>
      <Link href="/" className="inline-block mt-6 text-blue-600 hover:underline">
        ← Back to Home
      </Link>
    </div>
  );
}