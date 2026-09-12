# DESIGN_SYSTEM

Visual design reference for SITREP: colour, type, spacing, components, and screen layouts. The live tokens are `mobile/constants/tokens.ts` and `mobile/tailwind.config.js`; where a shipped screen differs from this spec, the code wins and the difference is listed under "Deviations from this spec".

| | |
| --- | --- |
| Status | Implemented. The design system shipped in v0.1 and is in the v0.21.10 build |
| Platform | Mobile-first, iOS + Android, AMOLED-optimised, dark only |
| Tokens | `mobile/constants/tokens.ts`, `mobile/tailwind.config.js` |
| Live app | **https://pcschmidt.github.io/sitrep/** |
| Facts checked | 2026-09-12 |

## Design philosophy

**Aesthetic**: Military intelligence briefing room  
**Tone**: Serious, technical, high-end, professional  
**Inspiration**: The LOWDOWN newsletter, military command centers, classified briefing documents  
**Platform**: Mobile-first (iOS + Android), AMOLED-optimized  

---

## Color palette

### Primary colors
```
Background (True Black):    #000000
Surface (Near Black):       #0A0A0A
Card Background:            #121212
Border/Divider:             #1A1A1A
```

### Accent colors
```
Primary Accent (Amber):     #FFA500  
Secondary Accent (Gold):    #FFD700
Warning (Red):              #FF4444
Success (Green):            #00FF41  (terminal green)
```

### Text colors
```
Heading (White):            #FFFFFF
Body (Gray):                #CCCCCC
Subtle (Dark Gray):         #888888
Disclaimer (Amber):         #FFA500
Source Citation (Gold):     #FFD700
```

### Semantic colors
```
Middle East:                #FF6B6B  (red tint)
Indo-Pacific:               #4ECDC4  (teal)
Europe/Africa:              #95E1D3  (mint)
Western Hemisphere:         #F38181  (coral)
```

---

## Typography

### Font stack
```
Primary: system default - 'SF Pro' on iOS, 'Roboto' on Android
Monospace: 'SF Mono' / 'Roboto Mono' (for timestamps and metadata)
```

No font files ship with the app. `mobile/constants/tokens.ts` and `mobile/tailwind.config.js` define only the monospace stack; everything else uses the platform system font. The PDF is the exception and bundles PT Serif and Lato - see "PDF design (generator v3)".

### Type scale
```
H1 (Screen Titles):         28px, weight 700, letter-spacing -0.5px
H2 (Section Headers):       20px, weight 600, letter-spacing -0.3px
H3 (Subsections):           16px, weight 600, letter-spacing 0px
Body (Content):             15px, weight 400, line-height 1.6
Caption (Metadata):         12px, weight 400, letter-spacing 0.5px
Label (Buttons):            14px, weight 600, letter-spacing 0.8px (uppercase)
```

### Text styles
```
BLUF Header:                H2, Amber (#FFA500), uppercase
Region Tag:                 Caption, Monospace, region semantic color
Timestamp:                  Caption, Monospace, Subtle Gray
Source Citation:            Caption, Gold (#FFD700), italic
Disclaimer:                 Body, Amber, bold
```

---

## Spacing system

Based on 4px grid:
```
4px  (xs)  - Tight spacing, icon padding
8px  (sm)  - Component internal padding
12px (md)  - Card padding
16px (lg)  - Section padding, default margin
24px (xl)  - Screen padding, major sections
32px (2xl) - Large gaps between major UI blocks
```

---

## Components

### 1. BriefingCard
```
Purpose: Display daily briefing summary on home screen
Layout:
  - Full width card
  - 12px padding
  - 1px amber border on left edge
  - True black background (#000000)
Content:
  - Timestamp (top right, caption, monospace, gray)
  - "WEEKLY SITREP" label (H3, amber, uppercase)
  - Briefing title/headline (H2, white)
  - 2-line preview text (body, gray)
  - Region tags (horizontal chips, semantic colors)
  - "View Full Report" CTA (amber text, right arrow icon)
```

