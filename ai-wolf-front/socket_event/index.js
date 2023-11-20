export default (io, socket) => {
  // 入室メッセージをクライアントに送信する
  socket.on("enterEvent", data => {
    socket.broadcast.emit("enterEvent", data);
  });

  // 退室メッセージをクライアントに送信する
  socket.on("exitEvent", data => {
    socket.broadcast.emit("exitEvent", data);
  });

  // 投稿メッセージを送信する
  socket.on("publishEvent", data => {
    io.sockets.emit("publishEvent", data);
  });

  socket.on("publishChat", data => {
    io.sockets.emit("publishChat", data);
  });

  socket.on("publishQuestion", data => {
    io.sockets.emit("publishQuestion", data);
  });
};
