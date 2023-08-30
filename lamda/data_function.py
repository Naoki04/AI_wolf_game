import boto3
from datetime import datetime
import random

# ゲーム管理DB
game_manager = boto3.resource('dynamodb').Table('game_manager')


def scan_game_manager():
    response = game_manager.scan()
    items = response['Items']
    #print(items)
    return items
    
    
# 新しいゲームを登録する関数
def add_new_game(ownerid, n_mem):
    # ゲーム管理テーブルのスキャン
    table = scan_game_manager()
    
    # ゲームIDの発行
    max_game_id = max(item['GameID'] for item in table)
    gameid = max_game_id + 1
    
    # ルームIDの発行
    ## 既存のルームIDのリスト化
    existing_room_ids = [item['RoomID'] for item in table]
    # ランダムなルームIDの作成とかぶりの確認
    roomid = random.randint(100000, 999999)
    while (roomid in existing_room_ids):
        roomid = random.randint(100000, 999999)
    
    # 現在の日時を取得
    current_datetime = datetime.now()
    # 日時を指定したフォーマットに変換
    timestamp = current_datetime.strftime("%Y%m%d-%H-%M-%S")
    
    # その他の属性
    userids = []
    state = 0

    # テーブルへのアイテムの追加
    game_manager.put_item(
        Item = {
            'GameID': gameid,
            'RoomID': roomid,
            'N_mem': n_mem,
            'OwnerID': ownerid,
            'UserIDs': userids,
            'State': state,
            'CreatedAt': timestamp,
        }
    )
    return int(roomid), int(gameid)
    