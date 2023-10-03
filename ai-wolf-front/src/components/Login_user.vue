<script setup>
import { ref, reactive, inject } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const User_input_room_id = inject("User_input_room_id");
const User_input_password = inject("User_input_password");
const User_input_username = inject("User_input_username");

// エラー情報を格納するための変数
const error = ref('');
const errorDetails = reactive({});

const onEnter_user = async () => {
  // ユーザー名が入力されているかチェック
  if (User_input_username.value.trim().replace("　", "") === "") {
    window.alert('ニックネームを入力してください');
    return;
  }
  
  try {
    const data = {
      mode: 'join_room',
      data: {
        "room_id": Number(User_input_room_id.value),
        "password": User_input_password.value,
        "user_name": User_input_username.value,
      },
    };
    console.log(data);

    // POSTリクエストを送信
    const response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    // レスポンスを処理
    console.log('ステータスコード:', response.status);
    console.log('レスポンスデータ:', response.data);

    if (response.data['message'] === 'OK') {
      router.push({ name: 'waiting_user', params: { roomID: User_input_room_id.value } });
    } else {
      console.error('エラー:', response.data['message']);
      // エラー内容を表示させるなどの処理を追加することができます
      error.value = response.data['message'];
      errorDetails.error = response.data; // エラーの詳細情報をerrorDetailsオブジェクトに設定
    }
  } catch (error) {
    // エラーハンドリング
    console.error('エラー:', error.message);
    // エラー内容を表示させるなどの処理を追加する
    error.value = error.message;
    errorDetails.error = error.response ? error.response.data : null; // エラーの詳細情報をerrorDetailsオブジェクトに設定
    console.log(errorDetails.error);
    console.log(errorDetails.error['message']);
  };
};
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">ユーザー登録</h1>
    <div class="mt-10">
      <p>ユーザー名</p>
      <input type="text" class="namearea" v-model="User_input_username" />
    </div>
    <div>
        <p>roomID</p>
        <input type="numver" class="namearea" v-model="User_input_room_id" />
    </div>
    <div>
        <p>Password</p>
        <input type="text" class="namearea" v-model="User_input_password"/>
    </div>
    <button type="button" @click="onEnter_user" class="loginbtn loginbtn--shadow">ルームに入る</button>
    <p v-if="errorDetails.error" class="error-msg">※{{ errorDetails.error['message'] }}</p>
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
.container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}

.button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error-message {
  color: #ff0000;
  margin-top: 10px;
}

.error-details {
  margin-top: 10px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
}
.error-msg{
  color: #ff0000;
  margin-top: 10px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  /*border: 1px solid #888;*/
  margin-bottom: 16px;
  width: 200px;
}
</style>
