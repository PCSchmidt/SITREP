import { View, Text, Pressable } from 'react-native';
import { Colors, Spacing } from '../constants/tokens';

interface DisclaimerBannerProps {
  onDismiss?: () => void;
  dismissible?: boolean;
}

/**
 * Quiet footnote, not a warning banner.
 *
 * It used to be an amber block at the top of every screen with an uppercase
 * "AI GENERATED CONTENT" heading. That overstated the risk: the cited sources
 * are real, published articles, and the only machine-written part is the
 * paraphrase. So it now sits at the bottom of the screen as small grey text.
 */
export default function DisclaimerBanner({ onDismiss, dismissible = false }: DisclaimerBannerProps) {
  return (
    <View
      style={{
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: Colors.nearBlack,
        borderTopWidth: 1,
        borderTopColor: Colors.border,
        paddingHorizontal: Spacing.lg,
        paddingVertical: Spacing.sm,
      }}
    >
      <Text
        style={{
          flex: 1,
          color: Colors.textSubtle,
          fontSize: 11,
          lineHeight: 15,
          letterSpacing: 0.2,
        }}
      >
        AI-generated summary. Sources are real and cited; the wording is model-written.
        Not official intelligence.
      </Text>
      {dismissible && onDismiss && (
        <Pressable onPress={onDismiss} hitSlop={10} style={{ paddingLeft: Spacing.md }}>
          <Text style={{ color: Colors.textSubtle, fontSize: 14 }}>×</Text>
        </Pressable>
      )}
    </View>
  );
}
