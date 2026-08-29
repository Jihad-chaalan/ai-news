"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { getSession } from "@/lib/session";
import { supabase } from "@/lib/supabase";
import { Database } from "@/lib/database.types";

type Story = Database["public"]["Tables"]["stories"]["Row"];
type StoryInsert = Database["public"]["Tables"]["stories"]["Insert"];

// ===================== AUTH =====================

export async function login(formData: FormData) {
  const username = formData.get("username") as string;
  const password = formData.get("password") as string;

  const adminUser = process.env.ADMIN_USERNAME;
  const adminPass = process.env.ADMIN_PASSWORD;

  if (username === adminUser && password === adminPass) {
    const session = await getSession();
    session.isLoggedIn = true;
    session.username = username;
    await session.save();
    redirect("/admin");
  } else {
    redirect("/admin/login?error=Invalid credentials");
  }
}

export async function logout() {
  const session = await getSession();
  session.destroy();
  redirect("/admin/login");
}

// ===================== READ =====================

export async function getAdminStories(): Promise<Story[]> {
  const { data, error } = await supabase
    .from("stories")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.error("Error fetching stories:", error);
    return [];
  }
  return data;
}

// ===================== IMAGE UPLOAD =====================

export async function uploadImage(formData: FormData): Promise<string> {
  const file = formData.get("file") as File;
  if (!file) {
    throw new Error("No file provided");
  }

  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2, 8);
  const fileName = `${timestamp}_${random}.png`;

  const arrayBuffer = await file.arrayBuffer();
  const buffer = new Uint8Array(arrayBuffer);

  const { error } = await supabase.storage
    .from("ai-news-images")
    .upload(`stories/${fileName}`, buffer, {
      contentType: file.type || "image/png",
      cacheControl: "3600",
      upsert: false,
    });

  if (error) {
    console.error("Upload error:", error);
    throw new Error("Failed to upload image");
  }

  const { data: urlData } = supabase.storage
    .from("ai-news-images")
    .getPublicUrl(`stories/${fileName}`);

  return urlData.publicUrl;
}

// ===================== CREATE =====================

export async function createStory(data: {
  title: string;
  summary: string;
  why_it_matters: string;
  key_points: string[];
  image_url: string | null;
}) {
  // 1. Get today's date
  const today = new Date().toISOString().split("T")[0];
  console.log("📅 Today's date:", today);

  // 2. Fetch today's briefing (if it exists)
  const { data: briefingData, error: briefingError } = await supabase
    .from("briefings")
    .select("id")
    .eq("date", today)
    .maybeSingle();

  if (briefingError) {
    console.error("❌ Error fetching briefing:", briefingError);
  }

  console.log("📋 Briefing data:", briefingData);

  const briefingId = briefingData?.id || null;
  console.log("🆔 Briefing ID:", briefingId);

  // 3. Build the story object
  const story: StoryInsert = {
    title: data.title,
    summary: data.summary,
    why_it_matters: data.why_it_matters,
    key_points: data.key_points,
    image_url: data.image_url,
    briefing_id: briefingId,
  };

  console.log("📝 Story to insert:", story);

  // 4. Insert and return the inserted row
  const { data: inserted, error } = await supabase
    .from("stories")
    .insert(story)
    .select();

  if (error) {
    console.error("❌ Error creating story:", error);
    throw new Error("Failed to create story");
  }

  console.log("✅ Inserted story:", inserted);

  revalidatePath("/admin");
  redirect("/admin");
}

// ===================== UPDATE =====================

export async function updateStory(
  id: string,
  data: {
    title: string;
    summary: string;
    why_it_matters: string;
    key_points: string[];
    image_url: string | null;
  }
) {
  const { error } = await supabase
    .from("stories")
    .update({
      title: data.title,
      summary: data.summary,
      why_it_matters: data.why_it_matters,
      key_points: data.key_points,
      image_url: data.image_url,
    })
    .eq("id", id);

  if (error) {
    console.error("Error updating story:", error);
    throw new Error("Failed to update story");
  }

  revalidatePath("/admin");
  revalidatePath(`/story/${id}`);
  redirect("/admin");
}

// ===================== DELETE =====================

export async function deleteStory(id: string) {
  const { error } = await supabase.from("stories").delete().eq("id", id);

  if (error) {
    console.error("Error deleting story:", error);
    throw new Error("Failed to delete story");
  }

  revalidatePath("/admin");
  redirect("/admin");
}