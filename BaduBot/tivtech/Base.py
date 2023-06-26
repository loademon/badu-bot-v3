from tivtech.dataclass import commands, tasks
class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.loops: list[tasks.Loop] = []

    async def cog_unload(self) -> None:
        for loop in self.loops:
            await loop.cancel()