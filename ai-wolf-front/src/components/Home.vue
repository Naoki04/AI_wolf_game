<script setup>
import { useRouter } from "vue-router";
const router = useRouter()

const onOwner = () => {
  router.push({ name: "login_owner" })
}

const onUser = () => {
  router.push({ name: "login_user" })
}
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">AI狼(あいろう)</h1>
    <div class="mt-10">
        <button type="button" @click="onOwner" class="loginbtn loginbtn--shadow">オーナー(部屋を新しく作成する)</button>
    </div>
    <div>
        <button type="button" @click="onUser" class="loginbtn loginbtn--shadow">ユーザー（部屋を選んで入室する）</button>
    </div>
  </div>
</template>

<style scoped>
.user-name-text {
  width: 200px;
  border: 1px solid #888;
  margin-bottom: 16px;
}
</style>
