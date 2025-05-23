import { defineStore } from "pinia";
import { ref } from "vue";
export const useOnlineModelsStore = defineStore(
  "OnlineModels",
  () => {
    const OnlineModelItems = ref(["Deepseek-V3"]);
    const selectedOnlineModel = ref("");
    return { OnlineModelItems, selectedOnlineModel };
  },
  {
    persist: true,
  }
);
