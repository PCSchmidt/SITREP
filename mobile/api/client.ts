import AsyncStorage from '@react-native-async-storage/async-storage';
import { Briefing } from '../types/briefing';

// API Configuration
// Production Railway URL
const API_BASE_URL = 'https://sitrep-production-6aac.up.railway.app';

// Backend API Response Types
interface BackendBriefingSource {
  source: string;
  title: string;
  url?: string;
  published_date?: string;
}

interface BackendBriefingSection {
  title: string;
  content: string;
  sources: BackendBriefingSource[] | string[]; // Support both old and new format
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

function formatSourceDate(publishedDate?: string): string {
  if (!publishedDate) {
    return '';
  }

  const normalized = publishedDate.replace('Z', '+00:00');
  const parsed = new Date(normalized);
  if (Number.isNaN(parsed.getTime())) {
    return publishedDate.slice(0, 10);
  }

  return parsed.toISOString().slice(0, 10);
}

// Transform backend briefing to mobile format
function transformBriefing(
  backendResponse: BackendBriefingResponse
): Briefing {
  const { briefing } = backendResponse;

  // Extract date from generated_at for ID. Some older briefings were saved without
  // the field at all, so guard the parse: an unparseable date used to throw and the
  // whole region disappeared from the app.
  const generatedDate = new Date(briefing.generated_at ?? '');
  const hasValidDate = !Number.isNaN(generatedDate.getTime());
  const dateStr = (hasValidDate ? generatedDate : new Date()).toISOString().split('T')[0];

  // Map region to short code (must match tokens.ts Regions)
  const regionMap: Record<string, string> = {
    'Europe/Africa': 'europe-africa',
    'Middle East': 'middle-east',
    'Indo-Pacific': 'indo-pacific',
    'Western Hemisphere': 'western-hemisphere',
    'Global': 'all',
  };

  const regionCode = regionMap[briefing.region] || briefing.region;

  // Create unique ID combining region and date to prevent collisions
  const uniqueId = `${regionCode}-${dateStr}`;

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

  // Create sources from section sources with inferred publication
  const inferPublication = (title: string): { publication: string; url: string } => {
    const titleLower = title.toLowerCase();

    // ISW patterns
    if (titleLower.includes('iran update') || titleLower.includes('russian offensive') ||
        titleLower.includes('occupation update') || titleLower.includes('korean peninsula') ||
        titleLower.includes('china & taiwan update')) {
      return { publication: 'ISW', url: 'https://understandingwar.org' };
    }

    // The War Zone patterns (very specific headlines)
    if (titleLower.includes('war zone') || titleLower.includes('carriers as of') ||
        titleLower.includes('bunker talk') || titleLower.includes('ghost bat') ||
        titleLower.includes('where are the carriers')) {
      return { publication: 'The War Zone', url: 'https://www.twz.com' };
    }

    // War on the Rocks
    if (titleLower.includes('war on the rocks')) {
      return { publication: 'War on the Rocks', url: 'https://warontherocks.com' };
    }

    // Defense One
    if (titleLower.includes('defense one') || titleLower.includes('pentagon')) {
      return { publication: 'Defense One', url: 'https://www.defenseone.com' };
    }

    // Breaking Defense
    if (titleLower.includes('breaking defense')) {
      return { publication: 'Breaking Defense', url: 'https://breakingdefense.com' };
    }

    // Al Jazeera
    if (titleLower.includes('al jazeera')) {
      return { publication: 'Al Jazeera', url: 'https://www.aljazeera.com' };
    }

    // CFR
    if (titleLower.includes('cfr') || titleLower.includes('council on foreign')) {
      return { publication: 'CFR', url: 'https://www.cfr.org' };
    }

    // Foreign Policy - now default for geopolitical/international headlines
    // Since FP doesn't include "Foreign Policy" in article titles, use it as fallback
    // for articles that discuss international relations, trade, diplomacy
    if (titleLower.includes('foreign policy') ||
        titleLower.includes('trade talks') || titleLower.includes('u.s.-') ||
        titleLower.includes('trump') || titleLower.includes('biden') ||
        titleLower.includes('eu-') || titleLower.includes('commodity') ||
        titleLower.includes('abandon') || titleLower.includes('cubans') ||
        titleLower.includes('magyar') || titleLower.includes('erdogan')) {
      return { publication: 'Foreign Policy', url: 'https://foreignpolicy.com' };
    }

    // Default for truly unknown sources
    return { publication: 'Multi-Source', url: '#' };
  };

  const sources = briefing.sections.flatMap((section) =>
    section.sources.map((sourceData) => {
      // Handle new format: {source: "ISW", title: "Article Title"}
      if (typeof sourceData === 'object' && 'source' in sourceData && 'title' in sourceData) {
        const urlMap: Record<string, string> = {
          'ISW': 'https://understandingwar.org',
          'Foreign Policy': 'https://foreignpolicy.com',
          'The War Zone': 'https://www.twz.com',
          'War on the Rocks': 'https://warontherocks.com',
          'Defense One': 'https://www.defenseone.com',
          'Breaking Defense': 'https://breakingdefense.com',
          'Al Jazeera': 'https://www.aljazeera.com',
          'CFR': 'https://www.cfr.org',
          'Council on Foreign Relations': 'https://www.cfr.org',
        };
        return {
          title: sourceData.title,
          publication: sourceData.source,
          date: formatSourceDate(sourceData.published_date),
          url: sourceData.url || urlMap[sourceData.source] || '#',
        };
      }

      // Handle old format (fallback): just article title string
      const sourceTitle = typeof sourceData === 'string' ? sourceData : '';
      const { publication, url } = inferPublication(sourceTitle);
      return {
        title: sourceTitle,
        publication,
        date: '',
        url,
      };
    })
  );

  return {
    id: uniqueId,
    timestamp: hasValidDate
      ? generatedDate.toISOString().replace('T', ' ').substring(0, 19) + ' UTC'
      : 'date unavailable',
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

// On-device cache
//
// The backend stores briefings on an ephemeral disk, so a restart can leave it
// with nothing to serve. Caching the last good copy means the app keeps showing
// briefings (marked stale) instead of an error while the backend recovers.

const CACHE_PREFIX = 'sitrep:briefing:v1:';

async function readCachedBriefing(key: string): Promise<Briefing | null> {
  try {
    const raw = await AsyncStorage.getItem(CACHE_PREFIX + key);
    return raw ? (JSON.parse(raw) as Briefing) : null;
  } catch (err) {
    console.warn('Failed to read cached briefing', key, err);
    return null;
  }
}

async function cacheBriefing(key: string, briefing: Briefing): Promise<void> {
  try {
    await AsyncStorage.setItem(CACHE_PREFIX + key, JSON.stringify(briefing));
  } catch (err) {
    console.warn('Failed to cache briefing', key, err);
  }
}

async function fetchBriefingWithCache(
  key: string,
  fetcher: () => Promise<Briefing>
): Promise<Briefing> {
  try {
    const fresh = await fetcher();
    const stamped: Briefing = { ...fresh, isStale: false, cachedAt: new Date().toISOString() };
    void cacheBriefing(key, stamped);
    return stamped;
  } catch (err) {
    const cached = await readCachedBriefing(key);
    if (cached) {
      console.warn(`Serving cached briefing for ${key} after fetch failure:`, err);
      return { ...cached, isStale: true };
    }
    throw err;
  }
}

// API Functions
export async function fetchLatestBriefing(region: string = 'Europe/Africa'): Promise<Briefing> {
  return fetchBriefingWithCache(`region:${region}`, async () => {
    const response = await fetch(`${API_BASE_URL}/briefing/latest?region=${encodeURIComponent(region)}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch briefing: ${response.status} ${response.statusText}`);
    }

    const data: BackendBriefingResponse = await response.json();
    return transformBriefing(data);
  });
}

export async function fetchGlobalBriefing(): Promise<Briefing> {
  return fetchBriefingWithCache('global', async () => {
    const response = await fetch(`${API_BASE_URL}/briefing/global`);

    if (!response.ok) {
      throw new Error(`Failed to fetch global briefing: ${response.status} ${response.statusText}`);
    }

    const data: BackendBriefingResponse = await response.json();
    return transformBriefing(data);
  });
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
