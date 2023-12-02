<script setup>
import Message from "../models/message";
import io from "socket.io-client";
import { inject, onMounted, ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';
const router = useRouter();

//ヘッダー
const isRoomInfoDrawerOpen = ref(false);
const isMemoDrawerOpen = ref(false);

// 左ヘッダー・ルーム情報
const roomID = inject("roomID");
const password = inject("password");
const Members = ref([]);
const N_mem = ref(0);
const N_hacked = ref(0);
const Dead = ref([]);
// 
const onExit = () => {
  router.push({ name: "home" })
  onInformation()
};
// 
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

// 右ヘッダー・メモ
const memoContent = ref('');
const memoList = ref([]);
const onMemo = () => {
  if (!memoContent.value.trim()) {
    // メモ内容が空の場合はアラートを表示して処理を中断
    window.alert('メモ内容を入力してください！');
    return;
  }

  memoList.value.push(memoContent.value);
  memoContent.value = ''; // メモ入力欄を空にする
};

// 左ヘッダー・ルーム情報
const Owner_input_username = inject("Owner_input_username");
const User_input_username = inject("User_input_username");
const userName = computed(() => {
  if (Owner_input_username.value) {
    return Owner_input_username.value;
  } else if (User_input_username.value) {
    return User_input_username.value;
  } else {
    return null;
  }
});

const onInformation = async () => {
  try {
    const data = {
      mode: "get_room_info",
      data: {
        room_id: Number(roomID.value),
      },
    };
    console.log("onInfomationの送るdata:", data)
    //const
    const response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log("onInfomationのステータスコード", response.status);
    console.log("onInfomationのレスポンスデータ", response.data);
    Members.value = response.data.room_info.Members;
    N_mem.value = response.data.room_info.N_mem;
    N_hacked.value = response.data.room_info.N_hacked;
    Dead.value = response.data.room_info.Dead;
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

const onStart = async (OnInfo) => {
  try {
    const data = {
      mode: "start_game",
      data: {
        room_id: Number(OnInfo.room_info.RoomID),
        owner_name: OnInfo.room_info.Members[0],
        n_hacked: OnInfo.room_info.N_hacked,
      },
    };
    console.log("onStartの送るdata:", data)
    const response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log("onStartのステータスコード", response.status);
    console.log("onStartのレスポンスデータ", response.data);
    //onGetAiAnswer(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

const onEnd = async () => {
  let response;
  try {
    const data = {
      mode: 'end_room',
      data: {
        room_id: Number(roomID.value),
      },
    };
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    // レスポンスを処理
    console.log('ステータスコード:', response.status);
    console.log('レスポンスデータ:', response.data);
  } catch (error) {
    console.error('エラー:', error);
  }
};

const socket = io();
const onReceiveMessage = (messageData) => {
  answerList.value.unshift(messageData);
};
const onReceiveQuestion = (questionData) => {
  questionList.value.unshift(questionData);
};
socket.on("publishChat", onReceiveMessage);
socket.on("publishQuestion", onReceiveQuestion);

const chatContent = ref("");
const questionList = ref([]);
const answerList = ref([]);

const onQuestion = () => {
  if (chatContent.value.trim().replace("　", "") === ""){
    window.alert('空白のみの投稿はできません！');
    return;
  };

  const message = new Message(chatContent.value, userName.value, socket, roomID.value, false);
  const messageData = message.getMessageObject();
  socket.emit("publishQuestion", messageData); // チャット用のイベントを送信
  chatContent.value = "";
  console.log("onQuestionのanswerList", answerList.value);
  console.log("onQuestionのquestionList", questionList.value);
};

const onAnswer = async () => {
  if (chatContent.value.trim().replace("　", "") === ""){
    window.alert('空白のみの投稿はできません！');
    return;
  };

  const onInfo = await onInformation();
  const Hackeds = onInfo.room_info.Hacked;
  console.log("onAnswerのHacked:", Hackeds);

  if (Hackeds.includes(Owner_input_username.value) || Hackeds.includes(User_input_username.value)) {
    console.log("onAnswerのHacked: Found");
    // Hackedの処理
    const messageContent = await onGetAiAnswer();
    const message = new Message(messageContent, userName.value, socket, roomID.value, true);
    const messageData = message.getMessageObject();
    console.log("onAnswerのmessageData", messageData)
    socket.emit("publishChat", messageData);
  } else {
    console.log("onAnswerのHacked: Not Found");
    // Hackedでない人の処理
    const message = new Message(chatContent.value, userName.value, socket, roomID.value, true);
    const messageData = message.getMessageObject();
    console.log("onAnswerのmessageData", messageData)
    socket.emit("publishChat", messageData); 
  };
  console.log("onAnswerのanswerList", answerList);
  chatContent.value = "";
};

const onGetAiAnswer = async () => {
  try {
    const data = {
      mode: "get_ai_answer",
      data: {
        room_id: Number(roomID.value),
        user_name: userName.value,
        question: questionList.value[0].content,
      },
    };
    //console.log("onGetAiAnswerの送るdata:", data)
    const response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log("onGetAiAnswerのステータスコード", response.status);
    console.log("onGetAiAnswerのレスポンスデータ", response.data);
    return response.data.answer;
  } catch (error) {
    console.error(error);
    return null;
  }
};

// Trueのときは質問、Falseのときは回答
let questionTF = ref(false);

const onSend = async () => {
  //console.log("1.質問or回答 : ", questionTF.value ? "質問" : "回答")
  //Q_Member();
  if (questionTF.value) {
    // 質問のとき
    onQuestion();
  } else {
    // 回答のとき
    onAnswer();
  }
  //console.log("2.質問or回答 : ", questionTF.value ? "質問" : "回答")
  chatContent.value = "";
};

// 非同期処理を含むonMountedフック
onMounted(async () => {
  if (Owner_input_username.value) {
    const OnInfo = await onInformation();
    console.log("onMountedのOnInfo:", OnInfo)
    if (OnInfo) {
      await onStart(OnInfo);
    }
  }
  onInformation();
  console.log("N_mem:", N_mem.value);
});


//

</script>

<template>
  <v-app>
    <!--　ヘッダー　-->
    <v-app-bar color="primary" dark app clipped-left>
      <v-app-bar-nav-icon variant="text" @click.stop="isRoomInfoDrawerOpen = !isRoomInfoDrawerOpen"
        icon="mdi-menu"></v-app-bar-nav-icon>
      <!-- 写真を挿入<v-img src="../assets/logo.png" max-height="48px" contain></v-img> -->
      <v-toolbar-title>AI狼</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn prepend-icon="mdi-note-edit" size="large" @click.stop="isMemoDrawerOpen = !isMemoDrawerOpen">Memo</v-btn>
    </v-app-bar>
    <!--　ルーム情報　-->
    <v-navigation-drawer app v-model="isRoomInfoDrawerOpen" clipped location="left">
      <v-container>
        <div class="room-info-container">
          <h1 class="room-info-title">ルーム情報</h1>
          <div class="room-info">
            <p class="room-info-item">参加人数: {{ N_mem }}</p>
            <p class="room-info-item">Hackedの人数: {{ N_hacked }}</p>
            <p class="room-info-item">参加者リスト: 
              <br>
              <span v-for="member in Members" :key="member">{{ member }}
                <br>
              </span>
            </p>
            <v-spacer></v-spacer>
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
        <div class="button-container">
          <button v-if="Owner_input_username !== ''" class="button-normal button-side-bar" @click="onClose">部屋を閉じる</button>
          <button v-else class="button-normal button-side-bar" @click="onExit">退室する</button>
        </div>
      </v-container>
    </v-navigation-drawer>
    <!--　メモ　-->
    <v-navigation-drawer app v-model="isMemoDrawerOpen" clipped location="right">
      <v-container>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title grey--text text--darken">あなたの残したメモ</v-list-item-title>
            <v-spacer></v-spacer>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item v-for="memo in memoList" :key="memo">
          <v-list-item-content>
            <v-list-item-title>{{ memo }}</v-list-item-title>
            <v-divider></v-divider>
          </v-list-item-content>
        </v-list-item>
        <v-list-item class="memo-publish">
          <v-list-content>
            <v-textarea v-model="memoContent" outlined placeholder="メモ欄" rows="1"></v-textarea>
          </v-list-content>
          <v-list-action>              
            <v-btn class="memo-button" color="primary" @click="onMemo">◀</v-btn>
          </v-list-action>
        </v-list-item>
      </v-container>
    </v-navigation-drawer>
    <!--　ゲームコンテント　-->
    <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <h1>ゲームルーム</h1>
            </v-card-title>
            <v-card-text>
              <p>ルームID: {{ roomID }}</p>
              <p v-if="Owner_input_username">オーナー: {{ Owner_input_username }}</p>
              <p v-if="User_input_username">ユーザー: {{ User_input_username }}</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title>
              <h1>チャット</h1>
            </v-card-title>
            <v-card-actions>
              <v-textarea v-model="chatContent" outlined placeholder="回答or質問を入力してください" rows="2"></v-textarea>
              <v-btn color="primary" @click="onQuestion">◀質問</v-btn>
              <v-btn color="primary" @click="onAnswer">◀回答</v-btn>
            </v-card-actions>
            <v-card-text>
              <v-list v-if="answerList.length % N_mem === 0 && answerList.length > 0 ">
                <v-list-item v-for="(chat, i) in answerList.slice(0, N_mem)" :key="i">
                  <v-list-item-content>
                    <li>{{ chat.userName }}さんの回答：{{ chat.content }}</li>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
              <v-list>
                <v-list-item v-if="questionList.length > 0" :key="questionList[0].id">
                  <v-list-item-content>
                    <li>{{ questionList[0].userName }}さんの質問：{{ questionList[0].content }}</li>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>


<style scoped>
.container {
  width: 50vw;
}

.area {
  width: 100%;
  margin: 16px 0;
}

.button-normal {
  background-color: #04aa6d;
  color: white;
  border: none;
  padding: 10px 15px;
  text-align: center;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  outline: none;
}

.button-exit {
  background-color: #ff3333;
  margin-left: 40px
}
.memo-button  {
  /* v-text-areaの右側に持っていきたい */ 
  position: absolute;
  right: 0;
  top: 0;
  /* ボタンを縦長にする */
  height: 62px;
  width: 20px;
  /* 他のスタイルが適用されないように !important を使用 */
  min-width: auto !important;
  max-width: none !important;
  /* サイズに合わせてコンテンツを中央に配置 */
  align-items: center;
  justify-content: center;
}
.memo-publish {
  position: fixed;
  bottom: 0;
  width: 88%;
  text-align: center; /* ボタンを横方向に中央に配置 */
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
  background-color: #f9f9f9;
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


/* 画面のbasicをブラックに */
.v-application {
  background-color: black;
}
/* カードの背景をホワイトに */
.v-card {
  background-color: white;
}
/* カードの文字をブラックに */
.v-card__title {
  color: black;
}
/* カードの文字をブラックに */
.v-card__text {
  color: black;
}
/* ボタンの背景をホワイトに */
.v-btn {
  background-color: white;
}
/* ボタンの文字をブラックに */
.v-btn__content {
  color: black;
}
.v-app-bar {
  background-color: #02194e;
  color: #ffffff;
}
.header-right{
  position: absolute;
  right: 20px;
  font-size: 16px;
  font-weight: bold;
}
/* 左ヘッダー：room-info */
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

/*ここから新規*/


</style>
