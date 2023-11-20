<script setup>
import Message from "../models/message";
import io from "socket.io-client";
import { inject, onMounted, reactive, ref, computed } from "vue";
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
console.log("N_mem:", N_mem.value)
const Current_mem = ref("");
const Members = ref([]);
const N_hacked = ref("");
const Hacked = ref([]);
let Dead = ref([]);
let GameState = ref("");
let Dead_user = ref([]);
let Hacked_username = ref("");
let question_member = ref("")
let count = ref(1)
let question = ref("");
let AI_answer = ref("");

// chatListに新しい要素を追加する例
function addMessage(message) {
  chatList.push(message);
}

const onInformation = async () => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'get_room_info',
      data: {
        "room_id": Number(roomID.value),
      },
    };
    console.log("onInfomationの送るdata",data)
    // POSTリクエストを送信
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    // レスポンスを処理
    //console.log('ステータスコード:', response.status);
    //console.log('レスポンスデータ:', response.data);
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
    await onStart(Members.value[0], N_hacked.value);
    //なおに質問：常に１人N_hacked＝１となっているのはなぜ？
    console.log('Hackedの人数:', N_hacked.value);
    console.log('Hackedリスト:', Hacked.value);
    console.log('死亡者リスト:', Dead.value);
    console.log('ゲームの状態:', GameState.value);
    const question_Member = () => {
        let selectedMember = Members.value[count.value]; // ランダムに選ばれたメンバーを取得
        //console.log("count", count.value)
        if (count.value == Members.value.length-1) {
          count.value = 0
        }
        else {
          count.value += 1
        }
        //console.log("count", count.value)
        console.log("質問する人", selectedMember)
      return selectedMember;
    };
    question_member.value = question_Member();
    console.log("質問者は：", question_member.value)
    addMessage(question_member.value + "さんは質問を投稿してください。");
  }
};

//onInformation();

const onStart = async (OwnerName, N_hacked) => {
  let response; // response を外部で宣言
  try {
    const data = {
      mode: 'start_game',
      data: {
        room_id: Number(roomID.value),
        owner_name: OwnerName,
        n_hacked: N_hacked,
      },
    };
    console.log("onStartのdata", data)
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log('ステータスコード:', response.status);
    console.log('レスポンスデータ:', response.data);

    if (response) {
      console.log("ゲーム開始")
      Hacked.value = response.data['hacked'];
      console.log('Hackedリスト:', Hacked.value);
      console.log("Hacked人数", N_hacked.value);
      // onStart関数で取得したHackedのデータをonGetAiAnswer関数のリクエストに送信
      for (let count = 0; count < Hacked.value.length; count++) {
        await onGetAiAnswer(Hacked.value[count]);
      }
    }
  } catch (error) {
    console.error('エラー:', error);
  };
};

let chatContent = ref(""); // 質問内容を保持するref変数
let chatMessages = ref([]); // 質問と回答を保持するリスト

const onQuestion = () => {
  if (chatContent.value.trim().replace("　", "") === ""){
    //alert("空白のみの投稿はできません！");
    return
  }
  const message = new Message(chatContent.value, userName.value, socket, currentRoomId.value, false);
  const messageData = message.getMessageObject();
  console.log("onQuestionのmessageData", messageData)
  // メッセージをサーバーに送信
  socket.emit("publishEvent", messageData);
  //onGetAiAnswer(Hacked.value, messageData["text"]);
  // 入力フィールドをクリア
  chatContent.value = "";
};

// 仮の回答を受け取ったと仮定
function onAnswer(answer) {
  chatMessages.value.push({ id: Date.now(), text: answer });
};

// 以下で質問の送信と回答の受信をシミュレート（APIの代わりに使用）
//onQuestion(); // クライアントが質問を送信したと仮定
//onAnswer("これは仮の回答です。"); // クライアントに対する仮の回答

