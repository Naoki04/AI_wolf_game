<script setup>
  import { provide, ref } from "vue"
  const userName = ref("")
  provide("userName", userName)
</script>

<template>
    <router-view />
</template>

<style scoped>
</style>