import requests
import json

# 送信するJSONデータ

# new room
data = {
    "mode": "new_room",
    "data": {
        "n_mem": 5, 
        "owner_id": "dahi11e32" 
        }
}



        
# APIエンドポイント
url = "https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf"

# JSONデータを含むPOSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスを表示
print(response.status_code)  # ステータスコード
print(response.json())       # レスポンスのJSONデータ


roomid = response.json()["room_id"]

#join room
data = {
            "mode": "join_room",
            "data": {
                "room_id": roomid,
                "user_id": "aahi11a12"
            }
        }

# JSONデータを含むPOSTリクエストを送信
response = requests.post(url, json=data)
print(response.status_code)  # ステータスコード
print(response.json())       # レスポンスのJSONデータ