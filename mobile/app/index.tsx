import { View, ScrollView, Text, ActivityIndicator } from 'react-native';
import { useState } from 'react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import RegionTab from '../components/RegionTab';
import BriefingCard from '../components/BriefingCard';
import { useAllBriefings } from '../hooks/useBriefings';
import { Spacing } from '../constants/tokens';

export default function HomeScreen() {
  const [activeRegion, setActiveRegion] = useState('all');
  const [showDisclaimer, setShowDisclaimer] = useState(true);

  const { data: briefings, isLoading, error } = useAllBriefings();

  // Filter briefings by active region
  const filteredBriefings = briefings?.filter(briefing => {
    if (activeRegion === 'all') return true;
    return briefing.regions.includes(activeRegion);
  }) || [];

  return (
    <View className="flex-1 bg-true-black">
      {showDisclaimer && (
        <DisclaimerBanner dismissible onDismiss={() => setShowDisclaimer(false)} />
      )}
      <RegionTab activeRegion={activeRegion} onRegionChange={setActiveRegion} />
      <ScrollView style={{ flex: 1, paddingHorizontal: Spacing.lg, paddingTop: Spacing.lg }}>
        {isLoading && (
          <View className="flex-1 items-center justify-center py-12">
            <ActivityIndicator size="large" color="#FFA500" />
            <Text className="text-amber-500 mt-4 text-base">Loading briefings...</Text>
          </View>
        )}
        {error && (
          <View className="flex-1 items-center justify-center py-12">
            <Text className="text-red-500 text-base text-center px-4">
              Failed to load briefings. Make sure the backend is running on localhost:8001.
            </Text>
            <Text className="text-gray-400 text-sm mt-2 text-center px-4">
              {error.message}
            </Text>
          </View>
        )}
        {!isLoading && !error && filteredBriefings.length === 0 && (
          <View className="flex-1 items-center justify-center py-12">
            <Text className="text-gray-400 text-base">No briefings available for this region.</Text>
          </View>
        )}
        {!isLoading && !error && filteredBriefings.map((briefing) => (
          <BriefingCard
            key={briefing.id}
            id={briefing.id}
            timestamp={briefing.timestamp}
            title={briefing.title}
            preview={briefing.preview}
            regions={briefing.regions}
          />
        ))}
      </ScrollView>
    </View>
  );
}
