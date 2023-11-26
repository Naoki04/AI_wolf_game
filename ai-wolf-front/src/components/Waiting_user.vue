<script setup>
import { ref, inject, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();
//const roomID = inject("roomID");
//const password = inject("password");
//const n_hacked = inject("n_hacked");
const emit = defineEmits();

// レスポンスデータを保持するリファレンス
const responseData = ref(null);
const responseStatus = ref(null);

const User_input_username = inject("User_input_username");
const User_input_room_id = inject("User_input_room_id");

let n_mem = ref("");
let Current_mem = ref("");
let Members = ref("");
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



const onInformation = async () => {
  let response; // response を外部で宣言
  //console.log("ああああ")
  
  try {
    const data = {
      mode: 'get_room_info',
      data: {
        "room_id": Number(User_input_room_id.value),
      },
    };
    console.log(data);

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
    n_mem.value = response.data['room_info']['N_mem'];
    Current_mem.value = response.data['room_info']['Current_mem'];
    Members.value = response.data['room_info']['Members'];
    console.log('現在の参加人数:', Current_mem.value);
    console.log('参加者:', Members.value);
  }
};

const room_id = User_input_room_id.value;
emit('usersend', room_id);

let intervalId;

const stopUpdates = () => {
  // intervalIdをクリアしてsetIntervalを停止
  clearInterval(intervalId);
};

onMounted(() => {
  // 初回のAPIリクエストを送信
  onInformation();
  // 5秒ごとにAPIリクエストを送信し、intervalIdを保持
  intervalId = setInterval(() => {
    onInformation();
    console.log("Current_mem.value: ", Current_mem.value);
    console.log("n_mem.value: ", n_mem.value);
    if (Current_mem.value === n_mem.value) {
      console.log("ゲーム開始");
      router.push({ name: "gaming_room", params: { roomID: User_input_room_id.value } });
    };
  }, 5000);
});

onBeforeUnmount(() => {
  // コンポーネントがアンマウントされたときにintervalIdをクリアしてsetIntervalを停止
  clearInterval(intervalId);
});

</script>


<template>
<div class="black-background">
  <div class="mx-auto my-5 px-4">
    <p class="text-h3 font-weight-medium">オーナーがゲームを開始するまで少々お待ちください。</p>
  </div>
  <div>    
    <!-- ボタンをクリックしてAPIリクエストを送信 -->
    <button type="button" @click="onLeave" class="loginbtn loginbtn--shadow">待機室を出る</button>
  </div>
  <div>
    <button type="button" @click="stopUpdates" class="loginbtn loginbtn--shadow">更新停止</button>
  </div>
</div>
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
</style>