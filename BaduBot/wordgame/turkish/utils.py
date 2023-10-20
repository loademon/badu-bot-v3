# coding: utf-8

import os
import random
import string
import asyncio
import pickle
from typing import Any

import discord
from discord.ext import commands

from wordgame.turkish.game import re


MPREFIX = "."
ENDCH = "ğ"
CHARS = (
    string.ascii_lowercase.replace("w", "").replace("x", "").replace("q", "") + "çşıöü"
)
MAX_WORD = 80
HARD_RESET_POINT = 1000
SOFT_RESET_POINT = 200
CORRECT_WORD_POINT = 100

WORD_FILE_PATH = "wordgame/turkish/kelimeler"
ERROR_COLOR = 0xFF0000

IMAGES = {
    "a": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/A.png",
    "b": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/B.png",
    "c": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/C.png",
    "ç": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/CC.png",
    "d": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/D.png",
    "e": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/E.png",
    "f": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/F.png",
    "g": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/G.png",
    "h": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/H.png",
    "ı": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/I.png",
    "i": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/II.png",
    "j": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/J.png",
    "k": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/K.png",
    "l": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/L.png",
    "m": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/M.png",
    "n": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/N.png",
    "o": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/O.png",
    "ö": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/OO.png",
    "p": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/P.png",
    "r": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/R.png",
    "s": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/S.png",
    "ş": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/SS.png",
    "t": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/T.png",
    "u": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/U.png",
    "ü": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/UU.png",
    "v": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/V.png",
    "y": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/Y.png",
    "z": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/Z.png",
    "w": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/W.png",
    "x": "https://raw.githubusercontent.com/loademon/bot-utils/main/Turkish_words_png/X.png",
}


def is_char_equals_endch(char):
    if char == ENDCH:
        return True
    return False


async def send_error_embed(msg: discord.Message, description: str):
    embed = discord.Embed(
        title="UYARI",
        description=description,
        color=ERROR_COLOR,
    )
    await msg.channel.send(embed=embed, delete_after=1.5)
    return await msg.delete()


def has_multiple_words(string: str):
    """Return True if string has multiple words"""
    return len(string.split(" ")) > 1


def is_valid_word(word: str, words: list[str]):
    """Return True if string in language word list"""
    return word in words


def is_author_equal(author1, author2):
    author1, author2 = str(author1), str(author2)
    if author1 == author2:
        return True
    return False


def is_char_not_equal(last_char: str, first_char: str):
    if last_char != first_char:
        return True
    return False


def is_word_used(word: str, used_words: list[str]):
    """Return True if string in used words list"""
    return word in used_words


async def set_last_char(redis: re.Redis, index: str, last_char: str):
    await redis.hset(index, "last_char", last_char)
    return last_char


async def update_score(redis: re.Redis, guild_id: str, author_id: str, points: int):
    if not await redis.exists(f"SCORE{guild_id}"):
        await redis.zadd(f"SCORE{guild_id}", {author_id: 0})
    else:
        if not await redis.zscore(f"SCORE{guild_id}", author_id):
            await redis.zadd(f"SCORE{guild_id}", {author_id: 0})

    await redis.zincrby(f"SCORE{guild_id}", points, author_id)


async def get_used_words(redis: re.Redis, index: str):
    used_words_pickle = await redis.hget(index, "used_words")
    used_words: list = await async_loads(used_words_pickle)
    return used_words


async def update_used_words(
    redis: re.Redis, index: str, used_words: list[str], message: str
):
    used_words.append(message)
    used_words_pickle = await async_dumps(used_words)
    await redis.hset(index, "used_words", used_words_pickle)
    return used_words


async def get_last_author(redis: re.Redis, index: str):
    return (await redis.hget(index, "last_author")).decode("utf-8")


async def set_last_author(redis: re.Redis, index: str, msg: discord.Message):
    await redis.hset(index, "last_author", str(msg.author.id))
    return str(msg.author.id)


async def update_message_count(redis: re.Redis, index: str):
    return await redis.hincrby(index, "msg_count", 1)


async def char_reset(
    msg: discord.Message, hard_reset: bool, msg_count: int, last_char: str
):
    last_char_up = up_normalize(last_char)
    if hard_reset:
        embed = discord.Embed(
            title="UYARI",
            description=f"Oyun Başından İtibaren Toplam {msg_count} Kelime Yazıldı Bu Oyunun Bitmesine Yeterli\nBu Yüzden Yeni Harf Belirlenecek ve Oyun Tamamen Sıfırlanacak\nOyunu Bitiren Kişi 1000xp Kazandı!",
            color=ERROR_COLOR,
        )
        embed_ = discord.Embed(
            title="KELİME TÜRETMECE",
            description=f"Harf Sıfırlandı! Yeni Harfiniz: [ {last_char_up} ]",
            color=ERROR_COLOR,
        )
        embed.set_thumbnail(url=IMAGES[last_char])
        await msg.channel.send(embeds=[embed, embed_])
        return hard_reset

    embed = discord.Embed(
        title="UYARI",
        description=f"Oyun Başından İtibaren Toplam {msg_count} Kelime Yazıldı Bu Yeterli Değil! \n Bu Yüzden Yeni Harf Belirlenecek Ancak Oyun Bitmiş Sayılmayacak!",
        color=ERROR_COLOR,
    )
    embed_ = discord.Embed(
        title="KELİME TÜRETMECE",
        description=f"Harf Sıfırlandı! Yeni Harfiniz: [ {last_char_up} ]",
        color=ERROR_COLOR,
    )
    embed.set_thumbnail(url=IMAGES[last_char])
    await msg.channel.send(embeds=[embed, embed_])
    return hard_reset


