# Lamdaで実装したRestAPIの仕様
- エンドポイント: (秘密)
## 関数一覧
### new_room: 実装済み
- 概要：オーナーが新しい部屋を作成する際に実行する関数。ゲームIDと部屋IDを発行し, ゲーム管理テーブルの新しいアイテムとして書き込む。
- Method: POST
- Request:
    ```
    {
        "mode": "new_room",
        "data": {
            "n_mem": 5, //ゲームに参加する人数(int)
            "owner_name": "ゆう"  //オーナーのユーザー名(str)
            }
    }
    ```
- Response：
    ```
    {
        "statusCode": 200,
        "body": "{
            \"room_id\": 754790,
            \"password\": "halkas",
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
                "room_id": 290912,  #入力された部屋ID(int)
                "password": "aahija" #4桁のアルファベット(str)
                "user_name": "みき", #参加者のユーザー名(str)
                }
    }
    ```
- Response:
    - 成功した場合
        ```
        {
            'status': 200,
            'message': "OK"
        }
        ```
    - 失敗した場合
        ```
        // 部屋が見つからない
        {
            'status': 404,
            'message': "RoomID is not found"
        }

        // パスワードが違う
        {
            'status': 401,
            'message': "Password is incorrect"
        }

        // ルームのstate(募集中)が0でない
        {
            'status': 403,
            'message': "Room is not available"
        }

        // ルームが満員
        {
            'status': 403,
            'message': "Room is full"
        }
        
        // ルームに同じユーザー名が既に存在する。
        {
            'status': 409,
            'message': "User name is already used"
        }
        ```

### close_room
- 概要： オーナーがルームをクローズする際の関数。ゲーム管理DBのStateを3にする。
- Method: POST
- Request:
    ```
    {
        "mode": "close_room",
        "data": {
                "room_id": 290912,  #入力された部屋ID(int)
                "owner_name": "みき", #自分(オーナー)のユーザー名(str)
                }
    }
    ```
- Response: 
    - 成功
    ```
    {
        'status': 200,
        'message': "OK"
    }
    ```
    - ユーザー名がオーナーでなかった場合
    ```
    {
        'status': 403,
        'message': "You are not owner"
    }
    ```

### leave_room
- 概要：
- Method: 
- Request:
- Response: 