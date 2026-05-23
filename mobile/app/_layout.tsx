import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import '../global.css';

export default function RootLayout() {
  return (
    <>
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
      </Stack>
    </>
  );
}
