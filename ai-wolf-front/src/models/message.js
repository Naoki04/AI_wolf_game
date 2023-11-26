class Message {
    constructor(content, userName, socket, roomId, isUpdate) {
      if (content.trim().replace("　", "") === "") {
        throw new Error("メッセージを入力してください。");
      }
      // メッセージIDは一意の値
      this.messageId = Date.now(); // メッセージ番号（昇順）をミリ秒単位のタイムスタンプとして設定
      this.content = content;
      this.userName = userName;
      this.userId = socket.id;
      this.date = new Date();
      this.roomId = roomId;
      this.isUpdate = isUpdate;
      //   //isReplyがtrueの時にのみ、connectedMessageIdを入力する。
      //   this.isReply = isReply;
  
      //   //isReplyがtrueならばconnectedMessageIdにフィールドを入力する。
      //   if (isReply) {
      //     this.connectedMessageId = connectedMessageId;
      //   }
    }
  
    // クライアント側のuserNameと照合する
    isMyMessage(userName) {
      return this.userName === userName;
    }
  
    // メッセージ内容のUpdate
    setContent(content) {
      this.content = content;
      this.isUpdate = true;
    }
  
    // メッセージをオブジェクトとして取得
    getMessageObject() {
      return {
        messageId: this.messageId,
        content: this.content,
        userName: this.userName,
        date: this.date,
        roomId: this.roomId,
        isUpdate: this.isUpdate
      };
    }
  }
  
  export default Message;