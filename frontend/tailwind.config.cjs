const path = require("path");
module.exports = {
  content: [
    path.join(__dirname, "../**/templates/**/*.html"),
    path.join(__dirname, "../**/templates/**/*.htm"),
    path.join(__dirname, "../**/*.js"),
    path.join(__dirname, "../**/*.ts"),
    // Add Flowbite's JS so tailwind scans its markup/classes:
    path.join(__dirname, "node_modules/flowbite/**/*.js"),
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#0275ff", // bg-brand
          strong: "#0055cc", // bg-brand-strong
          medium: "#99c7ff", // ring-brand-medium
        },
      },
      borderRadius: {
        base: "0.5rem", // generates rounded-base
      },
      boxShadow: {
        xs: "0 0 0 1px rgba(0,0,0,0.05)", // generates shadow-xs
      },
    },
  },
  plugins: [],
  // You are not using daisyui now; leave plugins empty unless you keep it.
};
