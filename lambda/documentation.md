# Lamdaで実装したRestAPIの仕様
- エンドポイント: (秘密)
## 関数一覧

### create_room:
- 概要：オーナーが新しい部屋を作成する際に実行する関数。ゲームIDと部屋IDを発行し, ゲーム管理テーブルの新しいアイテムとして書き込む。
- Method: POST
- Request:
    ```
    {
        "mode": "create_room",
        "data": {
            "n_mem": 5, //ゲームに参加する人数(int)
            "owner_name": "ゆう"  //オーナーのユーザー名(str)
            }
    }
    ```
- Response：
    ```
    {
        'statusCode': 200,
        "body": json.dumps({
            'message': "OK", 
            "roomid": 827912, 
            "password": "asakfj"})
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
            'statusCode': 200,
            "body": json.dumps({'message': "OK"})
        }
        ```
    - 失敗した場合
        ```
        // 部屋が見つからない
        {
            'statusCode': 404,
            "body": json.dumps({'message': "RoomID is not found"})
        }

        // パスワードが違う
        {
            'statusCode': 401,
            "body": json.dumps({'message': "Password is incorrect"})
        }

        // ルームのstate(募集中)が0でない
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not available"})
        }

        // ルームが満員
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is full"})
        }
        
        // ルームに同じユーザー名が既に存在する。
        {
            'statusCode': 409,
            "body": json.dumps({'message': "User name is already used"})
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
        'statusCode': 200,
        "body": json.dumps({'message': "OK"})
    }
    ```
    - ユーザー名がオーナーでなかった場合
    ```
    {
        'statusCode': 403,
        "body": json.dumps({'message': "You are not owner"})
    }
    ```

### leave_room
- 概要：waiting状態の時に参加者が部屋から退出する関数。オーナーは退出できない。
- Method: POST
- Request:
    ```
    {
        "mode": "leave_room",
        "data": {
                "room_id": 290912,  
                "user_name": "みき", #自分(参加者)のユーザー名(str)
                }
    }
    ```
- Response: 
    -   成功
        ```
        {
            'statusCode': 200,
            "body": json.dumps({'message': "OK"})
        }
        ```
    - 失敗
        ```
        # 部屋が存在しない場合
        {
            'statusCode': 404,
            "body": json.dumps({'message': "User name is not found"})
        }
        # オーナーだった場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "You are owner, so you cannot leave the room"})
        }
        # 部屋が待ち状態ではない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Waiting Mode"})
        }
        ```

### start_game
- 概要：条件(人数, state)が揃えば実行可能。n_hackedの人数を指定し, ゲームを開始する。Hackedを指定する。
- Method: POST
- Request: 
    ```
    {
        "mode": "start_game",
        "data": {
                "room_id": 290912,  #入力された部屋ID(int)
                "owner_name": "ゆう",
                "n_hacked": 1, #Hackedの人数(1以上, N_memの半分未満)
                }
    }
    ```
- Response: 
    - 成功
        ```
        {
            'statusCode': 200,
            "body": json.dumps({'message': "OK", "hacked": hacked})
        }
        ```
    - 失敗
        ```
        # オーナーじゃない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "You are not owner"})
        }
        # ルームの状態が待ち状態じゃない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Waiting Mode"})
        }
        # メンバー数がn_memに達していない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not full"})
        }
        # n_hackedが既定のレンジ外の場合(レンジ：1以上, n_memの半数未満)
        {
            'statusCode': 403,
            "body": json.dumps({'message': "n_hacked is out of range"})
        }
        ```

### get_room_info
- 概要：ルームIDに対して、参加者, ゲームの状態などを返す
- Method: POST
- Request: 
    ```
    {
        "mode": "get_room_info",
        "data": {
                "room_id": 290912,  #部屋ID(int)
                }
    }
    ```
- Response: 
    - 成功
        ```
        {
            'statusCode': 200,
            "body": json.dumps({
                    'message': "OK", 
                    "room_info": {
                        "RoomID": 123456, 
                        "Password": "akdjak",
                        "Created-at": "yyyymmdd-hh-mm-ss", 
                        "N_mem": 4,
                        "Current_mem": 4, 
                        "Members": ["ゆう", "みく", "はるか", "よう"], #先頭がオーナー
                        "N_hacked": 1,
                        "Hacked": ["よう"]
                        "Dead": ["みく"]
                        "GameState": 1, # 0:メンバー募集中, 1:ゲーム進行中, 2: ゲーム終了, 3: ゲーム中断
                        }
                }),
        }
        ```

