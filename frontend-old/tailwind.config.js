/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        inter: ["Inter", "sans-serif"],
      },
      colors: {
        "horizon-blue": "#1e3a8a",
        "horizon-light": "#3b82f6",
      },
    },
  },
  plugins: [],
};
