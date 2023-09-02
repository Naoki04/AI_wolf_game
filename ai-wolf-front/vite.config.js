import { defineConfig,loadEnv } from "vite"
import vue from "@vitejs/plugin-vue"
import socketIoPlugin from "./plugins/socket.io.plugin"
import socketEvents from "./socket_event"

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), "")

  return {
    plugins: [vue(), socketIoPlugin({ socketEvents })],
    server: {
      host: true,
      port: parseInt(env.PORT) || 3000
    }
  }
})
