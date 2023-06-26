from tivtech.dataclass import (
    YoutubeConfig,
    YoutubeEmbedConfig,
    timezone,
    timedelta,
    DataBaseConfig,
    DataConfig,
)

CONFIG = YoutubeConfig(
    logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
    channel_id=1116432482972205083,
    uploads_id="UUE3V90t9Ako4rRZH9Qe9gfg",
    api_key="AIzaSyCkMdzfuTd8P3csmaOZnCqfdHRVHQH7Rdo",
    embed=YoutubeEmbedConfig(
        color=0xFF0000,
        viewer_field="İzlenme Sayısı",
        title="Yeni Video Yayında!",
        time_zone=timezone(timedelta(hours=3)),
        go_to_video="Videoya Git",
    ),
    data=DataBaseConfig(
        from_url="redis://localhost",
        data={"Youtube": DataConfig(key="YoutubeLastNotification")},
    ),
)
