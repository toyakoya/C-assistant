<template>
  <v-main class="d-flex align-center justify-center">
    <v-container>
      <v-form>
        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-text-field
              hide-details="auto"
              type="input"
              label="网址"
              v-model="problemInfStore.website"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-text-field
              hide-details="auto"
              type="input"
              label="cookies"
              v-model="problemInfStore.cookies"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            @click="getWebsite"
          >
            自动获取
          </v-btn>
        </v-row>

        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-textarea
              hide-details="auto"
              label="题目"
              :auto-grow="true"
              v-model="problemInfStore.problem"
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-textarea
              hide-details="auto"
              label="代码"
              :auto-grow="true"
              v-model="problemInfStore.code"
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-select
              label="运行结果"
              :items="['AC', 'WA', 'TLE', 'RE', 'MLE']"
              v-model="problemInfStore.runResult"
            ></v-select>
          </v-col>
        </v-row>

        <!-- 表格输入 -->
        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-table class="mx-auto">
              <thead>
                <tr>
                  <th>样例输入</th>
                  <th>样例输出</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(row, index) in problemInfStore.examples"
                  :key="index"
                >
                  <td>
                    <v-textarea
                      v-model="row.input"
                      label="输入"
                      hide-details="auto"
                      :auto-grow="true"
                    ></v-textarea>
                  </td>
                  <td>
                    <v-textarea
                      v-model="row.output"
                      label="输出"
                      hide-details="auto"
                      :auto-grow="true"
                    ></v-textarea>
                  </td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            @click="addsample"
          >
            添加样例
          </v-btn>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            @click="deletesample"
          >
            删除样例
          </v-btn>
        </v-row>
        <v-row>
          <v-btn
            style="margin-left: auto; margin-right: auto"
            @click="startAssist"
          >
            开始
          </v-btn>
        </v-row>
        <v-row justify="center" align="center" class="text-center fill-height">
          <v-col>
            <v-textarea
              hide-details="auto"
              label="回答"
              :auto-grow="true"
              v-model="ChatStore.ans"
            ></v-textarea>
          </v-col>
        </v-row>
        <v-row v-for="(message, index) in ChatStore.chatHistory" :key="index">
          <v-col>
            <v-textarea
              v-model="message.content"
              :label="message.role"
              hide-details="auto"
              :auto-grow="true"
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-textarea
              hide-details="auto"
              :auto-grow="true"
              v-model="problemInfStore.inputMessage"
              placeholder="输入消息..."
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row>
          <v-btn style="margin-left: auto; margin-right: auto" @click="askmore">
            追问
          </v-btn>
        </v-row>
      </v-form>
    </v-container>
  </v-main>
</template>
<script setup>
import { useProblemInfStore } from "@/stores/problemInf";
import { useModelSelectStore } from "@/stores/ModelSelect";
import { useOnlineModelsStore } from "@/stores/onlineModels";
import { useLocalModelsStore } from "@/stores/localModels";
import { useApikeyStore } from "@/stores/apikey";
import { useChatStore } from "@/stores/chat";
import { LocalSolve } from "@/services/apiLocalSolve";
import { OnlineSolve } from "@/services/apiOnlineSolve";
import { LocalChat } from "@/services/apiLocalChat";
import { OnlineChat } from "@/services/apiOnlineChat";
import { GetProblem } from "@/services/apiGetProblem";
const problemInfStore = useProblemInfStore();
const ModelSelectStore = useModelSelectStore();
const OnlineModelsStore = useOnlineModelsStore();
const LocalModelsStore = useLocalModelsStore();
const ApikeyStore = useApikeyStore();
const ChatStore = useChatStore();
function addsample() {
  problemInfStore.examples.push({ input: "", output: "" });
}
function deletesample() {
  if (problemInfStore.examples.length > 0) {
    problemInfStore.examples.pop();
  } else {
    alert("没有更多样例可以删除");
  }
}
async function getWebsite() {
  const url = problemInfStore.website;
  const cookies = problemInfStore.cookies;
  if (url === "") {
    alert("请输入网址");
    return;
  }
  if (cookies === "") {
    alert("请输入cookies");
    return;
  }
  const response = await GetProblem(url, cookies);

  console.log("获取到的数据：", response);
  if (response) {
    problemInfStore.problem = response.problem_text;
    problemInfStore.examples = response.examples;
    problemInfStore.code = response.code;
  } else {
    alert("获取数据失败，请检查网址或网络连接");
  }
}
async function askmore() {
  if (problemInfStore.inputMessage === "") {
    alert("请输入消息");
    return;
  }
  if (ChatStore.ans === "") {
    alert("请先点击开始，生成第一次回答");
    return;
  }
  if (ChatStore.chatHistory.length > 5) {
    alert("追问已达上限，请重新开始");
    return;
  }
  const payload = {
    website: problemInfStore.website,
    // problem: problemInfStore.problem,
    // code: problemInfStore.code,
    // runResult: problemInfStore.runResult,
    // examples: problemInfStore.examples,
    // ans: ChatStore.ans,
    inputMessage: problemInfStore.inputMessage,
    // messages: ChatStore.chatHistory,
  };

  console.log("准备发送的数据：", payload);

  if (ModelSelectStore.Modelkind === "本地大模型") {
    const model = LocalModelsStore.selectedLocalModel;
    ChatStore.chatHistory.push({
      role: "user",
      content: problemInfStore.inputMessage,
    });
    problemInfStore.inputMessage = "";
    const ans = await LocalChat(model, payload);
    ChatStore.chatHistory.push({
      role: "assistant",
      content: ans.response,
    });
    console.log(ans.response);
  } else if (ModelSelectStore.Modelkind === "线上大模型") {
    const model = {
      modelName: OnlineModelsStore.selectedOnlineModel,
      apikey: ApikeyStore.apikey,
    };

    ChatStore.chatHistory.push({
      role: "user",
      content: problemInfStore.inputMessage,
    });
    problemInfStore.inputMessage = "";
    const ans = await OnlineChat(model, payload);
    ChatStore.chatHistory.push({
      role: "assistant",
      content: ans,
    });
  } else {
    console.error("请选择要使用的模型");
    return;
  }
}
async function startAssist() {
  // 将 problemInfStore 的状态合成 JSON
  const payload = {
    website: problemInfStore.website,
    problem: problemInfStore.problem,
    code: problemInfStore.code,
    runResult: problemInfStore.runResult,
    examples: problemInfStore.examples,
    // inputMessage: problemInfStore.inputMessage,
    // messages: problemInfStore.messages,
  };

  console.log("准备发送的数据：", payload);
  ChatStore.chatHistory = [];
  ChatStore.ans = "";
  if (ModelSelectStore.Modelkind === "本地大模型") {
    const model = LocalModelsStore.selectedLocalModel;
    const ans = await LocalSolve(model, payload);
    ChatStore.ans = ans.response;
    console.log(ans.response);
  } else if (ModelSelectStore.Modelkind === "线上大模型") {
    const model = {
      modelName: OnlineModelsStore.selectedOnlineModel,
      apikey: ApikeyStore.apikey,
    };
    const ans = await OnlineSolve(model, payload);
    ChatStore.ans = ans;
    console.log("使用线上大模型进行处理");
  } else {
    console.error("请选择要使用的模型");
    return;
  }
}
</script>
<style scoped>
.user {
  background-color: #e0f7fa;
  margin-bottom: 10px;
}
.assistant {
  background-color: #ffe0b2;
  margin-bottom: 10px;
}
.v-textarea {
  margin-bottom: 10px;
}
</style>
