from discord import TextChannel
from discord.ext import commands, tasks
from tiv_config import BaseCog


class Test(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.inte = 0
        self.channel_id = 1093500895091757087
        self.test_loop.start()
    

    @tasks.loop(seconds=2)
    async def test_loop(self):
        self.loops.append(self.test_loop)
        channel = TextChannel = self.bot.get_channel(self.channel_id)
        await channel.send(f"Test {self.inte}")
        self.inte += 1

    @test_loop.before_loop
    async def before_insta_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(name="restart")
    async def restarts(self,ctx):
        await self.bot.unload_extension("cogs.test")


async def setup(bot:commands.Bot):
    await bot.add_cog(Test(bot=bot))
