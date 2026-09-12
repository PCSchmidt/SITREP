# APP STORE LISTING

Store copy and metadata for SITREP, ready to paste into App Store Connect and Google Play Console. Nothing is submitted yet; Google Play closed testing comes first — see [STORE_SUBMISSION_CHECKLIST.md](STORE_SUBMISSION_CHECKLIST.md).

**Live privacy policy: https://pcschmidt.github.io/sitrep/privacy-policy · Terms of service: https://pcschmidt.github.io/sitrep/terms** — both return HTTP 200, checked 2026-09-12. The copy below must stay consistent with those two pages.

| | |
| --- | --- |
| Android package / iOS bundle ID | `com.pcschmidt.sitrep` |
| App version | 1.0.0, Android versionCode 7 (`mobile/app.json`) |
| Mobile stack | Expo SDK 56.0.8, React Native 0.85.3, React 19.2.3, expo-router 56.2.8 |
| Screenshots | 5 per store, not produced yet |
| Feature graphic | 1024x500, not produced yet |

---

## App Store (iOS)

### App name (30 chars max)

```
SITREP
```

### Subtitle (30 chars max — current copy is 25)

```
AI Intelligence Briefings
```

### Category

```
Primary:   News
Secondary: Reference
```

### Age rating

```
12+ (Infrequent/Mild Mature/Suggestive Themes — geopolitical conflict coverage)
```

### Privacy policy URL

```
https://pcschmidt.github.io/sitrep/privacy-policy
```

### Support URL

```
https://github.com/PCSchmidt/SITREP/issues
```
Returns HTTP 200, checked 2026-09-12.

### Keywords (100 chars max — comma-separated, no spaces after commas. Current copy is 97)

```
intelligence,military,geopolitics,briefing,OSINT,defense,security,news,analysis,threat assessment
```

### Description (4000 chars max — current copy is 2050)

```
SITREP delivers geopolitical intelligence briefings in BLUF (Bottom Line Up Front) format, built from open-source news.

BOTTOM LINE UP FRONT
Every briefing opens with the single most important takeaway, written for someone who needs to know what matters now.

FOUR REGIONAL BRIEFINGS
• Middle East — Iran, Israel, the Gulf, Strait of Hormuz
• Indo-Pacific — China-Taiwan tensions, South China Sea, Korean Peninsula, ASEAN
• Europe/Africa — Ukraine, Russia, NATO, sub-Saharan Africa
• Western Hemisphere — Latin America security, Mexico, Venezuela, the Caribbean

GLOBAL CROSS-REGIONAL VIEW
The ALL view stitches all four regional briefings together in full — about 120 articles in one report — rather than a thin summary. Connections between theaters, such as how US-China competition shapes decisions from Seoul to Santiago, land in one place.

SOURCES
Each run pulls roughly 540 articles through 13 scrapers, and cites the source article for each claim:
• ISW — daily Ukraine and Iran assessments
• Defense One, Breaking Defense — Pentagon policy, procurement, military technology
• War on the Rocks, Foreign Policy, CFR — strategic analysis
• The War Zone — military aviation and weapons systems
• Al Jazeera — Middle East and Africa coverage
• Reuters, Bloomberg, BBC, The Economist, World Bank — economic and market reporting
• Americas Quarterly — Latin America coverage
• GDELT, the Guardian Open Platform API, and US/UK government releases

PDF EXPORT
Every briefing is available as a PDF report with hyperlinked sources. Share it, save it to Files, or open it in any PDF reader.

DAILY UPDATES
New briefings are generated every day at 06:00 UTC. No subscription, no account.

DISCLAIMER
All content is AI-generated from open-source news. This is not official intelligence. Accuracy is not guaranteed, and sources are cited but not independently verified. Do not use it for operational, military, or government decisions.

A portfolio project by Chris Schmidt, a full-stack developer working on AI-integrated mobile apps.
pcschmidt.github.io
```

---

## Google Play (Android)

### App name (50 chars max — current copy is 33)

```
SITREP: AI Intelligence Briefings
```

### Short description (80 chars max — current copy is 70)

```
AI geopolitics briefings in BLUF format. 4 regions plus a global view.
```

