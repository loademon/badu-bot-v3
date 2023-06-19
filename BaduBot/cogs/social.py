import discord
from discord.ext import commands, tasks
from discord.ext import commands
from tiv_config import CONFIG, BaseCog, SocialAccount
import datetime

config = CONFIG.social


intents = discord.Intents.all()

timezone = config.time_zone
allowed_hours = config.allowed_hours
command = config.command
accounts = config.accounts


datetimes = [
    datetime.time(hour=hour, minute=0, tzinfo=timezone) for hour in allowed_hours
]


class Social(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.loop_done_datetimes = []
        self.social_loop.start()

    def embed_create(self, media: SocialAccount) -> discord.Embed:
        embed = discord.Embed(
            color=config.embed.color,
            title=media.name,
            description=media.link,
            url=media.link,
            timestamp=datetime.datetime.now(
                tz=config.time_zone
            ),
        )
        embed.set_thumbnail(url=media.logo)
        embed.set_footer(
            text=config.embed.footer_text.format(media.name),
            icon_url=config.logo,
        )
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Ready")

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded")

    @tasks.loop(time=datetimes)
    async def social_loop(self):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_datetime not in self.loop_done_datetimes:
            self.loop_done_datetimes.append(current_datetime)
            if current_time in [time.strftime("%H:%M") for time in datetimes]:
                embed = self.embed_create(media=config.accounts.Instagram)
                channel: discord.TextChannel = self.bot.get_channel(config.channel_id)
                try:
                    await channel.send(embed=embed)
                except:
                    pass

                if len(self.loop_done_datetimes) > 60:
                    del self.loop_done_datetimes[:45]

    @social_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_command(
        name=command.insta.command_name, aliases=command.insta.aliases,help=command.insta.description
    )
    async def insta(self, ctx: commands.Context):
        await ctx.send(embed=self.embed_create(media=accounts.Instagram))

    @commands.hybrid_command(
        name=command.youtube.command_name, aliases=command.youtube.aliases
    )
    async def youtube(self, ctx: commands.Context):
        await ctx.send(embed=self.embed_create(media=accounts.YouTube))

    @commands.hybrid_command(
        name=command.twitch.command_name, aliases=command.twitch.aliases
    )
    async def twitch(self, ctx: commands.Context):
        await ctx.send(embed=self.embed_create(media=accounts.Twitch))

    @commands.hybrid_command(
        name=command.reddit.command_name, aliases=command.reddit.aliases
    )
    async def reddit(self, ctx: commands.Context):
        await ctx.send(embed=self.embed_create(media=accounts.Reddit))


async def setup(bot: commands.Bot):
    await bot.add_cog(Social(bot=bot))
