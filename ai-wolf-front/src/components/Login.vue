<script setup>
import io from "socket.io-client";
import { inject } from "vue";
import { useRouter } from "vue-router";

const userName = inject("userName")

const router = useRouter()
const socket = io()

// 入室メッセージをクライアントに送信する
const onEnter = () => {
  console.log(userName.value);
  // ユーザー名が入力されているかチェック
  if (userName.value.trim().replace("　","")===""){
    window.alert("エラー");
    return;
  };

  // 入室メッセージを送信

  // 全体で使用するnameに入力されたユーザー名を格納

  // チャット画面へ遷移
  router.push({ name: "chat" })
}
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">Vue.js Chat サンプル</h1>
    <div class="mt-10">
      <p>ユーザー名</p>
      <input type="text" class="namearea" v-model="userName"/>
    </div>
    <button type="button" @click="onEnter" class="loginbtn loginbtn--shadow">入室する</button>
  </div>
</template>

<style scoped>
.user-name-text {
  width: 200px;
  border: 1px solid #888;
  margin-bottom: 16px;
}
</style>
