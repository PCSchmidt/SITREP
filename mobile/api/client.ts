import { Briefing } from '../types/briefing';

// API Configuration
// Production Railway URL
const API_BASE_URL = 'https://sitrep-production-6aac.up.railway.app';

// Backend API Response Types
interface BackendBriefingSection {
  title: string;
  content: string;
  sources: string[];
}

interface BackendBriefing {
  region: string;
  bluf: string;
  sections: BackendBriefingSection[];
  key_developments: string[];
  outlook: string;
  generated_at: string;
  metadata: {
    model_id: string;
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
    finish_reason: string;
    model_used: string;
    cost_estimate: string;
  };
  article_count: number;
}

interface BackendBriefingResponse {
  status: string;
  region: string;
  briefing: BackendBriefing;
  source_file: string;
  timestamp: string;
}

// Transform backend briefing to mobile format
function transformBriefing(
  backendResponse: BackendBriefingResponse
): Briefing {
  const { briefing } = backendResponse;

  // Extract date from generated_at for ID
  const dateStr = briefing.generated_at.split('T')[0];

  // Map region to short code (must match tokens.ts Regions)
  const regionMap: Record<string, string> = {
    'Europe/Africa': 'europe-africa',
    'Middle East': 'middle-east',
    'Indo-Pacific': 'indo-pacific',
    'Western Hemisphere': 'western-hemisphere',
  };

  const regionCode = regionMap[briefing.region] || briefing.region;

  // Calculate read time (rough estimate: 200 words per minute)
  const wordCount = briefing.sections.reduce(
    (acc, section) => acc + section.content.split(' ').length,
    0
  );
  const readTime = Math.ceil(wordCount / 200);

  // Create preview from BLUF (first 150 chars)
  const preview = briefing.bluf.substring(0, 150) + (briefing.bluf.length > 150 ? '...' : '');

  // Transform sections to remove sources array (not in mobile format)
  const transformedSections = briefing.sections.map(section => ({
    title: section.title,
    content: section.content,
  }));

  // Create sources from section sources
  const sources = briefing.sections.flatMap((section) =>
    section.sources.map((sourceTitle) => ({
      title: sourceTitle,
      publication: 'ISW', // Default publication
      date: dateStr,
      url: 'https://understandingwar.org', // Default URL
    }))
  );

  return {
    id: dateStr,
    timestamp: new Date(briefing.generated_at).toISOString().replace('T', ' ').substring(0, 19) + ' UTC',
    title: `${briefing.region} Intelligence Briefing`,
    preview,
    regions: [regionCode],
    bluf: briefing.bluf,
    readTime,
    content: [
      {
        region: briefing.region,
        bluf: briefing.bluf,
        sections: transformedSections,
      },
    ],
    sources,
  };
}

// API Functions
export async function fetchLatestBriefing(region: string = 'Europe/Africa'): Promise<Briefing> {
  const response = await fetch(`${API_BASE_URL}/briefing/latest?region=${encodeURIComponent(region)}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch briefing: ${response.status} ${response.statusText}`);
  }

  const data: BackendBriefingResponse = await response.json();
  return transformBriefing(data);
}

export async function fetchAllRegionBriefings(): Promise<Briefing[]> {
  const regions = ['Europe/Africa', 'Middle East', 'Indo-Pacific', 'Western Hemisphere'];

  console.log('Fetching briefings for regions:', regions);

  const briefingPromises = regions.map(region =>
    fetchLatestBriefing(region)
      .then(briefing => {
        console.log(`Successfully fetched ${region}:`, briefing.id);
        return briefing;
      })
      .catch(err => {
        console.warn(`Failed to fetch ${region}:`, err);
        return null;
      })
  );

  const briefings = await Promise.all(briefingPromises);
  const filtered = briefings.filter((b): b is Briefing => b !== null);
  console.log(`Total briefings fetched: ${filtered.length}`, filtered.map(b => b.id));
  return filtered;
}
