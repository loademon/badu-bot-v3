import redis.asyncio as re

from wordgame.turkish.utils import *

r = re.from_url(url="redis://localhost")


async def setup_game(ctx: commands.Context, redis: re.Redis):
    """Yeni bir, kelime oyunu başlatır"""
    key = str(f"KO{ctx.channel.id}")
    data = {
        "last_char": random_char(),
        "msg_count": 0,
        "used_words": await async_dumps([]),
        "last_author": 31,
    }
    await redis.hmset(name=key, mapping=data)
    await ctx.channel.send(
        embed=create_embed(last_char=data["last_char"], IMAGES=IMAGES)
    )


async def close_game(ctx: commands.Context, redis: re.Redis):
    """Mevcut oyunu bitirir"""
    key = str(f"KO{ctx.channel.id}")
    if await redis.exists(key):
        await redis.delete(key)
        embed = discord.Embed(
            title="TAMAMLANDI",
            description="Oyun başarıyla sonlandırıldı!",
            color=0xFF0000,
        )
        await ctx.channel.send(embed=embed, delete_after=5)

    else:
        embed = discord.Embed(
            title="UYARI",
            description="Bu sunucuda mevcut bir oyun bulunmuyor!",
            color=0xFF0000,
        )
        await ctx.channel.send(embed=embed, delete_after=5)


async def handle_game(self, msg: discord.Message, redis: re.Redis):
    index = f"KO{msg.channel.id}"
    message = normalize(msg.content)

    if has_multiple_words(string=message):
        return await send_error_embed(
            msg=msg, description="Yalnızca tek bir kelime yazabilirsiniz!"
        )

    last_author = await get_last_author(index=index, redis=redis)

    if is_author_equal(last_author, msg.author.id):
        return await send_error_embed(
            msg=msg, description="Aynı Kullanıcı Arka Arkaya Mesaj Gönderemez!"
        )

    first_char = message[0]
    last_char = (await redis.hget(index, "last_char")).decode("utf-8")

    if is_char_not_equal(last_char=last_char, first_char=first_char):
        return await send_error_embed(
            msg=msg, description=f"Girdiğiniz kelime {last_char} harfi ile başlamıyor!"
        )

    if not is_valid_word(word=message, words=self.words[first_char]):
        return await send_error_embed(
            msg=msg,
            description="Girdiğiniz Kelime TDK'ye Göre Güncel Türkçe Sözlükte Bulunmuyor veya Kelime Sıfatında Değil!",
        )

    used_words = await get_used_words(redis=redis, index=index)

    if is_word_used(word=message, used_words=used_words):
        return await send_error_embed(
            msg=msg, description="Girdiğiniz Kelime Daha Önce Yazılmış!"
        )

    last_char = message[-1]
    await set_last_char(redis=redis, index=index, last_char=last_char)

    if is_char_equals_endch(char=last_char):
        await msg.add_reaction("✅")

        last_char = await set_last_char(
            redis=redis, index=index, last_char=random_char()
        )

        used_words = await update_used_words(
            redis=redis, index=index, used_words=used_words, message=message
        )

        last_author = await set_last_author(redis=redis, index=index, msg=msg)
        msg_count = await update_message_count(redis=redis, index=index)

        if msg_count < MAX_WORD:
            return await end_game(
                redis=redis,
                index=index,
                msg=msg,
                message=message,
                msg_count=msg_count,
                used_words=used_words,
                last_char=last_char,
                hard_reset=False,
            )

        if msg_count >= MAX_WORD:
            return await end_game(
                redis=redis,
                index=index,
                msg=msg,
                message=message,
                msg_count=msg_count,
                used_words=used_words,
                last_char=last_char,
                hard_reset=True,
            )

    await msg.add_reaction("✅")

    used_words = await update_used_words(
        redis=redis, index=index, used_words=used_words, message=message
    )

    await set_last_author(redis=redis, index=index, msg=msg)
    await update_message_count(redis=redis, index=index)
    await update_score(
        redis=redis,
        guild_id=str(msg.guild.id),
        author_id=str(msg.author.id),
        points=CORRECT_WORD_POINT,
    )

    if normalize(msg.content) == "irem":
        await msg.add_reaction("💓")
