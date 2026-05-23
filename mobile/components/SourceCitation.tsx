import { View, Text, Pressable, Linking } from 'react-native';
import { Colors, Typography, Spacing } from '../constants/tokens';

interface SourceCitationProps {
  title: string;
  publication: string;
  date: string;
  url: string;
}

export default function SourceCitation({ title, publication, date, url }: SourceCitationProps) {
  const handlePress = () => {
    Linking.openURL(url);
  };

  return (
    <Pressable
      onPress={handlePress}
      style={{
        paddingVertical: Spacing.sm,
        borderBottomWidth: 1,
        borderBottomColor: Colors.border,
      }}
    >
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
        <View style={{ flex: 1, marginRight: Spacing.sm }}>
          <Text style={{ color: Colors.textHeading, ...Typography.body }} numberOfLines={2}>
            📰 {title}
          </Text>
          <View style={{ flexDirection: 'row', marginTop: 4 }}>
            <Text
              style={{
                color: Colors.gold,
                ...Typography.caption,
                textTransform: 'uppercase',
                marginRight: Spacing.md,
              }}
            >
              {publication}
            </Text>
            <Text
              style={{
                color: Colors.textSubtle,
                ...Typography.caption,
                fontFamily: 'monospace',
              }}
            >
              {date}
            </Text>
          </View>
        </View>
        <Text style={{ color: Colors.amber, fontSize: 18 }}>→</Text>
      </View>
    </Pressable>
  );
}
