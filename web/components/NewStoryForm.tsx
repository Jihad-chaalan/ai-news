"use client";

import { useTransition, useRef } from "react";
import { useRouter } from "next/navigation";
import { createStory, uploadImage } from "@/app/admin/actions";
import Link from "next/link";

export default function NewStoryForm() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    // Check if a file was uploaded
    const fileInput = formData.get("image_upload") as File;
    let imageUrl = formData.get("image_url") as string || null;

    if (fileInput && fileInput.size > 0) {
      // Upload the file
      const uploadFormData = new FormData();
      uploadFormData.append("file", fileInput);
      try {
        const uploadedUrl = await uploadImage(uploadFormData);
        imageUrl = uploadedUrl;
      } catch (error) {
        console.error("Image upload failed:", error);
        alert("Image upload failed. Please try again.");
        return;
      }
    }

    // Build the story data
    const storyData = {
      title: formData.get("title") as string,
      summary: formData.get("summary") as string,
      why_it_matters: formData.get("why_it_matters") as string,
      key_points: (formData.get("key_points") as string)
        .split("\n")
        .filter((p) => p.trim() !== ""),
      image_url: imageUrl,
    };

    startTransition(async () => {
      await createStory(storyData);
      router.push("/admin");
    });
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <input
          type="text"
          name="title"
          id="title"
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
          required
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="image_url" className="block text-sm font-medium text-gray-700">
          Image URL (or upload below)
        </label>
        <input
          type="url"
          name="image_url"
          id="image_url"
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="image_upload" className="block text-sm font-medium text-gray-700">
          Upload New Image (overrides URL above)
        </label>
        <input
          type="file"
          name="image_upload"
          id="image_upload"
          accept="image/*"
          className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
      </div>

      <div className="flex gap-4">
        <button
          type="submit"
          disabled={isPending}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition disabled:opacity-50"
        >
          {isPending ? "Creating..." : "Create Story"}
        </button>
        <Link
          href="/admin"
          className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition"
        >
          Cancel
        </Link>
      </div>
    </form>
  );
}