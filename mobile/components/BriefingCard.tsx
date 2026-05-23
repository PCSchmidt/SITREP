import { View, Text, Pressable } from 'react-native';
import { useRouter } from 'expo-router';
import { Colors, Typography, Spacing } from '../constants/tokens';

interface BriefingCardProps {
  id: string;
  timestamp: string;
  title: string;
  preview: string;
  regions: string[];
}

export default function BriefingCard({ id, timestamp, title, preview, regions }: BriefingCardProps) {
  const router = useRouter();

  return (
    <Pressable
      onPress={() => router.push(`/detail/${id}`)}
      style={{
        backgroundColor: Colors.trueBlack,
        borderLeftWidth: 1,
        borderLeftColor: Colors.amber,
        padding: Spacing.md,
        marginBottom: Spacing.lg,
      }}
    >
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: Spacing.sm }}>
        <Text
          style={{
            color: Colors.amber,
            ...Typography.h3,
            textTransform: 'uppercase',
          }}
        >
          WEEKLY SITREP
        </Text>
        <Text
          style={{
            color: Colors.textSubtle,
            ...Typography.caption,
            fontFamily: 'monospace',
          }}
        >
          {timestamp}
        </Text>
      </View>

      <Text
        style={{
          color: Colors.textHeading,
          ...Typography.h2,
          marginBottom: Spacing.sm,
        }}
      >
        {title}
      </Text>

      <Text
        style={{
          color: Colors.textBody,
          ...Typography.body,
          marginBottom: Spacing.md,
        }}
        numberOfLines={2}
      >
        {preview}
      </Text>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: Spacing.sm, marginBottom: Spacing.sm }}>
        {regions.map((region) => (
          <View
            key={region}
            style={{
              backgroundColor: Colors.cardBg,
              paddingVertical: 4,
              paddingHorizontal: Spacing.sm,
              borderRadius: 4,
            }}
          >
            <Text
              style={{
                color: Colors.gold,
                ...Typography.caption,
                textTransform: 'uppercase',
              }}
            >
              {region}
            </Text>
          </View>
        ))}
      </View>

      <Text style={{ color: Colors.amber, ...Typography.body, textAlign: 'right' }}>
        View Full Report →
      </Text>
    </Pressable>
  );
}
