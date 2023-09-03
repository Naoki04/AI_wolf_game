# AI_wolf
This is an AI assigned-conversational game for 3~8 players. Developped for a Monthly Hackathon by Supporters in Sep 2023.


## フロントの流れ
- "/" ルート
    - ボタン：新規ルームを作成する / 既存ルームに入室する
    - if 新規ルーム(N_mem, N_hacked, ニックネーム)
        ルームID, パスワードを発行, ゲーム管理表への書き込み(ルームID, N_mem, N_hacked, state, current_mem)
        待合室への移動

    - if 入室処理(ルームIDとパスワード, ニックネーム) \
        ルームに入れるかどうかの問い合わせ(ルームは存在する？参加待ち状態？人数に空きがある？)
        - if room.ok:\
            ゲーム管理DBのcurrent_memの更新, 待合室への移動\
        - else: \
            エラー返す(404 Roomがありません, 503 ルームが参加者募集中ではありません, 503 ルームに空きがありません)


- "/waiting_room/${roomID}" 待合室
    - 表示：RoomID, パスワード, 現在の参加人数, オーナーか参加者かの表示
    - ボタン: 
        - オーナーのみ: 
            - 開始ボタン(人数が揃えば開始可能)\
                Hackedの決定, gaming_roomへの移動, ゲーム管理DBのstateの更新
            - 閉室ボタン\
                参加者への閉室の通知, ルート画面への移動, ゲーム管理DBのstateの更新
        - メンバーのみ:
            - 退出ボタン\
                参加者への通知(〇〇さんが入室しました), ルート画面への移動, ゲーム管理DBのcurrent_memの更新

- "/gaming_room/${roomID}" ゲーム進行室