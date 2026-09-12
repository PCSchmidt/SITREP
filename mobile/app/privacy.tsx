import { View, Text, ScrollView } from 'react-native';
import type { ReactNode } from 'react';
import { Colors, Typography, Spacing } from '../constants/tokens';

const LAST_UPDATED = '2026-09-12';

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

      <Section title="What Stays on Your Device">
        <Body>
          Two things are stored locally and never sent anywhere:{'\n\n'}
          Briefing cache — the last briefings you opened are cached on the device so
          the app still works when the backend is unreachable or you are offline.{'\n\n'}
          Downloaded PDFs — a PDF is saved to the app's cache or documents folder only
          when you tap Share or Save.{'\n\n'}
          Both are removed when you uninstall the app, and neither contains personal data.
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
          {'Railway — backend hosting (railway.com/legal/privacy)\n'}
          {'Supabase — Postgres store for the generated briefings, no user data (supabase.com/privacy)\n'}
          {'OpenRouter — AI model routing for briefing synthesis (openrouter.ai/privacy)'}
          {'\n\n'}
          The backend collects public news content from open sources such as ISW, Defense
          One, Breaking Defense, War on the Rocks, The War Zone, Al Jazeera, Foreign
          Policy, CFR and Americas Quarterly, plus the Guardian Open Platform API, the
          GDELT project, and US and UK government releases. No user data is sent to any
          of them, and briefings are served read-only. The backend accepts nothing from
          your device except a read request.{'\n\n'}
          The collected article text, and nothing else, is sent to OpenRouter for
          synthesis. Content you read in the app is never sent back to a model provider.
        </Body>
      </Section>

      <Section title="AI-Generated Content">
        <Body>
          All briefings are AI-generated from public news sources. The primary model is
          DeepSeek V4 Flash via OpenRouter, with DeepSeek V3.2 and Kimi K2.5 as
          fallbacks. AI processing occurs on our backend servers — content you read is
          not sent back to any AI provider.{'\n\n'}
          Briefings are generated once a day and published as text and as a PDF.
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
