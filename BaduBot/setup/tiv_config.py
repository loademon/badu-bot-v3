from discord.ext import commands, tasks
from discord import ActivityType, PartialEmoji
from dataclasses import dataclass, field
from datetime import timezone, timedelta


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.loops: list[tasks.Loop] = []

    async def cog_unload(self) -> None:
        for loop in self.loops:
            await loop.cancel()


@dataclass
class ActivityConfig:
    type: ActivityType
    message: str


@dataclass
class Command:
    command_name: str
    aliases: list[str] = field(default_factory=list)
    description: str = field(default_factory=str)


@dataclass
class RoleCommands:
    game: Command
    love: Command


@dataclass
class SocialCommands:
    insta: Command
    youtube: Command
    twitch: Command
    reddit: Command


@dataclass
class CommandErrorConfig:
    """For errors that happen in the use of a command."""

    message: str
    delete_after: int


@dataclass
class CogConfig:
    name: str
    is_active: bool


@dataclass
class CogLoadConfig:
    Cogs: list[CogConfig]


@dataclass
class DataConfig:
    key: str


@dataclass
class DataBaseConfig:
    """for Redis"""

    from_url: str
    data: dict[str, DataConfig]


@dataclass
class ErrorConfig:
    CommandNotFound: CommandErrorConfig
    NotOwner: CommandErrorConfig


@dataclass
class ReadyConfig:
    message: str


@dataclass
class SelectOptionsConfig:
    placeholder: str  # Select menu placeholder
    custom_id: str


@dataclass
class SelectCallbackConfig:
    message: str
    ephemeral: bool


@dataclass
class SelectConfig:
    select_options: dict[str, SelectOptionsConfig]
    select_callback: dict[str, SelectCallbackConfig]


@dataclass
class MainConfig:
    api_key: str
    command_prefix: str
    activity: ActivityConfig
    ready: ReadyConfig
    error: ErrorConfig
    cogs: CogLoadConfig


@dataclass
class RoleConfig:
    """The emojis dictionary takes the key as a string (Role Id)."""

    emojis: dict[str, PartialEmoji]
    data_base: DataBaseConfig
    select: SelectConfig
    ready: ReadyConfig
    command: RoleCommands


@dataclass
class EmbedConfig:
    color: int
    footer_text: str


@dataclass
class SocialAccount:
    name: str
    logo: str
    link: str


@dataclass
class AccountsConfig:
    Instagram: SocialAccount
    Twitch: SocialAccount
    YouTube: SocialAccount
    Reddit: SocialAccount


@dataclass
class SocialConfig:
    logo: str
    accounts: AccountsConfig
    channel_id: int
    time_zone: timezone
    allowed_hours: list[int]
    command: SocialCommands
    embed: EmbedConfig


@dataclass
class LiveEmbedConfig:
    color: int
    game_field: str
    viewer_field: str
    channel_name: str  # Your Twitch Channel Name
    title: str  # Live notification embed title
    go_to_live: str  # Go to live button title
    message: str  # Live notification content Ex: @everyone xxx Live!
    end_title: str  # The title of the message to be sent after the broadcast is ended.
    end_got_to_live: str  # Go to live history button title
    end_message: str  # Live Ending notification content Ex: xxx's Live Closed
    go_to_youtube: str  # Go to youtube button title
    logo: str
    twitch_url: str
    thumbnail: str
    youtube: str
    time_zone: timezone


@dataclass
class TwitchAuth:
    client_id: str
    client_secret: str
    channel_id: str


@dataclass
class LiveConfig:
    embed: LiveEmbedConfig
    notification_channel_id: int
    live_presence: ActivityConfig  # Bot status message
    not_live_presence: ActivityConfig  # Bot status message
    auth: TwitchAuth


@dataclass
class WelcomeConfig:
    logo: str
    guild_id: int
    channel_id: int
    join_message: str
    footer_message: str
    color: int


@dataclass
class Config:
    main: MainConfig
    role: RoleConfig
    social: SocialConfig
    live: LiveConfig
    welcome: WelcomeConfig


