import pickle
import asyncio
from typing import Any
from tiv_config import CONFIG

import discord
from discord.ext import commands
from discord.ui import View, Select
import redis.asyncio as redis

config = CONFIG.role
emojis = config.emojis


async def async_dumps(obj: list[discord.SelectOption]):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pickle.dumps, obj)


async def async_loads(obj: Any):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pickle.loads, obj)


class LoveRoleView(View):
    def __init__(self, option):
        super().__init__(timeout=None)
        self.add_item(LoveRoleSelect(option=option))


class LoveRoleSelect(Select):
    def __init__(self, option):
        options = option
        love = config.select.select_options["Love"]
        super().__init__(placeholder=love.placeholder, custom_id=love.custom_id,
                         options=options, max_values=len(options) if option else 1)

    async def callback(self, interaction: discord.Interaction) -> None:
        love_give = config.select.select_callback["Love-Give"]
        love_delete = config.select.select_callback["Love-Delete"]
        for role in self.values:
            obj: discord.Role = interaction.guild.get_role(int(role))
            if obj in self.values:
                await interaction.user.remove_roles(obj)
                try:
                    await interaction.response.send_message(content=love_delete.message,
                                                            ephemeral=love_delete.ephemeral)
                except:
                    pass
            else:
                await interaction.user.add_roles(obj)
                try:
                    await interaction.response.send_message(content=love_give.message,
                                                            ephemeral=love_give.ephemeral)
                except:
                    pass

            options = self.options
            await interaction.message.edit(view=LoveRoleView(option=options))


class RoleView(View):
    def __init__(self, option):
        super().__init__(timeout=None)
        self.add_item(RoleSelect(option=option))


class RoleSelect(Select):
    def __init__(self, option):
        options = option
        game = config.select.select_options["Game"]
        super().__init__(placeholder=game.placeholder, custom_id=game.custom_id,
                         options=options, max_values=len(options) if option else 1)

    async def callback(self, interaction: discord.Interaction) -> None:
        game_give = config.select.select_callback["Game-Give"]
        game_delete = config.select.select_callback["Game-Delete"]
        for role in self.values:
            obj: discord.Role = interaction.guild.get_role(int(role))
            if obj in interaction.user.roles:
                await interaction.user.remove_roles(obj)
                try:
                    await interaction.response.send_message(content=game_delete.message,
                                                            ephemeral=game_delete.ephemeral)
                except:
                    pass
            else:
                await interaction.user.add_roles(obj)
                try:
                    await interaction.response.send_message(content=game_give.message,
                                                            ephemeral=game_give.ephemeral)
                except:
                    pass
            options = self.options
            await interaction.message.edit(view=RoleView(option=options))


class Role(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.r = redis.from_url(config.data_base.from_url)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            print(config.ready.message)
            await self.r.select(1)
            stroptions = await self.r.get(name=config.data_base.data["Game"].key)
            option = await async_loads(stroptions)
            self.bot.add_view(RoleView(option=option))
            stroptions = await self.r.get(name=config.data_base.data["Love"].key)
            option = await async_loads(stroptions)
            self.bot.add_view(LoveRoleView(option=option))
        except:
            pass

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded")

    @commands.command(name=config.command.game.command_name)
    async def game_roles(self, ctx: commands.Context):
        roles = ctx.message.content.split(" ")[1:]
        options = [discord.SelectOption(label=ctx.guild.get_role(role_id=int(role.replace(
            '<@&', '').replace('>', ''))).name, value=role.replace('<@&', '').replace('>', ''), emoji=emojis[role.replace('<@&', '').replace('>', '')]) for role in roles]
        view = RoleView(option=options)
        options = await async_dumps(obj=options)
        await self.r.set(name=config.data_base.data["Game"].key, value=options)
        await ctx.send(view=view)

    @commands.command(name=config.command.love.command_name)
    async def love_roles(self, ctx: commands.Context):
        roles = ctx.message.content.split(" ")[:1]
        options = [discord.SelectOption(label=discord.utils.get(ctx.guild.roles, id=int(role.replace(
            '<@&', '').replace('>', ''))).name, value=role.replace('<@&', '').replace('>', ''), emoji=emojis[role.replace('<@&', '').replace('>', '')]) for role in roles]
        view = LoveRoleView(option=options)
        options = await async_dumps(obj=options)
        await self.r.set(name=config.data_base.data["Love"].key)
        await ctx.send(view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Role(bot=bot))
