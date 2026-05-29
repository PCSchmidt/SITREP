import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Sentry, initAnalytics, trackAppOpen } from '../services/analytics';
import '../global.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

function RootLayout() {
  useEffect(() => {
    initAnalytics().then(() => {
      trackAppOpen();
    });
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: {
            backgroundColor: '#000000',
          },
          headerTintColor: '#FFA500',
          headerTitleStyle: {
            fontWeight: '600',
            fontSize: 20,
          },
          contentStyle: {
            backgroundColor: '#000000',
          },
        }}
      >
        <Stack.Screen
          name="index"
          options={{
            title: 'SITREP',
            headerShown: true,
          }}
        />
        <Stack.Screen
          name="detail/[id]"
          options={{
            title: 'Briefing Detail',
            headerShown: true,
          }}
        />
        <Stack.Screen
          name="about"
          options={{
            title: 'About',
            headerShown: true,
          }}
        />
        <Stack.Screen
          name="pdf/[id]"
          options={{
            title: 'PDF Viewer',
            headerShown: false, // Custom header in component
            presentation: 'fullScreenModal',
          }}
        />
      </Stack>
    </QueryClientProvider>
  );
}

export default Sentry.wrap(RootLayout);
