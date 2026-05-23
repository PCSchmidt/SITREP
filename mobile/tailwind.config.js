/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        // Background colors
        'true-black': '#000000',
        'near-black': '#0A0A0A',
        'card-bg': '#121212',
        'border': '#1A1A1A',

        // Accent colors
        'amber': '#FFA500',
        'gold': '#FFD700',
        'warning': '#FF4444',
        'success': '#00FF41',

        // Text colors
        'text-heading': '#FFFFFF',
        'text-body': '#CCCCCC',
        'text-subtle': '#888888',

        // Semantic region colors
        'region-middle-east': '#FF6B6B',
        'region-indo-pacific': '#4ECDC4',
        'region-europe-africa': '#95E1D3',
        'region-western-hemisphere': '#F38181',
      },
      fontFamily: {
        'mono': ['SF Mono', 'Roboto Mono', 'monospace'],
      },
      fontSize: {
        'h1': ['28px', { lineHeight: '1.2', letterSpacing: '-0.5px', fontWeight: '700' }],
        'h2': ['20px', { lineHeight: '1.3', letterSpacing: '-0.3px', fontWeight: '600' }],
        'h3': ['16px', { lineHeight: '1.4', letterSpacing: '0px', fontWeight: '600' }],
        'body': ['15px', { lineHeight: '1.6', fontWeight: '400' }],
        'caption': ['12px', { lineHeight: '1.4', letterSpacing: '0.5px', fontWeight: '400' }],
        'label': ['14px', { lineHeight: '1.2', letterSpacing: '0.8px', fontWeight: '600' }],
      },
      spacing: {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
      },
      borderRadius: {
        'DEFAULT': '8px',
      },
    },
  },
  plugins: [],
}
