/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
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