async def end_game(
    redis: re.Redis,
    index: str,
    msg: discord.Message,
    message: str,
    msg_count: int,
    used_words: list[str],
    last_char: str,
    hard_reset: bool,
):
    guild_id = msg.guild.id
    author_id = msg.author.id
    if hard_reset:
        await set_last_char(redis=redis, index=index, last_char=last_char)
        await redis.hset(index, "used_words", await async_dumps([]))
        await redis.hset(index, "last_author", 31)
        await redis.hset(index, "msg_count", 0)

        await char_reset(
            msg=msg, hard_reset=hard_reset, msg_count=msg_count, last_char=last_char
        )
        await update_score(
            redis=redis, guild_id=guild_id, author_id=author_id, points=HARD_RESET_POINT
        )

    else:
        await set_last_char(redis=redis, index=index, last_char=last_char)
        await update_used_words(
            redis=redis, index=index, used_words=used_words, message=message
        )
        await set_last_author(redis=redis, index=index, msg=msg)
        await update_message_count(redis=redis, index=index)
        await char_reset(
            msg=msg, hard_reset=hard_reset, msg_count=msg_count, last_char=last_char
        )
        await update_score(
            redis=redis, guild_id=guild_id, author_id=author_id, points=SOFT_RESET_POINT
        )


def random_char():
    """Harf listesinden random bir harf seçer"""
    return random.choice(CHARS)


def normalize(string):
    """Verilen kelimenin tüm harflerini küçük harf yapar"""
    return (
        string.replace("Â", "a")
        .replace("â", "a")
        .replace("Î", "i")
        .replace("î", "i")
        .replace("I", "ı")
        .replace("İ", "i")
        .replace("Ğ", "ğ")
        .lower()
    )


def up_normalize(string):
    """Verilen kelimenin tüm harflerini büyük harf yapar"""
    return (
        string.replace("â", "A")
        .replace("Â", "A")
        .replace("î", "İ")
        .replace("Î", "İ")
        .replace("ı", "I")
        .replace("i", "İ")
        .replace("ğ", "Ğ")
        .upper()
    )


def parse_words():
    """Kelimeleri düzgün bir listeye aktarır"""
    words = {}

    for file in sorted(os.listdir(WORD_FILE_PATH)):
        data = open(os.path.join(WORD_FILE_PATH, file), "r", encoding="utf8").read()
        data = (
            data.replace("Â", "a")
            .replace("â", "a")
            .replace("Î", "i")
            .replace("î", "i")
            .replace("I", "ı")
            .lower()
        )
        words[file[0]] = data.split("\n")[:-1]

    return words


def create_embed(last_char, IMAGES):
    """Discord için mesaj embedi oluşturur."""
    embed = discord.Embed(
        title="KELİME TÜRETMECE",
        url="https://twitch.tv/Badu_tv",
        description=f"Oyun Başladı! İlk Harfiniz: [ {up_normalize(last_char)} ]",
        color=0xFF0000,
    )
    embed.add_field(
        name="Bilgi;",
        value=f"Her doğru kelime için hanenize {CORRECT_WORD_POINT}xp yazarsınız. Eğer yazılan kelimenin sonu **{ENDCH}** ile bitiyorsa toplam mesaj sayısına bakılır oyun başından itibaren {MAX_WORD} kelimeden az kelime yazıldıysa oyun sıfırlanmaz ve yeni harf belirlenir mesajı yazan {SOFT_RESET_POINT}xp kazanır. Oyun başından itibaren {MAX_WORD} kelimeden fazla kelime yazıldıysa oyun sıfırlanır ve oyunu sıfırlayan kişi {HARD_RESET_POINT}xp kazanır.Sohbet etmek isterseniz {MPREFIX} kullanın. Rahatsızlık veren kullanıcılar için moderatörler ile iletişime geçin.",
        inline=False,
    )
    embed.set_footer(
        text="Botta yaşanan herhangi bir sorunda <@486106388561657867> ile iletişime geçiniz."
    )
    embed.set_thumbnail(url=IMAGES[last_char])
    return embed


async def async_dumps(obj: Any):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pickle.dumps, obj)


async def async_loads(obj: Any):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pickle.loads, obj)
