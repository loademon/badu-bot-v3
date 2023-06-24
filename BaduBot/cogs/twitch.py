import discord
import aiohttp
import asyncio
import datetime
from discord.ext import commands, tasks
from discord.ui import View, Button
from tiv_config import CONFIG, BaseCog, TwitchAuth


config = CONFIG.live


class Live(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.token = None
        self.notification = None
        self.notification_channel = None
        self.presence = "Not Live"

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__class__.__name__} Ready")

    async def cog_load(self) -> None:
        self.notification_channel = self.bot.get_channel(config.notification_channel_id)
        print(f"{__class__.__name__} loaded")

    async def get_token(self, auth: TwitchAuth) -> str:
        endpoint = "https://id.twitch.tv/oauth2/token"
        body = {
            "client_id": f"{auth.client_id}",
            "client_secret": f"{auth.client_secret}",
            "grant_type": "client_credentials",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(data=body, url=endpoint) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("access_token")
                else:
                    return "None"

    async def get_live(self, token: str, auth: TwitchAuth):
        endpoint = f"https://api.twitch.tv/helix/streams?user_id={auth.channel_id}"
        headers = {"Authorization": f"Bearer {token}", "Client-Id": f"{auth.client_id}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=endpoint) as response:
                if response.status == 401:
                    return None, None
                elif response.status == 200:
                    data = await response.json()
                    data = data["data"]
                    if data == []:
                        return False, None
                    else:
                        return True, data
                else:
                    return False, None

    @tasks.loop(count=None)
    async def live_check(self):
        self.loops.append(self.live_check)
        live, data = await self.get_live(token=self.token, auth=config.auth)
        if live is None:
            self.token = await self.get_token(auth=config.auth)
            return "loop_pass"

        await asyncio.sleep(0.7)

        if live is True and self.notification is False:
            self.notification = True
            embed = discord.Embed(
                color=config.embed.color,
                title=data[0]["title"],
                url=config.embed.twitch_url,
                timestamp=datetime.datetime.now(tz=config.embed.time_zone),
            )
            embed.add_field(
                name=config.embed.game_field, value=data[0]["game_name"], inline=True
            )
            embed.add_field(
                name=config.embed.viewer_field,
                value=data[0]["viewer_count"],
                inline=True,
            )
            embed.set_image(url=config.embed.thumbnail)
            embed.set_author(
                name=config.embed.title,
                url=config.embed.twitch_url,
                icon_url=config.embed.logo,
            )
            embed.set_thumbnail(url=config.embed.logo)
            view = View()
            view.add_item(
                Button(
                    style=discord.ButtonStyle.primary,
                    label=config.embed.go_to_live,
                    url=config.embed.twitch_url,
                    disabled=False,
                )
            )
            await self.notification_channel.send(
                content=f"{config.embed.message}\n{config.embed.twitch_url}",
                embed=embed,
                view=view,
            )

        if live is False and self.notification is True:
            self.notification = False
            embed = discord.Embed(
                color=0xFF0000,
                title=config.embed.end_title,
                description=config.embed.end_message,
            )
            embed.set_image(url=config.embed.logo)
            embed.set_author(
                name=config.embed.channel_name,
                url=config.embed.twitch_url,
                icon_url=config.embed.logo,
            )
            view = View()
            view.add_item(
                Button(
                    style=discord.ButtonStyle.primary,
                    label=config.embed.end_got_to_live,
                    url=f"{config.embed.twitch_url}/videos",
                    disabled=False,
                )
            )
            view.add_item(
                Button(
                    style=discord.ButtonStyle.primary,
                    label=config.embed.go_to_youtube,
                    url=config.embed.youtube,
                    disabled=False,
                )
            )
            await self.notification_channel.send(embed=embed, view=view)

        if live is True and self.presence is "Not Live":
            await self.bot.change_presence(
                activity=discord.Streaming(
                    name=config.live_presence.message, url=config.embed.twitch_url
                )
            )
            self.presence = "Live"

        if live == False and self.presence == "Live":
            activity = discord.Activity(
                type=config.not_live_presence.type,
                name=config.not_live_presence.message,
            )
            self.presence = "Not Live"
            await self.bot.change_presence(
                status=discord.Status.online, activity=activity
            )

    @live_check.before_loop
    async def before_live_check_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Live(bot=bot))
