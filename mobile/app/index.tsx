import { View, ScrollView, Text, ActivityIndicator } from 'react-native';
import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import DisclaimerBanner from '../components/DisclaimerBanner';
import RegionTab from '../components/RegionTab';
import BriefingCard from '../components/BriefingCard';
import { useAllBriefings } from '../hooks/useBriefings';
import { Spacing } from '../constants/tokens';

const REGION_STORAGE_KEY = '@sitrep_selected_region';

export default function HomeScreen() {
  const [activeRegion, setActiveRegion] = useState('all');
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const [isLoadingRegion, setIsLoadingRegion] = useState(true);

  const { data: briefings, isLoading, error } = useAllBriefings();

  // Debug logging
  useEffect(() => {
    console.log('HomeScreen state:', {
      briefingsCount: briefings?.length ?? 0,
      isLoading,
      error: error?.message,
      activeRegion
    });
  }, [briefings, isLoading, error, activeRegion]);

  // Load saved region preference on mount
  useEffect(() => {
    const loadRegion = async () => {
      try {
        const savedRegion = await AsyncStorage.getItem(REGION_STORAGE_KEY);
        if (savedRegion) {
          setActiveRegion(savedRegion);
        }
      } catch (err) {
        console.warn('Failed to load saved region:', err);
      } finally {
        setIsLoadingRegion(false);
      }
    };
    loadRegion();
  }, []);

  // Save region preference when it changes
  useEffect(() => {
    if (!isLoadingRegion) {
      AsyncStorage.setItem(REGION_STORAGE_KEY, activeRegion).catch(err =>
        console.warn('Failed to save region:', err)
      );
    }
  }, [activeRegion, isLoadingRegion]);

  // Filter briefings by active region
  const filteredBriefings = briefings?.filter(briefing => {
    if (activeRegion === 'all') return true;
    return briefing.regions.includes(activeRegion);
  }) || [];

  // Debug filtered briefings
  useEffect(() => {
    console.log('Filtered briefings:', {
      count: filteredBriefings.length,
      activeRegion,
      briefings: filteredBriefings.map(b => ({ id: b.id, regions: b.regions }))
    });
  }, [filteredBriefings, activeRegion]);

  return (
    <View style={{ flex: 1, backgroundColor: '#000000' }}>
      {showDisclaimer && (
        <DisclaimerBanner dismissible onDismiss={() => setShowDisclaimer(false)} />
      )}
      <RegionTab activeRegion={activeRegion} onRegionChange={setActiveRegion} />

      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={{ paddingHorizontal: Spacing.lg, paddingTop: Spacing.lg, paddingBottom: Spacing.xl }}
      >
        {isLoading && (
          <View style={{ padding: Spacing.xl, alignItems: 'center' }}>
            <ActivityIndicator size="large" color="#FFA500" />
            <Text style={{ color: '#FFA500', marginTop: Spacing.md }}>Loading briefings...</Text>
          </View>
        )}
        {error && (
          <View style={{ padding: Spacing.xl }}>
            <Text style={{ color: '#FF4444', textAlign: 'center' }}>
              Failed to load briefings. {error.message}
            </Text>
          </View>
        )}
        {!isLoading && !error && filteredBriefings.length === 0 && (
          <View style={{ padding: Spacing.xl }}>
            <Text style={{ color: '#888888', textAlign: 'center' }}>No briefings available for this region.</Text>
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
