<script setup>
import { inject, defineProps } from "vue";

const Issued_roomID = 4444
const Issued_password = "password"
const n_mem = inject("n_mem"); // デフォルト値を指定
const n_hacked = inject("n_hacked"); // デフォルト値を指定
</script>

<template>
  <div class="mx-auto my-5 px-4">
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>ルームID: {{ Issued_roomID }}です。</p>
    </div>
    <div>
      <h1 class="text-h3 font-weight-medium"></h1>
      <p>パスワード: {{ Issued_password }}です。</p>
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