<script setup>
import io from "socket.io-client";
import { inject, onMounted, reactive, ref } from "vue";

const Owner_input_username = inject("Owner_input_username");
const User_input_room_id = inject("User_input_room_id");
const User_input_username = inject("User_input_username");
const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");

console.log(Owner_input_username.value);
console.log(User_input_room_id.value);
console.log(User_input_username.value);
console.log(n_mem.value);
console.log(n_hacked.value);

const roomID = inject("roomID");
const password = inject("password");
console.log(roomID);
console.log(password);

const socket = io()
socket.emit("enterEvent",`${User_input_username.value}さんが入室しました。`)
const chatContent = ref("")
const chatList = reactive([])

onMounted(() => {
  registerSocketEvent()
})

// 投稿メッセージをサーバに送信する
const onPublish = () => {
  socket.emit("publishEvent",`${User_input_username.value}さん：${chatContent.value}`)
  socket.emit("publishEvent",`${Owner_input_username.value}さん：${chatContent.value}`)
  chatContent.value =""
}


// 退室メッセージをサーバに送信する
const onExit = () => {
  socket.emit("exitEvent", `${User_input_username.value}さんが退出しました。`)
}

// サーバから受信した入室メッセージ画面上に表示する
const onReceiveEnter = (data) => {
  chatList.unshift(data)
}

// サーバから受信した退室メッセージを受け取り画面上に表示する
const onReceiveExit = (data) => {
  chatList.unshift(data)
}

// サーバから受信した投稿メッセージを画面上に表示する
const onReceivePublish = (data) => {
  chatList.unshift(data)
}
// イベント登録をまとめる
const registerSocketEvent = () => {
  // 入室イベントを受け取ったら実行
  socket.on("enterEvent", (data) => {
    onReceiveEnter(data);
  })

  // 退室イベントを受け取ったら実行
  socket.on("exitEvent", (data) => {
    onReceiveExit(data);
  })

  // 投稿イベントを受け取ったら実行
  socket.on("publishEvent", (data) => {
    onReceivePublish(data);
  })
}
// #endregion
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="text-h3 font-weight-medium">Vue.js Chat チャットルーム</h1>
    <div class="mt-10">
      <p>ログインユーザ：{{ Owner_input_username }}さん</p>
      <textarea variant="outlined" placeholder="投稿文を入力してください" rows="4" class="area" v-model="chatContent"></textarea>
      <div class="mt-5">
        <button class="button-normal" @click="onPublish">投稿</button>
      </div>
      <div class="mt-5" v-if="chatList.length !== 0">
        <ul>
          <li class="item mt-4" v-for="(chat, i) in chatList" :key="i">{{ chat }}</li>
        </ul>
      </div>
    </div>
    <router-link to="/" class="link">
      <button type="button" class="button-normal button-exit" @click="onExit">退室する</button>
    </router-link>
  </div>
</template>

<style scoped>
.link {
  text-decoration: none;
}

.area {
  width: 500px;
  border: 1px solid #000;
  margin-top: 8px;
}

.item {
  display: block;
}

.util-ml-8px {
  margin-left: 8px;
}

.button-exit {
  color: #000;
  margin-top: 8px;
}
</style>