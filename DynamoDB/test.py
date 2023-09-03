import boto3
import credentials
import random
from datetime import datetime
import string

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
            'State': 0,
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
    state = 0

    # テーブルへのアイテムの追加
    game_manager.put_item(
        Item = {
            'RoomID': roomid,
            'Password': password,
            'N_mem': n_mem,
            'Members': members,
            'N_hacked': 1,
            'Hacked': [],
            'State': state,
            'Created-at': timestamp,
            'Current_mem': len(members),
        }
    )
    print("Room Created| roomid:", roomid, ", password:", password)
    return int(roomid), password


def get_item(roomid):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'RoomID': roomid,
        }
    )
    item = response['Item']
    print(item)
    return item


def join_room(roomid, password, user_name):
    # ゲーム管理テーブルのスキャン
    items = scan_game_manager()

    # ルームIDの存在確認
    existing_room_ids = [item['RoomID'] for item in items]
    if roomid not in existing_room_ids:
        print("RoomID", roomid, "is not found")
        response = {
            'status': 404,
            'message': "RoomID is not found"
        }
        return response
    # 該当ルーム情報の取得
    room_info = [item for item in items if item['RoomID'] == roomid][0]
    # パスワードの確認
    if room_info['Password'] != password:
        print("Password is incorrect")
        response = {
            'status': 401,
            'message': "Password is incorrect"
        }
        return response
    # メンバー数の確認
    if room_info['Current_mem'] >= room_info['N_mem']:
        print("Room is full")
        response = {
            'status': 403,
            'message': "Room is full"
        }
        return response
    # 名前の重複確認
    if user_name in room_info['Members']:
        print("User name is already used")
        response = {
            'status': 409,
            'message': "User name is already used"
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
        'status': 200,
        'message': "OK"
    }
    return response
    


def main():
    # ゲーム管理テーブルの作成
    ## テーブル作成をAWSマネジメントコンソールで行うとkeyschemaがHASHにならないので, scanで条件指定した際に怒られる。
    #make_game_table()
    #new_item()
    #get_item(419211)

    #create_room(4, "ゆう")

    join_room(390296, "jcamvr", "めい")
    return 0


if __name__ == '__main__':
    main()
