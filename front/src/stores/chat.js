import { defineStore } from "pinia";
import { ref } from "vue";
export const useChatStore = defineStore("Chat", () => {
  const ans = ref("");
  const chatHistory = ref([]);
  return { ans, chatHistory };
});
