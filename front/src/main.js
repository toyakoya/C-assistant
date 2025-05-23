// Plugins
import { registerPlugins } from "@/plugins";
import router from "./router";
// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

const app = createApp(App);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

app.use(router);
app.use(pinia);
registerPlugins(app);

app.mount("#app");
