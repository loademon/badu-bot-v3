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
class Config:
    main: MainConfig
    role: RoleConfig
    social: SocialConfig


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
            insta=Command(
                command_name="insta", aliases=["instagram", "Insta", "Instagram"]
            ),
            youtube=Command(command_name="youtube", aliases=["yt", "YouTube", "Youtube"]),
            twitch=Command(command_name="twitch", aliases=["tw", "Twitch"]),
            reddit=Command(command_name="reddit"),
        ),
        embed=EmbedConfig(
            color=0xFF0000,
            # {} this is your media name. Footer_text is media announcement message
            footer_text="Yukarıdaki linkten {} hesabına ulaşabilirsiniz. Takip Etmeyi Unutmayın!"
        )
    ),
)
