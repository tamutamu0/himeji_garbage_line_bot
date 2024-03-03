import plistlib
from datetime import datetime, timedelta
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os
import json

# URL配列の定義
area_urls = [
    "https://admin.gomisuke.jp/app/0083/data/files/1-1/area.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-2/area.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-3/area.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-4/area.plist"
]

calendar_urls = [
    "https://admin.gomisuke.jp/app/0083/data/files/1-1/calendar.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-2/calendar.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-3/calendar.plist",
    "https://admin.gomisuke.jp/app/0083/data/files/1-4/calendar.plist"
]

def download_and_combine_plist_data(urls):
    combined_data = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = plistlib.loads(response.content)
            combined_data.extend(data)
        else:
            print(f"Error downloading data from {url}")
    return combined_data

def find_area_by_name(area_data, search_name):
    return [area['areaID'] for area in area_data if search_name in area['name']]

def find_calendar_events(calendar_data, year_month, area_id):
    for data in calendar_data:
        if data.get('yearMonth') == year_month:
            for area in data.get('areaArray', []):
                if area.get('areaID') == area_id:
                    return area.get('dateDictionary', {})
    return {}

def translate_event_codes_to_trash_types(event_codes, trash_types):
    return [trash_types[code] for code in event_codes.split(',') if code in trash_types]

def load_plist_file(file_path):
    with open(file_path, 'rb') as fp:
        return plistlib.load(fp)

def get_trash_collection_days(calendar_data, year_month, area_id):
    event_codes = find_calendar_events(calendar_data, year_month, area_id)
    trash_types = {'1':'可燃ごみ', '2':'プラごみ', '3':'ミックスペーパー', '4':'粗大ごみ'}
    return {day: translate_event_codes_to_trash_types(codes, trash_types) for day, codes in event_codes.items()}

def send_line_notification(message, user_id):
    """
    LINEに通知を送信する。
    
    :param message: 送信するメッセージの内容
    :param user_id: 通知を送信するユーザーのID
    """
    line_bot_api = LineBotApi(os.environ['LINE_ACCESS_TOKEN'])
    text_message = TextSendMessage(text=message)
    line_bot_api.push_message(user_id, messages=text_message) 


def main():
    print(os.environ['AREA_NAME'])
    area_data = download_and_combine_plist_data(area_urls)
    calendar_data = download_and_combine_plist_data(calendar_urls)

    area_ids = find_area_by_name(area_data, os.environ['AREA_NAME'])
    if not area_ids:
        print(f"areaIDは見つかりませんでした。")
        return

    now = datetime.now()
    year_month = now.strftime('%Y%m')
    trash_collection_days = get_trash_collection_days(calendar_data, year_month, area_ids[0])

    tomorrow = now + timedelta(days=1)
    tomorrow_events = trash_collection_days.get(str(tomorrow.day))

    if tomorrow_events:
        message = f"明日({datetime.now().strftime('%Y-%m-%d')})は、{'、'.join(tomorrow_events)}の収集日です。"
        print(message)
        send_line_notification(message, os.environ['LINE_GROUP_ID'])

def handler(event, context):
    main()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
