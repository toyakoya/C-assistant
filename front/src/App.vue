<template>
  <v-layout class="rounded rounded-md border">
    <MyNavigationDrawer></MyNavigationDrawer>
    <MyAppBar></MyAppBar>
    <RouterView />
  </v-layout>
</template>
<script setup>
import MyNavigationDrawer from "./components/MyNavigationDrawer.vue";
import MyAppBar from "./components/MyAppBar.vue";
import MainPage from "./views/MainPage.vue";
import { RouterLink, RouterView } from "vue-router";
</script>
