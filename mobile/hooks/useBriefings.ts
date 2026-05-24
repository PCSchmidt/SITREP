import { useQuery } from '@tanstack/react-query';
import { fetchLatestBriefing, fetchAllRegionBriefings } from '../api/client';
import { Briefing } from '../types/briefing';

// Query keys
export const briefingKeys = {
  all: ['briefings'] as const,
  allRegions: () => [...briefingKeys.all, 'all-regions'] as const,
  byRegion: (region: string) => [...briefingKeys.all, 'region', region] as const,
};

// Hook to fetch all region briefings
export function useAllBriefings() {
  return useQuery({
    queryKey: briefingKeys.allRegions(),
    queryFn: fetchAllRegionBriefings,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
  });
}

// Hook to fetch a single region briefing
export function useBriefing(region: string) {
  return useQuery({
    queryKey: briefingKeys.byRegion(region),
    queryFn: () => fetchLatestBriefing(region),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes
    enabled: !!region, // Only fetch if region is provided
  });
}

// Hook to fetch a briefing by ID (date)
// Since we don't have a direct endpoint for this, we'll fetch all and filter
export function useBriefingById(id: string) {
  return useQuery({
    queryKey: [...briefingKeys.all, 'by-id', id],
    queryFn: async () => {
      const allBriefings = await fetchAllRegionBriefings();
      const briefing = allBriefings.find(b => b.id === id);
      if (!briefing) {
        throw new Error(`Briefing with id ${id} not found`);
      }
      return briefing;
    },
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
    enabled: !!id,
  });
}
