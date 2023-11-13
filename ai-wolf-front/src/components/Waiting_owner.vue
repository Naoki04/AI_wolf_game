<script setup>
import { inject, ref, onBeforeUnmount, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';
//import { useClipboard } from 'vuetify';

const router = useRouter();
const roomID = inject("roomID");
const password = inject("password");
//console.log("roomID: ", roomID.value);
//console.log("password: ", password.value);
const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");
//同期的に処理を行うために、ref()を用いていた
let Current_mem = ref("");
let Members = ref("");
let GameState = ref("");

const onInformation = async () => {
  let response; // response を外部で宣言
  //console.log("ああああ")
  try {
    const data = {
      mode: 'get_room_info',
      data: {
        "room_id": Number(roomID.value),
      },
    };

    // POSTリクエストを送信
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // レスポンスを処理
    console.log('ステータスコード:', response.status);
    console.log('レスポンスデータ:', response.data);
  } catch (error) {
  // エラーハンドリング
    console.error('エラー:', error);
  }
  if (response) {
    Current_mem.value = response.data['room_info']['Current_mem'];
    Members.value = response.data['room_info']['Members'];
    GameState.value = response.data['room_info']['GameState'];
    console.log('現在の参加人数:', Current_mem.value);
    console.log('参加者:', Members.value);
    console.log('ゲームの状態:', GameState.value);
  }
};

let intervalId;

const stopUpdates = () => {
  // intervalIdをクリアしてsetIntervalを停止
  clearInterval(intervalId);
  router.push({ name: "home" });
};

onMounted(() => {
  // 初回のAPIリクエストを送信
  onInformation();
  // 3秒ごとにAPIリクエストを送信し、intervalIdを保持
  intervalId = setInterval(() => {
    onInformation();
    if (Current_mem.value === n_mem.value) {
      console.log("ゲーム開始");
      router.push({ name: "gaming_room", params: { roomID: roomID.value } });
    };
  }, 3000);
});

//このコードではintervalId変数を使用して
//setIntervalのIDを保持し
//コンポーネントがアンマウントされたときに
//onBeforeUnmountフック内でclearIntervalを使用してsetIntervalを停止しています。
//これにより、不要なリクエストの送信が停止されます。
onBeforeUnmount(() => {
  // コンポーネントがアンマウントされたときにintervalIdをクリアしてsetIntervalを停止
  clearInterval(intervalId);
});

const writeToClipboard = (text) => {
  navigator.clipboard.writeText(text).catch((e) => {
    console.error(e);
  });
};
</script>

<template>
  <v-app class="black-background">
    <v-container fluid>
      <v-row>
        <v-col cols="6">
          <v-row>
            <v-col class="mx-auto my-5 px-4">
              <h1 class="text-h3 font-weight-medium">ゲーム開始まで少々お待ちください。</h1>
            </v-col>
            <v-col cols="9">
              <p>ルームID: {{ roomID }}</p>
            </v-col>
            <v-col cols="1">
              <v-btn class="copy-btn" @click="writeToClipboard(roomID)">COPY</v-btn>
            </v-col>
            <v-col cols="9">
              <p>パスワード: {{ password }}</p>
            </v-col>
            <v-col cols="1">
              <v-btn class="copy-btn" @click="writeToClipboard(password)">COPY</v-btn>
            </v-col>
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
            <div>
              <button type="button" @click="stopUpdates" class="loginbtn loginbtn--shadow">部屋を削除する</button>
            </div>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>


<style scoped>
.black-background {
  background-color: black;
  color: white;
  height: 100vh;
  width: 100vw;
  /*display: flex;
  justify-content: center;
  align-items: center;*/
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
.copy-btn {
  size: 1px;
  background-color: #007bff;
  color: white;
  padding: 1px 1px;
  border: none;
  cursor: pointer;
  width: 100%;
}
.copy-btn--shadow {
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}
</style>