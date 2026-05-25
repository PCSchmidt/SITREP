import { View, Text, ActivityIndicator, TouchableOpacity, Alert, Platform } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useState, useEffect } from 'react';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Sharing from 'expo-sharing';
import { cacheDirectory, documentDirectory, downloadAsync } from 'expo-file-system/legacy';
import { Colors, Typography, Spacing } from '../../constants/tokens';

const API_BASE_URL = 'http://10.0.0.201:8001';

export default function PDFViewerScreen() {
  const { id } = useLocalSearchParams();
  const insets = useSafeAreaInsets();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [PdfComponent, setPdfComponent] = useState<any>(null);

  // Lazy load PDF component to avoid native module errors at app startup
  useEffect(() => {
    const loadPdf = async () => {
      try {
        const Pdf = (await import('react-native-pdf')).default;
        setPdfComponent(() => Pdf);
      } catch (error) {
        console.error('Failed to load PDF component:', error);
        setError('Failed to load PDF viewer. Please restart the app.');
      }
    };
    loadPdf();
  }, []);

  const pdfSource = {
    uri: `${API_BASE_URL}/briefing/latest/pdf`,
    cache: true,
  };

  const handleShare = async () => {
    console.log('Share button pressed');
    try {
      // Download PDF to local file system first
      const localUri = `${cacheDirectory}sitrep_${id}.pdf`;
      console.log('Downloading PDF to:', localUri);

      const downloadResult = await downloadAsync(
        `${API_BASE_URL}/briefing/latest/pdf`,
        localUri
      );
      console.log('Download result:', downloadResult.status);

      if (downloadResult.status === 200) {
        const canShare = await Sharing.isAvailableAsync();

        if (canShare) {
          await Sharing.shareAsync(downloadResult.uri, {
            mimeType: 'application/pdf',
            dialogTitle: 'Share SITREP Briefing',
            UTI: 'com.adobe.pdf',
          });
        } else {
          Alert.alert('Sharing Not Available', 'Sharing is not available on this device.');
        }
      } else {
        Alert.alert('Download Failed', 'Could not download PDF for sharing.');
      }
    } catch (err) {
      console.error('Share error:', err);
      Alert.alert('Share Failed', 'Could not share PDF. Please try again.');
    }
  };

  const handleDownload = async () => {
    console.log('Save button pressed');
    try {
      const localUri = `${documentDirectory}sitrep_${id}.pdf`;
      console.log('Saving PDF to:', localUri);

      const downloadResult = await downloadAsync(
        `${API_BASE_URL}/briefing/latest/pdf`,
        localUri
      );
      console.log('Save result:', downloadResult.status);

      if (downloadResult.status === 200) {
        Alert.alert(
          'PDF Saved',
          `Briefing saved to ${Platform.OS === 'ios' ? 'Files app' : 'Downloads'}`,
          [{ text: 'OK' }]
        );
      } else {
        Alert.alert('Download Failed', 'Could not save PDF.');
      }
    } catch (err) {
      console.error('Download error:', err);
      Alert.alert('Save Failed', 'Could not save PDF. Please try again.');
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: Colors.trueBlack }}>
      {/* Header with actions */}
      <View
        style={{
          flexDirection: 'row',
          justifyContent: 'space-between',
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

        <View style={{ flexDirection: 'row', gap: Spacing.md }}>
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
        </View>
      </View>

      {/* PDF Viewer */}
      {error && (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: Spacing.lg }}>
          <Text style={{ color: Colors.warning, ...Typography.body, textAlign: 'center' }}>
            {error}
          </Text>
          <Text style={{ color: Colors.textSubtle, ...Typography.caption, textAlign: 'center', marginTop: Spacing.sm }}>
            Make sure the backend is running on http://10.0.0.201:8001
          </Text>
        </View>
      )}

      {!error && PdfComponent && (
        <PdfComponent
          source={pdfSource}
          onLoadComplete={(numberOfPages: number) => {
            console.log(`PDF loaded: ${numberOfPages} pages`);
            setIsLoading(false);
          }}
          onError={(error: any) => {
            console.error('PDF error:', error);
            setError('Failed to load PDF. Make sure the backend is running.');
            setIsLoading(false);
          }}
          onLoadProgress={(percent: number) => {
            console.log(`PDF loading: ${percent}%`);
          }}
          style={{ flex: 1, backgroundColor: Colors.trueBlack }}
          trustAllCerts={false}
          enablePaging={true}
          horizontal={false}
          spacing={10}
          fitPolicy={0}
        />
      )}

      {isLoading && (
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
