import { defineStore } from "pinia";
import { ref } from "vue";
export const useModelSelectStore = defineStore(
  "ModelSelect",
  () => {
    const Modelkind = ref("");
    return { Modelkind };
  },
  {
    persist: true,
  }
);
