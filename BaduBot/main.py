from discord import Activity, Intents
from tivtech.MainConfig import CONFIG as config
from discord.ext import commands


class BaduBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.command_prefix,
            intents=Intents.all(),
            activity=Activity(type=config.activity.type, name=config.activity.message),
        )

    async def on_ready(self) -> None:
        print(config.ready.message)

    async def on_command_error(
        self, context: commands.Context, e: Exception, /
    ) -> None:
        if e.__class__ == commands.CommandNotFound:
            error = config.error.CommandNotFound
            await context.send(
                f"**{context.message.content.split()[0]}** {error.message}",
                delete_after=error.delete_after,
            )

        if e.__class__ == commands.NotOwner:
            error = config.error.NotOwner
            await context.send(error.message, delete_after=error.delete_after)

    async def setup_hook(self) -> None:
        for cog in config.cogs.Cogs:
            if cog.is_active:
                try:
                    await self.load_extension(f"cogs.{cog.name}")
                except Exception as e:
                    print(str(e))


BaduBot().run(config.api_key)
