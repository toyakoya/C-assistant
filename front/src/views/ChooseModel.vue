<template>
  <v-main class="d-flex align-center justify-center">
    <v-container>
      <v-form>
        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-select
              label="本地大模型"
              :items="LocalModelsStore.LocalModelItems"
              v-model="LocalModelsStore.selectedLocalModel"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            :disabled="ModelSelectStore.Modelkind === '本地大模型'"
            @click="
              () => {
                ModelSelectStore.Modelkind = '本地大模型';
              }
            "
          >
            {{ ModelSelectStore.Modelkind === "本地大模型" ? "锁定" : "确认" }}
          </v-btn>
        </v-row>

        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-select
              label="线上大模型"
              :items="OnlineModelsStore.OnlineModelItems"
              v-model="OnlineModelsStore.selectedOnlineModel"
            ></v-select>
          </v-col>
        </v-row>

        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-text-field
              hide-details="auto"
              type="input"
              label="apikey"
              v-model="ApikeyStore.apikey"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            :disabled="ModelSelectStore.Modelkind === '线上大模型'"
            @click="
              () => {
                ModelSelectStore.Modelkind = '线上大模型';
              }
            "
          >
            {{ ModelSelectStore.Modelkind === "线上大模型" ? "锁定" : "确认" }}
          </v-btn>
        </v-row>
      </v-form>
    </v-container>
  </v-main>
</template>
<script setup>
import { getModels } from "@/services/apiChooseModels";
import { onMounted, ref } from "vue";
import { useLocalModelsStore } from "@/stores/localModels";
import { useOnlineModelsStore } from "@/stores/onlineModels";
import { useModelSelectStore } from "@/stores/ModelSelect";
import { useApikeyStore } from "@/stores/apikey";

const LocalModelsStore = useLocalModelsStore();
const OnlineModelsStore = useOnlineModelsStore();
const ModelSelectStore = useModelSelectStore();
const ApikeyStore = useApikeyStore();
onMounted(async () => {
  OnlineModelsStore.OnlineModelItems = ref(["Deepseek-V3"]);
  OnlineModelsStore.selectedOnlineModel = ref("");
  ModelSelectStore.Modelkind = "";
  try {
    const data = await getModels();
    if (data && data.length > 0) {
      LocalModelsStore.LocalModelItems = data;
    } else {
      console.warn("getModels returned empty data");
    }
  } catch (error) {
    console.error("Failed to fetch models:", error);
  }
});
</script>
