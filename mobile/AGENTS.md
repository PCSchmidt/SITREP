# AGENTS

Instructions for coding agents working in `mobile/`. Read this before changing anything
here.

This directory builds the mobile app and the web build at
**https://pcschmidt.github.io/sitrep/**; both read the production API at
**https://sitrep-production-6aac.up.railway.app**.

## Expo has changed - use the versioned docs

This app runs Expo SDK ~56.0.8. APIs move between SDKs, and examples from older blog posts
or from memory are often wrong. Read the exact versioned docs at
**https://docs.expo.dev/versions/v56.0.0/** before writing or changing native or
Expo-module code.

## Project facts

| | |
| --- | --- |
| Expo SDK | ~56.0.8, React Native 0.85.3, React 19.2.3 |
| Routing | expo-router ~56.2.8, typed routes, web `baseUrl` `/sitrep` |
| Language | TypeScript 6, strict mode - `npx tsc --noEmit` must pass |
| Styling | NativeWind 4 plus `constants/tokens.ts` |
| Data | TanStack Query 5 hooks in `hooks/useBriefings.ts`, fetching via `api/client.ts` |
| API | production `https://sitrep-production-6aac.up.railway.app` |

## Commands

```bash
npm install
npx expo start              # dev server; i, a, w to pick a target
npx tsc --noEmit            # type check, no output on success
npx expo run:android        # native dev build, ~10 minutes
npx expo export -p web      # web export; the portfolio repo publishes this
```

## Rules

- Do not edit `dist/`, `node_modules/`, or `package-lock.json` by hand.
- Keep the platform fork in `PlatformPdfViewer.tsx` / `PlatformPdfViewer.web.tsx`:
  `react-native-pdf` is native-only, so the web build must stay on the iframe path.
- `api/client.ts` caches every briefing in AsyncStorage and returns the cached copy with
  `isStale: true` when a fetch fails. Do not remove that path - it is what keeps the app
  readable offline.
- Parse dates defensively. An unparseable `generated_at` used to throw and remove a whole
  desk from the app.
- Do not add a dependency for something `expo-*` or React Native already provides at this
  SDK version.

## See also

- [README.md](README.md) - app overview, structure, and store state.
- [../README.md](../README.md) - the project as a whole.
- [../DEPLOYMENT.md](../DEPLOYMENT.md) - how the app and API are deployed.