### Full description (4000 chars max — current copy is 1149)

```
SITREP delivers geopolitical intelligence briefings in BLUF (Bottom Line Up Front) format, built from open-source news.

FOUR REGIONAL BRIEFINGS
• Middle East — Iran, Israel, the Gulf, Strait of Hormuz
• Indo-Pacific — China, Taiwan, South China Sea, Korea, ASEAN
• Europe/Africa — Ukraine, Russia, NATO, sub-Saharan Africa
• Western Hemisphere — Latin America, Mexico, the Caribbean

GLOBAL VIEW
The ALL tab stitches all four regional briefings together in full, so cross-regional connections show up in one report.

SOURCES
About 540 articles per run through 13 scrapers: ISW, Defense One, Breaking Defense, War on the Rocks, The War Zone, Al Jazeera, Foreign Policy, CFR, Americas Quarterly, Reuters, Bloomberg, BBC, The Economist, World Bank, GDELT, the Guardian Open Platform API, and US/UK government releases. Every claim cites its source article.

PDF BRIEFINGS
Every briefing exports as a PDF with hyperlinked sources. Share it or save it to the device.

DAILY UPDATES, NO ACCOUNT
New briefings every day at 06:00 UTC. Free. No login, no subscription.

AI-generated from open-source news. Not official intelligence. Not for operational use.
```

### Category

```
News & Magazines
```

### Tags (5 max)

```
news, military, intelligence, geopolitics, security
```

### Content rating

```
Teen (Violence — references to war and conflict)
```

### Privacy policy URL

```
https://pcschmidt.github.io/sitrep/privacy-policy
```

### Terms of service URL (linked in the app, not a Play field)

```
https://pcschmidt.github.io/sitrep/terms
```

---

## Screenshots (not produced yet)

5 screens are needed for each store. Take them on a device or emulator; the app's default tab is the composite ALL briefing.

### iOS (6.7" iPhone — 1290x2796px)

Take on an iPhone 15 Pro Max or a simulator at that resolution. Show:
1. Home screen — ALL tab with the global briefing card
2. Home screen — MIDDLE EAST tab with the regional briefing card
3. Detail screen — full briefing with the BLUF and sections
4. PDF viewer — briefing PDF open and paginated
5. About screen — disclaimer and legal links

### Android (phone — 1080x1920px minimum)

Same 5 screens as iOS. The Android preview APK runs on device (Samsung S25+).

### Feature graphic (Google Play only, 1024x500)

Not produced. SITREP wordmark on the black/amber palette is the plan.

### App preview video (optional, iOS only — 15-30 seconds)

Show: open app -> switch region tabs -> open a briefing -> view PDF -> share

---

## What-you-see-is-what-you-get metadata

| Field | Value |
| --- | --- |
| Android package | com.pcschmidt.sitrep |
| iOS bundle ID | com.pcschmidt.sitrep |
| Version | 1.0.0 (`mobile/app.json`) |
| iOS build number | 1 |
| Android version code | 7; auto-increments on production builds |
| Mobile stack | Expo SDK 56.0.8, React Native 0.85.3, React 19.2.3, expo-router 56.2.8 |
| Min Android | API 24 (Android 7.0), the Expo `minSdkVersion` default |
| Min iOS | not verified in this repo; read it off the EAS build or App Store Connect |
| Languages | English |
| In-app purchases | None |
| Ads | None |
| Subscription | None |
| Analytics | anonymous Mixpanel events and Sentry crash reports — see [PRIVACY_POLICY.md](PRIVACY_POLICY.md) |

Every claim above comes from `mobile/app.json`, `mobile/package.json`, or `mobile/eas.json`. The store listings must match the live legal pages; if either legal page changes, update the copy here.

---

## See also

- [README.md](README.md) — project overview and current state.
- [STORE_SUBMISSION_CHECKLIST.md](STORE_SUBMISSION_CHECKLIST.md) — build, testing gate, and submission order.
- [PRIVACY_POLICY.md](PRIVACY_POLICY.md) and [TERMS_OF_SERVICE.md](TERMS_OF_SERVICE.md) — the text behind the two live legal pages.
