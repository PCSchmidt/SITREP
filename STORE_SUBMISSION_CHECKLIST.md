# STORE SUBMISSION CHECKLIST

Submission state for SITREP on Google Play and the Apple App Store, in the order the two stores will be worked.

**Web app: https://pcschmidt.github.io/sitrep/ · Privacy policy: https://pcschmidt.github.io/sitrep/privacy-policy · Terms of service: https://pcschmidt.github.io/sitrep/terms** — all three return HTTP 200, checked 2026-09-12.

| | |
| --- | --- |
| Android package | `com.pcschmidt.sitrep` |
| iOS bundle ID | `com.pcschmidt.sitrep` |
| App version | 1.0.0 (`mobile/app.json`) |
| Android version code | 7, with `autoIncrement: true` on the production profile |
| Mobile stack | Expo SDK 56.0.8, React Native 0.85.3, React 19.2.3, expo-router 56.2.8 |
| Backend | v0.21.11 at https://sitrep-production-6aac.up.railway.app (Railway, Docker, uvicorn + FastAPI) |
| Production AAB | `cd mobile && eas build --platform android --profile production` |
| Submission order | Google Play closed testing (20 testers, 14 days) -> Google Play production -> Apple App Store |

Store assets are not finished: 5 screenshots and a 1024x500 feature graphic are still to produce (step 9).

## Step 1 - EAS account and project (done)

1. Create account at expo.dev
2. Run in terminal:
   ```bash
   npx install-expo-modules
   npm install -g eas-cli
   eas login
   ```
3. Initialize project (generates EAS project ID):
   ```bash
   cd mobile
   eas init
   ```
4. Copy the generated `projectId` into `mobile/app.json` under `extra.eas.projectId`

---

## Step 2 - App icons and splash (done)

SITREP-branded assets are checked in at `mobile/assets/` and wired in `mobile/app.json` (`icon`, `adaptiveIcon.foregroundImage`, `adaptiveIcon.backgroundImage`, `adaptiveIcon.monochromeImage`, `favicon`).

### iOS icon (`mobile/assets/icon.png`)

- Size: 1024×1024 pixels
- Format: PNG, no transparency, no rounded corners (Apple adds them)
- Content: SITREP wordmark or military-aesthetic emblem on black background

### Android adaptive icons

- `android-icon-foreground.png` — icon foreground (1024×1024, transparent bg)
- `android-icon-background.png` — icon background (1024×1024, solid color)
- `android-icon-monochrome.png` — monochrome version for themed icons

### Splash screen (`mobile/assets/splash-icon.png`)

- Size: 1284×2778 or larger (will be contained on black background)
- Content: SITREP wordmark centered, dark military aesthetic

**Tool recommendation:** Use Figma or Adobe Illustrator. Canva also works for simple icons.

---

## Step 3 - Analytics tokens (done)

Both tokens are set in all three `eas.json` build profiles (`development`, `preview`, `production`). Keep the steps below for the day a token is rotated.

1. Create Mixpanel account at mixpanel.com
   - Create new project "SITREP Production"
   - Copy Project Token from: Settings → Project Settings → Project Token

2. Create Sentry account at sentry.io
   - Create new React Native project "SITREP"
   - Copy DSN from: Project Settings → Client Keys → DSN

3. Add to `mobile/.env.local`:
   ```
   EXPO_PUBLIC_MIXPANEL_TOKEN=<your_token>
   EXPO_PUBLIC_SENTRY_DSN=<your_dsn>
   ```

4. Rebuild dev APK to activate native analytics:
   ```bash
   cd mobile
   npx expo run:android
   ```

---

## Step 4 - Legal pages (done)

Both pages are live, and both `app.json` and the store listings point at them:

- https://pcschmidt.github.io/sitrep/privacy-policy
- https://pcschmidt.github.io/sitrep/terms

They are hosted from the `PCSchmidt/PCSchmidt.github.io` portfolio repo, from `public/sitrep/privacy-policy.html` and `public/sitrep/terms.html`; the deploy workflow rebuilds the app export into `public/sitrep/` and leaves those two files alone. The copies kept here, `docs/privacy-policy.html` and `docs/terms.html`, were byte-identical to the live pages on 2026-09-12. The source text is [PRIVACY_POLICY.md](PRIVACY_POLICY.md) and [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md).

If either markdown file changes, regenerate the HTML and republish it. The markdown is not the published artifact. As of 2026-09-12 this repo's markdown is ahead of the published pages: the markdown names the Supabase store, the Guardian Open Platform API, the on-device cache, and the model waterfall, and none of that is on the live pages yet.

---

## Step 5 - Production builds

Once icons and tokens are ready.

### Android production build (AAB for Play)

```bash
cd mobile
eas build --platform android --profile production
```

- The production profile builds an app bundle (`.aab`), not an APK.
- Upload the `.aab` to Google Play Console.
- `versionCode` auto-increments on every production build; the last local value is 7 in `mobile/app.json`.

### iOS production build (IPA for App Store)

```bash
cd mobile
eas build --platform ios --profile production
```

- Requires an Apple Developer account ($99/year).
- EAS manages signing certificates automatically and can upload to App Store Connect.
- Deferred: Android ships first.

---

## Step 6 - Google Play Console: closed testing (next)

Dashboard: play.google.com/console

