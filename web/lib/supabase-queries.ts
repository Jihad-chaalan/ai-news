import { supabase } from './supabase';
import { Database } from './database.types';

type Story = Database['public']['Tables']['stories']['Row'];
type Briefing = Database['public']['Tables']['briefings']['Row'];
type Source = Database['public']['Tables']['sources']['Row'];

export interface StoryWithSources extends Story {
  sources: Source[];
}

export interface BriefingWithStories extends Briefing {
  stories: StoryWithSources[];
}

// Get today's briefing (delegates to getBriefingByDate)
export async function getTodayBriefing(): Promise<BriefingWithStories | null> {
  const today = new Date().toISOString().split('T')[0];
  return getBriefingByDate(today);
}

// Get briefing by date (YYYY-MM-DD)
export async function getBriefingByDate(date: string): Promise<BriefingWithStories | null> {
  const { data, error } = await supabase
    .from('briefings')
    .select(`
      *,
      stories (
        *,
        sources (*)
      )
    `)
    .eq('date', date)
    .maybeSingle();

  if (error) {
    console.error('Error fetching briefing:', error);
    return null;
  }

  return data as BriefingWithStories | null;
}

// Get latest briefing (most recent date)
export async function getLatestBriefing(): Promise<BriefingWithStories | null> {
  const { data, error } = await supabase
    .from('briefings')
    .select(`
      *,
      stories (
        *,
        sources (*)
      )
    `)
    .order('date', { ascending: false })
    .limit(1)
    .maybeSingle();

  if (error) {
    console.error('Error fetching latest briefing:', error);
    return null;
  }

  return data as BriefingWithStories | null;
}

// Get list of dates for the last 7 days
export async function getBriefingDates(): Promise<string[]> {
  const { data, error } = await supabase
    .from('briefings')
    .select('date')
    .order('date', { ascending: false })
    .limit(7);

  if (error) {
    console.error('Error fetching dates:', error);
    return [];
  }

  return data.map((row) => row.date);
}

// Get a single story by ID
export async function getStoryById(id: string): Promise<StoryWithSources | null> {
  const { data, error } = await supabase
    .from('stories')
    .select(`
      *,
      sources (*)
    `)
    .eq('id', id)
    .maybeSingle();

  if (error) {
    console.error('Error fetching story:', error);
    return null;
  }

  return data as StoryWithSources | null;
}