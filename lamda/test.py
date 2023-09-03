import requests
import json

# 送信するJSONデータ


# new room
"""
data = {
    "mode": "create_room",
    "data": {
        "n_mem": 3, 
        "owner_name": "るき" 
        }
}
"""
"""
# join_room
data = {
    "mode": "join_room",
    "data": {
        "room_id": 676252,
        "password": "wephzj",
        "user_name": "はる"
    }
}
"""
"""
# leave_room
data = {
    "mode": "leave_room",
    "data": {
        "room_id": 385920,
        "user_name": "ゆう"
    }
}
"""

# start_game
data = {
    "mode": "start_game",
    "data": {
        "room_id": 676252,
        "owner_name": "るき",
        "n_hacked": 1
    }
}




        
# APIエンドポイント
url = "https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf"

# JSONデータを含むPOSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスを表示
print(response.status_code)  # ステータスコード
print(response.json())       # レスポンスのJSONデータ

"""
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
"""