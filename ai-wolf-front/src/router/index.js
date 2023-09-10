import { createRouter, createWebHistory } from "vue-router"
import Home from "../components/Home.vue"
import Login_owner from "../components/Login_owner.vue"
import Login_user from "../components/Login_user.vue"
import Gaming_room from "../components/Gaming_room.vue"
import Waiting_user from "../components/Waiting_user.vue"
import Waiting_owner from "../components/Waiting_owner.vue"
import test from "../components/test.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },{
      path: "/test/",
      name: "test",
      component: test
    },
    {
      path: "/login_owner/",
      name: "login_owner",
      component: Login_owner
    },{
      path: "/login_user/",
      name: "login_user",
      component: Login_user
    },{
      path: "/waiting_owner/:roomID",
      name: "waiting_owner",
      component: Waiting_owner,
    },{
      path: "/waiting_user/:roomID",
      name: "waiting_user",
      component: Waiting_user,
    },{
      path: "/gaming_room/:roomID",
      name: "gaming_room",
      component: Gaming_room,
    },
  ],
})

export default router