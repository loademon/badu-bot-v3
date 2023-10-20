from tivtech.dataclass import YoutubeConfig

CONFIG = YoutubeConfig(
    # Logo URL
    logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
    # YouTube API key
    api_key="AIzaSyCkMdzfuTd8P3csmaOZnCqfdHRVHQH7Rdo",
    # Discord webhook URL
    webhook_url="https://discord.com/api/webhooks/1131651014919991336/2JPbEdQJhvmD-pvwvwesR9A4kGBV2xsjLaMKSkCT_hwBEE4uIumTE9-6JHk3b_IKX1bz",
    # Discord webhook bot name
    webhook_bot_name="Badu Youtube",
    # New video notification message
    new_video_msg="@everyone **Yeni Video Yayında İzlemeyi Unutmayın!**",
    # Feed message warning, without new video notification
    not_entry_msg="Bir feed geldi ancak yeni video bildirimi değil.",
)
