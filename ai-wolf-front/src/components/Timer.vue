<script setup>
  import { Socket } from "socket.io-client";
  import { inject, ref, computed, resolveDirective } from "vue";
  import io from "socket.io-client";
  import { useRouter } from "vue-router"

const socket = io();

// 初期値入力
const min = ref(0);
const sec = ref(20);
// 開始ボタンが押されたかどうか
const timerOn = ref(false);
//setIntervalの返り値を入れておく変数止めるときに使う
const timerObj = ref(null);
//ゲーム中かどうか
const game = ref(true);
//サーバーとのやり取り成功か
const isSarver = ref(false);
//残り10秒以下かどうか
const tenSec = ref(false);


//timerの色初期値は黒
const isColorRed = ref({
      color: "black"
});


// min, secを動かす関数
const count = () => {
  if(min.value >= 1){
    isColorRed.value = {
      color: "brack"
    };
  }
  if(min.value === 1 && sec.value === 1){
    isColorRed.value = {
      color: "red"
    };
  }
  if (min.value < 1) {//01:00から赤く、大きくなる
    isColorRed.value = {
      color: "red"
    };
  }

  if(sec.value <= 16 && min.value === 0){
    tenSec.value = true;
  }
  if (sec.value === 0 && min.value >= 1) {//00秒かつ１分以上
    min.value--;
    sec.value = 59;

  } else if (sec.value === 0 && min.value === 0) {//00:00のとき
    complete();
  } else {
    sec.value--;
  }
};

//開始ボタンを押したとき1秒ごとにcount関数を呼び出すtimerOn, gameにtrueを入れる関数
const start = () => {
  socket.emit("start", "ゲームスタート");
  timerObj.value = setInterval(count, 1000);
  timerOn.value = true;
  game.value = true;
};
//サーバーからスタートイベントが届いたら
socket.on("start", (data) => {
  timerObj.value = setInterval(count, 1000);
  timerOn.value = true;
  game.value = true;
});

//ストップボタンを押したときsetIntervalを止めてtimerOnにfalseを入れる関数
const stop = () => {
  socket.emit("stop", "ゲームストップ");
  clearInterval(timerObj.value);
  timerOn.value = false;
  tenSec.value = false;
};

  //サーバーからストップイベントが届いたら
    socket.on("stop", (data) =>{
      clearInterval(timerObj.value);
      timerOn.value = false;
    });

//時間が足りないときに1分プラスする関数
const add = () => {
  socket.emit("add", "1分追加");
  min.value += 1;
  isColorRed.value = {
    color: "black"
  };
  tenSec.value = false;
};
socket.on("add", (data) => {
  min.value += 1;
  tenSec.value = false;
  tenSec.value = false;
});

const subtract = () => {
  if(min.value > 0){
    socket.emit("subtract", "1分削減");
    min.value -= 1;
    if(min.value === 0 && sec.value <= 15){
    tenSec.value = true;
    }
  }
};
socket.on("subtract", (data) => {
  min.value -= 1;
  if(min.value === 0 && sec.value <= 15){
    tenSec.value = true;  
  }
});
//formatTimeにmin:secの形で代入する
const formatTime = computed(() => {
  //配列timeStringsにmin, secをString型で入れる（mapを使って条件をプラスする）
  const timeStrings = [min.value.toString(), sec.value.toString()].map(str => {
    if (str.length < 2) {//一桁の時0を付ける
      return "0" + str;
    } else {
      return str;
    }
  });
  //配列を区切り文字":"で結合してのformatTimeに返す
  return timeStrings;
});

  // ーーーーーーーーーーーーーーここから変更ーーーーーーーーーーーーーー

  const userName = inject("userName")
  const voteList = inject("voteList");
  const showModal = inject("showModal");
  let sent = false;
  const router = useRouter()

  const defReset = () => {
    clearInterval(timerObj.value);
    timerOn.value = false;
    game.value = false;
    min.value = 10;
    sec.value = 0;
  }

  //00:00か終了ボタンが押されたときsetIntervalを止めてgameをfalse,その他を初期値に戻す
  // ▶▶ 0:00になった時のみの動作とする
  const complete = () =>{
    defReset();
    // 自分の名前を送り送信済みに
    socket.emit("finishDiscussion", userName.value);
    sent = true;
    // もし他の人全員の名前を受け取り終わっていたら投票へ
    if (voteList.length == 3) {
      showModal.value = true;
      router.push({ name: "vote" })
      // ラグなどでループしないためにオフに
      sent = false;
    }
  };

  // 自分が終了ボタンを押したら
  const endButton = () => {
    if(confirm("終了しますか？")){
      defReset();
      // 自分の名前を送り送信済みにする
      socket.emit("endButtonSubmit", userName.value);
      sent = true;
    }
  }

  // サーバーからストップイベントが届いたら
  // ▶▶　他の人が終了ボタンを押したら
  socket.on("finish", (otherName) =>{
    defReset();
    // 終了ボタンを押した人の名前を受け取る
    voteList.push(otherName);
    // 自分の名前を送り送信済みにする
    socket.emit("finishDiscussion", userName.value);
    sent = true;
  });

  // 他の人の名前を受け取る
  socket.on("submitMyName",(otherName) => {
      voteList.push(otherName);
      console.log(voteList);
      // もし他の人全員の名前を受け取り終わっている、かつ、自分の名前を送り終えていたら投票へ
      if ((voteList.length == 3) && (sent == true)) {
        showModal.value = true;
        router.push({ name: "vote" })
        // ラグなどでループしないためにオフに
        sent = false;
      }
  });

</script>

<template>
  <div class="timer">
    <div class="time" v-bind:style="[isColorRed]" v-if="game" v-bind:class="{bound: tenSec}">
      {{ formatTime[0] }}
      <span v-bind:class="{ colon: timerOn }">
        :
      </span>
      {{ formatTime[1] }}
    </div>
    <div class="gameSet" v-if="!game">
      終了！
    </div>
    <!-- timerOnがfalseの時開始（start関数呼び出し）、trueの時ストップ（stop関数呼び出し）ボタンを表示 -->
    <v-btn v-on:click="start" v-if="!timerOn" class="Button" color="#455A64" elevation="2">スタート</v-btn>
    <v-btn v-on:click="stop" v-if="timerOn" class="Button" color="#455A64" elevation="2">ストップ</v-btn>
    <!-- 追加/削減ボタン（add/subtract関数を呼び出し）を表示 -->
    <v-btn v-on:click="subtract" class="Button2" color="#455A64" elevation="2">-１分</v-btn>
    <v-btn v-on:click="add" class="Button3" color="#455A64" elevation="2">+１分</v-btn>
    <v-btn v-on:click="endButton" class="Button" color="#455A64" elevation="2">終了</v-btn>
  </div>
</template>

<style scoped>
.timer {
  text-align: center;
  /* width: 20%; */
  width: 10rem;
  margin-left: 7.5rem;
}

.time {
  display: inline-block;
  margin-bottom: 10px;
  font-size: 26px;
}

.bound{
  animation: bounce-in 1s infinite;
}
@keyframes bounce-in {
  0%, 100%{
    transform: scale(1);
  }
  50% {
    transform: scale(1.8);
  }
}

.colon {
  /**真ん中の：を点滅させる */
  animation: flash 1s ease infinite;
  animation-delay: 0.5s;
}

@keyframes flash {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }
}

.Button {
  margin: 5px 0;
  width: 100%;
}
.Button2{
  margin-right: 6px;
  width: 48%;
}
.Button3{
  width: 48%;
}
.gameSet {
  font-size: 50px;
  color: red;
  margin-left: 10px;
}
</style>