import { createWebHistory, createRouter } from "vue-router";
import Main from "@/components/Main.vue";
import Results from "@/components/Results.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Main,
  }, {
    path: "/search",
    name: "Search",
    component: Results,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;