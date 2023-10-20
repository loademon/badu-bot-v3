import discord
import redis.asyncio as redis

EDITOR_ROLE_ID = 1116432482343080016
ADMIN_ROLE_ID = 1116432482364035084


async def get_user_id(redis: redis.Redis, inter: discord.Interaction):
    return (
        (await redis.hget(name="Editor Interactions", key=inter.message.id)).decode(
            "utf-8"
        )
        if (await redis.hget(name="Editor Interactions", key=inter.message.id))
        is not None
        else None
    )


async def check_user_id(redis: redis.Redis, inter: discord.Interaction):
    user_id = await get_user_id(redis=redis, inter=inter)
    if user_id == None:
        raise await inter.response.send_message(
            "Beklenmeyen bir hata oluştu.", ephemeral=True
        )
    return user_id


async def get_user_status(redis: redis.Redis, inter: discord.Interaction, user_id: str):
    return (
        (await redis.hget(name="Editor Status", key=user_id)).decode("utf-8")
        if (await redis.hget(name="Editor Status", key=user_id)) is not None
        else None
    )


async def check_user_status(
    redis: redis.Redis, inter: discord.Interaction, user_id: str
):
    user_status = await get_user_status(redis=redis, inter=inter, user_id=user_id)
    if user_status == None:
        raise await inter.response.send_message(
            "Beklenmeyen bir hata oluştu.", ephemeral=True
        )

    if user_status == "Kabul Edildi" or user_status == "Reddedildi":
        raise await inter.response.send_message(
            f"Kullanıcının başvurusu zaten yanıtlanmış: **{user_status}**",
            ephemeral=True,
        )

    return user_status


async def add_editor_role(inter: discord.Interaction, user_id: int, redis: redis.Redis):
    role: discord.Role = inter.guild.get_role(EDITOR_ROLE_ID)
    user: discord.Member = inter.guild.get_member(int(user_id))
    await redis.hset(name="Editor Status", key=user_id, value="Kabul Edildi")
    await user.add_roles(role)
    await inter.response.send_message(
        "Başvuru başarıyla kabul edildi. Roller eklendi.", ephemeral=True
    )


async def reject_editor(redis: redis.Redis, inter: discord.Interaction, user_id: int):
    await redis.hset(name="Editor Status", key=user_id, value="Reddedildi")
    await inter.response.send_message("Başvuru başarıyla reddedildi.", ephemeral=True)


class ConfirmButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.r = redis.from_url("redis://localhost")

    @discord.ui.button(
        label="Kabul Et",
        style=discord.ButtonStyle.green,
        emoji="✔️",
        custom_id="editor:accept",
    )
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            user_id = await check_user_id(redis=self.r, inter=interaction)
        except:
            return
        try:
            await check_user_status(redis=self.r, inter=interaction, user_id=user_id)
        except:
            return

        await add_editor_role(inter=interaction, user_id=user_id, redis=self.r)

    @discord.ui.button(
        label="Reddet",
        style=discord.ButtonStyle.red,
        emoji="✖️",
        custom_id="editor:reject",
    )
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            user_id = await check_user_id(redis=self.r, inter=interaction)
        except:
            return
        try:
            await check_user_status(redis=self.r, inter=interaction, user_id=user_id)
        except:
            return
        await reject_editor(redis=self.r, inter=interaction, user_id=user_id)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # return 1078376343294713866 in [role.id for role in interaction.user.roles]
        return ADMIN_ROLE_ID in [role.id for role in interaction.user.roles]


class EditorButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.r = redis.from_url("redis://localhost")

    @discord.ui.button(
        label="Başvuru Yap!",
        style=discord.ButtonStyle.blurple,
        emoji="📋",
        custom_id="EditorButton",
    )
    async def callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if await self.r.hexists(name="Editor Status", key=interaction.user.id):
            user_status = (
                (
                    await self.r.hget(name="Editor Status", key=interaction.user.id)
                ).decode("utf-8")
                if (await self.r.hget(name="Editor Status", key=interaction.user.id))
                is not None
                else None
            )
            if user_status == None:
                return await interaction.response.send_message(
                    "Beklenmeyen bir hata oluştu.", ephemeral=True
                )

            return await interaction.response.send_message(
                f"Aynı kullanıcı daha sonra izin verilmediği sürece birden fazla kez başvuru yapamaz\nŞu anki başvuru durumunuz: **{user_status}**",
                ephemeral=True,
            )

        msg: discord.Message = await interaction.channel.send(
            f"{interaction.user.mention} başvuru yaptı!", view=ConfirmButtons()
        )

        await self.r.hset(
            name="Editor Interactions", key=msg.id, value=interaction.user.id
        )
        await self.r.hset(
            name="Editor Status", key=interaction.user.id, value="Beklemede"
        )
        await interaction.response.send_message(
            "Başvurunuz başarıyla yapıldı", ephemeral=True
        )
