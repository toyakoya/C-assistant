import { defineStore } from "pinia";
import { ref } from "vue";
export const useProblemInfStore = defineStore(
  "ProblemInf",
  () => {
    const examples = ref([]);
    const website = ref("");

    const problem = ref("");
    const code = ref("");
    const inputMessage = ref("");
    const runResult = ref("");
    const cookies = ref("");
    return {
      examples,
      website,
      cookies,
      problem,
      code,
      inputMessage,
      runResult,
    };
  },
  {
    persist: true,
  }
);
