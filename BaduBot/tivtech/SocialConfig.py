from tivtech.dataclass import (
    SocialConfig,
    AccountsConfig,
    SocialAccount,
    timezone,
    timedelta,
    SocialCommands,
    Command,
    EmbedConfig,
)

CONFIG = SocialConfig(
    # The logo/icon that will be displayed in the author section of embed messages.
    logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badubot_logo.png",
    accounts=AccountsConfig(
        Instagram=SocialAccount(
            name="Instagram",
            logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Instagram_logo.png",
            link="https://www.instagram.com/batuhansygili/",
        ),
        Twitch=SocialAccount(
            name="Twitch",
            logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Twitch_logo.png",
            link="https://www.twitch.tv/badu_tv",
        ),
        YouTube=SocialAccount(
            name="YouTube",
            logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Youtube_logo.png",
            link="https://www.youtube.com/@batuhansygili",
        ),
        Reddit=SocialAccount(
            name="Reddit",
            logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Reddit_logo.png",
            link="https://www.reddit.com/r/BaduveSipahileri/",
        ),
    ),
    # The ID of the message channel where social links will be posted at intervals.
    channel_id=1116432483538440268,
    # Timezone your country
    # Ex: Change the hours to 3 for UTC+3
    time_zone=timezone(timedelta(hours=3)),
    allowed_hours=[10, 22],
    command=SocialCommands(
        # The "command_name" parameter represents the command name used to invoke the selected social media account when called.
        # It also specifies the name displayed for the slash command.
        # The "aliases" parameter specifies alternative command names for prefix commands.
        insta=Command(
            command_name="insta",
            aliases=["instagram", "Insta", "Instagram"],
            description="Kullanıldığı Kanala Instagram Hesap Bağlantısını Yollar",
        ),
        youtube=Command(
            command_name="youtube",
            aliases=["yt", "YouTube", "Youtube"],
            description="Kullanıldığı Kanala YouTube Hesap Bağlantısını Yollar",
        ),
        twitch=Command(
            command_name="twitch",
            aliases=["tw", "Twitch"],
            description="Kullanıldığı Kanala Twitch Hesap Bağlantısını Yollar",
        ),
        reddit=Command(
            command_name="reddit",
            description="Kullanıldığı Kanala Reddit Hesap Bağlantısını Yollar",
        ),
    ),
    embed=EmbedConfig(
        color=0xFF0000,
        # {} this is your media name. Footer_text is media announcement message
        footer_text="Yukarıdaki linkten {} hesabına ulaşabilirsiniz. Takip Etmeyi Unutmayın!",
    ),
)
