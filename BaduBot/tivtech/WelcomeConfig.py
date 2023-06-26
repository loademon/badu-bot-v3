from tivtech.dataclass import WelcomeConfig

CONFIG = WelcomeConfig(
    # The image that will be displayed on the right side of the embed. (Thumbnail)
    logo="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png",
    # The ID of the guild where user join will be tracked.
    guild_id=1116432482343080007,
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
)
