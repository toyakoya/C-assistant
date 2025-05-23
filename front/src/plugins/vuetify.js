/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */
import "@mdi/font/css/materialdesignicons.css";
import { createVuetify } from "vuetify";

export default createVuetify({
  icons: {
    defaultSet: "mdi", // This is already the default value - only for display purposes
  },
});
