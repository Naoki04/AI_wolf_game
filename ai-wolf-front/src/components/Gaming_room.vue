<script setup>
//import CenterChat from './CenterChat.vue';
//import Cards from './Cards.vue';
//import Timer from './Timer.vue';
//import Chat from './Chat.vue';
//import UserList from './UserList.vue';


import { ref } from 'vue';
</script>

<template>
  <v-container class="mt-15">
    <v-row>
      <v-col cols="3" class="mt-10">
        <Cards />
      </v-col>
      <v-col cols="6">
        <CenterChat />
      </v-col>
      <v-col cols="3" class="mt-5 pa-5">
        <Timer class="mb-10" />
        <UserList />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped></style>
