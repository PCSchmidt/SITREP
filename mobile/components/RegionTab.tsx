import { View, Pressable, Text } from 'react-native';
import { Colors, Spacing, Regions } from '../constants/tokens';

interface RegionTabProps {
  activeRegion: string;
  onRegionChange: (regionId: string) => void;
}

export default function RegionTab({ activeRegion, onRegionChange }: RegionTabProps) {
  return (
    <View
      style={{
        paddingHorizontal: Spacing.lg,
        paddingTop: Spacing.sm,
        paddingBottom: Spacing.md
      }}
    >
      {Regions.map((region) => {
        const isActive = activeRegion === region.id;
        return (
          <Pressable
            key={region.id}
            onPress={() => onRegionChange(region.id)}
            style={{
              paddingVertical: Spacing.lg,
              paddingHorizontal: Spacing.md,
              marginBottom: Spacing.sm,
              borderLeftWidth: 3,
              borderLeftColor: isActive ? Colors.amber : 'transparent',
              backgroundColor: isActive ? 'rgba(255, 165, 0, 0.1)' : 'transparent',
            }}
          >
            <Text
              style={{
                color: isActive ? Colors.textHeading : Colors.textSubtle,
                fontSize: 16,
                fontWeight: '600',
                lineHeight: 24,
                textTransform: 'uppercase',
              }}
            >
              {region.label}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}
