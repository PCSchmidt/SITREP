import { View, Text } from 'react-native';
import { Colors, Typography, Spacing } from '../constants/tokens';

interface BLUFSectionProps {
  summary: string;
  readTime?: number;
}

export default function BLUFSection({ summary, readTime }: BLUFSectionProps) {
  return (
    <View
      style={{
        backgroundColor: Colors.nearBlack,
        borderLeftWidth: 4,
        borderLeftColor: Colors.amber,
        padding: Spacing.lg,
        marginVertical: Spacing.md,
      }}
    >
      <Text
        style={{
          color: Colors.amber,
          ...Typography.caption,
          textTransform: 'uppercase',
          fontFamily: 'monospace',
          marginBottom: Spacing.sm,
        }}
      >
        BLUF
      </Text>
      <Text
        style={{
          color: Colors.textHeading,
          ...Typography.body,
          fontWeight: '600',
          marginBottom: readTime ? Spacing.sm : 0,
        }}
      >
        {summary}
      </Text>
      {readTime && (
        <Text
          style={{
            color: Colors.textSubtle,
            ...Typography.caption,
            fontFamily: 'monospace',
          }}
        >
          ⏱ {readTime} min read
        </Text>
      )}
    </View>
  );
}
