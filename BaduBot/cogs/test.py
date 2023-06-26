# from pyyoutube import Api

# uploads_id = "UUE3V90t9Ako4rRZH9Qe9gfg"
# api = Api(api_key="AIzaSyCkMdzfuTd8P3csmaOZnCqfdHRVHQH7Rdo")

# while True:
#     playlist = api.get_playlist_items(
#             playlist_id=uploads_id,
#             count=1,
#         )

#     print(playlist.items[0].snippet.resourceId.videoId)
#     video = api.get_video_by_id(video_id=f"{playlist.items[0].snippet.resourceId.videoId}")
#     print(video.items[0].snippet)


import requests
import json

def send_discord_message(webhook_url, message):
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print("Mesaj gönderilemedi. Hata kodu:", response.status_code)
    else:
        print("Mesaj başarıyla gönderildi.")

# Webhook URL'sini ve göndermek istediğiniz mesajı belirtin
webhook_url = "https://discord.com/api/webhooks/1122491924599803944/2G3EDXXIarwoNyoKkrkf8DGhFRqrZKN5GI_sg_zblN_5U1es4qJDQk9Ac98z_qqtsqmi"
message = "Merhaba, bu bir Discord webhook testidir."

# Discord'a mesaj gönderme işlemi
send_discord_message(webhook_url, message)
