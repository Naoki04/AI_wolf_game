<script setup>
import { inject } from "vue";

const roomID = inject("roomID");
const password = inject("password");
console.log("roomID: ", roomID.value);
console.log("password: ", password.value);
const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>ルームID: {{ roomID }}です。</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>パスワード: {{ password }}です。</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>メンバー数: {{ n_mem }}人</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>ハックされた人数: {{ n_hacked }}人</p>
    </div>
  </div> 
</template>



<style scoped>
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