// InRoomMessageList = {room1: [Message...], room2:[Message...]};
const InRoomMessageList = {};

// GlobalMessageList = [Message...];
const GlobalMessageList = [];

// receiverUserIdに送られた、sendUserIdごとの辞書
// 初めて送られたときに、userIdに対応するキーを作成する。
// 2回目以降のDMは、排列の末尾に追加する。
// DirectMessageList = {user1: {user2: [Message...], user3: [Message...]}, user2: {user1: [Message...]}};
const DirectMessageList = {};

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
};
