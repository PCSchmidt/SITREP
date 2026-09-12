import { View, Text, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { Colors, Typography, Spacing } from '../constants/tokens';

export default function AboutScreen() {
  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: Colors.trueBlack }}
      contentContainerStyle={{ padding: Spacing.lg, paddingBottom: Spacing['2xl'] }}
    >
      {/* Header */}
      <Text style={{ color: Colors.textHeading, ...Typography.h1, textAlign: 'center', marginBottom: 4 }}>
        SITREP
      </Text>
      <Text style={{ color: Colors.textSubtle, ...Typography.caption, textAlign: 'center', marginBottom: Spacing.xl }}>
        AI Intelligence Briefing Platform
      </Text>

      {/* How the content is made — calm, not a warning */}
      <View
        style={{
          backgroundColor: Colors.cardBg,
          padding: Spacing.lg,
          borderRadius: 4,
          borderLeftWidth: 2,
          borderLeftColor: Colors.border,
          marginBottom: Spacing.xl,
        }}
      >
        <Text style={{ color: Colors.textSubtle, ...Typography.caption, marginBottom: Spacing.sm, textTransform: 'uppercase', letterSpacing: 0.8 }}>
          How this is written
        </Text>
        <Text style={{ color: Colors.textBody, ...Typography.body, lineHeight: 22 }}>
          Briefings are written by an AI model from real, linked open-source reporting.
          The cited sources are published articles; the summary and analysis are
          machine-written, so the wording can drift from the original and details can
          be wrong. Check anything important against the linked source.{'\n\n'}
          Briefings are generated once a day and may not reflect later events. This is
          not official intelligence and not a substitute for professional analysis.
        </Text>
      </View>

      {/* About the app */}
      <View style={{ marginBottom: Spacing.xl }}>
        <Text style={{ color: Colors.textHeading, ...Typography.h2, marginBottom: Spacing.md }}>
          About
        </Text>
        <Text style={{ color: Colors.textBody, ...Typography.body, lineHeight: 22 }}>
          SITREP delivers daily geopolitical intelligence briefings in BLUF (Bottom Line
          Up Front) format — the same structure used by military intelligence products.{'\n\n'}
          Sources include ISW, Defense One, Breaking Defense, War on the Rocks, The War
          Zone, Al Jazeera, and other open-source defense publications. Content is
          synthesized using DeepSeek V4 Flash via OpenRouter.{'\n\n'}
          This is a personal portfolio project by Chris Schmidt.
        </Text>
      </View>

      {/* Legal links */}
      <View style={{ marginBottom: Spacing.xl }}>
        <Text style={{ color: Colors.textHeading, ...Typography.h2, marginBottom: Spacing.md }}>
          Legal
        </Text>

        <Pressable
          onPress={() => router.push('/privacy' as any)}
          style={{
            paddingVertical: Spacing.md,
            paddingHorizontal: Spacing.lg,
            backgroundColor: Colors.cardBg,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: Colors.border,
            marginBottom: Spacing.sm,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <Text style={{ color: Colors.textBody, ...Typography.body }}>Privacy Policy</Text>
          <Text style={{ color: Colors.textSubtle, ...Typography.body }}>›</Text>
        </Pressable>

        <Pressable
          onPress={() => router.push('/terms' as any)}
          style={{
            paddingVertical: Spacing.md,
            paddingHorizontal: Spacing.lg,
            backgroundColor: Colors.cardBg,
            borderRadius: 4,
            borderWidth: 1,
            borderColor: Colors.border,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <Text style={{ color: Colors.textBody, ...Typography.body }}>Terms of Service</Text>
          <Text style={{ color: Colors.textSubtle, ...Typography.body }}>›</Text>
        </Pressable>
      </View>

      {/* Footer */}
      <Text style={{ color: Colors.textSubtle, ...Typography.caption, textAlign: 'center', marginTop: Spacing.lg }}>
        Built by Chris Schmidt{'\n'}
        pcschmidt.github.io{'\n\n'}
        UNCLASSIFIED // AI-GENERATED
      </Text>
    </ScrollView>
  );
}
