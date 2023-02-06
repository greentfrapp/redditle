const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'title': ['Poppins', ...defaultTheme.fontFamily.sans],
        'sans': ['Arial', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        'light-blue': '#075DFF',
        'dark-blue': '#6591e6',
        'link-blue': '#0E00A8',
        'link-visited': '#b135ad',
        'link-visited-dark': '#c58af9',
      },
      boxShadow: {
        'around': '0 1px 3px 1px rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
      },
      maxWidth: {
        'screen': '100vw',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}