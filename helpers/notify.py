import os
ONESIGNAL_APP_ID = os.environ.get('ONESIGNAL_APP_ID')
ONESIGNAL_API_KEY  = os.environ.get('ONESIGNAL_API_KEY')

import requests

api_url = 'https://api.onesignal.com/notifications'
headers = {
    'Accept': 'application/json',
    'Authorization': f'Basic {ONESIGNAL_API_KEY}',
    'Content-Type': 'application/json'
}
def send_notification(title, message, url:None, image:None,priority=10):
    data = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "data": None,
        "contents": {"en":  message},
        "url": url,
        "global_image": "",
        'name':title,
        "android_visibility": "1",
        "huawei_visibility": "1",
        "headings": {
            "en": title
        },
        "big_picture": image,
        "priority": priority
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

