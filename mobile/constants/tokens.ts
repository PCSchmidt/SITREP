/**
 * SITREP Design System Tokens
 * Military intelligence aesthetic - AMOLED optimized
 */

export const Colors = {
  // Background
  trueBlack: '#000000',
  nearBlack: '#0A0A0A',
  cardBg: '#121212',
  border: '#1A1A1A',

  // Accent
  amber: '#FFA500',
  gold: '#FFD700',
  warning: '#FF4444',
  success: '#00FF41',

  // Text
  textHeading: '#FFFFFF',
  textBody: '#CCCCCC',
  textSubtle: '#888888',

  // Semantic regions
  regionMiddleEast: '#FF6B6B',
  regionIndoPacific: '#4ECDC4',
  regionEuropeAfrica: '#95E1D3',
  regionWesternHemisphere: '#F38181',
} as const;

export const Typography = {
  h1: {
    fontSize: 28,
    fontWeight: '700' as const,
    letterSpacing: -0.5,
    lineHeight: 34,
  },
  h2: {
    fontSize: 20,
    fontWeight: '600' as const,
    letterSpacing: -0.3,
    lineHeight: 26,
  },
  h3: {
    fontSize: 16,
    fontWeight: '600' as const,
    letterSpacing: 0,
    lineHeight: 22,
  },
  body: {
    fontSize: 15,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    letterSpacing: 0.5,
    lineHeight: 17,
  },
  label: {
    fontSize: 14,
    fontWeight: '600' as const,
    letterSpacing: 0.8,
    lineHeight: 17,
  },
} as const;

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  '2xl': 32,
} as const;

export const BorderRadius = {
  default: 8,
  sm: 4,
  lg: 12,
} as const;

export const Regions = [
  { id: 'all', label: 'ALL', color: Colors.textHeading },
  { id: 'middle-east', label: 'MIDDLE EAST', color: Colors.regionMiddleEast },
  { id: 'indo-pacific', label: 'INDO-PACIFIC', color: Colors.regionIndoPacific },
  { id: 'europe-africa', label: 'EUROPE/AFRICA', color: Colors.regionEuropeAfrica },
  { id: 'western-hemisphere', label: 'W. HEMISPHERE', color: Colors.regionWesternHemisphere },
] as const;