### 2. RegionTab
```
Purpose: Filter briefings by geographic region
Layout:
  - Horizontal scrollable tabs
  - 8px vertical padding, 12px horizontal padding
  - Active: amber underline (2px), white text
  - Inactive: no underline, gray text
Regions:
  - ALL (default)
  - MIDDLE EAST (red tint)
  - INDO-PACIFIC (teal)
  - EUROPE/AFRICA (mint)
  - W. HEMISPHERE (coral)
Interaction:
  - Tap to filter
  - Smooth scroll animation
  - Active state persists across sessions
```

### 3. BLUFSection
```
Purpose: Display Bottom Line Up Front analysis
Layout:
  - Near-black background (#0A0A0A)
  - Amber left border (4px)
  - 16px padding
Content:
  - "BLUF" label (caption, amber, uppercase, monospace)
  - Summary text (body, white, bold)
  - Read time estimate (caption, gray, monospace)
```

### 4. SourceCitation
```
Purpose: Link to original article source
Layout:
  - Compact list item
  - 8px vertical padding
  - Border-bottom divider (#1A1A1A)
Content:
  - Source icon (publication logo, 16x16px, grayscale)
  - Article title (body, white)
  - Publication name (caption, gold, uppercase)
  - Date (caption, gray, monospace)
  - External link icon (→)
Interaction:
  - Tap opens in-app browser or external browser
  - Haptic feedback on tap
```

### 5. DisclaimerBanner
```
Purpose: quiet provenance note (the sources are real; the paraphrase is machine-written)
Layout:
  - Full-width footer strip, 1px top hairline (#1A1A1A), near-black background (#0A0A0A)
  - No colour block, no uppercase heading, no warning icon
  - 8px vertical padding, 16px horizontal
Content:
  - "AI-generated summary. Sources are real and cited; the wording is model-written.
     Not official intelligence." (11px, #888888, 15px line height)
Placement:
  - Bottom of the home screen, below the briefing list (dismissible, × on the right)
  - Bottom of the briefing detail screen, below the sources (not dismissible)
  - The About screen carries the long-form disclaimer instead
History:
  - Until 2026-09-12 this was an amber banner at the top of both screens with an
    uppercase "AI GENERATED CONTENT" heading. It was moved to the footer and toned
    down: the earlier copy implied the content itself was unreliable, when only the
    paraphrase is machine-written and every claim links to a real source.
```

### 6. PDFActionButton
```
Purpose: Primary CTA to view briefing as PDF
Layout:
  - Amber background (#FFA500)
  - Black text
  - Icon + label ("View as PDF")
  - 12px padding vertical, full width
  - Rounded corners (8px)
Content:
  - PDF icon (left)
  - "View as PDF" label (H3, black, bold, uppercase)
  - File size estimate (caption, black, right)
Placement:
  - Top of briefing detail screen (sticky below disclaimer)
  - Also in home screen briefing card (as secondary action)
Interaction:
  - Tap opens PDF viewer
  - Haptic feedback
  - Loading state while PDF fetches
```

### 7. RegionFilterChip
```
Purpose: Visual indicator of active region filter
Layout:
  - Pill-shaped chip
  - 4px padding vertical, 8px horizontal
  - Semantic color background (20% opacity)
  - Semantic color border (1px)
Content:
  - Region name (caption, uppercase, white)
  - X icon (to remove filter)
```

---

## PDF design (generator v3)

The PDF is a separate design from the app. `api/pdf_generation/pdf_generator_v3.py` produces an editorial, executive look, not the amber app palette:

| | |
| --- | --- |
| Fonts | PT Serif for headlines and cover, Lato for body (bundled TTFs; falls back to base-14 fonts if they are missing) |
| Palette | Navy `#13233b` masthead and headings, ink `#1c2330` body, slate `#5b6675` labels, hairline rules `#c5ccd4`, link blue `#1d4e89` |
| Cover | Two columns: Contents and Executive Summary |
| Sections | Numbered, region-tagged, with a numbered hyperlinked reference list per section |
| Disclaimer | AI-generated notice on the cover and in the page footer |
| Global | One document that renders all four regions in full, not a condensed summary |

