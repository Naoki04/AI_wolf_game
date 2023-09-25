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

const chatContent = ref("")
const chatList = reactive([])

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
  //if (response) {
  //  // レスポンスデータから必要な情報を抽出
  //  // 以下は例です。実際のデータ構造に合わせて変更してください。
  //}
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
  //  // レスポンスデータから必要な情報を抽出
  //  // 以下は例です。実際のデータ構造に合わせて変更してください。
    AI_answer = response.data['answer'];
    console.log('AIの回答:', AI_answer);
  }
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
const onReceiveEnter = (data) => {
  chatList.unshift(data)
}

// サーバから受信した退室メッセージを受け取り画面上に表示する
const onReceiveExit = (data) => {
  chatList.unshift(data)
}

// サーバから受信した投稿メッセージを画面上に表示する
const onReceivePublish = (data) => {
  chatList.unshift(data)
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
  //  // レスポンスデータから必要な情報を抽出
  //  // 以下は例です。実際のデータ構造に合わせて変更してください。
  //}
  router.push({ name: "home" });
};
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="text-h3 font-weight-medium">AI狼</h1>
    <div class="mt-10">
      <p v-if="Owner_input_username !== ''">ログインユーザ：{{ Owner_input_username }}さん</p>
      <p v-else-if="User_input_username !==''">ログインユーザ：{{ User_input_username }}さん</p>
      <p v-else>ログインユーザがいません。</p>
      <textarea variant="outlined" placeholder="投稿文を入力してください" rows="4" class="area" v-model="chatContent"></textarea>
      <div class="mt-5">
        <button class="button-normal" @click="onPublish">回答</button>
        <button class="button-normal" @click="onGetAiAnswer">質問</button>
      </div>
      <div class="mt-5">
        <button v-if="Owner_input_username !== ''" type="button" class="button-normal button-exit" @click="onClose">部屋を閉じる</button>
        <button v-else-if="User_input_username !==''" type="button" class="button-normal button-exit" @click="onExit">退室する</button>
      </div>
      <div class="mt-5">
        <button v-if="Owner_input_username !== ''" type="button" class="button-normal button-exit" @click="onStart">ゲーム開始</button>
        <button v-if="Owner_input_username !== ''" type="button" class="button-normal button-exit" @click="onEnd">ゲーム終了</button>
      </div>
      <div class="mt-5" v-if="chatList.length !== 0">
        <ul>
          <li class="item mt-4" v-for="(chat, i) in chatList" :key="i">{{ chat }}</li>
        </ul>
      </div>
    </div>
    <router-link to="/" class="link">
    </router-link>
  </div>
</template>

<style scoped>
.link {
  text-decoration: none;
}

.area {
  width: 500px;
  border: 1px solid #000;
  margin-top: 8px;
}

.item {
  display: block;
}

.util-ml-8px {
  margin-left: 8px;
}

.button-exit {
  color: #000;
  margin-top: 8px;
}
</style>