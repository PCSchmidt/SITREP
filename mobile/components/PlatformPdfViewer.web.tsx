import { createElement, useRef } from 'react';
import { View } from 'react-native';
import { Colors } from '../constants/tokens';

/**
 * Web PDF viewer.
 *
 * react-native-pdf is a native-only module, so the web build renders the Railway
 * PDF URL in a plain iframe instead. Metro picks this file for the web platform;
 * native builds use PlatformPdfViewer.tsx.
 */
export default function PlatformPdfViewer({
  uri,
  onLoadComplete,
  onError,
  style,
}: {
  uri: string;
  onLoadComplete: (numberOfPages: number) => void;
  onError: (error: unknown) => void;
  style?: object;
}) {
  const settledRef = useRef(false);

  const handleLoad = () => {
    if (settledRef.current) return;
    settledRef.current = true;
    // An embedded PDF has no page count on web; 0 keeps the interface honest while
    // still telling the screen that loading finished.
    onLoadComplete(0);
  };

  const handleError = () => {
    if (settledRef.current) return;
    settledRef.current = true;
    onError(new Error('The PDF could not be displayed in this browser.'));
  };

  return (
    <View style={[{ flex: 1, backgroundColor: Colors.trueBlack }, style]}>
      {createElement('iframe', {
        src: uri,
        title: 'SITREP briefing PDF',
        onLoad: handleLoad,
        onError: handleError,
        style: { width: '100%', height: '100%', border: 'none', backgroundColor: Colors.trueBlack },
      })}
    </View>
  );
}