The v3 generator replaced the earlier amber ReportLab, v1, and v2 generators, which were deleted. The "PDF Viewer Screen" mockup below still shows the old cover text; the app chrome around it is current.

---

## Screen layouts

### Home Screen (Latest Briefing)
```
┌─────────────────────────────────────┐
│                                     │
│  SITREP                     ⋮       │  ← Header (title + menu icon)
│  Intelligence Briefing              │
│                                     │
│  ┌─ ALL ─ MIDDLE EAST ─ INDO... ─┐ │  ← RegionTabs (horizontal scroll)
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 2026-05-18 0600 UTC        │   │  ← BriefingCard
│  │                             │   │
│  │ DAILY SITREP                │   │
│  │ Global Security Update      │   │
│  │                             │   │
│  │ Tensions escalate in...     │   │
│  │ Regional analysis shows...  │   │
│  │                             │   │
│  │ [M.EAST] [INDO-PAC] [EUR]   │   │
│  │                             │   │
│  │ View Full Report        →   │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 2026-05-11 0600 UTC        │   │  ← Previous briefing (grayed)
│  │ ...                         │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│ AI-generated summary. Sources are   │  ← DisclaimerBanner footer
│ real and cited. Not official intel. │     (dismissible ×)
└─────────────────────────────────────┘
```

### Briefing Detail Screen
```
┌─────────────────────────────────────┐
│  ← SITREP          Share    ⋯       │  ← Header (back + actions)
│                                     │
│  2026-05-18 0600 UTC               │  ← Timestamp
│  DAILY INTELLIGENCE BRIEFING        │  ← Title
│                                     │
│  ┌─ ALL ─ MIDDLE EAST ─ INDO... ─┐ │  ← Region filter (optional)
│                                     │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃ BLUF                         ┃   │  ← BLUF Section
│  ┃ U.S.-Israel military...     ┃   │
│  ┃ Economic blockades...        ┃   │
│  ┃ .. 8 min read                 ┃   │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛   │
│                                     │
│  ▼ Middle East                     │  ← Expandable sections
│  ┌─────────────────────────────┐   │
│  │ BLUF: The U.S.-Israel...   │   │
│  │                             │   │
│  │ 1. Covert Operations        │   │
│  │ Decapitation and failed...  │   │
│  │                             │   │
│  │ 2. Military Operations      │   │
│  │ U.S. Aircraft Losses...     │   │
│  │ ...                         │   │
│  └─────────────────────────────┘   │
│                                     │
│  ▶ Indo-Pacific                    │  ← Collapsed
│  ▶ Europe and Africa               │
│  ▶ Western Hemisphere              │
│                                     │
│  ─────────────────────────────────  │
│  SOURCES                           │
│  ┌─────────────────────────────┐   │
│  │ -- Congressional Report...  │   │  ← SourceCitation
│  │    THE AVIATIONIST      →   │   │
│  ├─────────────────────────────┤   │
│  │ -- CENTCOM head calls...    │   │
│  │    DEFENSE ONE          →   │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

### About Screen
```
┌─────────────────────────────────────┐
│  ← About                            │
│                                     │
│      [SITREP LOGO]                  │  ← App icon
│                                     │
│  SITREP v1.0                        │
│  Intelligence Briefing Platform     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ !!  IMPORTANT DISCLAIMER    │   │  ← Full legal disclaimer
│  │                             │   │
│  │ This app generates AI-      │   │
│  │ powered intelligence        │   │
│  │ summaries from open-source  │   │
│  │ news articles. This content │   │
│  │ is NOT official intelligence│   │
│  │ and should not be used for  │   │
│  │ operational decision-making.│   │
│  │                             │   │
│  │ Sources are cited but       │   │
│  │ accuracy is not guaranteed. │   │
│  │ Use at your own discretion. │   │
│  └─────────────────────────────┘   │
│                                     │
│  Sources                        →   │  ← Link to sources page
│  Privacy Policy                 →   │
│  Terms of Service               →   │
│  Contact                        →   │
│                                     │
│  Built by Chris Schmidt             │
│  pcschmidt.github.io                │
│                                     │
└─────────────────────────────────────┘
```

### PDF Viewer Screen
```
┌─────────────────────────────────────┐
│  ← Back             Share    ⋯      │  ← Header (back, share, more menu)
├─────────────────────────────────────┤
│  ╔═══════════════════════════════╗  │
│  ║ [PDF PAGE CONTENT]            ║  │  ← Full-screen PDF viewer
│  ║                               ║  │     (react-native-pdf)
│  ║  THE LOWDOWN                  ║  │
│  ║                               ║  │
│  ║  SITREP                       ║  │
│  ║  Weekly Intelligence Briefing ║  │
│  ║                               ║  │
│  ║  2026-05-18                   ║  │
│  ║                               ║  │
│  ║  !! AI GENERATED CONTENT      ║  │
│  ║                               ║  │
│  ║  [Pinch to zoom]              ║  │
│  ║  [Swipe for next page]        ║  │
│  ║                               ║  │
│  ╚═══════════════════════════════╝  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Page 1 of 18          [1/18] │  │  ← Page indicator (bottom overlay)
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘

