import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/MainPage.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/model",
      name: "model",
      component: () => import("../views/ChooseModel.vue"),
    },
  ],
});
export default router;
