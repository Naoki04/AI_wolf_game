# 本サービスで使うDynamoDBのTableについて
参考: https://www.wakuwakubank.com/posts/639-aws-dynamodb-introduction/

## game_manager(ゲーム管理テーブル)
1ゲームを1行で管理するテーブル。ゲームの進行状態などを記録する。
- RoomID: ランダムな6桁の整数。
- Password: ６桁のアルファベット
- N_mem: そのゲームに参加する人数(3~8人)
- Members: []
- N_hacked: 人数(1~参加者の半数未満)
- Hacked: []
- State: ゲームの状態
    - 0: 募集中
    - 1: ゲーム中
    - 2: ゲーム終了
    - 3: ゲーム取り消し・中断
- CreatedAt: ゲームが作成された時刻(yyyymmdd-hh-mm-ss形式で文字列)

|Partiation Key|Attribute|Attribute|Attribute|Attribute|Attribute|Attribute|Attribute|
|--|--|--|--|--|--|--|--|
|RoomID(int)|Password(str)|n_mem(int)|Members(str list)|N_hacked(int)|Hacked(str list)|State(int)|Created-at|
|201301|"djakdl"|3|[""]|1|[""]|0|"20130912-12-31-01"|
|312001|"alfkl"|5|[""]|2|[""]|0|"20130912-12-34-01"|


## 質問テーブル
事前に用意した質問から出題するモードで使う質問を格納しておくテーブル
