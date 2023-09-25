<script setup>
import { inject, ref } from 'vue';
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();
const roomID = inject("roomID");
const password = inject("password");

const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");
let Current_mem = ref();
let Members = ref();

const roomInfo = ref(null);

const sendRequest = async () => {
  try {
    const requestData = {
      mode: 'get_room_info',
      data: {
        room_id: 290912,
      },
    };

    const response = await axios.post('https://your-api-url.com/your-endpoint', requestData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // レスポンスデータを取得
    const responseData = response.data;

    // レスポンスデータを処理
    if (response.status === 200 && responseData.statusCode === 200) {
      roomInfo.value = responseData.body.room_info;
    } else {
      console.error('エラーレスポンス:', responseData);
    }
  } catch (error) {
    console.error('エラー:', error);
  }
};

// リクエストを送信する関数を呼び出すためのトリガーを定義
const requestButtonClicked = () => {
  sendRequest();
};
</script>

<template>
  <button @click="requestButtonClicked">リクエスト送信</button>
  <div class="mx-auto my-5 px-4">
    <h1 class="text-h3 font-weight-medium">オーナー待機室</h1>
  </div> 
  <div class="mx-auto my-5 px-4">
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>ルームID: {{ roomID }}です。</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>パスワード: {{ password }}です。</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>メンバー数: {{ n_mem }}人</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>ハックされた人数: {{ n_hacked }}人</p>
    </div>
    <div>
      <p>参加者予定数：{{ n_mem }}</p>
      <p>現在の参加者数：{{ Current_mem }}</p>
      <p>参加者：{{ Members }}</p>
    </div>
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