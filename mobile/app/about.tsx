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

      {/* AI Disclaimer — prominent */}
      <View
        style={{
          backgroundColor: Colors.cardBg,
          padding: Spacing.lg,
          borderRadius: 4,
          borderLeftWidth: 4,
          borderLeftColor: Colors.amber,
          marginBottom: Spacing.xl,
        }}
      >
        <Text style={{ color: Colors.amber, ...Typography.h3, marginBottom: Spacing.sm }}>
          ⚠ IMPORTANT DISCLAIMER
        </Text>
        <Text style={{ color: Colors.textBody, ...Typography.body, lineHeight: 22 }}>
          All briefings are AI-generated from open-source news articles. This content
          is NOT official intelligence and should NOT be used for operational or
          government decision-making.{'\n\n'}
          Accuracy is not guaranteed. AI models can mischaracterize or hallucinate facts.
          Briefings are generated weekly and may not reflect current events. Sources are
          cited but independently unverified.{'\n\n'}
          Use at your own discretion.
        </Text>
      </View>

      {/* About the app */}
      <View style={{ marginBottom: Spacing.xl }}>
        <Text style={{ color: Colors.textHeading, ...Typography.h2, marginBottom: Spacing.md }}>
          About
        </Text>
        <Text style={{ color: Colors.textBody, ...Typography.body, lineHeight: 22 }}>
          SITREP delivers weekly geopolitical intelligence briefings in BLUF (Bottom Line
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
