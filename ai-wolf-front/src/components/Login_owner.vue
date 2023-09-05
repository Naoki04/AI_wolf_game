<script setup>
import { inject, provide, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter()

const roomID = ref("")
provide("roomID", roomID)
const Password = ref("")
provide("Password", Password)

const userName = inject("userName")

//roomIDを6桁の数字を用いてランダムに発行する関数
function generateRandomNumber() {
  const min = 100000; // 最小値 (100000)
  const max = 999999; // 最大値 (999999)
  return Math.floor(Math.random() * (max - min + 1)) + min;
}
//passwordも同様に発行
function generateRandomPassword() {
  const charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+[]{}|;:,.<>?";
  let password = "";
  for (let i = 0; i < 8; i++) { // 長さを8文字に固定
    const randomIndex = Math.floor(Math.random() * charset.length);
    password += charset[randomIndex];
  }
  return password;
}


// 入室管理
const onEnter = () => {
    console.log(userName.value);
  // ユーザー名が入力されているかチェック
    if (userName.value.trim().replace("　","")===""){
        window.alert("エラー");
        return;
    };

    //roomIDを6桁の数字を用いてランダムに発行
    roomID = generateRandomNumber();
    console.log(roomID.value);

    //passwordも同様に発行
    // 8文字のランダムなパスワードを生成
    Password = generateRandomPassword();
    console.log(Password.value);
    //待合室に移動
    router.push({ name: "waiting_owner" })
    
}
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">オーナー登録</h1>
    <div class="mt-10">
      <p>ユーザー名</p>
      <input type="text" class="namearea" v-model="userName" />
    </div>
    <div>
        <p>参加人数(3~10)</p>
        <input type="number" class="namearea" min="3" max="10" />
    </div>
    <div>
        <p>ハックされた人数(推奨2人)</p>
        <input type="number" class="namearea" min="2" max="4" />
    </div>
    <button type="button" @click="onEnter" class="loginbtn loginbtn--shadow">ルームを作成</button>
  </div>
</template>

<style scoped>
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
