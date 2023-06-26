from discord.ext import commands, tasks
from discord import ActivityType, PartialEmoji
from dataclasses import dataclass, field
from datetime import timezone, timedelta

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
class YoutubeEmbedConfig:
    color: int
    viewer_field: str
    title: str
    time_zone: timezone
    go_to_video: str


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
class YoutubeConfig:
    logo: str
    channel_id: int
    uploads_id: str
    api_key: str
    embed: YoutubeEmbedConfig
    data: DataBaseConfig