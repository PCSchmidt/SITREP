import { useEffect, useRef, useState } from 'react';
import { View, Text } from 'react-native';
import { Colors, Typography, Spacing } from '../constants/tokens';

/**
 * Native PDF viewer.
 *
 * react-native-pdf is a native module: it is imported lazily so the module never
 * loads at app startup (a top-level import crashed startup before). The web
 * counterpart of this file is PlatformPdfViewer.web.tsx, which renders an iframe.
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
  const [PdfComponent, setPdfComponent] = useState<any>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  // Keep the latest callbacks without re-running the lazy-load effect.
  const onErrorRef = useRef(onError);
  onErrorRef.current = onError;

  useEffect(() => {
    let cancelled = false;

    const loadPdf = async () => {
      try {
        const Pdf = (await import('react-native-pdf')).default;
        if (!cancelled) setPdfComponent(() => Pdf);
      } catch (err) {
        console.error('Failed to load PDF component:', err);
        if (!cancelled) {
          setLoadError('Failed to load PDF viewer. Please restart the app.');
          onErrorRef.current(err);
        }
      }
    };

    loadPdf();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loadError) {
    return (
      <View style={[{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: Spacing.lg }, style]}>
        <Text style={{ color: Colors.warning, ...Typography.body, textAlign: 'center' }}>{loadError}</Text>
      </View>
    );
  }

  if (!PdfComponent) {
    return <View style={[{ flex: 1, backgroundColor: Colors.trueBlack }, style]} />;
  }

  return (
    <PdfComponent
      source={{ uri, cache: false }}
      onLoadComplete={onLoadComplete}
      onError={onError}
      style={[{ flex: 1, backgroundColor: Colors.trueBlack }, style]}
      trustAllCerts={false}
      enablePaging={true}
      horizontal={false}
      spacing={10}
      fitPolicy={0}
    />
  );
}
