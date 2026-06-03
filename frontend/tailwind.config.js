/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        coffee: {
          50: '#fff7ed',
          100: '#f5eadc',
          200: '#ead2bb',
          300: '#d6aa7f',
          400: '#c27a3f',
          500: '#8b5a3c',
          600: '#6f432b',
          700: '#4b2f22',
          800: '#2f2018',
          900: '#211611',
        },
        leaf: {
          500: '#2f8f46',
          600: '#23733a',
        },
      },
      boxShadow: {
        hard: '4px 4px 0 #2f2018',
        'hard-lg': '6px 6px 0 #2f2018',
      },
      borderWidth: {
        3: '3px',
      },
      fontFamily: {
        sans: ['Be Vietnam Pro', 'Noto Sans', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
