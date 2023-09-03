import boto3
import credentials
import random
from datetime import datetime
import string
import json

table_name = 'game_manager_2'

dynamodb = boto3.resource(
        "dynamodb", 
        region_name='ap-northeast-3',
        aws_access_key_id=credentials.aws_access_key,
        aws_secret_access_key=credentials.aws_secret_key,
        #aws_session_token='YOUR_SESSION_TOKEN
        )
game_manager = dynamodb.Table(table_name)

def make_game_table():
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'RoomID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'RoomID',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def new_item():
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'RoomID': 419211,
            'Password': "alaksa",
            'N_mem': 4,
            'Members': ["asae", "asda"],
            'N_hacked': 1,
            'Hacked': [],
            'GameState': 0,
            'Created-at': '20230931-09-12-43',
            'Current_mem': len([])
        }
    )
    return  0

# ゲーム管理テーブルの全項目取得
def scan_game_manager():
    response = game_manager.scan()
    items = response['Items']
    return  items

def create_room(n_mem, user_name):
    # ゲーム管理テーブルのスキャン
    items = scan_game_manager()
    
    # ルームIDの発行
    ## 既存のルームIDのリスト化
    existing_room_ids = [item['RoomID'] for item in items]
    # ランダムなルームIDの作成とかぶりの確認
    roomid = random.randint(100000, 999999)
    while (roomid in existing_room_ids):
        roomid = random.randint(100000, 999999)

    # パスワード(６桁string)の発行
    alphabet = string.ascii_lowercase  # 小文字のアルファベット
    password = ''.join(random.choice(alphabet) for _ in range(6))   
    
    # 現在の日時を取得
    current_datetime = datetime.now()
    # 日時を指定したフォーマットに変換
    timestamp = current_datetime.strftime("%Y%m%d-%H-%M-%S")
    
    # その他の属性
    members = [user_name]
    gamestate = 0

    # テーブルへのアイテムの追加
    game_manager.put_item(
        Item = {
            'RoomID': roomid,
            'Password': password,
            'N_mem': n_mem,
            'Members': members,
            'N_hacked': 1,
            'Hacked': [],
            'GameState': gamestate,
            'Created-at': timestamp,
            'Current_mem': len(members),
        }
    )
    print("Room Created| roomid:", roomid, ", password:", password)
    response = {
        'statusCode': 200,
        "body": json.dumps({'message': "OK", "roomid": roomid, "password": password})
    }
    return response


def get_item(roomid):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'RoomID': roomid,
        }
    )
    item = response['Item']
    #print(item)
    return item


def join_room(roomid, password, user_name):
    # ゲーム管理テーブルのスキャン
    items = scan_game_manager()

    # ルームIDの存在確認
    existing_room_ids = [item['RoomID'] for item in items]
    if roomid not in existing_room_ids:
        print("RoomID", roomid, "is not found")
        response = {
            'statusCode': 404,
            "body": json.dumps({'message': "RoomID is not found"})
        }
        return response
    # 該当ルーム情報の取得
    room_info = [item for item in items if item['RoomID'] == roomid][0]
    # パスワードの確認
    if room_info['Password'] != password:
        print("Password is incorrect")
        response = {
            'statusCode': 401,
            "body": json.dumps({'message': "Password is incorrect"})
        }
        return response
    # GameStateの確認
    if room_info['GameState'] != 0:
        print("Room is not available")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not available"})
        }
        return response
    # メンバー数の確認
    if room_info['Current_mem'] >= room_info['N_mem']:
        print("Room is full")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is full"})
        }
        return response
    # 名前の重複確認
    if user_name in room_info['Members']:
        print("User name is already used")
        response = {
            'statusCode': 409,
            "body": json.dumps({'message': "User name is already used"})
        }
        return response
    # メンバーの追加
    members = room_info['Members']
    members.append(user_name)

    # データベースの更新
    game_manager.update_item(
        Key={
            'RoomID': roomid,
        },
        UpdateExpression='SET Members = :val1, Current_mem = :val2',
        ExpressionAttributeValues={
            ':val1': members,
            ':val2': len(members),
        }
    )
    print(user_name, "joined", roomid)
    response = {
        'statusCode': 200,
        "body": json.dumps({'message': "OK"})
    }
    return response
    
def close_room(roomid, owner_name):
    # 該当ルーム情報の取得
    room_info = get_item(roomid)
    # オーナー名の確認
    if room_info['Members'][0] != owner_name:
        print("You are not owner")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "You are not owner"})
        }
        return response
    
    # GameStateの更新(3: 取り消し)
    game_manager.update_item(
        Key={
            'RoomID': roomid,
        },
        UpdateExpression='SET GameState = :val1',
        ExpressionAttributeValues={
            ':val1': 3,
        }
    )
    print("Room", roomid, "is closed by owner")
    response = {
        'statusCode': 200,
        "body": json.dumps({'message': "OK"})
    }
    return response

def leave_room(roomid, user_name):
    # 該当ルーム情報の取得
    room_info = get_item(roomid)
    # メンバーの確認
    if user_name not in room_info['Members']:
        print("User name is not found in the room")
        response = {
            'statusCode': 404,
            "body": json.dumps({'message': "User name is not found"})
        }
        return response
    # オーナーでないことの確認
    if user_name == room_info['Members'][0]:
        print("You are owner, so you cannot leave the room")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "You are owner, so you cannot leave the room"})
        }
        return response
    
    # GameStateの確認
    if room_info['GameState'] != 0:
        print("Room is not in Waiting Mode")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Waiting Mode"})
        }
        return response
    # メンバーの削除
    members = room_info['Members']
    members.remove(user_name)
    # データベースの更新
    game_manager.update_item(
        Key={
            'RoomID': roomid,
        },
        UpdateExpression='SET Members = :val1, Current_mem = :val2',
        ExpressionAttributeValues={
            ':val1': members,
            ':val2': len(members),
        }
    )
    print(user_name, "left room", roomid)
    response = {
        'statusCode': 200,
        "body": json.dumps({'message': "OK"})
    }
    return response


def start_game(roomid, owner_name, n_hacked):
    # 部屋の情報を取得
    room_info = get_item(roomid)
    # オーナー名の確認
    if room_info['Members'][0] != owner_name:
        print("You are not owner")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "You are not owner"})
        }
        return response
    # GameStateの確認
    if room_info['GameState'] != 0:
        print("Room is not in Waiting Mode")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not in Waiting Mode"})
        }
        return response
    # メンバー数の確認
    if room_info['Current_mem'] != room_info['N_mem']:
        print("Room is not full")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "Room is not full"})
        }
        return response
    # n_hackedの数の確認
    if n_hacked >= room_info['N_mem']/2 or n_hacked <= 0:
        print("n_hacked is out of range")
        response = {
            'statusCode': 403,
            "body": json.dumps({'message': "n_hacked is out of range"})
        }
        return response
    
    # Hackedの選択
    members = room_info['Members']
    hacked = random.sample(members, n_hacked)
    # GameStateの更新(1: ゲーム中)
    game_manager.update_item(
        Key={
            'RoomID': roomid,
        },
        UpdateExpression='SET GameState = :val1, Hacked = :val2',
        ExpressionAttributeValues={
            ':val1': 1,
            ':val2': hacked,
        }
    )
    print("Game started in room", roomid, "| Hacked:" ,hacked)
    response = {
        'statusCode': 200,
        "body": json.dumps({'message': "OK", "hacked": hacked})
    }
    return response
    

