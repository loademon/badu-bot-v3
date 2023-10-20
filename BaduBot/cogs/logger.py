from tivtech.LogConfig import *
import datetime

import discord
from discord.ext import commands


class Logger(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} Ready")

    async def cog_load(self) -> None:
        print(f"{__class__.__name__} loaded")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel: discord.TextChannel = self.bot.get_channel(MemberJoin.log_channel)
        activities = "\n".join(
            [
                act.name
                for act in member.activities
                if not isinstance(act, discord.CustomActivity)
            ]
        )

        # ------------------------------------------------------------------>
        embed = discord.Embed(
            color=MemberJoin.log_color,
            title=MemberJoin.log_message.format(member.global_name),
            url=DEFAULT_USER_URL.format(member.id),
            timestamp=member.joined_at,
        )
        embed.set_author(
            name="Yeni Üye",
            icon_url=MemberJoin.log_icon,
        )
        embed.add_field(name="Global İsim", value=member.global_name, inline=True)
        embed.add_field(name="Sunucu İsmi", value=member.display_name, inline=True)
        embed.add_field(name="Kullanıcı Adı", value=member.name, inline=True)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(
            name="Önceden Katılım",
            value="✅" if member.flags.did_rejoin else "⛔",
            inline=True,
        )
        embed.add_field(
            name="Karşılama Yönlendirmesi",
            value="✅" if member.flags.completed_onboarding else "⛔",
            inline=True,
        )
        embed.add_field(
            name="Doğrulama Atlama",
            value="✅" if member.flags.bypasses_verification else "⛔",
            inline=True,
        )
        embed.add_field(name="", value="", inline=False)
        embed.add_field(
            name="Bot",
            value="✅" if member.flags.bypasses_verification else "⛔",
            inline=False,
        )

        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text="Katılım Zamanı")

        await channel.send(embed=embed)

    @commands.hybrid_command(name="embed-test")
    async def embedtest(self, ctx: commands.Context):
        embed1 = discord.Embed(url="https://astrixbot.cf").set_image(
            url=ctx.author.display_avatar
        )
        embed2 = discord.Embed(url="https://astrixbot.cf").set_image(
            url=ctx.author.display_avatar
        )
        embed3 = discord.Embed(url="https://astrixbot.cf",description="before - after")
        embed4 = discord.Embed(url="https://astrixbot.cf",description="a")
        await ctx.send(embeds=[embed3, embed4,embed1, embed2])


async def setup(bot: commands.Bot):
    await bot.add_cog(Logger(bot=bot))
