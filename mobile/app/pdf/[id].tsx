import { View, Text, ActivityIndicator, TouchableOpacity, Alert, Platform, Linking } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useState, useEffect } from 'react';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { trackPdfView, trackPdfShare } from '../../services/analytics';
import * as Sharing from 'expo-sharing';
import { cacheDirectory, documentDirectory, downloadAsync } from 'expo-file-system/legacy';
import PlatformPdfViewer from '../../components/PlatformPdfViewer';
import { Colors, Typography, Spacing } from '../../constants/tokens';

const API_BASE_URL = 'https://sitrep-production-6aac.up.railway.app';

const isWeb = Platform.OS === 'web';

export default function PDFViewerScreen() {
  const { id } = useLocalSearchParams();
  const insets = useSafeAreaInsets();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Extract region from briefing ID (e.g., "middle-east-2026-05-31" -> "Middle East",
  // "all-2026-05-31" -> "Global"). Strip the trailing -YYYY-MM-DD rather than
  // assuming a fixed number of '-' segments, which broke for single-token codes.
  const getRegionFromId = (briefingId: string): string => {
    const regionMap: Record<string, string> = {
      'europe-africa': 'Europe/Africa',
      'middle-east': 'Middle East',
      'indo-pacific': 'Indo-Pacific',
      'western-hemisphere': 'Western Hemisphere',
      'all': 'Global',
      'global': 'Global',
    };

    const regionCode = String(briefingId).replace(/-\d{4}-\d{2}-\d{2}$/, '');
    return regionMap[regionCode] || 'Europe/Africa';
  };

  const region = getRegionFromId(id as string);
  // Always fetch fresh: briefings regenerate (sometimes same-day), and on-disk
  // caching previously pinned stale/old-design PDFs and a cached Global 404.
  const pdfUrl = `${API_BASE_URL}/briefing/latest/pdf?region=${encodeURIComponent(region)}`;

  // Track pdf_view on mount
  useEffect(() => {
    trackPdfView(id as string);
  }, [id]);

  const handleShare = async () => {
    trackPdfShare(id as string);
    console.log('[PDF Share] Button pressed');
    try {
      // Check if sharing is available first
      const canShare = await Sharing.isAvailableAsync();
      console.log('[PDF Share] Sharing available:', canShare);

      if (!canShare) {
        Alert.alert('Sharing Not Available', 'Sharing is not available on this device.');
        return;
      }

      // Download PDF to local file system first
      const localUri = `${cacheDirectory}sitrep_${id}.pdf`;
      console.log('[PDF Share] Downloading PDF to:', localUri);

      const downloadResult = await downloadAsync(pdfUrl, localUri);
      console.log('[PDF Share] Download result:', downloadResult.status);

      if (downloadResult.status === 200) {
        console.log('[PDF Share] Opening share dialog for:', downloadResult.uri);
        await Sharing.shareAsync(downloadResult.uri, {
          mimeType: 'application/pdf',
          dialogTitle: 'Share SITREP Briefing',
          UTI: 'com.adobe.pdf',
        });
        console.log('[PDF Share] Share completed successfully');
      } else {
        console.error('[PDF Share] Download failed with status:', downloadResult.status);
        Alert.alert('Download Failed', 'Could not download PDF for sharing.');
      }
    } catch (err) {
      console.error('[PDF Share] Error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      Alert.alert('Share Failed', `Could not share PDF: ${errorMessage}`);
    }
  };

  const handleDownload = async () => {
    console.log('[PDF Save] Button pressed');
    try {
      const localUri = `${documentDirectory}sitrep_${id}.pdf`;
      console.log('[PDF Save] Saving PDF to:', localUri);

      const downloadResult = await downloadAsync(pdfUrl, localUri);
      console.log('[PDF Save] Save result:', downloadResult.status);

      if (downloadResult.status === 200) {
        console.log('[PDF Save] PDF saved successfully to:', downloadResult.uri);
        Alert.alert(
          'PDF Saved',
          `Briefing saved to ${Platform.OS === 'ios' ? 'Files app' : 'Downloads'}`,
          [{ text: 'OK' }]
        );
      } else {
        console.error('[PDF Save] Save failed with status:', downloadResult.status);
        Alert.alert('Download Failed', 'Could not save PDF.');
      }
    } catch (err) {
      console.error('[PDF Save] Error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      Alert.alert('Save Failed', `Could not save PDF: ${errorMessage}`);
    }
  };

  // Browsers cannot share or save to a device folder the way the native app does,
  // so web opens the Railway PDF in a new tab instead.
  const handleOpenInTab = async () => {
    trackPdfShare(id as string);
    try {
      await Linking.openURL(pdfUrl);
    } catch (err) {
      console.error('[PDF Open] Error:', err);
      setError('Could not open the PDF in a new tab.');
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: Colors.trueBlack }}>
      {/* Header with actions */}
      <View
        style={{
          flexDirection: 'row',
          alignItems: 'center',
          paddingTop: 70,
          paddingBottom: Spacing.md,
          paddingHorizontal: Spacing.md,
          backgroundColor: Colors.trueBlack,
          borderBottomWidth: 1,
          borderBottomColor: Colors.amber,
        }}
      >
        <TouchableOpacity
          onPress={() => router.back()}
          style={{ padding: Spacing.sm }}
        >
          <Text style={{ color: Colors.amber, ...Typography.body }}>← Back</Text>
        </TouchableOpacity>

        <View style={{ flex: 1, flexDirection: 'row', justifyContent: 'center', gap: Spacing.md, paddingRight: isWeb ? Spacing.md : 80 }}>
          {isWeb ? (
            <TouchableOpacity
              onPress={handleOpenInTab}
              style={{
                paddingHorizontal: Spacing.md,
                paddingVertical: Spacing.sm,
                backgroundColor: Colors.amber,
                borderRadius: 4,
              }}
            >
              <Text style={{ color: Colors.trueBlack, ...Typography.caption, fontWeight: '600' }}>
                Open PDF
              </Text>
            </TouchableOpacity>
          ) : (
            <>
              <TouchableOpacity
                onPress={handleShare}
                style={{
                  paddingHorizontal: Spacing.md,
                  paddingVertical: Spacing.sm,
                  backgroundColor: Colors.amber,
                  borderRadius: 4,
                }}
              >
                <Text style={{ color: Colors.trueBlack, ...Typography.caption, fontWeight: '600' }}>
                  Share
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                onPress={handleDownload}
                style={{
                  paddingHorizontal: Spacing.md,
                  paddingVertical: Spacing.sm,
                  borderWidth: 1,
                  borderColor: Colors.amber,
                  borderRadius: 4,
                }}
              >
                <Text style={{ color: Colors.amber, ...Typography.caption, fontWeight: '600' }}>
                  Save
                </Text>
              </TouchableOpacity>
            </>
          )}
        </View>
      </View>

      {/* PDF Viewer */}
      {error && (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: Spacing.lg }}>
          <Text style={{ color: Colors.warning, ...Typography.body, textAlign: 'center' }}>
            {error}
          </Text>
        </View>
      )}

      {!error && (
        <PlatformPdfViewer
          uri={pdfUrl}
          onLoadComplete={(numberOfPages: number) => {
            console.log(`PDF loaded: ${numberOfPages} pages`);
            setIsLoading(false);
          }}
          onError={(err: unknown) => {
            console.error('PDF error:', err);
            setError('Failed to load PDF. Make sure the backend is running.');
            setIsLoading(false);
          }}
          style={{ flex: 1 }}
        />
      )}

      {isLoading && !error && (
        <View
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            justifyContent: 'center',
            alignItems: 'center',
            backgroundColor: 'rgba(0,0,0,0.7)',
          }}
        >
          <ActivityIndicator size="large" color={Colors.amber} />
          <Text style={{ color: Colors.amber, ...Typography.body, marginTop: Spacing.md }}>
            Loading PDF...
          </Text>
        </View>
      )}
    </View>
  );
}