const onGetAiAnswer = async (hackedData, question) => {
  let response;
  try {
    const data = {
      mode: 'get_ai_answer',
      data: {
        room_id: Number(roomID.value),
        user_name: hackedData, // Hackedのデータを送信
        question: question, // 質問内容を送信
      },
    };
    console.log("onGetAiAnswerに送るdata:", data)
    response = await axios.post('https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf', data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log('ステータスコード:', response.status);
    console.log('レスポンスデータ:', response.data);

    if (response) {
      AI_answer = response.data['answer'];
      console.log('AIの回答:', AI_answer);
    }
  } catch (error) {
    console.error('エラー:', error);
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

// 退室メッセージをサーバに送信する
const onExit = () => {
  router.push({ name: "home" })
  onInformation()
  socket.emit("exitEvent", `${User_input_username.value}さんが退出しました。`)
}


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

const addAnswer = (questionIndex, username, answer) => {
  if (answerList[questionIndex]) {
    answerList[questionIndex].answers.push([username, answer]);
  } else {
    console.error(`質問 ${questionIndex} が定義されていません。`);
  }
};

onMounted(() => {
  // 初回のAPIリクエストを送信
  onInformation();
  //onStart();
  //10秒後に2回目のAPIリクエストを送信
  //setInterval(onInformation, 10000);
});

const chatList = reactive([])

const isRoomInfoDrawerOpen = ref(false);
const toggleDrawer = () => {
  isRoomInfoDrawerOpen.value = !isRoomInfoDrawerOpen.value;
};

// 何らかのイベントや関数でchatListに新しいメッセージを追加する
addMessage("メンバーがそろいました。オーナーはゲーム開始ボタンを押してください");
console.log("chatListの中身:", chatList)
const answerList = reactive([
  {
      question: "質問1",
    answers: [
      ["user1", "回答1"],
      ["user2", "回答2"],
    ],
  },
]);
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
  chatList.unshift(data)
  //chatList.push(data)
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

//addAnswer(0, "user3", "回答3");
//addAnswer(0, "user4", "回答4");
//addAnswer(0, "user5", "回答5");
//addAnswer(0, "user6", "回答6");
//console.log("answerListの中身:", answerList);
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
<!-- サイドバー -->
    <v-navigation-drawer app temporary v-model="isRoomInfoDrawerOpen" clipped location="left">
      <v-container>
        <!-- サイドバーのコンテンツ -->
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
        <div class="button-container">
          <button v-if="Owner_input_username !== ''" class="button-normal button-side-bar" @click="onClose">部屋を閉じる</button>
          <button v-else class="button-normal button-side-bar" @click="onExit">退室する</button>
        </div>
      </v-container>
    </v-navigation-drawer>
    <!-- 上側のブロック（5人以下）-->
    <v-row v-if="Current_mem<=5" class="fill-height1">
      <v-col cols="12" class="top-block">
        <!--ユーザーの解答をそれぞれ表示する-->
        <div v-for="(question, questionIndex) in answerList" :key="questionIndex">
          <h2>{{ question.question }}</h2>
          <div v-for="(answer, answerIndex) in question.answers" :key="answerIndex">
            <p class="user-answer">{{ answer[0] }}さんの回答：{{ answer[1] }}</p>
          </div>
        </div>
      </v-col>
    </v-row>
    <!--  6人以上　-->
    <v-row v-if="Current_mem>5" class="fill-height2">
      <v-col cols="6" class="left-block mx-auto my-5 px-4">
        <div class="chat-container">
          <!-- 左側のコンテンツをここに配置 -->
          <div v-for="(question, questionIndex) in answerList" :key="questionIndex">
            <h2>{{ question.question }}</h2>
            <div v-for="(answer, answerIndex) in question.answers" :key="answerIndex">
              <p class="user-answer">{{ answer[0] }}さんの回答：{{ answer[1] }}</p>
            </div>
          </div>
        </div>
      </v-col>
      <!-- 右側のブロック -->
      <v-col cols="6" class="right-block mx-auto my-5 px-4">
        <div class="chat-container">
          <!-- 右側のコンテンツをここに配置 -->
          <div v-for="(question, questionIndex) in answerList" :key="questionIndex">
            <h2>{{ question.question }}</h2>
            <div v-for="(answer, answerIndex) in question.answers" :key="answerIndex">
              <p class="user-answer">{{ answer[4] }}さんの回答：{{ answer[1] }}</p>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
    <!-- 下側のブロック -->
    <v-row class="fill-height3">
      <v-col cols="12" class="bottom-block">
        <!-- 下側のコンテンツをここに配置 -->
        <div class="mx-auto my-5 px-4">
          <!-- 右側のコンテンツをここに配置 -->
          <div>
            <div class="game-progress">
              <p class="game-progress-title">ゲーム進行</p>
              <ul class="game-progress-content">
                <li v-if="chatList.length > 0">{{ chatList[chatList.length - 1] }}</li>
              </ul>
            </div>
          </div>
          <div class="mt-10">
            <div class="mt-5">
              <div class="input-container">
                <textarea variant="outlined" placeholder="回答or質問を入力してください" rows="2" class="area" v-model="chatContent"></textarea>
                <div class="button-left">
                  <button class="button-normal button-content" @click="onPublish">回答</button>
                  <button class="button-normal button-content" @click="onQuestion">質問</button>
                </div>
                <div class="buttons-right">
                  <button v-if="Owner_input_username !== ''" class="button-normal button-content" @click="onStart">ゲーム開始</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-app>
</template>

<style scoped>

.black-background {
  background-color: black;
  color: white;
  /*画面全体を黒い背景にしたい */
  height: 100vh;
  width: 100vw;
  /*文字を真ん中にしたい 
  display: flex;
  justify-content: center;
  align-items: center;*/
}
body, html {
  height: 100%; /* ページ全体の高さを100%に設定 */
  margin: 0; /* マージンをリセットして余白を削除 */
  padding: 0; /* パディングをリセットして余白を削除 */
  overflow: hidden; /* スクロールを無効にする */
}
.fill-height1 {
  margin: 100px;
  height: 180%;
  display: flex;
  flex-direction: column;
  margin-bottom: 165px;
}
.fill-height2 {
  margin: 100px;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 165px;
}
.fill-height3 {
  margin: 100px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.left-block {
  /*flex: 1;*/
  background-color: #f0f0f0;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto;
  margin-right: 10px; /* 左右のブロックを分けるスペース */
}

.right-block {
  /*flex: 1;*/
  background-color: #f0f0f0;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto;
  margin-left: 10px; /* 左右のブロックを分けるスペース */
}

.top-block {
  background-color: #f0f0f0; /* 上側のブロックの背景色 */
  flex: 1; /* 上側のブロックが残りの高さを占める */
  padding: 50px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto; /* コンテンツがはみ出した場合にスクロールバーを表示 */
  /*上の空白をなくす*/
  margin-top: 100px;
}

.bottom-block {
  background-color: #ffffff; /* 下側のブロックの背景色 */
  flex: 1; /* 下側のブロックが残りの高さを占める */
  padding: 50px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: auto; /* コンテンツがはみ出した場合にスクロールバーを表示 */
  /*下の空白をなくす*/
  margin-top: -300px; /* ここのサイズをかなりいじった。 */
  margin-bottom: 10px;
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

.chat-container {
  margin-bottom: 100px;
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

.user-answer {
  font-size: 16px;
  margin: 5px 0;
  font-weight: bold;
  border: 1px solid #000; /* 縁取りのスタイルを設定 */
  padding: 10px; /* テキストと縁取りの間に余白を作成 */
  border-radius: 5px; /* 縁取りの角を丸くする場合に設定 */
  background-color: #f0f0f0;
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
  outline: none
}
.selected-room {
  background-color: #f0f0f0;
  color: #04aa6d;
}
.game-progress {
  background-color: #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  margin-bottom: 20px;
}

.game-progress-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.game-progress-content {
  font-size: 30px;
  font-weight: bold;
  text-align: center;
  list-style: none;
  padding: 0;
}

.game-progress-content li {
  margin-bottom: 10px;
}

.game-progress-content li:last-child {
  margin-bottom: 0;
}

.chatitem {
  list-style: none;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
  word-wrap: break-word;
  background-color: #f9f9f9;
}
</style>


<!--<template>
  <v-app>
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
            <v-card-text>
              <v-list>
                <v-list-item v-for="message in messages" :key="message.id">
                  <v-list-item-content>
                    <v-list-item-title>{{ message.text }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              ボタンを押すとonAnswer関数が実行されて
              <textarea variant="outlined" placeholder="回答or質問を入力してください" rows="2" class="area" v-model="chatContent"></textarea>
              <button class="button-normal button-content" @click="onSend">回答</button>
            </v-card-actions>
            <div class="mt-5" v-if="chatList.length !== 0">
              <ul>
                <li class="chatitem" v-for="(chat, i) in chatList" :key="i"
                  :class="{ 'my-message': chat.userName === userName }">
                  {{ chat.userName }}さん：{{ chat.content }}
                </li>
              </ul>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>-->