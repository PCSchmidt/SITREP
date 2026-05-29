import { View, ScrollView, Text, ActivityIndicator } from 'react-native';
import { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import DisclaimerBanner from '../components/DisclaimerBanner';
import RegionTab from '../components/RegionTab';
import BriefingCard from '../components/BriefingCard';
import { useAllBriefings, useGlobalBriefing } from '../hooks/useBriefings';
import { trackRegionFilter } from '../services/analytics';
import { Spacing } from '../constants/tokens';

const REGION_STORAGE_KEY = '@sitrep_selected_region';

export default function HomeScreen() {
  const [activeRegion, setActiveRegion] = useState('all');
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const [isLoadingRegion, setIsLoadingRegion] = useState(true);

  // Global briefing for ALL tab; regional briefings for specific region tabs
  const globalQuery = useGlobalBriefing();
  const regionalQuery = useAllBriefings();

  const isGlobal = activeRegion === 'all';
  const isLoading = isGlobal ? globalQuery.isLoading : regionalQuery.isLoading;
  const error = isGlobal ? globalQuery.error : regionalQuery.error;

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

  // Save region preference and track filter change when it changes
  useEffect(() => {
    if (!isLoadingRegion) {
      AsyncStorage.setItem(REGION_STORAGE_KEY, activeRegion).catch(err =>
        console.warn('Failed to save region:', err)
      );
      trackRegionFilter(activeRegion);
    }
  }, [activeRegion, isLoadingRegion]);

  // Determine which briefings to show
  const displayedBriefings = isGlobal
    ? (globalQuery.data ? [globalQuery.data] : [])
    : (regionalQuery.data?.filter(b => b.regions.includes(activeRegion)) ?? []);

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
              Failed to load briefings. {(error as Error).message}
            </Text>
          </View>
        )}
        {!isLoading && !error && displayedBriefings.length === 0 && (
          <View style={{ padding: Spacing.xl }}>
            <Text style={{ color: '#888888', textAlign: 'center' }}>No briefings available for this region.</Text>
          </View>
        )}
        {!isLoading && !error && displayedBriefings.map((briefing) => (
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
