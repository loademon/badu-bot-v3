from tivtech.dataclass import (
    MainConfig,
    ActivityConfig,
    ActivityType,
    ReadyConfig,
    ErrorConfig,
    CommandErrorConfig,
    CogLoadConfig,
    CogConfig,
)

CONFIG = MainConfig(
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
)
