import { View, Text, Pressable } from 'react-native';
import { Colors, Typography, Spacing } from '../constants/tokens';

interface DisclaimerBannerProps {
  onDismiss?: () => void;
  dismissible?: boolean;
}

export default function DisclaimerBanner({ onDismiss, dismissible = false }: DisclaimerBannerProps) {
  return (
    <View
      style={{
        backgroundColor: Colors.amber,
        padding: Spacing.md,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <View style={{ flex: 1 }}>
        <Text
          style={{
            color: Colors.trueBlack,
            ...Typography.h3,
            textTransform: 'uppercase',
            marginBottom: 4,
          }}
        >
          ⚠️ AI GENERATED CONTENT
        </Text>
        <Text style={{ color: Colors.trueBlack, ...Typography.caption }}>
          Not official intelligence. Accuracy not guaranteed. Use at your own discretion.
        </Text>
      </View>
      {dismissible && onDismiss && (
        <Pressable onPress={onDismiss} style={{ padding: Spacing.sm }}>
          <Text style={{ color: Colors.trueBlack, fontSize: 20, fontWeight: '600' }}>×</Text>
        </Pressable>
      )}
    </View>
  );
}