1. Create the developer account ($25 one-time fee) if it does not exist yet.
2. Create app -> SITREP -> Default language: English.
3. Fill in the store listing (paste from [APP_STORE_LISTING.md](APP_STORE_LISTING.md)):
   - App name, short description, full description
   - 5 phone screenshots
   - Icon (512x512 PNG — build it from the 1024x1024 `mobile/assets/icon.png`, Play resizes)
   - Feature graphic (1024x500, see step 9)
4. Content rating: complete the questionnaire (references to war and conflict -> Teen).
5. Target audience: 13+.
6. Privacy policy URL: https://pcschmidt.github.io/sitrep/privacy-policy
7. App category: News & Magazines. Pricing: Free.
8. Create a release, upload the `.aab`, and roll it out to the **closed testing** track.
9. Recruit at least 20 testers and keep them opted in for 14 continuous days. A new personal developer account needs that closed-test record before it can apply for production access.
10. Apply for production access in the Play Console.

The 14-day clock is the long pole: start it as soon as one AAB is stable, and collect tester feedback in that window. Play review for a first submission takes 3-7 days.

---

## Step 7 - Google Play Console: production (after the closed test)

1. Promote the tested release to production.
2. Roll out to 100%, or use a staged rollout for a slow ramp.
3. Keep the listing text, screenshots, and privacy policy URL consistent with the live pages.

---

## Step 8 - App Store Connect (deferred until Android ships)

Dashboard: appstoreconnect.apple.com

1. Sign in with the Apple ID tied to the Apple Developer Program.
2. My Apps -> + -> New App.
3. Fill in:
   - Platform: iOS
   - Name: SITREP
   - Primary Language: English (U.S.)
   - Bundle ID: com.pcschmidt.sitrep
   - SKU: SITREP001
4. App Information:
   - Subtitle: AI Intelligence Briefings
   - Category: News / Reference
   - Privacy Policy URL: https://pcschmidt.github.io/sitrep/privacy-policy
5. Pricing: Free.
6. Version Information (paste from [APP_STORE_LISTING.md](APP_STORE_LISTING.md)):
   - Description
   - Keywords
   - Support URL
7. Screenshots: upload the 5 iOS screenshots (see step 9).
8. Build: select the EAS production build.
9. App Review Information:
   - Notes: "AI-generated content app. Content comes from public news sources. No user login."
   - Demo account: not required (no auth)
10. Submit for review. First review typically takes 24-48 hours.

---

## Step 9 - Screenshots and feature graphic (not produced)

Run the app on a physical device or simulator and capture these 5 screens:

| # | Screen | What to show |
| --- | --- | --- |
| 1 | Home - ALL tab | Global briefing card with amber header |
| 2 | Home - MIDDLE EAST tab | Regional briefing with the region filter highlighted |
| 3 | Detail | Full briefing: BLUF section plus one content section |
| 4 | PDF viewer | Multi-page PDF with amber header and Share/Save buttons |
| 5 | About | Disclaimer plus Privacy/Terms links |

- iOS: 6.7" display, 1290x2796 (iPhone 15 Pro Max).
- Android: 1080x1920 minimum.
- Google Play also needs a 1024x500 feature graphic. Nothing is produced yet.

An iOS app preview video (15-30 seconds) is optional: open app -> switch region tabs -> open a briefing -> view PDF -> share.

---

## Status tracker

| Step | Item | Status |
| --- | --- | --- |
| 1 | EAS account and `eas init` | Done - project ID `c0284b13-8077-4be7-acc5-e0cafbf0f3e2` in `mobile/app.json` |
| 2 | App icon 1024x1024 and adaptive icons | Done - `mobile/assets/` |
| 2 | Splash screen config | Done - legacy `splash` key removed (Expo SDK 56) |
| 3 | Mixpanel token configured | Done - set in all three `eas.json` profiles |
| 3 | Sentry DSN configured | Done - set in all three `eas.json` profiles |
| 3 | Analytics APK tested on device | Done - Samsung S25+, 2026-05-30 |
| 4 | Privacy policy hosted | Done - live, HTTP 200 on 2026-09-12 |
| 4 | Terms of service hosted | Done - live, HTTP 200 on 2026-09-12 |
| 5 | Android preview APK (v8, current copy) | Done - EAS build `5e7b26af`, installed on Samsung SM-S936U via adb (2026-09-15) |
| 5 | Android production AAB | Done - EAS build `d8ff7a74`, versionCode 8, commit 6fa68bd (2026-09-15). AAB at `C:/Users/pchri/.prime/agent/session-artifacts/sitrep-store/sitrep-v8-production.aab` |
| 5 | iOS production IPA | Deferred - Android first |
| 6 | Play Console account | Next step |
| 6 | Closed testing track, 20 testers for 14 days | Not started - gated on the AAB |
| 7 | Play production rollout | Blocked on step 6 |
| 8 | App Store Connect listing, screenshots, review | Deferred |
| 9 | 5 phone screenshots | Done - captured from the v8 preview APK on-device, `mobile/store-assets/screenshots/` (1080x2340) |
| 9 | 1024x500 feature graphic | Done - `mobile/store-assets/feature-graphic.png` (draft-1 style, black/amber wordmark); draft-2 alternate kept |

---

## See also

- [README.md](README.md) - project overview and current state.
- [APP_STORE_LISTING.md](APP_STORE_LISTING.md) - the copy to paste into both consoles, plus store metadata.
- [PRIVACY_POLICY.md](PRIVACY_POLICY.md) and [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) - the text behind the two live legal pages.
- [DEPLOYMENT.md](DEPLOYMENT.md) - backend and web deployment.