CONFIG = Config(
    main=MainConfig(
        api_key="MTExNjA2MjQ5NTk1MDUyNDQ0Ng.Gqhjuh.Jnn_1_3G7khdQf_-8febmoWXHQpNC8Dcc36ny0",
        # If add a command that uses a prefix to the bot, the character you add to the beginning.
        # Ex: "!" for !help
        command_prefix="!",
        # Bot's discord status
        activity=ActivityConfig(
            # .playing, .streaming, .listening, .watching
            # Ex: ActivityType.listening
            type=ActivityType.watching,
            # In bot's activity, it appears as message + activity type.
            # Ex: For activity type "watching" if you set this variable to "xxx's video".
            # The bot's activity as "watching xxx's video".
            message="Badu'nun geçmiş yayınını",
        ),
        # To be used in script is ready (in the on_ready event)
        ready=ReadyConfig(message="BaduBOT Hazır"),
        # To be used in Error events
        error=ErrorConfig(
            # If command not found
            CommandNotFound=CommandErrorConfig(
                # returns this message
                # Ex: !xxx + message (!xxx is not command)
                message="komudu geçerli bir komut değil.",
                # How long to wait for the message to be deleted (seconds)
                delete_after=5,
            ),
            # Error returned from commands requesting unauthorized access
            NotOwner=CommandErrorConfig(
                # returns this message
                message="Yasaklı komut",
                # How long to wait for the message to be deleted (seconds)
                delete_after=5,
            ),
        ),
        # Cogs you want to load while the bot is running
        # Warning: If you haven't added any extra Cog or if you don't have any idea about what it is;
        # only change the is_active value!
        cogs=CogLoadConfig(
            # For the Cog you want to be active, set the is_active value to True.
            # For the Cog you want to be inactive, set the is_active value to False.
            Cogs=[
                CogConfig(name="role", is_active=True),
                CogConfig(name="social", is_active=True),
                CogConfig(name="sync", is_active=True),
                CogConfig(name="twitch", is_active=True),
                CogConfig(name="welcome", is_active=True),
                CogConfig(name="youtube", is_active=True),
            ]
        ),
    ),
    role=RoleConfig(
        # You should enter the name and ID of a role and an emoji present on your server.
        # Warning: This part must be modified according to your server!
        # "role_id": PartialEmoji(name="emoji_name", id="emoji_id") or
        # "role_id": ASCII_Emoji
        emojis={
            # Emojis for Game Role Select
            # Emojis for Love Role Select
            "1116432482343080013": "❤️",
        },
        data_base=DataBaseConfig(
            data={
                "Game": DataConfig(key="GameOptions"),
                "Love": DataConfig(key="LoveOptions"),
            },
            from_url="redis://localhost",
        ),
        select=SelectConfig(
            select_options={
                "Game": SelectOptionsConfig(
                    placeholder="Oyun Rollerinizi Bu Menüden Seçebilirsiniz",
                    custom_id="Role-Select",
                ),
                "Love": SelectOptionsConfig(
                    placeholder="İlişki Rollerinizi Bu Menüden Seçebilirsiniz",
                    custom_id="Love-Role-Select",
                ),
            },
            select_callback={
                "Game-Give": SelectCallbackConfig(
                    message="Rol/Roller Başarıyla Eklendi", ephemeral=True
                ),
                "Game-Delete": SelectCallbackConfig(
                    message="Rol/Roller Başarıyla Silindi", ephemeral=True
                ),
                "Love-Give": SelectCallbackConfig(
                    message="Rol/Roller Başarıyla Eklendi", ephemeral=True
                ),
                "Love-Delete": SelectCallbackConfig(
                    message="Rol/Roller Başarıyla Silindi", ephemeral=True
                ),
            },
        ),
        ready=ReadyConfig(message="Role Ready"),
        command=RoleCommands(
            game=Command(command_name="game-role-select"),
            love=Command(command_name="love-role-select"),
        ),
    ),
    social=SocialConfig(
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
    ),
    live=LiveConfig(
        embed=LiveEmbedConfig(
            color=0xFF0000,
            game_field="Oyun",
            viewer_field="İzleyici Sayısı",
            channel_name="BADU_TV",
            # Live Notification embed title
            title="BADU_TV Yayında!",
            go_to_live="Yayına Git",
            message="@everyone Yayın Başladı **Kop Gel**",
            end_title="Her Güzel Şeyin Sonu",
            end_message="Evet, yayının kapanmasını biz de istemezdik ama arada olur böyle şeyler.\nBadu'nun yayın açmasını beklerken ben geçmiş yayınları izliyor olacağım.\n\n**Sen de aşağıdaki butonlardan bana katılabilir veya Youtube'da takılabilirsin!**",
            end_got_to_live="Yayın Geçmişine Git",
            go_to_youtube="Youtube'a Git",
            logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
            twitch_url="https://twitch.tv/BADU_TV",
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
    ),
    welcome=WelcomeConfig(
        # The image that will be displayed on the right side of the embed. (Thumbnail)
        logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
        # The ID of the guild where user join will be tracked.
        guild_id=1116432482343080007    ,
        # The ID of the channel where the welcome message will be sent after the user joins the server.
        channel_id=1116432482972205083,
        # The content of the welcome message. After this message, the user will be mentioned.
        # Ex, if you enter "Welcome to our community"
        # the message will appear as "Welcome to our community @xxx".
        join_message="Aramıza Hoşgeldin",
        # This message will also appear in the footer.
        # Suggested usage: 'I hope you never leave.'
        footer_message="Umarım Hiç Ayrılmazsın",
        # Embed color
        color=0xFF0000,
    ),
)
