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

def create_room(n_mem, user_name):
    # ゲーム管理テーブルのスキャン
    response = game_manager.scan()
    items = response['Items']
    
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

def main():
    # ゲーム管理テーブルの作成
    ## テーブル作成をAWSマネジメントコンソールで行うとkeyschemaがHASHにならないので, scanで条件指定した際に怒られる。
    #make_game_table()
    #new_item()

    create_room(4, "ゆう")

    #get_item(419211)
    return 0


if __name__ == '__main__':
    main()
