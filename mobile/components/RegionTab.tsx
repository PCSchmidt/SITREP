import { ScrollView, Pressable, Text } from 'react-native';
import { Colors, Typography, Spacing, Regions } from '../constants/tokens';

interface RegionTabProps {
  activeRegion: string;
  onRegionChange: (regionId: string) => void;
}

export default function RegionTab({ activeRegion, onRegionChange }: RegionTabProps) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={{ flexGrow: 0 }}
      contentContainerStyle={{ paddingHorizontal: Spacing.lg, paddingVertical: Spacing.sm }}
    >
      {Regions.map((region) => {
        const isActive = activeRegion === region.id;
        return (
          <Pressable
            key={region.id}
            onPress={() => onRegionChange(region.id)}
            style={{
              paddingVertical: Spacing.sm,
              paddingHorizontal: Spacing.md,
              marginRight: Spacing.md,
              borderBottomWidth: 2,
              borderBottomColor: isActive ? Colors.amber : 'transparent',
            }}
          >
            <Text
              style={{
                color: isActive ? Colors.textHeading : Colors.textSubtle,
                ...Typography.label,
                textTransform: 'uppercase',
              }}
            >
              {region.label}
            </Text>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}
