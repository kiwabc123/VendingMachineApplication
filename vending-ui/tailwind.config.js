/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cafe: {
          bg: "#FFEAC5",
          surface: "#FFDDB8",
          primary: "#6B4A2E",
          text: "#4A321E",
          muted: "#9C7A5A",

          success: "#8BC34A",
          danger: "#E57373",
        },
      },
      boxShadow: {
        soft: "0 4px 12px rgba(0,0,0,0.08)",
      },
      borderRadius: {
        xl: "1rem",
      },
      fontFamily: {
        heading: ["Playfair Display", "serif"],
        body: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}
