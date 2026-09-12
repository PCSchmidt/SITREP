# SITREP mobile

The Expo / React Native app for SITREP: four regional desks plus the composite Global
briefing, each with a BLUF, key developments, sourced sections, and a PDF.

The same codebase ships three surfaces: the phone app, the web build at
**https://pcschmidt.github.io/sitrep/**, and the development build used on a physical
device. All of them read the production API at
**https://sitrep-production-6aac.up.railway.app**.

## Tech stack

| | |
| --- | --- |
| Framework | Expo SDK ~56.0.8, React Native 0.85.3, React 19.2.3 |
| Routing | expo-router ~56.2.8 (file-based), typed routes, `baseUrl` `/sitrep` |
| Language | TypeScript 6, strict |
| Styling | NativeWind 4 (Tailwind for React Native) + `constants/tokens.ts` |
| Server state | TanStack Query 5 (`staleTime` 5 minutes, `gcTime` 10 minutes) |
| On-device cache | AsyncStorage, keyed `sitrep:briefing:v1:<desk>` |
| PDF | `react-native-pdf` on device; an `<iframe>` on web |
| Analytics | Mixpanel (events) + Sentry (crashes), no-op when tokens are unset |
| Builds | EAS (`eas.json` profiles: development, preview, production) |

`zustand` is still listed in `package.json` but no screen or hook uses it today; TanStack
Query holds all shared client state.

## Project structure

```
mobile/
├── api/client.ts               # production API base URL, fetch + transform, AsyncStorage cache
├── app/
│   ├── _layout.tsx             # QueryClientProvider, AppState refetch, nav chrome
│   ├── index.tsx               # home: Global + four desk tabs, stale-data banner
│   ├── detail/[id].tsx         # briefing detail
│   ├── pdf/[id].tsx            # full-screen PDF viewer
│   ├── about.tsx               # about and AI disclaimer
│   ├── privacy.tsx             # privacy policy
│   └── terms.tsx               # terms of service
├── components/
│   ├── BriefingCard.tsx        # briefing preview card
│   ├── RegionTab.tsx           # region filter tabs
│   ├── BLUFSection.tsx         # BLUF highlighted section
│   ├── DisclaimerBanner.tsx    # AI content warning
│   ├── SourceCitation.tsx      # article source links
│   ├── PlatformPdfViewer.tsx   # native: react-native-pdf
│   └── PlatformPdfViewer.web.tsx # web: iframe with a 6s fallback timer
├── constants/tokens.ts         # colours, typography, spacing
├── hooks/useBriefings.ts       # TanStack Query hooks and query keys
├── services/analytics.ts       # Mixpanel + Sentry wrappers
├── data/mockBriefings.ts       # placeholder briefings for local UI work
├── types/briefing.ts           # briefing models
├── app.json                    # Expo config, version 1.0.0, Android versionCode 7
└── eas.json                    # build and submit profiles
```

## Quick start

```bash
cd mobile
npm install
npx expo start        # then press i (iOS), a (Android), or w (web)
```

The scripts in `package.json` wrap the same commands. Note that `npm run ios` and
`npm run android` call `expo run:ios` and `expo run:android`, which build and install a
development client (about 10 minutes on Android), not just open an emulator.

```bash
npm start             # expo start
npm run android       # expo run:android - native dev build
npm run ios           # expo run:ios - native dev build
npm run web           # expo start --web
```

The app talks to the production API by default, so no backend needs to run locally. To
point it at a local API, change `API_BASE_URL` in `api/client.ts`.

Analytics tokens are optional and live in `mobile/.env.local` (git-ignored) for local runs;
the values used by EAS builds are pinned in `eas.json`.

```
EXPO_PUBLIC_MIXPANEL_TOKEN=<mixpanel token>
EXPO_PUBLIC_SENTRY_DSN=<sentry DSN>
```

## How data loads

- Each desk is one TanStack Query fetch against `/briefing/latest?region=...`; Global uses
  `/briefing/global`.
- Every successful response is written to AsyncStorage. If a later fetch fails, the cached
  briefing is returned with `isStale: true` and the home screen shows a stale-data banner
  instead of an empty screen.
- The root layout invalidates the briefing queries when the app returns to the foreground,
  so a briefing generated overnight appears without a restart. On web, window focus does
  the same job.
- Dates are parsed defensively. An unparseable `generated_at` used to throw during
  transform and wipe a whole desk from the app; the parser now falls back to today's date
  and the desk still renders.

## PDFs

The PDF screen embeds `GET /briefing/latest/pdf` for the desk. On device that URL is handed
to `react-native-pdf`; on web, `PlatformPdfViewer.web.tsx` renders it in an `<iframe>`.
Because a browser can decide to download a PDF instead of rendering it, the web viewer
clears its spinner on a 6-second timer and reports page count `0` rather than pretending to
know the page total. The API serves the file with `Content-Disposition: inline` for the
same reason.

PDFs are not stored anywhere: the API regenerates one from the stored briefing whenever the
container cache is missing or stale.

## Design system

Military aesthetic, AMOLED-optimised.

| Token | Value |
| --- | --- |
| True black | `#000000` |
| Amber accent | `#FFA500` |
| Gold | `#FFD700` |

System fonts (SF Pro, Roboto), monospace for timestamps and metadata. Full tokens live in
`constants/tokens.ts`.

## Store state

| | |
| --- | --- |
| app.json version | 1.0.0 |
| Android package | `com.pcschmidt.sitrep`, versionCode 7 |
| iOS bundle id | `com.pcschmidt.sitrep` |
| Production build | `npx eas build --profile production` (Android AAB) |
| Release status | Google Play closed testing next (20 testers, 14 days), then Apple App Store |
| Still to produce | 5 store screenshots, a 1024x500 feature graphic |

Store and legal pages: https://pcschmidt.github.io/sitrep/privacy-policy and
https://pcschmidt.github.io/sitrep/terms.

## See also

- [../README.md](../README.md) - what SITREP is and how to run the whole project.
- [../DEPLOYMENT.md](../DEPLOYMENT.md) - production topology and runbook.
- [../CONTRACT.md](../CONTRACT.md) - API surface the client depends on.
- [AGENTS.md](AGENTS.md) - instructions for coding agents working in this directory.

## Licence

MIT. The app is built on the Expo template, whose own MIT licence (`LICENSE`, © 650
Industries) covers the template code.
