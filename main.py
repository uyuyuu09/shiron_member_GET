import requests
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from env.env import TOKEN, DEFAULT_API, GET_HUB, GET_MEMBER, SPREADSHEET_ID, GOOGLE_AUTH_JSON

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
    for i, hub in enumerate(hubs):
        print(f"{i + 1}. {hub[0]} ({hub[1]})")

    while True:
        try:
            choice = int(input("どのハブのメンバーを取得しますか？ (番号を入力): "))
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
    try:
        request = requests.get(get_member_url, headers=headers)
        res = request.json()
        print(res)
    except:
        print("request error")
        return

    member_list = []
    for member in res:
        member_list.append([member['name'], member['email']])

    with open(f"output/{hubs[choice - 1][0]}.json", "w", encoding="utf-8") as member_json:
        json.dump(res, member_json, indent=4, ensure_ascii=False)
    
    # 放送部公式hub用処理, GSSに書き込み
    if choice == 4:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        worksheet = spreadsheet.worksheet('test')
        worksheet.clear()

        for member in member_list:
            if member[1] != "uyuyu.0301@gmail.com":
                worksheet.append_row([member[0][:4], member[0][4:], member[1]])

    print("OK")
    return member_list

get_member_from_Hub_id()