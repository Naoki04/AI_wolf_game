<script setup>
import Message from "../models/message";
import io from "socket.io-client";
import { inject, onMounted, reactive, ref, computed } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';
const router = useRouter();

const Owner_input_username = inject("Owner_input_username");
const User_input_username = inject("User_input_username");
const roomID = inject("roomID");
console.log("Owner_input_username", Owner_input_username);
console.log("User_input_username", User_input_username);
console.log("roomID", roomID); 

const socket = io();

const response = ref("");

// onInformation関数をasyncを用いて呼び出す
const onInformation = async () => {
  //let response;
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
    // await onStart(response.data);
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};
//ゲームが始まったときの初期化処理
//const initializeGame = () => {
//}

// onStart関数で"start_game"modeを送信
// 得たデータをもとに、HackedメンバーをonGetAiAnswer関数のdataとして"get_ai_answer"modeで送信
const onStart = async (OnInfo) => {
  //console.log("onStartのOnInfo:", OnInfo.room_info)
  //console.log("onStartのOnInfo.Members:", OnInfo.room_info.Members[0])
  //console.log("onStartのOnInfo.N_hacked:", OnInfo.room_info.N_hacked)
  // let response;
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
}

// 非同期処理を含むonMountedフック
onMounted(async () => {
  if (Owner_input_username.value) {
    const OnInfo = await onInformation();
    if (OnInfo) {
      await onStart(OnInfo);
    }
  }
  onInformation();
});


//一回onInformationを呼び出して、onStart()を呼び出す
//そこで得たonStart()のresponseをもとにonInformation()を呼び出して
//Hackedメンバーdataをクライアント側に渡す。

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
              <v-text-field
                v-model="message"
                label="メッセージを入力"
                outlined
              ></v-text-field>
              <v-btn @click="sendMessage">送信</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<style scoped>
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
</style>