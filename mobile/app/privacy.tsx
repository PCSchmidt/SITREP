import { View, Text, ScrollView } from 'react-native';
import type { ReactNode } from 'react';
import { Colors, Typography, Spacing } from '../constants/tokens';

const LAST_UPDATED = '2026-05-29';

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <View style={{ marginBottom: Spacing.xl }}>
      <Text style={{ color: Colors.amber, ...Typography.h3, marginBottom: Spacing.sm }}>
        {title}
      </Text>
      {children}
    </View>
  );
}

function Body({ children }: { children: ReactNode }) {
  return (
    <Text style={{ color: Colors.textBody, ...Typography.body, lineHeight: 22 }}>
      {children}
    </Text>
  );
}

export default function PrivacyScreen() {
  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: Colors.trueBlack }}
      contentContainerStyle={{ padding: Spacing.lg, paddingBottom: Spacing['2xl'] }}
    >
      <Text style={{ color: Colors.textHeading, ...Typography.h1, marginBottom: Spacing.sm }}>
        Privacy Policy
      </Text>
      <Text style={{ color: Colors.textSubtle, ...Typography.caption, marginBottom: Spacing.xl }}>
        Last updated: {LAST_UPDATED}
      </Text>

      <Section title="Who We Are">
        <Body>
          SITREP is a free personal portfolio project by Chris Schmidt. It delivers
          AI-generated geopolitical intelligence briefings. It is not affiliated with
          any government agency, military organization, or intelligence service.{'\n\n'}
          Contact: p.christopher.schmidt@gmail.com
        </Body>
      </Section>

      <Section title="What We Collect">
        <Body>
          SITREP collects no personal information and requires no account or login.{'\n\n'}
          Analytics (Mixpanel): We track anonymous usage events — app_open,
          briefing_view, region_filter, pdf_view, pdf_share — with a device-level
          anonymous UUID assigned by Mixpanel. No names, emails, or personal
          identifiers are collected.{'\n\n'}
          Crash reports (Sentry): If the app crashes, Sentry captures the stack trace,
          device type, OS version, and app version. No personal data is included.{'\n\n'}
          We do NOT collect: location, device hardware IDs, reading history beyond
          event names, payment information, or anything that identifies you personally.
        </Body>
      </Section>

      <Section title="How We Use It">
        <Body>
          Analytics data is used only to understand feature usage and improve the app.
          Crash data is used only to find and fix bugs. We do not sell, share, or
          monetize any data collected.
        </Body>
      </Section>

      <Section title="Third-Party Services">
        <Body>
          {'Mixpanel — anonymous analytics (mixpanel.com/legal/privacy-policy)\n'}
          {'Sentry — crash reporting (sentry.io/privacy)\n'}
          {'Railway — backend hosting (railway.app/legal/privacy)\n'}
          {'OpenRouter — AI model routing (openrouter.ai/privacy)'}
        </Body>
      </Section>

      <Section title="AI-Generated Content">
        <Body>
          All briefings are AI-generated from public news sources. AI processing
          occurs on our backend servers — content you read is not sent back to any
          AI provider.
        </Body>
      </Section>

      <Section title="Data Retention">
        <Body>
          Mixpanel retains events per their standard policy. Sentry retains crash
          reports for 90 days. We maintain no separate user data store.
        </Body>
      </Section>

      <Section title="Children">
        <Body>
          SITREP is not directed at children under 13 and we do not knowingly collect
          information from children.
        </Body>
      </Section>

      <Section title="Contact">
        <Body>p.christopher.schmidt@gmail.com</Body>
      </Section>
    </ScrollView>
  );
}
