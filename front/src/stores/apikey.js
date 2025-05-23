import { defineStore } from "pinia";
import { ref } from "vue";
export const useApikeyStore = defineStore(
  "apikey",
  () => {
    const apikey = ref("");
    return { apikey };
  },
  {
    persist: true,
  }
);
