/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    "./activities/templates/**/*.{html,js}",
  ],
  theme: {
    extend: {},
  },
  plugins: ["prettier-plugin-tailwindcss", require("daisyui")],
  daisyui: {
    themes: ["light"],
  },
};
