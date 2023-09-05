<script setup>
import { inject } from "vue";
import { useRouter } from "vue-router";

const userName = inject("userName")
const roomID = inject("roomID")
const Password = inject("Password")
const router = useRouter()
// 入室メッセージをクライアントに送信する
const onEnter = () => {
  console.log(userName.value);

  // ユーザー名が入力されているかチェック
  if (userName.value.trim().replace("　","")===""){
    window.alert("ニックネームを入力してください");
    return;
  };

  //未 DBを参照してroomIDが正しいかチェック
  // 部屋番号がか正しいチェック
  if (roomID.value===""){
    window.alert("roomIDを入力してください");
    return;
  };
  
  //未 DBを参照してPasswordが正しいかチェック
  //passwordが正しいかチェック
  if (Password.value===""){
    window.alert("パスワードが間違っています。");
    return;
  };

  router.push({ name: "waiting_room" })
}
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">ユーザー登録</h1>
    <div class="mt-10">
      <p>ユーザー名</p>
      <input type="text" class="namearea" v-model="userName"/>
    </div>
    <div>
      <p>部屋番号を入力</p>
      <input type="number" class="namearea" v-model="roomID"/>
    </div>
    <div>
      <p>パスワードを入力</p>
      <input type="text" class="namearea" v-model="Password"/>
    </div>
    <button type="button" @click="onEnter" class="loginbtn loginbtn--shadow">入室</button>
  </div>
</template>

<style scoped>
.user-name-text {
  width: 200px;
  border: 1px solid #888;
  margin-bottom: 16px;
}

.header {
  font-size: 24px;
}

.namearea {
  width: 200px;
  border: 1px solid #888;
  margin-bottom: 16px;
}

.loginbtn {
  /* スタイルを追加 */
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

.loginbtn--shadow {
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
