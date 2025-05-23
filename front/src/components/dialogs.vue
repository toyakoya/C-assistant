<template>
  <div class="chat-container">
    <div class="chat-messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.role]"
      >
        <div class="message-content">{{ message.content }}</div>
      </div>
    </div>
    <div class="chat-input">
      <input v-model="inputMessage" placeholder="输入消息..." />
      <!-- <button @click="sendMessage">发送</button> -->
      <button></button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const messages = ref([]);
const inputMessage = ref("");
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.chat-messages {
  height: 500px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
}
.message {
  margin-bottom: 10px;
}
.message.user {
  text-align: right;
}
.message.assistant {
  text-align: left;
}
.message-content {
  display: inline-block;
  padding: 10px;
  border-radius: 5px;
  background-color: #f1f1f1;
}
.chat-input {
  display: flex;
}
.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.chat-input button {
  margin-left: 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
