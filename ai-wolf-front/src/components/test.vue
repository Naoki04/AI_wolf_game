<script setup>
import { inject } from "vue";

const Issued_roomID = inject("Issued_roomID");
const Issued_password = inject("Issued_password");
const n_mem = inject("n_mem");
const n_hacked = inject("n_hacked");

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
