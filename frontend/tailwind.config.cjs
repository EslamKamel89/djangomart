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
  plugins: [],
  // You are not using daisyui now; leave plugins empty unless you keep it.
};
