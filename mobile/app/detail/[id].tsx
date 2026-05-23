import { View, Text, ScrollView } from 'react-native';
import { useLocalSearchParams } from 'expo-router';
import DisclaimerBanner from '../../components/DisclaimerBanner';
import BLUFSection from '../../components/BLUFSection';
import SourceCitation from '../../components/SourceCitation';
import { mockBriefings } from '../../data/mockBriefings';
import { Colors, Typography, Spacing } from '../../constants/tokens';

export default function DetailScreen() {
  const { id } = useLocalSearchParams();
  const briefing = mockBriefings.find((b) => b.id === id);

  if (!briefing) {
    return (
      <View className="flex-1 bg-true-black items-center justify-center">
        <Text style={{ color: Colors.textBody, ...Typography.body }}>Briefing not found</Text>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-true-black">
      <DisclaimerBanner />
      <ScrollView style={{ flex: 1 }}>
        <View style={{ padding: Spacing.lg }}>
          <Text
            style={{
              color: Colors.textSubtle,
              ...Typography.caption,
              fontFamily: 'monospace',
              marginBottom: Spacing.sm,
            }}
          >
            {briefing.timestamp}
          </Text>
          <Text
            style={{
              color: Colors.textHeading,
              ...Typography.h1,
              marginBottom: Spacing.lg,
            }}
          >
            {briefing.title}
          </Text>

          <BLUFSection summary={briefing.bluf} readTime={briefing.readTime} />

          {briefing.content.map((section, idx) => (
            <View key={idx} style={{ marginTop: Spacing.lg }}>
              <Text
                style={{
                  color: Colors.amber,
                  ...Typography.h2,
                  marginBottom: Spacing.md,
                }}
              >
                {section.region}
              </Text>
              <Text
                style={{
                  color: Colors.textBody,
                  ...Typography.body,
                  fontWeight: '600',
                  marginBottom: Spacing.md,
                }}
              >
                BLUF: {section.bluf}
              </Text>
              {section.sections.map((subsection, subIdx) => (
                <View key={subIdx} style={{ marginBottom: Spacing.md }}>
                  <Text
                    style={{
                      color: Colors.textHeading,
                      ...Typography.h3,
                      marginBottom: Spacing.sm,
                    }}
                  >
                    {subsection.title}
                  </Text>
                  <Text style={{ color: Colors.textBody, ...Typography.body }}>
                    {subsection.content}
                  </Text>
                </View>
              ))}
            </View>
          ))}

          <View style={{ marginTop: Spacing['2xl'], marginBottom: Spacing.xl }}>
            <Text
              style={{
                color: Colors.textHeading,
                ...Typography.h2,
                marginBottom: Spacing.md,
              }}
            >
              SOURCES
            </Text>
            {briefing.sources.map((source, idx) => (
              <SourceCitation key={idx} {...source} />
            ))}
          </View>
        </View>
      </ScrollView>
    </View>
  );
}
