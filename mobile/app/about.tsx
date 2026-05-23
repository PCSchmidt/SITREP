import { View, Text, ScrollView } from 'react-native';
import { Colors, Typography } from '../constants/tokens';

export default function AboutScreen() {
  return (
    <ScrollView className="flex-1 bg-true-black">
      <View className="p-xl">
        <Text style={{ color: Colors.textHeading, ...Typography.h1, textAlign: 'center', marginBottom: 8 }}>
          SITREP
        </Text>
        <Text style={{ color: Colors.textSubtle, ...Typography.caption, textAlign: 'center', marginBottom: 32 }}>
          Intelligence Briefing Platform v0.1.0
        </Text>

        <View className="bg-card-bg p-md rounded-lg mb-4" style={{ borderLeftWidth: 4, borderLeftColor: Colors.amber }}>
          <Text style={{ color: Colors.amber, ...Typography.h3, marginBottom: 8 }}>
            ⚠️ IMPORTANT DISCLAIMER
          </Text>
          <Text style={{ color: Colors.textBody, ...Typography.body }}>
            This app generates AI-powered intelligence summaries from open-source news articles.
            This content is NOT official intelligence and should not be used for operational decision-making.
            {'\n\n'}
            Sources are cited but accuracy is not guaranteed. Use at your own discretion.
          </Text>
        </View>

        <Text style={{ color: Colors.textSubtle, ...Typography.caption, textAlign: 'center', marginTop: 32 }}>
          Built by Chris Schmidt{'\n'}
          pcschmidt.github.io
        </Text>
      </View>
    </ScrollView>
  );
}
