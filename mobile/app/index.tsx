import { View, ScrollView } from 'react-native';
import { useState } from 'react';
import DisclaimerBanner from '../components/DisclaimerBanner';
import RegionTab from '../components/RegionTab';
import BriefingCard from '../components/BriefingCard';
import { mockBriefings } from '../data/mockBriefings';
import { Spacing } from '../constants/tokens';

export default function HomeScreen() {
  const [activeRegion, setActiveRegion] = useState('all');
  const [showDisclaimer, setShowDisclaimer] = useState(true);

  return (
    <View className="flex-1 bg-true-black">
      {showDisclaimer && (
        <DisclaimerBanner dismissible onDismiss={() => setShowDisclaimer(false)} />
      )}
      <RegionTab activeRegion={activeRegion} onRegionChange={setActiveRegion} />
      <ScrollView style={{ flex: 1, paddingHorizontal: Spacing.lg, paddingTop: Spacing.lg }}>
        {mockBriefings.map((briefing) => (
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
