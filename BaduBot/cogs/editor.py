import discord
from discord.ext import commands

import redis.asyncio as redis

from tivtech.EditorConfig import ConfirmButtons, EditorButton


class Editor(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Ready")

    async def cog_load(self) -> None:
        self.bot.add_view(EditorButton())
        self.bot.add_view(ConfirmButtons())
        print(f"{self.__class__.__name__} loaded")

    @commands.hybrid_command(name="editor-iste")
    @commands.is_owner()
    async def editor(self, ctx: commands.Context):
        content = "@everyone"
        embed = discord.Embed(
            color=0xFF0000,
            title="Editör Başvuru Nedir ?",
            description="Youtube ve Youtube Shorts içeriklerimiz için video editör arıyoruz.  Eğlenceli içerikler çıkarmak için yeteneğin varsa bu iş tam olarak sana göre. Karşılığını alacağını asla unutma. Başvurmak için **Başvuru Yap** butonuna tıklaman yeterli.",
        )
        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/loademon/bot-utils/main/Badu_logo.png"
        )

        await ctx.channel.send(
            content=content,
            embed=embed,
            view=EditorButton(),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Editor(bot=bot))
