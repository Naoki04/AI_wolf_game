<script setup>
import Message from "../models/message";
import io from "socket.io-client";
import { inject, onMounted, ref, computed, watch } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';
const router = useRouter();

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
const roomID = inject("roomID");
const N_mem = ref(0);

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
    N_mem.value = response.data.room_info.N_mem;
    console.log("onInfomationのN_mem:", N_mem.value);
    console.log("onInfomationのHackeds:", response.data.room_info.Hacked);
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

const socket = io();
const onReceiveMessage = (messageData) => {
  chatList.value.unshift(messageData);
};
const onReceiveQuestion = (questionData) => {
  questionList.value.unshift(questionData);
};
socket.on("publishChat", onReceiveMessage);
socket.on("publishQuestion", onReceiveQuestion);

const questionList = ref([]);
const chatList = ref([]);
const chatContent = ref("");


const onQuestion = () => {
  if (chatContent.value.trim().replace("　", "") === ""){
    window.alert('空白のみの投稿はできません！');
    return;
  };

  const message = new Message(chatContent.value, userName.value, socket, roomID.value, false);
  const messageData = message.getMessageObject();
  socket.emit("publishQuestion", messageData); // チャット用のイベントを送信
  chatContent.value = "";
  console.log("onQuestionのchatList", chatList.value);
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
  console.log("onAnswerのchatList", chatList);
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

</script>
<template>
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
            <v-card-actions>
              <v-textarea v-model="chatContent" outlined placeholder="回答or質問を入力してください" rows="2"></v-textarea>
              <v-btn color="primary" @click="onQuestion">◀質問</v-btn>
              <v-btn color="primary" @click="onAnswer">◀回答</v-btn>
            </v-card-actions>
            <v-card-text>
              <v-list v-if="chatList.length % N_mem === 0 && chatList.length > 0 ">
                <v-list-item v-for="(chat, i) in chatList.slice(0, N_mem)" :key="i">
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


/*ここから新規*/


</style>

<!--<template>
  <v-card-text>
    <v-list>
      <v-list-item v-for="(chat, i) in chatList" :key="i">
        <v-list-item-content>
          <li>{{ chat.userName }}さん：{{ chat.content }}:{{ i }}</li>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="chatList.length === /* 期待する人数 */">
         ここで全ての回答が集まった時に表示する内容を記述 
      </v-list-item>
    </v-list>
  </v-card-text>
</template>-->