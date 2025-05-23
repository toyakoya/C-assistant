<template>
  <v-app-bar scroll-behavior="collapse" :elevation="2">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template>

    <template v-slot:append>
      <v-btn icon="mdi-dots-vertical"></v-btn>
    </template>
    <v-app-bar-title>C语言助教系统</v-app-bar-title>
  </v-app-bar>
</template>
