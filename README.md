# AI_wolf
This is an AI assigned-conversational game for 3~8 players. Developped for a Monthly Hackathon by Supporters in Sep 2023.

# ゲーム進行

1. ゲーム開始
      - 条件
        - メンバーが全員集合
        - オーナーがゲーム開始ボタンを押す

2. 質問を投稿（ユーザー1人）
      - ランダムに質問者を選ぶ
      - 質問を投稿「○○さん質問を投稿して下さい」
         - タイマー2分
         - HackedユーザーはAIが回答する
3. 質問に回答（ユーザー全員）
      - タイマー2分に設定
4. 話し合い
      - タイマー3分に設定
5. Judgement Time
     - 「○○さんが駆逐されました」
     - ① ゲームは続行　
         - 「まだ、AIが潜んでいるようです」
         - ⇒　2.質問を投稿へ戻る
     - ② ゲーム終了
         - AI勝利　　「AIに浸食され切ってしまいました」
         - 人間勝利　「AIが全員駆逐されました」
     - 結果発表
         - 人間チーム
         - AIチーム
         
            ⇒　3に戻る