<script setup>
//scriptタグは問答無用で実行される
import io from "socket.io-client";
import { inject, onMounted, reactive, ref } from "vue";

const userName = inject("userName")
console.log(userName.value)

const socket = io()
socket.emit("enterEvent",`${userName.value}さんが入室しました。`)

const chatContent = ref("")
const chatList = reactive([])

onMounted(() => {
  registerSocketEvent()
})


// #region browser event handler
// 投稿メッセージをサーバに送信する
const onPublish = () => {
  socket.emit("publishEvent",`${userName.value}さん：${chatContent.value}`)
  chatContent.value =""// 入力欄を初期化

}

const onExit = () => {
  socket.emit("exitEvent", `${userName.value}さんが退出しました。`)
}

const onMemo = () => {
  chatList.unshift(`${userName.value}さんのメモ：${chatContent.value}`)
  chatContent.value=""
}

const onReceiveEnter = (data) => {
  chatList.unshift(data)
}

const onReceiveExit = (data) => {
  chatList.unshift(data)
}

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
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="text-h3 font-weight-medium">Vue.js Chat チャットルーム</h1>
    <div class="mt-10">
      <p>ログインユーザ：{{ userName }}さん</p>
      <textarea variant="outlined" placeholder="投稿文を入力してください" rows="4" class="area" v-model="chatContent"></textarea>
      <div class="mt-5">
        <button class="button-normal" @click="onPublish">投稿</button>
        <button class="button-normal util-ml-8px" @click="onMemo">メモ</button>
      </div>
      <div class="mt-5" v-if="chatList.length !== 0">
        <ul>
          <li class="chatitem" v-for="(chat, i) in chatList" :key="i">{{ chat }}</li><!--クラス変更有-->
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