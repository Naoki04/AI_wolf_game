import { Server } from "socket.io"

const connectionEvents = (io, socketEvents) => {
  io.on("connection", socket => socketEvents(io, socket))
}

const socketEvents = (io, socket) => {
  console.log("socket.io - connection")
  socket.on("disconnect", () => {
    console.log(`socket.io - socket.id \`${socket.id}\` disconnected`)
  })
}

export default (options = {}) => ({
  name: "socket.io",
  configureServer(server) {
    const defaults = { connectionEvents, socketEvents }
    options = Object.assign(defaults, options)
    const io = new Server(server.httpServer)
    options.connectionEvents(io, options.socketEvents)
  }
})
