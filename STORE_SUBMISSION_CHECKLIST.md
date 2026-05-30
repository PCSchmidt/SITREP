# STORE_SUBMISSION_CHECKLIST.md
# SITREP | App Store & Google Play Submission Checklist
# Work through this sequentially before v0.17 Beta Testing.

---

## STEP 1: EAS Account Setup (Expo Application Services)

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

## STEP 2: App Icons

Current status: Expo default icons are in `mobile/assets/`.
**These need to be replaced with SITREP-branded assets.**

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

## STEP 3: Analytics Tokens

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

## STEP 4: Privacy Policy Hosting

The app.json and store listings reference:
`https://pcschmidt.github.io/sitrep/privacy-policy`

To host it:
1. In your `PCSchmidt/pcschmidt.github.io` portfolio repo (or create one)
2. Create `sitrep/privacy-policy.html` or `sitrep/privacy-policy.md`
3. Content is in `PRIVACY_POLICY.md` in this repo — convert to HTML
4. Push to GitHub Pages (auto-hosted at pcschmidt.github.io)

Terms of Service similarly at: `https://pcschmidt.github.io/sitrep/terms`

---

## STEP 5: Production Build

Once icons and tokens are ready:

### Android Production Build (AAB for Play Store)
```bash
cd mobile
eas build --platform android --profile production
```
- Downloads as `.aab` file
- Upload to Google Play Console

### iOS Production Build (IPA for App Store)
```bash
cd mobile
eas build --platform ios --profile production
```
- Requires Apple Developer account ($99/year)
- EAS manages signing certificates automatically
- Uploads directly to App Store Connect

---

## STEP 6: App Store Connect (iOS)

Dashboard: appstoreconnect.apple.com

1. Sign in with Apple ID associated with Apple Developer Program
2. My Apps → + → New App
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
5. Pricing: Free
6. Version Information (paste from APP_STORE_LISTING.md):
   - Description
   - Keywords
   - Support URL
7. Screenshots: Upload 5 iOS screenshots (see APP_STORE_LISTING.md)
8. Build: Select the EAS production build
9. App Review Information:
   - Notes: "AI-generated content app. Pulls from public news APIs. No user login."
   - Demo account: not required (no auth)
10. Submit for Review

**Review time**: typically 24-48 hours for first submission.

---

## STEP 7: Google Play Console (Android)

Dashboard: play.google.com/console

1. Create developer account ($25 one-time fee)
2. Create app → SITREP → Default language: English
3. Fill in store listing (paste from APP_STORE_LISTING.md):
   - App name, short description, full description
   - Screenshots (5 Android screenshots)
   - Icon (512×512 PNG — use same 1024×1024 icon, Play resizes)
   - Feature graphic (1024×500 banner — create separately)
4. Content rating: Complete questionnaire (Teen / Violence references)
5. Target audience: 13+
6. Privacy Policy URL
7. App category: News & Magazines
8. Pricing: Free
9. Release:
   - Create new release → Internal testing
   - Upload `.aab` from EAS build
   - Roll out to internal testing (you only — up to 100 testers for internal)
10. After internal test passes → Promote to Production

**Review time**: 3-7 days for first submission.

---

## STEP 8: Screenshots

Run the app on a physical device or simulator and capture these 5 screens:

| # | Screen | What to show |
|---|--------|--------------|
| 1 | Home — ALL tab | Global briefing card with amber header |
| 2 | Home — MIDDLE EAST tab | Regional briefing with region filter highlighted |
| 3 | Detail | Full briefing: BLUF section + one content section |
| 4 | PDF Viewer | Multi-page PDF with amber header and Share/Save buttons |
| 5 | About | Disclaimer + Privacy/Terms links |

**iOS sizes needed**: 6.7" (1290×2796) — iPhone 15 Pro Max
**Android size needed**: 1080×1920 minimum

---

## STATUS TRACKER

| Step | Item | Status |
|------|------|--------|
| 1 | EAS account + eas init | ✅ Complete (2026-05-30) |
| 2 | App icon 1024×1024 | ✅ Complete (pre-existing) |
| 2 | Splash screen | ✅ Complete (pre-existing) |
| 3 | Mixpanel token configured | ✅ Complete (2026-05-30) |
| 3 | Sentry DSN configured | ✅ Complete (2026-05-30) |
| 3 | Analytics dev APK rebuilt | ⬜ Pending (v0.17) |
| 4 | Privacy policy hosted | ✅ Complete (2026-05-30) |
| 4 | Terms of service hosted | ✅ Complete (2026-05-30) |
| 5 | Android AAB production build | ⬜ Pending |
| 5 | iOS IPA production build | ⬜ Pending |
| 6 | App Store Connect listing created | ⬜ Pending |
| 6 | iOS screenshots uploaded | ⬜ Pending |
| 6 | iOS submitted for review | ⬜ Pending |
| 7 | Google Play Console account | ⬜ Pending |
| 7 | Android screenshots uploaded | ⬜ Pending |
| 7 | Android internal track uploaded | ⬜ Pending |
| 8 | Screenshots taken (5 screens) | ⬜ Pending |
