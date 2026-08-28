"use server";

import { redirect } from "next/navigation";
import { getSession } from "@/lib/session";
import { supabase } from "@/lib/supabase";
import { revalidatePath } from "next/cache";

// Login action
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

// Logout action
export async function logout() {
  const session = await getSession();
  session.destroy();
  redirect("/admin/login");
}

// Get all stories (admin dashboard)
export async function getAdminStories() {
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

// Update a story
export async function updateStory(id: string, formData: FormData) {
  const title = formData.get("title") as string;
  const summary = formData.get("summary") as string;
  const why_it_matters = formData.get("why_it_matters") as string;
  const key_points = (formData.get("key_points") as string)
    .split("\n")
    .filter((p) => p.trim() !== "");

  const { error } = await supabase
    .from("stories")
    .update({
      title,
      summary,
      why_it_matters,
      key_points,
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

// Delete a story
export async function deleteStory(id: string) {
  const { error } = await supabase.from("stories").delete().eq("id", id);

  if (error) {
    console.error("Error deleting story:", error);
    throw new Error("Failed to delete story");
  }

  revalidatePath("/admin");
  redirect("/admin");
}

// Create a new story
export async function createStory(formData: FormData) {
  const title = formData.get("title") as string;
  const summary = formData.get("summary") as string;
  const why_it_matters = formData.get("why_it_matters") as string;
  const key_points = (formData.get("key_points") as string)
    .split("\n")
    .filter((p) => p.trim() !== "");

  const { error } = await supabase.from("stories").insert({
    title,
    summary,
    why_it_matters,
    key_points,
    briefing_id: null, 
  });

  if (error) {
    console.error("Error creating story:", error);
    throw new Error("Failed to create story");
  }

  revalidatePath("/admin");
  redirect("/admin");
}