import requests
import redis
from discord import SyncWebhook
from tivtech.WebhookConfig import CONFIG as config
from flask import Flask, request
import xmltodict

app = Flask(__name__)
r = redis.Redis()


@app.route("/feed", methods=["GET", "POST"])
def feed():
    challenge = request.args.get("hub.challenge")

    if challenge:
        return challenge

    data = xmltodict.parse(request.data)

    try:
        video_link = data["feed"]["entry"]["link"]["@href"]
        video_id: str = data["feed"]["entry"]["id"]
        video_id = video_id.split(":")[2]
        head = requests.head(url=f"https://www.youtube.com/shorts/{video_id}")

    except:
        video_link = False
        pass

    if (
        video_link
        and not r.sismember("youtube_list", video_id)
        and head.status_code == 303
    ):
        r.sadd("youtube_list", video_id)
        webhook = SyncWebhook.from_url(url=config.webhook_url)
        webhook.send(
            content=f"{config.new_video_msg}\n{video_link}",
            username=config.webhook_bot_name,
            avatar_url=config.logo,
        )

    elif head.status_code == 200:
        print("Shorts bu hacı")
        # TODO: Log kanalı muhabbeti

    else:
        print(f"{config.not_entry_msg}")  # TODO: Bot Log kanalına atılacak bildirim.
        pass

    return "", 204


app.run(host="0.0.0.0", port=5000)
