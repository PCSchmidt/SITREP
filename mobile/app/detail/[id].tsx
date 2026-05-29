import { View, Text, ScrollView, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useEffect } from 'react';
import DisclaimerBanner from '../../components/DisclaimerBanner';
import BLUFSection from '../../components/BLUFSection';
import SourceCitation from '../../components/SourceCitation';
import { useBriefingById } from '../../hooks/useBriefings';
import { trackBriefingView } from '../../services/analytics';
import { Colors, Typography, Spacing } from '../../constants/tokens';

export default function DetailScreen() {
  const { id } = useLocalSearchParams();
  const { data: briefing, isLoading, error } = useBriefingById(id as string);

  useEffect(() => {
    if (briefing) {
      trackBriefingView(
        briefing.id,
        briefing.regions[0] ?? 'unknown',
        briefing.title
      );
    }
  }, [briefing?.id]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, backgroundColor: '#000000', alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator size="large" color="#FFA500" />
        <Text style={{ color: '#FFA500', marginTop: 16, fontSize: 15 }}>Loading briefing...</Text>
      </View>
    );
  }

  if (error || !briefing) {
    return (
      <View style={{ flex: 1, backgroundColor: '#000000', alignItems: 'center', justifyContent: 'center', paddingHorizontal: 16 }}>
        <Text style={{ color: '#FF4444', fontSize: 15, textAlign: 'center' }}>
          {error ? 'Failed to load briefing' : 'Briefing not found'}
        </Text>
        {error && (
          <Text style={{ color: '#888888', fontSize: 12, marginTop: 8, textAlign: 'center' }}>
            {(error as Error).message}
          </Text>
        )}
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: '#000000' }}>
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

          {/* View as PDF Button */}
          <TouchableOpacity
            onPress={() => router.push(`/pdf/${briefing.id}` as any)}
            style={{
              marginTop: Spacing.lg,
              marginBottom: Spacing.lg,
              backgroundColor: Colors.amber,
              paddingVertical: Spacing.md,
              paddingHorizontal: Spacing.lg,
              borderRadius: 4,
              alignItems: 'center',
            }}
          >
            <Text
              style={{
                color: Colors.trueBlack,
                ...Typography.body,
                fontWeight: '700',
                textTransform: 'uppercase',
                letterSpacing: 1,
              }}
            >
              📄 View as PDF
            </Text>
          </TouchableOpacity>

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
