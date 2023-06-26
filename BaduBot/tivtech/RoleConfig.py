from tivtech.dataclass import (
    RoleConfig,
    DataBaseConfig,
    DataConfig,
    SelectConfig,
    SelectOptionsConfig,
    SelectCallbackConfig,
    ReadyConfig,
    RoleCommands,
    Command,
)

CONFIG = RoleConfig(
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
)