### end_game
- 概要：ゲームが正常に終了した際, DBのGameStateを更新する
- Method: POST
- Request: 
    ```
    {
        "mode": "end_game",
        "data": {
                "room_id": 290912,  #部屋ID(int)
                }
    }
    ```
- Response: 
    - 成功
        ```
        {
            'statusCode': 200,
            "body": json.dumps({'message': "OK"}),
        }
        ```
    - 失敗
        ```
        # ルームがゲーム中ではない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Game Mode"}),
        }
        ```

### add_dead
- 概要：DBのDead属性に死亡判定のユーザーを追加する
- Method: POST
- Request: 
    ```
    {
        "mode": "add_dead",
        "data": {
                "room_id": 290912,  #入力された部屋ID(int)
                "user_name": "ゆう", #deadに追加する人
                }
    }
    ```
- Response: 
    - 成功
        ```
        {
        'statusCode': 200,
        "body": json.dumps({'message': "OK"}),
        }
        ```
    - 失敗
        ```
        # ゲームが進行中でない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Game Mode"}),
        }
        # ルーム内に指定のユーザー名がない場合
        {
            'statusCode': 404,
            "body": json.dumps({'message': "User name is not found in the room"}),
        }

### get_ai_answer
- 概要：特定のHackedを担当するChatGPTに質問に対する回答をさせる。ChatGPTに入力するmessages(人格の設定や過去の会話履歴を格納)はゲーム管理DBのAI_msgsに辞書型(キーは担当のユーザー名)で格納されている。get_ai_answerが呼ばれると、指定されたHacked担当のmsgに質問を追加した上で、ChatGPT APIを呼び出し、その回答もmsgに格納してDBに保存する。
- Method: POST
- Request: 
    ```
    {
        "mode": "get_ai_answer",
        "data": {
                "room_id": 290912,  #ゲーム中の部屋のID
                "user_name": "ゆう", #Hackedのユーザーネーム
                "question": "好きな食べ物は？" #質問内容
                }
    }
    ```
- Response: 
    - 成功
        ```
        {
        'statusCode': 200,
        "body": json.dumps({'message': 'OK', 'answer': '優しい人'}),
        }
        ```
    - 失敗
        ```
        # ユーザー名がHackedでない場合
        {
            'statusCode': 404,
            "body": json.dumps({'message': "User name is not found in the room"}),
        },
        # ルームがゲームモードでない場合
        {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Game Mode"}),
        },
        
        ```
    - 補足：AI-msgsの中身は以下のようになっている。
    ```
    AI-msgs = {
        "ゆい": messages1,
        "はる": messages2
        }

    messages1=[
        {
            "role": "system",
            "content": "あなたは20代前半女性で、友達とアイスブレイクゲームをしています。簡単なクイズに対して、簡潔に答えます。必ずしも文章で答える必要はありません。敬語は禁止で、できれば体現止めで答えてください。'答え：'などの形式も不要です。AIであると気づかれないように回答してください。です、ますは禁止です。"
        },
        
        {
            "role": "user",
            "content": "好きなタイプは"
        },
        {
            "role": "assistant",
            "content": "まじめで素直な人。"
        },
        {
            "role": "user",
            "content": "好きな食べ物は"
        },
        {
            "role": "assistant",
            "content": "寿司"
        },
    ]

    message2=[
        {
            "role": "system",
            "content": "あなたは70代男性で、友達とアイスブレイクゲームをしています。簡単なクイズに対して、簡潔に答えます。必ずしも文章で答える必要はありません。敬語は禁止で、できれば体現止めで答えてください。'答え：'などの形式も不要です。AIであると気づかれないように回答してください。です、ますは禁止です。"
        },
        
        {
            "role": "user",
            "content": "好きなタイプは"
        },
        {
            "role": "assistant",
            "content": "優しい人"
        },
        {
            "role": "user",
            "content": "好きな食べ物は"
        },
        {
            "role": "assistant",
            "content": "佃煮"
        },
    ]

    ```