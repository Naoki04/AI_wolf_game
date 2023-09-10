<script setup>
import { ref, inject } from 'vue';
import axios from 'axios';
// レスポンスデータを保持するリファレンス
const responseData = ref(null);
const responseStatus = ref(null);

const User_input_username = inject("User_input_username");
const User_input_room_id = inject("User_input_room_id");

// APIリクエストを送信する関数
const onLeave = async () => {
  let response; // response を外部で宣言

  try {
    const data = {
      mode: 'leave_room',
      data: {
        "room_id": Number(User_input_room_id.value),
        "user_name": User_input_username.value,
      }
    };
    console.log(data);
    
    // POSTリクエストを送信
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // レスポンスを処理
    responseStatus.value = response.status;
    responseData.value = response.data;
  } catch (error) {
    // エラーハンドリング
    console.error('エラー:', error);
  }
};
</script>


<template>
  <div class="mx-auto my-5 px-4">
    <p class="text-h3 font-weight-medium">オーナーがゲームを開始するまで少々お待ちください。</p>
  </div>
  <div>    
    <!-- ボタンをクリックしてAPIリクエストを送信 -->
    <button type="button" @click="onLeave" class="loginbtn loginbtn--shadow">待機室を出る</button>
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