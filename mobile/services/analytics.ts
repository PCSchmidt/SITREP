/**
 * analytics.ts — central analytics service for SITREP
 *
 * Wraps Mixpanel (user events) and Sentry (crash reporting).
 * Gracefully no-ops when tokens are not configured.
 * Call initAnalytics() once at app startup, then use the track* helpers.
 */
import * as Sentry from '@sentry/react-native';

// Tokens come from mobile/.env.local (EXPO_PUBLIC_ prefix makes them available client-side)
const MIXPANEL_TOKEN = process.env.EXPO_PUBLIC_MIXPANEL_TOKEN ?? '';
const SENTRY_DSN = process.env.EXPO_PUBLIC_SENTRY_DSN ?? '';

let _mixpanel: any = null;

export async function initAnalytics(): Promise<void> {
  // Sentry — initialize crash reporting
  if (SENTRY_DSN) {
    Sentry.init({
      dsn: SENTRY_DSN,
      tracesSampleRate: 0.1,  // 10% performance traces (free tier friendly)
      debug: false,
    });
  }

  // Mixpanel — initialize event tracking
  if (MIXPANEL_TOKEN) {
    try {
      const { Mixpanel } = await import('mixpanel-react-native');
      const instance = new Mixpanel(MIXPANEL_TOKEN, /* trackAutomaticEvents */ true);
      await instance.init();
      _mixpanel = instance;
    } catch (e) {
      console.warn('[Analytics] Mixpanel init failed:', e);
    }
  }
}

function track(event: string, props?: Record<string, unknown>): void {
  if (_mixpanel) {
    _mixpanel.track(event, props ?? {});
  }
}

// --- Typed event helpers ---

export function trackAppOpen(): void {
  track('app_open');
}

export function trackBriefingView(briefingId: string, region: string, title: string): void {
  track('briefing_view', { briefing_id: briefingId, region, title });
}

export function trackRegionFilter(region: string): void {
  track('region_filter', { region });
}

export function trackPdfView(briefingId: string): void {
  track('pdf_view', { briefing_id: briefingId });
}

export function trackPdfShare(briefingId: string): void {
  track('pdf_share', { briefing_id: briefingId });
}

// Re-export Sentry so screens can call Sentry.captureException() directly
export { Sentry };
