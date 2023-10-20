from dataclasses import dataclass

DEFAULT_LOG_CHANNEL = 1116438616126787624  # Write the ID of the channel where you want the logs to be sent.
DEFAULT_LOG_URL = (
    "https://raw.githubusercontent.com/loademon/bot-utils/main/Logs/DiscordLogs/{}"
)
DEFAULT_USER_URL = "https://discordapp.com/users/{}"
GREEN = 0x43B14B
RED = 0xFF0000
ORANGE = 0xFFB000


STATUS = {
    "online": "Çevrimiçi 🟢",
    "offline": "Çevrimdışı ⚫",
    "dnd": "Rahatsız Etmeyin ⭕",
    "idle": "Boşta 🟡",
    "streaming": "Yayında 📺",
}


@dataclass
class Log:
    log_message: str
    log_channel: int = DEFAULT_LOG_CHANNEL
    log_icon: str = (
        "https://raw.githubusercontent.com/loademon/bot-utils/main/Error_poop.png"
    )
    log_color: int = 0xFF0000
    delete_after: float = None


def icon_url(name: str):
    return DEFAULT_LOG_URL.format(name)


# ----------------------------------------------------------------------------------------------->

MemberJoin = Log(
    log_message="{} sunucuya katıldı.",
    log_icon=icon_url("MemberJoin.png"),
    log_color=GREEN,
)

MemberLeave = Log(
    log_message="{} sunucudan ayrıldı.",
    log_icon=icon_url("MemberLeave.png"),
    log_color=RED,
)

MessageEdit = Log(
    log_message="{} kullanıcısının bir mesajı düzenledi.",
    log_icon=icon_url("MessageEdit"),
    log_color=GREEN,
)

MessageDelete = Log(
    log_message="{} kullanıcısının bir mesajı silindi.",
    log_icon=icon_url("MessageDelete"),
    log_color=RED,
)

ChannelCreate = Log(
    log_message="Yeni bir {} kanalı oluşturuldu.",
    log_icon=icon_url("ChannelCreate"),
    log_color=GREEN,
)

ChannelDelete = Log(
    log_message="Bir {} kanalı sunucudan silindi.",
    log_icon=icon_url("ChannelDelete"),
    log_color=RED,
)

ChannelUpdate = Log(
    log_message="Bir {} kanalında değişiklikler yapıldı.",
    log_icon=icon_url("ChannelUpdate"),
    log_color=ORANGE,
)

MessagePin = Log(
    log_message="Bir mesaj sabitlendi.",
    log_icon=icon_url("MessagePin"),
    log_color=GREEN,
)

CreateInvite = Log(
    log_message="Davet linki oluşturuldu.",
    log_icon=icon_url("CreateInvite"),
    log_color=GREEN,
)

MemberUpdate = Log(
    log_message="Bir kullanıcı (Sunucu Bazlı) profili güncellendi.",
    log_icon=icon_url("MemberUpdate"),
    log_color=ORANGE,
)

UserUpdate = Log(
    log_message="Bir kullanıcı (Discord Bazlı) profili güncellendi.",
    log_icon=icon_url("UserUpdate"),
    log_color=ORANGE,
)

MemberBan = Log(
    log_message="Bir kullanıcı sunucudan yasaklandı.",
    log_icon=icon_url("MemberBan"),
    log_color=RED,
)

MemberUnban = Log(
    log_message="Bir kullanıcının yasaklaması kaldırıldı.",
    log_icon=icon_url("MemberUnban"),
    log_color=GREEN,
)

ReactionAdd = Log(
    log_message="Bir mesaja tepki eklendi.",
    log_icon=icon_url("ReactionAdd"),
    log_color=GREEN,
)

ReactionRemove = Log(
    log_message="Bir mesaja gönderilen tepki kaldırıldı.",
    log_icon=icon_url("ReactionRemove"),
    log_color=RED,
)

RoleCreate = Log(
    log_message="Bir rol oluşturuldu.", log_icon=icon_url("RoleCreate"), log_color=GREEN
)

RoleUpdate = Log(
    log_message="Bir rol üzerinde değişiklikler yapıldı",
    log_icon=icon_url("RoleUpdate"),
    log_color=ORANGE,
)

RoleDelete = Log(
    log_message="Bir rol sunucudan kaldırıldı.",
    log_icon=icon_url("RoleDelete"),
    log_color=RED,
)

VoiceUpdate = Log(
    log_message="Bir kullanıcının ses etkinliği güncellendi.",
    log_icon=icon_url("VoiceUpdate"),
    log_color=ORANGE,
)
