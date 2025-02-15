from tivtech.dataclass import (
    LiveConfig,
    LiveEmbedConfig,
    timezone,
    timedelta,
    ActivityConfig,
    ActivityType,
    TwitchAuth,
)


CONFIG = LiveConfig(
    embed=LiveEmbedConfig(
        # Color of embed message box
        color=0xFF0000,
        # Tittle of game field
        game_field="İçerik/Oyun",
        # Title of viewer count field
        viewer_field="İzleyici Sayısı",
        # Twitch channel name
        channel_name="BADU_TV",
        # Live Notification embed title
        title="BADU_TV Yayında!",
        # Text of go to live button
        go_to_live="Yayına Git",
        # Live notification message
        message="@everyone Yayın Başladı **Kop Gel**",
        # Live end embed tittle
        end_title="Her Güzel Şeyin Sonu",
        # Live end embed message
        end_message="Evet, yayının kapanmasını biz de istemezdik ama arada olur böyle şeyler.\nBadu'nun yayın açmasını beklerken ben geçmiş yayınları izliyor olacağım.\n\n**Sen de aşağıdaki butonlardan bana katılabilir veya Youtube'da takılabilirsin!**",
        # Go to twitch/videos button text
        end_got_to_live="Yayın Geçmişine Git",
        # Go to youtube button text
        go_to_youtube="Youtube'a Git",
        logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
        twitch_url="https://twitch.tv/BADU_TV",
        # If live goes online, this image sending
        thumbnail="https://raw.githubusercontent.com/loademon/bot-utils/main/yayin_basliyor.png",
        youtube="https://www.youtube.com/@batuhansygili",
        time_zone=timezone(timedelta(hours=3)),
    ),
    notification_channel_id=1116432483538440268,
    live_presence=ActivityConfig(type=ActivityType.streaming, message="Badu_TV"),
    not_live_presence=ActivityConfig(
        type=ActivityType.watching, message="Badu'nun geçmiş yayınını"
    ),
    auth=TwitchAuth(
        client_id="zcsriby5sboppd3eimnwlof3j88hho",
        client_secret="y7t8l0a42fkbqyiduzccqhkttsu32q",
        channel_id="181504421",
    ),
)