Actions in More Menu (⋯):
- Save to Files
- Open in...
- Print (iOS AirPrint)
```

### Splash Screen (First Launch)
```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│      [SITREP LOGO]                  │  ← Large logo (amber on black)
│                                     │
│      SITREP                         │  ← App name
│      Intelligence Briefing          │
│                                     │
│  ┌─────────────────────────────┐   │
│  │  AI-GENERATED SUMMARY      │   │  ← First-launch notice (NOT built; the
│  │                             │   │     shipped app shows the footer note
│  │                             │   │     below the briefing list instead)
│  │                             │   │     (must tap to proceed)
│  │ This application synthesizes│   │
│  │ open-source intelligence    │   │
│  │ using artificial intelligence.│  │
│  │                             │   │
│  │ NOT OFFICIAL INTELLIGENCE   │   │
│  │                             │   │
│  │ Content is AI-generated and │   │
│  │ should not be used for      │   │
│  │ official decision-making.   │   │
│  │                             │   │
│  │ By continuing, you          │   │
│  │ acknowledge these risks.    │   │
│  │                             │   │
│  │ [I UNDERSTAND]              │   │  ← Button (amber)
│  │                             │   │
│  │ Privacy Policy | Terms →    │   │
│  └─────────────────────────────┘   │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

---

## Interactions and animations

### Transitions
- Screen-to-screen: Slide from right (iOS) / Material fade (Android)
- Tab switches: Crossfade (200ms)
- Expand/collapse sections: Smooth height animation (300ms, ease-in-out)
- Pull-to-refresh: Amber spinner at top

### Haptic Feedback
- Tap button: Light impact
- Region filter applied: Medium impact
- Error state: Notification feedback (vibration pattern)
- Briefing loaded: Success feedback

### Loading States
- Skeleton screens (dark gray shimmer on black)
- "Analyzing intelligence sources..." text
- Amber progress bar (determinate when possible)

### Error States
- Red accent color
- "Unable to load briefing" message
- "Retry" button (amber)
- Offline state: "No connection" with cached briefing option

---

## Accessibility

### WCAG AA compliance
- All body text needs a 4.5:1 contrast ratio minimum
- Contrast against `#000000`, recomputed from the tokens on 2026-09-12 with the WCAG 2.1 relative-luminance formula:
  - Amber `#FFA500`: 10.6:1, passes AA
  - White `#FFFFFF`: 21.0:1, passes AA
  - Body gray `#CCCCCC`: 13.1:1, passes AA
  - Subtle gray `#888888`: 5.9:1, passes AA for body text, so it is usable for captions
