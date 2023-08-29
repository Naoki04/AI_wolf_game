# Lamdaで実装したRestAPIの仕様
- エンドポイント: (秘密)
## 関数一覧
### new_room
- 概要：オーナーが新しい部屋を作成する際に実行する関数。部屋IDを発行し, ゲーム管理DBに書き込む。
- Method: POST
- Request:
    ```
    {
        "mode": "new_room",
        "data": {
            "n_mem": 5, //ゲームに参加する人数
            "owner_id": "dahi11e32"  //オーナーのユーザー識別子
            }
    }
    ```
- Response：
    ```
    {
        "statusCode": 200,
        "body": "{
            \"room_id\": 754790 //発行された部屋ID
            }"
    }
    ```

### join_room
- 概要：既存のルームに対して他のメンバーが参加する場合, そのユーザーIDをゲーム管理DBに書き込む。部屋が溢れていたり, 既にゲームが始まっている, 部屋が存在しない場合はエラーを返す。
- Method: POST
- Request:
    ```
    {
        "mode": "join_room",
        "data": {
                "room_id": 290912,  //入力された部屋ID
                "user_id": "aahi11a12" //ユーザー識別子
                }
    }
    ```
- Response:
    - 成功した場合
        ```
        {
            "statusCode": 200,
            'body': json.dumps({
                    "message": "successfully done"
                    })
        }
        ```