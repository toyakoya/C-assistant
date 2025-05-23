import { defineStore } from "pinia";
import { ref } from "vue";
export const useLocalModelsStore = defineStore(
  "LocalModels",
  () => {
    const LocalModelItems = ref([]);
    const selectedLocalModel = ref("");

    // const doubleCount = computed(() => count.value * 2);
    // function increment() {
    // }

    return { LocalModelItems, selectedLocalModel };
  },
  {
    persist: true,
  }
);