- No automated contrast test runs in this repo; the numbers above come from the token values, not from a device screenshot

### Touch Targets
- Minimum 44x44pt tap area (iOS Human Interface Guidelines)
- Minimum 48x48dp tap area (Android Material Design)

### Screen Reader Support
- Semantic HTML/React Native accessibility labels
- ARIA roles for screen readers
- Descriptive alt text for images/icons

### Dark Mode
- Always dark (AMOLED-optimized)
- No light mode toggle (intentional design choice)

---

## Responsive breakpoints

### Phone (Primary Target)
- iPhone: 375px - 428px width
- Android: 360px - 412px width
- Portrait orientation primary
- Landscape: Maintain vertical scroll

### Tablet (Future Consideration)
- iPad: Two-column layout (briefing list + detail)
- Android tablets: Material Design large screen patterns

---

## Icon system

### App Icon
```
Design: Stylized "S" letterform
Style: Amber (#FFA500) on black (#000000)
Shape: Rounded square (iOS), adaptive icon (Android)
Variants: 1024x1024 (app store), various sizes for system
```

### In-App Icons
- System icons from SF Symbols (iOS) / Material Icons (Android)
- Monochrome (white or amber)
- 20x20pt standard size
- Custom icons for region filters (simple geometric shapes)

---

## Platform-specific notes

### iOS
- Use native tab bar pattern for main navigation (if needed)
- Follow iOS Human Interface Guidelines
- SF Pro font family
- Haptic feedback via UIImpactFeedbackGenerator

### Android
- Material Design 3 components
- Roboto font family
- Ripple effects on tappable elements
- Follow Material Design guidelines

---

## Deviations from this spec (verified 2026-09-12)

The tokens match this document. Four details do not, and the spec is not the source of truth for them:

- `mobile/components/BriefingCard.tsx` still prints "WEEKLY SITREP" on the card. The pipeline runs daily, so this label is stale UI copy. No code was changed in this documentation pass.
- `mobile/app/about.tsx` still says "Briefings are generated weekly" and describes "weekly geopolitical intelligence briefings". Same stale copy.
- The About screen shows no version string. The app version lives in `mobile/app.json` (`1.0.0`); the backend version is `v0.21.10`.
- Store screenshots do not exist yet. Five phone screenshots and a 1024x500 feature graphic are still to be produced before the Google Play submission.

---

## Design checklist (all items shipped)

- [x] Color palette defined (military aesthetic: black + amber)
- [x] Typography scale established
- [x] Core components designed (BriefingCard, RegionTab, BLUF, PDFActionButton, etc.)
- [x] Key screens wireframed (Home, Detail, About, Splash, **PDF Viewer**)
- [x] **PDF generation & viewing** flow specified
- [x] **PDF sharing/save actions** documented
- [x] Heavy disclaimer placement confirmed (splash + sticky header + **PDF footer**)
- [x] Region filtering UI specified
- [x] Source citation format defined
- [x] WCAG AA contrast ratios verified
- [x] Touch target sizes meet platform guidelines
- [x] Loading/error states documented
- [x] Platform-specific considerations noted

---

## Next steps

Written when the frontend was approved. Steps 1 to 4 shipped in v0.1; step 5 is still open and is now a store requirement.

1. Implement the design system in the NativeWind config - done, v0.1 (`mobile/tailwind.config.js`)
2. Build the reusable component library - done, v0.1 (`mobile/components/`)
3. Create static screens with placeholder content - done, v0.1
4. Test on iOS Simulator and Android Emulator - done, v0.1; device testing continued through v0.17
5. Capture screenshots for store verification - open. Five phone screenshots and a 1024x500 feature graphic

---

## Where to read next

- [README.md](README.md) - overview, live URLs, and how to run the project
- [SPEC.md](SPEC.md) - the shipped feature list these screens belong to
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - which gate shipped each screen
- [CONTRACT.md](CONTRACT.md) - visual verification fields and the store checklist
