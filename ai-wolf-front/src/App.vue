<script setup>
  import { provide, ref } from "vue"
  import { useRouter } from "vue-router"
  //import Login_owner from "./components/Login_owner.vue"

  const router = useRouter()
  const Owner_input_username = ref("")
  const n_mem = ref(0)
  const n_hacked = ref(0)

  const User_input_room_id = ref("");
  const User_input_password = ref("");
  const User_input_username = ref("");

  // 入室管理
  provide("Owner_input_username", Owner_input_username)
  provide("n_mem", n_mem)
  provide("n_hacked", n_hacked)
  provide("User_input_room_id", User_input_room_id)
  provide("User_input_password", User_input_password)
  provide("User_input_username", User_input_username)

  const roomID = ref();
  const password = ref("");
  const issued_event = (data) => {
    roomID.value = data["Issued_roomID"];
    password.value = data["Issued_password"];
    //console.log(roomID);
    //console.log(password);
    //console.log("ああああ");
  };

  const user_send_event = (room_id) => {
    roomID.value = room_id;
  };
  //eventの外側にprovideを書く。<->
  provide("roomID", roomID)
  provide("password", password)

</script>

<template>
  <!-- <Login_owner>タグである必要があったが、router-viewタグに設定することで回避できた。 -->
  <router-view @issued="issued_event" @usersend="user_send_event"/>
    <!--Login_ownerじゃないといけないのか,それともdivタグでもいいのか？
    <div @issued="issued_event"></div>  これはダメだった
  <Login_owner @issued="issued_event"></Login_owner>-->
</template>


<style scoped>
</style>