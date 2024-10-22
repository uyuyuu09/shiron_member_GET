import requests
import os
from dotenv import load_dotenv
import csv
import pprint
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

TOKEN = os.getenv("TOKEN")
DEFAULT_API = os.getenv("DEFAULT_API")
GET_HUB = os.getenv("GET_HUB")
GET_MEMBER = os.getenv("GET_MEMBER")

# Google Sheets 認証情報
SCOPE = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
# 認証情報ファイルのパスを指定
creds_file = 'credentials.json'  # 認証情報ファイルのパス

# 認証情報を取得
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, SCOPE)
# Google Sheets API に接続
client = gspread.authorize(creds)

def get_all_Hub():
    get_all_hub_url = DEFAULT_API + GET_HUB

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    request = requests.get(get_all_hub_url, headers=headers)
    res = request.json()

    Hub_id = []

    for hub in res:
        Hub_id.append([hub['name'], hub['id']])

    return Hub_id

def get_member_from_Hub_id():
    hubs = get_all_Hub()

    while True:
        try:
            # choice = int(input("どのハブのメンバーを取得しますか？ (番号を入力): "))
            choice = 4
            if 1 <= choice <= len(hubs):
                selected_hub_id = hubs[choice - 1][1]
                break
            else:
                print("無効な番号です。もう一度入力してください。")
        except ValueError:
            print("無効な入力です。番号を入力してください。")

    get_member_url = DEFAULT_API + GET_MEMBER + selected_hub_id

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    request = requests.get(get_member_url, headers=headers)
    res = request.json()

    member_list = []
    for member in res:
        member_list.append([member['name'], member['email']])

    # スプレッドシートに書き込む
    spreadsheet_id = 'あなたのスプレッドシートID'  # スプレッドシートのIDをここに設定
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet('Sheet1')  # シート名を設定

    # メンバー情報をスプレッドシートに書き込む
    worksheet.append_rows(member_list)

    print("メンバー情報がスプレッドシートに書き込まれました。")
    return member_list

get_member_from_Hub_id()