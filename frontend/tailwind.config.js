/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      colors: {
        primary: {
          50: '#e6f7f6',
          100: '#b3e8e5',
          200: '#80d9d4',
          300: '#4dcac3',
          400: '#2B7A78', // Main teal
          500: '#3AAFA9', // Soft cyan
          600: '#2B7A78',
          700: '#1f5a58',
          800: '#17252A', // Dark slate
          900: '#0f1a1c',
        },
        health: {
          teal: '#2B7A78',
          cyan: '#3AAFA9',
          slate: '#17252A',
          offwhite: '#FEFFFF',
        },
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

