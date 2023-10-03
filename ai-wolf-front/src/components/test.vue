<script setup>
import io from "socket.io-client";
import { inject, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();
const Owner_input_username = inject("Owner_input_username");
const User_input_username = inject("User_input_username");
console.log("Owner_input_username: ", Owner_input_username.value);
console.log("User_input_username: ", User_input_username.value);

const roomID = inject("roomID");
//console.log("ルームID", roomID.value);

const socket = io()
if (User_input_username.value !== '') {
    socket.emit("publishEvent",`${User_input_username.value}さんが入室しました。`)
  }
else if (Owner_input_username.value !== '') {
    socket.emit("publishEvent",`${Owner_input_username.value}さんが入室しました。`)
}



//get_room_infoで取得した値を格納する変数
let Created_at = ref("");
const N_mem = ref("");
const Current_mem = ref("");
const Members = ref("");
const N_hacked = ref("");
const Hacked = ref("");
let Dead = ref("");
let GameState = ref("");

let Dead_user = ref("");
let Hacked_username = ref("");
let question = ref("");
let AI_answer = ref("");

const onInformation = async () => {
  let response; // response を外部で宣言
  console.log("ああああ")
  try {
    const data = {
      mode: 'get_room_info',
      data: {
        "room_id": Number(roomID.value),
      },
    };
    console.log(data)
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
    Created_at.value = response.data['room_info']['Created-at']
    N_mem.value = response.data['room_info']['N_mem']
    Current_mem.value = response.data['room_info']['Current_mem'];
    Members.value = response.data['room_info']['Members'];
    N_hacked.value = response.data['room_info']['N_hacked']
    Hacked.value = response.data['room_info']['Hacked']
    Dead.value = response.data['room_info']['Dead']
    GameState.value = response.data['room_info']['GameState']
    console.log('作成日時:', Created_at.value);
    console.log('参加人数:', N_mem.value);
    console.log('現在の参加人数:', Current_mem.value);
    console.log('参加者リスト:', Members.value);
    console.log('Hackedの人数:', N_hacked.value);
    console.log('Hackedリスト:', Hacked.value);
    console.log('死亡者リスト:', Dead.value);
    console.log('ゲームの状態:', GameState.value);
  }
};

onMounted(() => {
  onInformation();
  registerSocketEvent();
})

const onStart = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'start_game',
      data: {
        room_id: Number(roomID.value), // 入力された部屋IDを整数に変換
        owner_name: Owner_input_username.value, // 自分(オーナー)のユーザー名
        n_hacked: Number(N_hacked.value), // Hackedの人数
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
    // レスポンスデータから必要な情報を抽出
    // 以下は例です。実際のデータ構造に合わせて変更してください。
    console.log("ゲーム開始")
    Hacked.value = response.data['Hacked'];
    console.log('Hackedリスト:', Hacked.value);
    console.log("Hackedされた人は", N_hacked.value)  
  }
};

const onEnd = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'end_room',
      data: {
        room_id: Number(roomID.value), // 入力された部屋IDを整数に変換
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
  //if (response) {
  //  // レスポンスデータから必要な情報を抽出
  //  // 以下は例です。実際のデータ構造に合わせて変更してください。
  //}
};


const onGetAiAnswer = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'get_ai_answer',
      data: {
        room_id: Number(roomID.value), // 入力された部屋IDを整数に変換
        user_name: Hacked_username.value, //Hackedのユーザー名
        question: question.value,//全体に質問する内容
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
    AI_answer = response.data['answer'];
    console.log('AIの回答:', AI_answer);
  }
};


const onAddDead = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'add_dead',
      data: {
        room_id: Number(roomID.value), // 入力された部屋IDを整数に変換
        user_name: Dead_user.value, // 死亡したユーザー名
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
  //if (response) {
  //  //Dead_userを表示する
  //}
  Dead_user.value = input()
};

// 投稿メッセージをサーバに送信する
const onPublish = () => {
  if (User_input_username.value !== '') {
    socket.emit("publishEvent",`${User_input_username.value}さん：${chatContent.value}`)
  }
  else if (Owner_input_username.value !== '') {
    socket.emit("publishEvent",`${Owner_input_username.value}さん：${chatContent.value}`)
  }
  chatContent.value =""
}

// 退室メッセージをサーバに送信する
const onExit = () => {
  router.push({ name: "home" })
  onInformation()
  socket.emit("exitEvent", `${User_input_username.value}さんが退出しました。`)
}

// サーバから受信した入室メッセージ画面上に表示する
//const onReceiveEnter = (data) => {
//  //chatList.unshift(data)
//  chatList.push(data)
//}
// サーバから受信した退室メッセージを受け取り画面上に表示する
//const onReceiveExit = (data) => {
//  //chatList.unshift(data)
//  chatList.push(data)
//}
// サーバから受信した投稿メッセージを画面上に表示する
const onReceivePublish = (data) => {
  //chatList.unshift(data)
  chatList.push(data)
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
};

const onClose = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'close_room',
      data: {
        room_id: Number(roomID.value), // 入力された部屋IDを整数に変換
        owner_name: Owner_input_username.value, // 自分(オーナー)のユーザー名
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
  //if (response) {
  //}
  router.push({ name: "home" });
};

const chatContent = ref("")
const chatList = reactive([])
//const isMemoDrawerOpen = ref(false);
const isRoomInfoDrawerOpen = ref(false);
//const onInformationUpdate = () => {
//  onInformation();
//};
const toggleDrawer = () => {
  isRoomInfoDrawerOpen.value = !isRoomInfoDrawerOpen.value;
};

