# SITREP Mobile

React Native + Expo mobile application for SITREP intelligence briefing platform.

## Tech Stack

- **Framework**: React Native + Expo SDK 56
- **Language**: TypeScript (strict mode)
- **Navigation**: Expo Router (file-based routing)
- **Styling**: NativeWind (Tailwind CSS for React Native)
- **State**: TanStack Query + Zustand
- **PDF**: react-native-pdf

## Project Structure

```
mobile/
├── app/                    # Expo Router screens
│   ├── _layout.tsx        # Root layout with navigation
│   ├── index.tsx          # Home screen (briefing list)
│   ├── detail/[id].tsx    # Briefing detail screen
│   └── about.tsx          # About/disclaimer screen
├── components/            # Reusable UI components
│   ├── BriefingCard.tsx   # Briefing preview card
│   ├── RegionTab.tsx      # Region filter tabs
│   ├── BLUFSection.tsx    # BLUF highlighted section
│   ├── DisclaimerBanner.tsx # AI content warning
│   └── SourceCitation.tsx # Article source links
├── constants/             # Design system
│   └── tokens.ts          # Colors, typography, spacing
├── data/                  # Mock data
│   └── mockBriefings.ts   # Placeholder briefings
├── types/                 # TypeScript types
│   └── briefing.ts        # Briefing data models
├── app.json               # Expo configuration
├── tailwind.config.js     # NativeWind config
└── package.json           # Dependencies

## Quick Start

Install dependencies:
```bash
npm install
```

Start development server:
```bash
npm start
```

Run on specific platform:
```bash
npm run ios       # iOS Simulator
npm run android   # Android Emulator
npm run web       # Web browser
```

## Design System

**Color Palette**: Military aesthetic (AMOLED-optimized)
- True Black: `#000000`
- Amber Accent: `#FFA500`
- Gold: `#FFD700`

**Typography**:
- System fonts (SF Pro / Roboto)
- Monospace for timestamps/metadata

**Components**: See `/components` directory for full library

## Current Status

**Version**: v0.1.0  
**Gate**: Mobile Foundation ✅ COMPLETE

**What Works**:
- Dark military aesthetic UI
- Component library (5 core components)
- Expo Router navigation
- Mock data rendering
- Region filtering tabs

**Next**: Backend API integration (v0.2+)

## Bundle IDs

- **iOS**: `com.pcschmidt.sitrep`
- **Android**: `com.pcschmidt.sitrep`

## License

MIT - see [LICENSE](LICENSE)
