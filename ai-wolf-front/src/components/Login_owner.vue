<script setup>
import { inject, ref } from "vue";
//import { defineEmits } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';
const router = useRouter();
//ここで入力 Login_owner.vue
const Owner_input_username = inject("Owner_input_username");
const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");
const emit = defineEmits();

// 入室管理
const onEnter_owner = async () => {
  let response; // response を外部で宣言
  console.log(Owner_input_username.value);
  // ユーザー名が入力されているかチェック
  if (Owner_input_username.value.trim().replace("　","") === ""){
    window.alert("ニックネームを入力してください");
    return;
  };
  try {
    const data = {
      mode: 'create_room',
      data: {
        n_mem: n_mem.value, // ゲームに参加する人数(int)
        owner_name: Owner_input_username.value, // オーナーのユーザー名(str)
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
  console.log('ユーザー名:', Owner_input_username.value);
  console.log('参加人数:', n_mem.value);
  console.log('ハックされた人数:', n_hacked.value);

  if (response) {
    // roomIDを6桁の数字を用いてランダムに発行
    const Issued_roomID = response.data['roomid'];
    // passwordも同様に発行
    const Issued_password = response.data['password']
    //console.log('パスワード:', Issued_password);
    const data = {
      "Issued_roomID": Issued_roomID,
      "Issued_password": Issued_password,
    }
    console.log(data)
    //camelCaseは禁止。issuedは小文字じゃないとだめ。issued_room_idはOK
    //camelCaseとは…　先頭の文字が小文字, 2つ目以降の単語の頭文字は大文字<=>snake_case
    emit('issued', data);
    // 待合室に移動
    router.push({ name: "waiting_owner", params: { roomID: Issued_roomID } });
  };
};
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <h1 class="header">オーナー登録</h1>
    <div class="mt-10">
      <p>ユーザー名</p>
      <input type="text" class="namearea" v-model="Owner_input_username" />
    </div>
    <div>
      <p>参加人数(3~10)</p>
      <input type="number" class="namearea" min="3" max="10" v-model="n_mem" />
    </div>
    <div>
      <p>ハックされた人数(推奨2人)</p>
      <input type="number" class="namearea" min="1" max="4" v-model="n_hacked"/>
    </div>
    <button type="button" @click="onEnter_owner" class="loginbtn loginbtn--shadow">ルームを作成</button>
  </div>
</template>

<style scoped>
/*真っ黒の背景に白い文字を表示 */
.black-background {
  background-color: #000;
  color: #fff;
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

.container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.input {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}

.button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error-message {
  color: #ff0000;
  margin-top: 10px;
}

.error-details {
  margin-top: 10px;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
}
</style>
