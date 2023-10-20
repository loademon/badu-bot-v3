from wordgame.turkish.game import (
    re,  # redis.asyncio as re
    discord,
    setup_game,
    close_game,
    commands,
    handle_game,
)


from wordgame.turkish.utils import (
    MPREFIX,
    parse_words,
)


class WordGame(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.words = parse_words()
        self.r = re.from_url(url="redis://localhost")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Ready")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded")

    @commands.hybrid_command(name="kelime-oyunu")
    @commands.has_permissions(ban_members=True)
    async def word_game(self, ctx: commands.Context):
        await setup_game(redis=self.r, ctx=ctx)

    @commands.hybrid_command(name="kelime-oyunu-bitir")
    @commands.has_permissions(ban_members=True)
    async def close_word_game(self, ctx: commands.Context):
        await close_game(redis=self.r, ctx=ctx)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.id == self.bot.user.id:
            return
        if await self.r.exists(f"KO{msg.channel.id}") and not msg.content.startswith(
            self.bot.command_prefix
        ):
            if not msg.content.startswith(MPREFIX):
                await handle_game(self, msg=msg, redis=self.r)


async def setup(bot: commands.Bot):
    await bot.add_cog(WordGame(bot=bot))
