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

export default function TermsScreen() {
  return (
    <ScrollView
      style={{ flex: 1, backgroundColor: Colors.trueBlack }}
      contentContainerStyle={{ padding: Spacing.lg, paddingBottom: Spacing['2xl'] }}
    >
      <Text style={{ color: Colors.textHeading, ...Typography.h1, marginBottom: Spacing.sm }}>
        Terms of Service
      </Text>
      <Text style={{ color: Colors.textSubtle, ...Typography.caption, marginBottom: Spacing.xl }}>
        Last updated: {LAST_UPDATED}
      </Text>

      <Section title="Acceptance">
        <Body>
          By using SITREP, you agree to these terms. If you do not agree, do not use the app.
        </Body>
      </Section>

      <Section title="What SITREP Is">
        <Body>
          SITREP is a free personal portfolio project. It synthesizes open-source news
          articles using AI to produce geopolitical briefings in BLUF format.{'\n\n'}
          SITREP is NOT an official intelligence product, is NOT affiliated with any
          government or military organization, and is NOT a verified news service.
        </Body>
      </Section>

      <Section title="⚠ AI Content Disclaimer">
        <Body>
          ALL CONTENT IN SITREP IS AI-GENERATED.{'\n\n'}
          Accuracy is not guaranteed — AI models can mischaracterize or hallucinate
          facts. Content may be incomplete or outdated (briefings are weekly).
          Source citations are AI-extracted and may contain errors.{'\n\n'}
          DO NOT rely on this content for any real-world decisions, especially
          operational, military, intelligence, or government decisions.
        </Body>
      </Section>

      <Section title="Prohibited Uses">
        <Body>
          {'• Operational military, intelligence, or government decision-making\n'}
          {'• Redistribution as factual or official intelligence\n'}
          {'• Commercial resale or monetization of the content\n'}
          {'• Any use that represents SITREP content as authoritative'}
        </Body>
      </Section>

      <Section title="Limitation of Liability">
        <Body>
          TO THE MAXIMUM EXTENT PERMITTED BY LAW, SITREP AND ITS DEVELOPER ARE NOT
          LIABLE FOR ANY DAMAGES ARISING FROM YOUR USE OF THE APP OR RELIANCE ON ITS
          CONTENT. YOU USE THIS APP AT YOUR OWN RISK.
        </Body>
      </Section>

      <Section title="No Warranty">
        <Body>
          SITREP is provided "AS IS" without warranty of any kind. We do not warrant
          that content will be accurate, complete, current, or that the app will be
          error-free or uninterrupted.
        </Body>
      </Section>

      <Section title="Sources">
        <Body>
          SITREP synthesizes content from public sources including ISW, Defense One,
          Breaking Defense, War on the Rocks, The War Zone, Al Jazeera, and others.
          SITREP has no affiliation with these sources and does not represent their views.
        </Body>
      </Section>

      <Section title="Contact">
        <Body>p.christopher.schmidt@gmail.com</Body>
      </Section>
    </ScrollView>
  );
}
