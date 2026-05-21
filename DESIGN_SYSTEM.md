# DESIGN_SYSTEM.md
# SITREP Visual Design Specification

## DESIGN PHILOSOPHY

**Aesthetic**: Military intelligence briefing room  
**Tone**: Serious, technical, high-end, professional  
**Inspiration**: The LOWDOWN newsletter, military command centers, classified briefing documents  
**Platform**: Mobile-first (iOS + Android), AMOLED-optimized  

---

## COLOR PALETTE

### Primary Colors
```
Background (True Black):    #000000
Surface (Near Black):       #0A0A0A
Card Background:            #121212
Border/Divider:             #1A1A1A
```

### Accent Colors
```
Primary Accent (Amber):     #FFA500  
Secondary Accent (Gold):    #FFD700
Warning (Red):              #FF4444
Success (Green):            #00FF41  (terminal green)
```

### Text Colors
```
Heading (White):            #FFFFFF
Body (Gray):                #CCCCCC
Subtle (Dark Gray):         #888888
Disclaimer (Amber):         #FFA500
Source Citation (Gold):     #FFD700
```

### Semantic Colors
```
Middle East:                #FF6B6B  (red tint)
Indo-Pacific:               #4ECDC4  (teal)
Europe/Africa:              #95E1D3  (mint)
Western Hemisphere:         #F38181  (coral)
```

---

## TYPOGRAPHY

### Font Stack
```
Primary: 'SF Pro' (iOS) / 'Roboto' (Android)
Monospace: 'SF Mono' / 'Roboto Mono' (for timestamps, metadata)
```

### Type Scale
```
H1 (Screen Titles):         28px, weight 700, letter-spacing -0.5px
H2 (Section Headers):       20px, weight 600, letter-spacing -0.3px
H3 (Subsections):           16px, weight 600, letter-spacing 0px
Body (Content):             15px, weight 400, line-height 1.6
Caption (Metadata):         12px, weight 400, letter-spacing 0.5px
Label (Buttons):            14px, weight 600, letter-spacing 0.8px (uppercase)
```

### Text Styles
```
BLUF Header:                H2, Amber (#FFA500), uppercase
Region Tag:                 Caption, Monospace, region semantic color
Timestamp:                  Caption, Monospace, Subtle Gray
Source Citation:            Caption, Gold (#FFD700), italic
Disclaimer:                 Body, Amber, bold
```

---

## SPACING SYSTEM

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

## COMPONENTS

### 1. BriefingCard
```
Purpose: Display weekly briefing summary on home screen
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
Purpose: Heavy AI-generated content warning (compliance)
Layout:
  - Full-width banner
  - Amber background (#FFA500)
  - Black text for contrast
  - 12px padding
  - ⚠️ icon (left)
Content:
  - "AI GENERATED CONTENT" (H3, black, bold, uppercase)
  - "Not official intelligence. Use at your own discretion." (caption, black)
Placement:
  - Splash screen (full screen)
  - Top of every briefing detail screen (sticky header)
  - About page (expanded version with full disclaimer)
```

### 6. PDFActionButton
```
Purpose: Primary CTA to view briefing as PDF
Layout:
  - Amber background (#FFA500)
  - Black text
  - Icon + label (📄 "View as PDF")
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

## SCREEN LAYOUTS

### Home Screen (Latest Briefing)
```
┌─────────────────────────────────────┐
│  ⚠️ AI GENERATED CONTENT            │  ← DisclaimerBanner (dismissible)
├─────────────────────────────────────┤
│                                     │
│  SITREP                     ⋮       │  ← Header (title + menu icon)
│  Intelligence Briefing              │
│                                     │
│  ┌─ ALL ─ MIDDLE EAST ─ INDO... ─┐ │  ← RegionTabs (horizontal scroll)
│                                     │
│  ┌─────────────────────────────┐   │
│  │ 2026-05-18 0600 UTC        │   │  ← BriefingCard
│  │                             │   │
│  │ WEEKLY SITREP               │   │
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
└─────────────────────────────────────┘
```

### Briefing Detail Screen
```
┌─────────────────────────────────────┐
│  ⚠️ AI GENERATED - NOT OFFICIAL     │  ← Sticky disclaimer
├─────────────────────────────────────┤
│  ← SITREP          Share    ⋯       │  ← Header (back + actions)
│                                     │
│  2026-05-18 0600 UTC               │  ← Timestamp
│  WEEKLY INTELLIGENCE BRIEFING       │  ← Title
│                                     │
│  ┌─ ALL ─ MIDDLE EAST ─ INDO... ─┐ │  ← Region filter (optional)
│                                     │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓   │
│  ┃ BLUF                         ┃   │  ← BLUF Section
│  ┃ U.S.-Israel military...     ┃   │
│  ┃ Economic blockades...        ┃   │
│  ┃ ⏱ 8 min read                 ┃   │
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
│  │ 📰 Congressional Report...  │   │  ← SourceCitation
│  │    THE AVIATIONIST      →   │   │
│  ├─────────────────────────────┤   │
│  │ 📰 CENTCOM head calls...    │   │
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
│  │ ⚠️  IMPORTANT DISCLAIMER    │   │  ← Full legal disclaimer
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
│  ║  ⚠️ AI GENERATED CONTENT      ║  │
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
│  │ ⚠️  AI GENERATED CONTENT    │   │  ← Full-screen disclaimer
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

## INTERACTIONS & ANIMATIONS

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

## ACCESSIBILITY

### WCAG AA Compliance
- All text has 4.5:1 contrast ratio minimum
- Amber (#FFA500) on black (#000000): 7.5:1 ✅
- White (#FFFFFF) on black: 21:1 ✅
- Gray (#CCCCCC) on black: 12.6:1 ✅

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

## RESPONSIVE BREAKPOINTS

### Phone (Primary Target)
- iPhone: 375px - 428px width
- Android: 360px - 412px width
- Portrait orientation primary
- Landscape: Maintain vertical scroll

### Tablet (Future Consideration)
- iPad: Two-column layout (briefing list + detail)
- Android tablets: Material Design large screen patterns

---

## ICON SYSTEM

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

## PLATFORM-SPECIFIC NOTES

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

## MOCKUP APPROVAL CHECKLIST

- ✅ Color palette defined (military aesthetic: black + amber)
- ✅ Typography scale established
- ✅ Core components designed (BriefingCard, RegionTab, BLUF, PDFActionButton, etc.)
- ✅ Key screens wireframed (Home, Detail, About, Splash, **PDF Viewer**)
- ✅ **PDF generation & viewing** flow specified
- ✅ **PDF sharing/save actions** documented
- ✅ Heavy disclaimer placement confirmed (splash + sticky header + **PDF footer**)
- ✅ Region filtering UI specified
- ✅ Source citation format defined
- ✅ WCAG AA contrast ratios verified
- ✅ Touch target sizes meet platform guidelines
- ✅ Loading/error states documented
- ✅ Platform-specific considerations noted

---

## NEXT STEPS (FRONTEND APPROVED PHASE)

Once mockups approved:
1. Implement design system in NativeWind config
2. Build reusable component library
3. Create static screens with placeholder content
4. Test on iOS Simulator and Android Emulator
5. Capture screenshots for CONTRACT verification