</script>


<template>
  <v-app>
    <!-- ヘッダー -->
    <v-app-bar app dark color="primary">
      <!-- ハンバーガーメニューボタン -->
      <v-btn icon @click="toggleDrawer">
        <v-icon>mdi-menu</v-icon>
      </v-btn>
      <v-toolbar-title>AI狼</v-toolbar-title>
      <div class="header-right">
        <p v-if="Owner_input_username !== ''">ログインユーザ：{{ Owner_input_username }}さん</p>
        <p v-else-if="User_input_username !==''">ログインユーザ：{{ User_input_username }}さん</p>
        <p v-else>ログインユーザがいません。</p>
      </div>
    </v-app-bar>
    <!-- 左側のドロワー -->
    <v-navigation-drawer app temporary v-model="isRoomInfoDrawerOpen" clipped location="left">
      <!-- ドロワーの中身 -->
      <v-container>
        <!-- ルーム情報 -->
        <v-row class="mb-5">
          <v-col cols="12">
            <div class="room-info-container">
              <h1 class="room-info-title">ルーム情報</h1>
              <div class="room-info">
                <p class="room-info-item">参加人数: {{ N_mem }}</p>
                <p class="room-info-item">Hackedの人数: {{ N_hacked }}</p>
                <p class="room-info-item">参加者リスト: 
                  <br>
                  <span v-for="member in Members" :key="member">
                    {{ member }}
                  <br>
                </span>
              </p>
              <p class="room-info-item">死亡者リスト: 
                <br>
                <span v-for="dead in Dead" :key="dead">
                  {{ dead }}さん
                  <br>
                </span>
              </p>
            </div>
            <button class="update-button" @click="updateInformation">情報を更新</button>
            </div>
          </v-col>
        </v-row>
        <!-- ボタンコンテナ -->
        <v-row>
          <v-col cols="12">
            <div class="button-container">
              <button v-if="Owner_input_username !== ''" class="button-normal button-side-bar" @click="onClose">部屋を閉じる</button>
              <button v-else class="button-normal button-side-bar" @click="onExit">退室する</button>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-navigation-drawer>

    <!-- 右側のコンテンツ -->
    <v-container class="mx-auto my-5 px-4">
      <!-- チャット表示エリア -->
      <v-row class="mt-5" v-if="chatList.length !== 0">
        <v-col cols="12">
          <ul>
            <li class="item mt-4" v-for="(chat, i) in chatList" :key="i">{{ chat }}</li>
          </ul>
        </v-col>
      </v-row>

      <!-- ゲーム進行エリア -->
      <v-row class="mt-10">
        <v-col cols="12">
          <p>ゲーム進行</p>
          <div class="mt-5">
            <div class="input-container">
              <!-- ...（省略）... -->
            </div>
          </div>
        </v-col>
      </v-row>

      <router-link to="/" class="link"></router-link>
    </v-container>
  </v-app>
</template>


<style scoped>
.v-app-bar {
  background-color: #02194e;
  color: #ffffff;
}
.header-right{
  position: absolute;
  right: 20px;
}
.room-info-container {
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.room-info-title {
  font-size: 24px;
  margin-bottom: 10px;
}

.room-info {
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
  padding: 20px;
  border-radius: 5px;
  text-align: left; /* すべての内容を左寄せに */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.room-info-item {
  font-size: 16px;
  margin: 5px 0;
}

.update-button {
  background-color: #02194e;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.update-button:hover {
  background-color: #0056b3;
}
.container {
  width: 50vw;
}

.area {
  width: 200%;
  margin: 16px 0;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  outline: none;
  resize: none;
  font-size: 16px;
  flex: 1; /* ボタンを横方向に中央に配置 */
}
.button-container {
  position: fixed;
  bottom: 0;
  width: 88%;
  text-align: center; /* ボタンを横方向に中央に配置 */
}
.button-normal {
  background-color: #02194e;
  text-align: center; /* ボタンを横方向に中央に配置 */
  color: white;
  border: none;
  padding: 10px 15px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  outline: none;
}
/* ボタンを一番下に配置したい*/
.button-side-bar {
  background-color: #02194e;
  text-align: center; /* ボタンを横方向に中央に配置 */
  color: white;
  border: none;
  padding: 10px 15px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  outline: none;
  width: 100%;
  margin-bottom: 10px;
}
.button-content {
  background-color: #02194e;
  text-align: center; /* ボタンを横方向に中央に配置 */
  color: white;
  padding: 2px 5px;
  font-size: 16px;
  border-radius: 5px;
  outline: none;
  width: 80%;
  margin-bottom: 5px;
}
.input-container {
  display: flex;
  align-items: center;
}
.button-left {
  margin-left: 8px;
}
.button-right {
  margin-right: 8px;
  
}

.link {
  text-decoration: none;
}

.chatitem {
  list-style: none;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
  /*background-color: #f9f9f9;*/
  word-wrap: break-word;
}

.my-message {
  border: 3px solid #3498db;
}

.other-message {
  background-color: #3f3d3d
}

.room-buttons {
  display: flex;
  margin-top: 20px;
}

.room-button {
  background-color: #04aa6d;
  color: white;
  border: none;
  padding: 10px 15px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 10px;
  outline: none;
}

.selected-room {
  background-color: #f0f0f0;
  color: #04aa6d;
}
</style>