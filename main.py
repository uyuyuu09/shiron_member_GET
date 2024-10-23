import requests
import os
from dotenv import load_dotenv
import csv
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

TOKEN = os.getenv("TOKEN")
DEFAULT_API = os.getenv("DEFAULT_API")
GET_HUB = os.getenv("GET_HUB")
GET_MEMBER = os.getenv("GET_MEMBER")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

SCOPE = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']

GOOGLE_AUTH_JSON = os.getenv('GOOGLE_AUTH_JSON')

creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_AUTH_JSON, SCOPE)
client = gspread.authorize(creds)

def get_all_Hub():
    get_all_hub_url = DEFAULT_API + GET_HUB

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    request = requests.get(get_all_hub_url, headers=headers)
    res = request.json()
    with open('output/all_hub.json', "w", encoding="utf-8") as all_hub_json:
        json.dump(res, all_hub_json, indent=4, ensure_ascii=False)

    Hub_id = []

    for hub in res:
        Hub_id.append([hub['name'], hub['id']])
    with open('output/hub_id.json', "w", encoding="utf-8") as hub_id_json:
        json.dump(Hub_id, hub_id_json, indent=4, ensure_ascii=False)

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
    print(res)

    with open('output/member.json', "w", encoding="utf-8") as member_json:
        json.dump(res, member_json, indent=4, ensure_ascii=False)

    member_list = []
    for member in res:
        member_list.append([member['name'], member['email']])

    spreadsheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet('test')
    worksheet.clear()
    worksheet.append_rows(member_list)

    print("OK")
    return member_list

get_member_from_Hub_id()