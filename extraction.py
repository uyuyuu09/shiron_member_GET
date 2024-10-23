import json

member_list = []

def extraction_member(hub_name:str):
    with open(f'output/{hub_name}.json', "r", encoding="utf-8") as member_json:
        all_member_info = json.load(member_json)
    
    for i, member in enumerate(all_member_info, start=1):
        print(f"{str(i).zfill(2)}.{member['name'][4:]}  {member['email']}")
