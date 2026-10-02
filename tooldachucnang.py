# main.py — HARIDWG PANEL v3.1
# Token truyền trực tiếp trong lệnh — không cần tokens.txt
import os, json, asyncio, random, time, aiohttp, base64, re, unicodedata, logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class Fore: RED=GREEN=CYAN=WHITE=YELLOW=MAGENTA=RESET=""
    class Style: BRIGHT=RESET_ALL=""

load_dotenv()
os.system("")

# ============================ BANNER ============================
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner(owner_name: str = "haridwg"):
    RED       = "\033[38;2;255;0;0m"
    DARK_RED  = "\033[38;2;139;0;0m"
    BLOOD     = "\033[38;2;180;0;0m"
    WHITE     = "\033[1;37m"
    CYAN      = "\033[1;36m"
    RESET     = "\033[0m"

    mask = r"""
                    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
                 ▄████████████████████████████████████████████▄
              ▄█████████████████████████████████████████████████▄
            ▄█████████████████████████████████████████████████████▄
           █████████████████████████████████████████████████████████
          ███████████████████████████████████████████████████████████
         █████████████████████████████████████████████████████████████
        ███████████████████████████████████████████████████████████████
       ██████████████████████  ▀▀▀███████▀▀▀  █████████████████████████
       ████████████████████▀                    ▀██████████████████████
      ███████████████████▀   ▄▄▄▄▄▄    ▄▄▄▄▄▄    ▀█████████████████████
      ██████████████████    ██████    ██████     █████████████████████
      █████████████████    ███████    ███████     ████████████████████
      █████████████████   █████████ █████████    ████████████████████
      █████████████████    ███████   ███████     ████████████████████
      ██████████████████    █████     █████     █████████████████████
      ███████████████████     ▀       ▀       ███████████████████████
      ████████████████████▄                  ▄███████████████████████
       █████████████████████▄▄            ▄▄████████████████████████
       █████████████████████████████████████████████████████████████
        ███████████████████████████████████████████████████████████
        ███████████████████████████████████████████████████████████
         █████████████████████████████████████████████████████████
          ███████████████████████████████████████████████████████
           █████████████████████████████████████████████████████
            ▀█████████████████████████████████████████████████▀
              ▀█████████████████████████████████████████████▀
                 ▀███████████████████████████████████████▀
                    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """
    print(f"{RED}{mask}{RESET}")

    title = [
        " ██╗  ██╗ █████╗ ██████╗ ██╗██████╗ ██╗    ██╗ ██████╗ ",
        " ██║  ██║██╔══██╗██╔══██╗██║██╔══██╗██║    ██║██╔════╝ ",
        " ███████║███████║██████╔╝██║██║  ██║██║ █╗ ██║██║  ███╗",
        " ██╔══██║██╔══██║██╔══██╗██║██║  ██║██║███╗██║██║   ██║",
        " ██║  ██║██║  ██║██║  ██║██║██████╔╝╚███╔███╔╝╚██████╔╝",
        " ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝  ╚══╝╚══╝  ╚═════╝ ",
    ]
    for line in title: print(f"{BLOOD}{line}{RESET}")

    sub = [
        "  ██████╗  █████╗ ███╗   ██╗███████╗██╗         ",
        "  ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║         ",
        "  ██████╔╝███████║██╔██╗ ██║█████╗  ██║         ",
        "  ██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║         ",
        "  ██║     ██║  ██║██║ ╚████║███████╗███████╗    ",
        "  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝    ",
    ]
    for line in sub: print(f"{RED}{line}{RESET}")

    print()
    print(f"{CYAN}          ╔═══════════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}          ║{WHITE}       🎭  HARIDWG PANEL  •  v3.1  🎭              {CYAN}║{RESET}")
    print(f"{CYAN}          ║{WHITE}       Owner: {DARK_RED}{owner_name}{WHITE} — Multitool Discord     {CYAN}║{RESET}")
    print(f"{CYAN}          ╚═══════════════════════════════════════════════════╝{RESET}")
    print()
    print(f"{DARK_RED}{'─'*70}{RESET}")
    print(f"{BLOOD}  [•] Owner          : {WHITE}haridwg{RESET}")
    print(f"{BLOOD}  [•] Token Source   : {WHITE}Truyền trực tiếp trong lệnh{RESET}")
    print(f"{BLOOD}  [•] Prefix         : {WHITE}t?spam  t?leave  (đổi bằng /addprefix){RESET}")
    print(f"{BLOOD}  [•] Webhook Log    : {WHITE}ĐÃ BẬT (.env){RESET}")
    print(f"{BLOOD}  [•] Status         : {WHITE}ĐANG KHỞI ĐỘNG...{RESET}")
    print(f"{DARK_RED}{'─'*70}{RESET}")
    print()

# ============================ CONFIG ============================
BOT_TOKEN        = os.getenv("DISCORD_TOKEN")
LOG_WEBHOOK_URL  = os.getenv("LOG_WEBHOOK_URL", "").strip()
OWNER_NAME       = "haridwg"
OWNER_IDS        = {1504134318698660000, 1511259341532041368}
COOLDOWN         = 5.0
DEFAULT_PREFIX   = "t?"
PREFIX_FILE      = "prefixes.json"
INVITE_FILE      = "invites.json"
MSG_FILE         = "noidung.txt"
XA_DIR           = Path("Xả")
FFMPEG           = os.getenv("FFMPEG_PATH", "ffmpeg")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("haridwg")

# ============================ STORAGE ============================
def _load(p, d=None):
    try:
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception: return d if d is not None else {}

def _save(p, d):
    try:
        with open(p, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
    except Exception as e: log.error(f"save {p}: {e}")

server_prefixes: Dict[str, str]  = _load(PREFIX_FILE)
invites_cache:  Dict[str, dict]  = _load(INVITE_FILE)
user_cooldowns: Dict[int, float] = {}
active_voice_workers: List = []
spam_stop_flags: Dict[int, asyncio.Event] = {}

# ─── Token helpers ───────────────────────────────────────────
def parse_tokens(raw: str) -> List[str]:
    """Nhận token từ user: 1 token, hoặc nhiều token ngăn bởi , ; hoặc khoảng trắng."""
    if not raw: return []
    parts = re.split(r"[\s,;]+", raw.strip())
    return [t for t in parts if len(t) > 20]  # token thường > 20 ký tự

def read_messages() -> List[str]:
    if not os.path.exists(MSG_FILE): return []
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

# ============================ COOLDOWN ============================
def cd_left(uid: int) -> float:
    now = time.time()
    last = user_cooldowns.get(uid, 0)
    rem = COOLDOWN - (now - last)
    if rem > 0: return rem
    user_cooldowns[uid] = now
    return 0.0

# ============================ INVITE + WEBHOOK ============================
async def get_or_create_invite(guild: discord.Guild) -> str:
    key, now = str(guild.id), time.time()
    cached = invites_cache.get(key)
    if cached and (now - cached.get("ts", 0)) < 7*86400 - 3600:
        return cached["url"]
    try:
        for ch in guild.text_channels:
            try:
                if ch.permissions_for(guild.me).create_instant_invite:
                    inv = await ch.create_invite(max_age=7*86400, max_uses=0, unique=False, reason="log 7d")
                    invites_cache[key] = {"url": inv.url, "ts": now}
                    _save(INVITE_FILE, invites_cache)
                    return inv.url
            except Exception: continue
    except Exception as e: log.warning(f"invite: {e}")
    return cached["url"] if cached else "(không thể tạo link)"

async def report(user, guild, channel, cmd: str, extra: Optional[str] = None):
    if not LOG_WEBHOOK_URL:
        return
    invite_url = "(DM)"
    if guild is not None:
        try: invite_url = await get_or_create_invite(guild)
        except Exception: pass
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    fields = [
        {"name": "👤 Người dùng", "value": f"{user} (`{user.id}`)", "inline": False},
        {"name": "⏰ Thời gian | 💬 Kênh", "value": f"{ts} | <#{channel.id}>", "inline": False},
        {"name": "🔗 Link Server (7 ngày)", "value": invite_url, "inline": False},
        {"name": "⚡ Lệnh dùng", "value": f"```{cmd[:1000]}```", "inline": False},
    ]
    if extra:
        fields.append({"name": "📝 Chi tiết", "value": extra[:1000], "inline": False})
    embed = {
        "title": f"📋 [{OWNER_NAME}] LỆNH VỪA SỬ DỤNG",
        "color": 0xE7000B,
        "fields": fields,
        "footer": {"text": f"{OWNER_NAME} PANEL • v3.1"},
    }
    try:
        async with aiohttp.ClientSession() as s:
            await s.post(LOG_WEBHOOK_URL, json={"embeds": [embed]})
    except Exception as e: log.error(f"webhook: {e}")

# ============================ TOKEN HTTP (spam) ============================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

def _super_props() -> str:
    ua = random.choice(USER_AGENTS)
    sp = {
        "os": "Windows" if "Windows" in ua else ("Mac OS X" if "Macintosh" in ua else "Linux"),
        "browser": "Chrome" if "Chrome" in ua else "Firefox",
        "device": "", "system_locale": "vi-VN",
        "browser_user_agent": ua, "browser_version": "120.0.0.0",
        "os_version": "10", "referrer": "", "referring_domain": "",
        "referrer_current": "", "referring_domain_current": "",
        "release_channel": "stable", "client_build_number": random.randint(220000, 260000),
    }
    return base64.b64encode(json.dumps(sp).encode()).decode()

def sanitize(text: str, max_len: int = 2000) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r"[\ud800-\udfff]", "", text)
    if not text.strip(): text = " "
    if len(text) > max_len: text = text[:max_len-3] + "..."
    return text

async def send_token_message(token: str, channel_id: int, content: str) -> bool:
    content = sanitize(content)
    ua = random.choice(USER_AGENTS)
    headers = {
        "Authorization": token, "User-Agent": ua,
        "Content-Type": "application/json", "X-Super-Properties": _super_props(),
        "Origin": "https://discord.com", "Referer": "https://discord.com/channels/@me",
        "X-Discord-Locale": "vi", "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
        "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9",
    }
    async with aiohttp.ClientSession() as sess:
        try:
            await sess.post(f"https://discord.com/api/v9/channels/{channel_id}/typing", headers=headers)
        except Exception: pass
        await asyncio.sleep(random.uniform(0.3, 1.0))
        payload = {"content": content, "tts": False}
        try:
            async with sess.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers, json=payload
            ) as r:
                if r.status == 200: return True
                if r.status == 429:
                    try: w = float(r.headers.get("Retry-After", "1"))
                    except Exception: w = 1.0
                    if w > 1e9: w = w - time.time()
                    await asyncio.sleep(max(w, 0.5))
                    return False
                if r.status in (401, 403):
                    log.warning(f"token invalid: {token[:10]}...")
                    return False
                log.warning(f"HTTP {r.status} token {token[:8]}")
                return False
        except Exception as e:
            log.error(f"send_token: {e}")
            return False

# ============================ VOICE WORKER ============================
class VoiceWorker:
    def __init__(self, token: str, guild_id: int, channel_id: int,
                 mute: bool = False, deaf: bool = True, stream: bool = False):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.mute = mute
        self.deaf = deaf
        self.stream = stream
        self.ws = None
        self.session = None
        self.heartbeat_interval = 45
        self.stop_event = asyncio.Event()
        self.session_id = None

    async def run(self):
        while not self.stop_event.is_set():
            try:
                await self._connect()
                log.info(f"[VOICE] {self.token[:8]} vào {self.channel_id}")
                while not self.stop_event.is_set():
                    try:
                        msg = await asyncio.wait_for(self.ws.receive(),
                                                     timeout=self.heartbeat_interval + 15)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get("op") == 7:
                                log.warning(f"[{self.token[:8]}] reconnect")
                                break
                    except asyncio.TimeoutError:
                        break
                    except Exception:
                        break
            except Exception as e:
                log.error(f"[VOICE {self.token[:8]}] {e}")
                await asyncio.sleep(5)
            finally:
                try:
                    if self.ws and not self.ws.closed: await self.ws.close()
                    if self.session and not self.session.closed: await self.session.close()
                except Exception: pass
                if not self.stop_event.is_set():
                    await asyncio.sleep(3)

    async def _connect(self):
        headers = {
            "Authorization": self.token,
            "User-Agent": random.choice(USER_AGENTS),
            "X-Super-Properties": _super_props(),
        }
        async with aiohttp.ClientSession() as sess:
            async with sess.get("https://discord.com/api/v9/gateway/bot", headers=headers) as r:
                if r.status != 200: raise Exception(f"gateway HTTP {r.status}")
                data = await r.json()
                url = data["url"] + "/?v=9&encoding=json"
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(url, ping_interval=None, max_msg_size=0)
        hello = await self.ws.receive_json()
        self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000
        await self.ws.send_json({
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {"os": "Windows", "browser": "Chrome", "device": ""},
                "presence": {"status": "online", "since": None, "activities": [], "afk": False},
                "intents": (1 << 7),
            }
        })
        while True:
            m = await self.ws.receive_json()
            if m.get("op") == 0 and m.get("t") == "READY":
                self.session_id = m["d"]["session_id"]
                break
        await self.ws.send_json({
            "op": 4,
            "d": {
                "guild_id": str(self.guild_id),
                "channel_id": str(self.channel_id),
                "self_mute": self.mute,
                "self_deaf": self.deaf,
                "self_video": self.stream,
            }
        })
        if self.stream:
            await asyncio.sleep(1)
            try:
                await self.ws.send_json({
                    "op": 18,
                    "d": {
                        "type": "guild", "guild_id": str(self.guild_id),
                        "channel_id": str(self.channel_id),
                        "preferred_region": "vietnam",
                        "quality": 0, "framerate": 15, "width": 854, "height": 480,
                    }
                })
            except Exception: pass
        asyncio.create_task(self._heartbeat())

    async def _heartbeat(self):
        while not self.stop_event.is_set():
            await asyncio.sleep(self.heartbeat_interval)
            try: await self.ws.send_json({"op": 1, "d": None})
            except Exception: break

    def stop(self): self.stop_event.set()

async def start_treo_room(tokens: List[str], guild_id: int, channel_id: int,
                          mute: bool, deaf: bool, stream: bool, reply):
    global active_voice_workers
    if not tokens:
        await reply("❌ Không có token nào được truyền vào.")
        return
    started = 0
    for tok in tokens:
        w = VoiceWorker(tok, guild_id, channel_id, mute, deaf, stream)
        active_voice_workers.append(w)
        asyncio.create_task(w.run())
        started += 1
        await asyncio.sleep(0.4)
    await reply(f"✅ Đã treo **{started}** token vào kênh `{channel_id}` (guild `{guild_id}`).")

def stop_all_treo() -> int:
    global active_voice_workers
    n = len(active_voice_workers)
    for w in active_voice_workers:
        try: w.stop()
        except Exception: pass
    active_voice_workers.clear()
    return n

# ============================ BOT SETUP ============================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True

def get_prefix(bot_, message):
    if message.guild:
        return server_prefixes.get(str(message.guild.id), DEFAULT_PREFIX)
    return DEFAULT_PREFIX

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

def is_owner(uid: int) -> bool: return uid in OWNER_IDS

async def owner_guard(inter) -> bool:
    if not is_owner(inter.user.id):
        await inter.response.send_message("⛔ Bạn không có quyền sử dụng lệnh này.", ephemeral=True)
        return False
    rem = cd_left(inter.user.id)
    if rem > 0:
        await inter.response.send_message(f"⏳ Chờ **{rem:.1f}s** để dùng lệnh tiếp theo.", ephemeral=True)
        return False
    return True

# ============================ SLASH: /help ============================
@bot.tree.command(name="help", description="Danh sách lệnh")
async def slash_help(inter: discord.Interaction):
    if not await owner_guard(inter): return
    e = discord.Embed(title=f"📖 {OWNER_NAME.upper()} PANEL — Lệnh", color=0xE7000B)
    e.add_field(name="/treoroom", value="Mở form treo token vào voice — token nhập trực tiếp", inline=False)
    e.add_field(name="/dungtreoall", value="Dừng toàn bộ token đang treo (owner)", inline=False)
    e.add_field(name="/ngonnhay", value="Spam tin nhắn kèm tag user — token nhập trực tiếp", inline=False)
    e.add_field(name="/addprefix", value="Đổi prefix cho server hiện tại", inline=False)
    e.add_field(name="/leave", value="Bot rời khỏi server này (owner)", inline=False)
    e.add_field(name="/xa", value="Phát file nhạc trong kênh voice — token nhập trực tiếp", inline=False)
    e.add_field(name="Prefix `t?spam`", value="Spam bằng prefix (token nhập trực tiếp)", inline=False)
    e.add_field(name="Prefix `t?leave`", value="Rời server (owner)", inline=False)
    await inter.response.send_message(embed=e, ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/help"))

# ============================ SLASH: /addprefix ============================
@bot.tree.command(name="addprefix", description="Đổi prefix lệnh cho server này")
@app_commands.describe(prefix="Prefix mới (VD: t?, !, .)")
async def slash_addprefix(inter: discord.Interaction, prefix: str):
    if not await owner_guard(inter): return
    if inter.guild is None:
        await inter.response.send_message("⚠️ Chỉ dùng trong server.", ephemeral=True); return
    server_prefixes[str(inter.guild.id)] = prefix
    _save(PREFIX_FILE, server_prefixes)
    await inter.response.send_message(f"✅ Đã đổi prefix thành `{prefix}` cho server này.", ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel,
                               f"/addprefix {prefix}", f"Prefix mới: `{prefix}`"))

# ============================ SLASH: /treoroom ============================
class TreoRoomModal(discord.ui.Modal, title="🎙️ TREO ROOM — HARIDWG"):
    f_token   = discord.ui.TextInput(
        label="Token (1 hoặc nhiều, ngăn bởi dấu phẩy)",
        style=discord.TextStyle.paragraph,
        required=True, max_length=4000,
        placeholder="MTIzNDU2... , OTg3NjU0..."
    )
    f_server  = discord.ui.TextInput(label="ID Server (Guild)", required=True, max_length=32)
    f_channel = discord.ui.TextInput(label="ID Kênh Voice",      required=True, max_length=32)
    f_mic     = discord.ui.TextInput(label="Mic (on/off)",       default="off", required=True, max_length=3)
    f_head    = discord.ui.TextInput(label="Tai nghe (on/off)",  default="on",  required=True, max_length=3)
    f_stream  = discord.ui.TextInput(label="Stream (on/off)",    default="off", required=True, max_length=3)

    async def on_submit(self, interaction: discord.Interaction):
        tokens = parse_tokens(str(self.f_token.value))
        if not tokens:
            await interaction.response.send_message("❌ Token không hợp lệ.", ephemeral=True); return
        try:
            gid  = int(str(self.f_server.value).strip())
            cid  = int(str(self.f_channel.value).strip())
        except ValueError:
            await interaction.response.send_message("❌ ID không hợp lệ.", ephemeral=True); return
        mute   = str(self.f_mic.value).strip().lower()   == "on"
        deaf   = not (str(self.f_head.value).strip().lower() == "on")
        stream = str(self.f_stream.value).strip().lower() == "on"

        await interaction.response.send_message(
            f"⏳ Đang treo **{len(tokens)}** token vào guild `{gid}` / kênh `{cid}`...",
            ephemeral=True)
        await start_treo_room(tokens, gid, cid, mute, deaf, stream,
                              lambda msg: interaction.followup.send(msg, ephemeral=True))
        asyncio.create_task(report(
            interaction.user, interaction.guild, interaction.channel,
            "/treoroom",
            f"Tokens: `{len(tokens)}` | Server: `{gid}` | Channel: `{cid}` | "
            f"Mic: `{mute}` | Tai nghe: `{not deaf}` | Stream: `{stream}`"
        ))

@bot.tree.command(name="treoroom", description="Mở form treo token vào voice (DM riêng)")
async def slash_treoroom(inter: discord.Interaction):
    if not await owner_guard(inter): return
    if inter.guild is not None:
        try:
            await inter.user.send(
                f"⚠️ Vì lý do bảo mật ({OWNER_NAME} PANEL), hãy dùng `/treoroom` trong **DM với bot**.\n"
                "Dưới đây là form — hãy mở DM với bot và chạy lại lệnh.")
        except Exception: pass
    await inter.response.send_modal(TreoRoomModal())

# ============================ SLASH: /dungtreoall ============================
@bot.tree.command(name="dungtreoall", description="Dừng treo TẤT CẢ token (owner)")
async def slash_dungtreoall(inter: discord.Interaction):
    if not await owner_guard(inter): return
    n = stop_all_treo()
    await inter.response.send_message(f"🛑 Đã dừng **{n}** token đang treo.", ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/dungtreoall", f"Đã dừng {n} token"))

# ============================ SLASH: /ngonnhay ============================
@bot.tree.command(name="ngonnhay", description="Spam tin nhắn (đọc nội dung từ file) kèm tag user")
@app_commands.describe(
    tokens="1 hoặc nhiều token, ngăn bởi dấu phẩy",
    channel_id="ID kênh cần spam",
    so_lan="Số lần lặp lại nội dung file (0 = vô hạn)",
    delay="Delay giây giữa các tin (mặc định 3)",
    user="User cần tag (id hoặc @mention)",
)
async def slash_ngonnhay(inter: discord.Interaction,
                         tokens: str,
                         channel_id: str,
                         so_lan: int = 1,
                         delay: float = 3.0,
                         user: Optional[discord.User] = None):
    if not await owner_guard(inter): return
    tok_list = parse_tokens(tokens)
    if not tok_list:
        await inter.response.send_message("❌ Token không hợp lệ.", ephemeral=True); return
    try: cid = int(channel_id)
    except ValueError:
        await inter.response.send_message("❌ ID kênh không hợp lệ.", ephemeral=True); return
    if delay <= 0: delay = 3.0
    msgs = read_messages()
    if not msgs:
        await inter.response.send_message(f"❌ File `{MSG_FILE}` rỗng hoặc không tồn tại.", ephemeral=True); return

    tag_prefix = f"<@{user.id}> " if user else ""
    stop = asyncio.Event()
    spam_stop_flags[cid] = stop

    async def _token_loop(tok):
        for _ in range(so_lan if so_lan > 0 else 10**9):
            if stop.is_set(): return
            for line in msgs:
                if stop.is_set(): return
                content = line if line.startswith("<@") else f"{tag_prefix}{line}"
                ok = await send_token_message(tok, cid, content)
                if not ok: await asyncio.sleep(2)
                else:      await asyncio.sleep(max(0.5, delay + delay*random.uniform(-0.15, 0.15)))

    async def run_all():
        tasks = [asyncio.create_task(_token_loop(tok)) for tok in tok_list]
        try: await asyncio.gather(*tasks)
        except Exception as e: log.error(f"ngonnhay: {e}")
        finally: spam_stop_flags.pop(cid, None)

    asyncio.create_task(run_all())
    await inter.response.send_message(
        f"🚀 Bắt đầu spam kênh `{cid}` với **{len(tok_list)}** token | loops={so_lan} | delay={delay}s",
        ephemeral=True)
    asyncio.create_task(report(
        inter.user, inter.guild, inter.channel, "/ngonnhay",
        f"Tokens: `{len(tok_list)}` | Channel: `{cid}` | Loops: `{so_lan}` | "
        f"Delay: `{delay}s` | Tag: `{user.id if user else 'none'}`"))

# ============================ SLASH: /leave ============================
@bot.tree.command(name="leave", description="Bot rời khỏi server này (owner)")
async def slash_leave(inter: discord.Interaction):
    if not await owner_guard(inter): return
    if inter.guild is None:
        await inter.response.send_message("⚠️ Chỉ dùng trong server.", ephemeral=True); return
    name = inter.guild.name
    gid = inter.guild.id
    await inter.response.send_message(f"👋 Đang rời `{name}`...", ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/leave", f"Rời guild `{gid}`"))
    try: await inter.guild.leave()
    except Exception as e: log.error(f"leave: {e}")

# ============================ SLASH: /xa ============================
@bot.tree.command(name="xa", description="Phát file nhạc trong voice (token nhập trực tiếp)")
@app_commands.describe(
    tokens="1 hoặc nhiều token, ngăn bởi dấu phẩy",
    channel_id="ID kênh voice",
    user="User nhận thông báo",
    file="File nhạc (upload) — để trống nếu dùng file trong thư mục Xả",
    so_thu_tu="Số thứ tự file trong thư mục Xả (VD: 1 → 1.mp3)",
)
async def slash_xa(inter: discord.Interaction,
                   tokens: str,
                   channel_id: str,
                   user: discord.User,
                   file: Optional[discord.Attachment] = None,
                   so_thu_tu: Optional[int] = None):
    if not await owner_guard(inter): return
    tok_list = parse_tokens(tokens)
    if not tok_list:
        await inter.response.send_message("❌ Token không hợp lệ.", ephemeral=True); return
    try: cid = int(channel_id)
    except ValueError:
        await inter.response.send_message("❌ ID kênh không hợp lệ.", ephemeral=True); return

    target_path: Optional[Path] = None
    if file is not None:
        XA_DIR.mkdir(exist_ok=True)
        target_path = XA_DIR / file.filename
        try: await file.save(target_path)
        except Exception as e:
            await inter.response.send_message(f"❌ Không lưu được file: {e}", ephemeral=True); return
    elif so_thu_tu is not None:
        for ext in (".mp3", ".wav", ".ogg", ".m4a"):
            c = XA_DIR / f"{so_thu_tu}{ext}"
            if c.exists(): target_path = c; break
        if target_path is None:
            await inter.response.send_message(
                f"❌ Không tìm thấy file `{so_thu_tu}.mp3/wav/ogg/m4a` trong thư mục `Xả/`.",
                ephemeral=True); return
    else:
        await inter.response.send_message("❌ Cần upload file hoặc nhập `so_thu_tu`.", ephemeral=True); return

    try:
        with open("xa_config.json", "w", encoding="utf-8") as f:
            json.dump({"file": str(target_path.resolve()), "channel_id": cid,
                       "user_id": user.id, "tokens": tok_list, "ts": time.time()},
                      f, ensure_ascii=False)
    except Exception as e: log.warning(f"xa_config: {e}")

    started = 0
    for tok in tok_list:
        w = VoiceWorker(tok, inter.guild_id or 0, cid, mute=True, deaf=False, stream=False)
        active_voice_workers.append(w)
        asyncio.create_task(w.run())
        started += 1
        await asyncio.sleep(0.4)

    await inter.response.send_message(
        f"🎶 Đã treo **{started}** token vào kênh `{cid}` với file `{target_path.name}`.\n"
        f"⚠️ Để phát nhạc thực sự, chạy kèm `node xa 4.js` (đọc `xa_config.json`).",
        ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/xa",
        f"Tokens: `{len(tok_list)}` | Channel: `{cid}` | User: <@{user.id}> | File: `{target_path.name}`"))

# ============================ PREFIX COMMANDS ============================
@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound): return
    if isinstance(error, commands.CheckFailure):
        try: await ctx.reply("⛔ Không có quyền.", mention_author=False)
        except Exception: pass
        return
    log.error(f"cmd error: {error}")

def _prefix_guard(ctx: commands.Context) -> bool:
    if not is_owner(ctx.author.id): return False
    if cd_left(ctx.author.id) > 0: return False
    return True

@bot.command(name="spam")
async def prefix_spam(ctx: commands.Context, tokens: str, channel_id: str, count: int, *args):
    """t?spam <tokens> <channel_id> <count> [delay] <content...>"""
    if not _prefix_guard(ctx): return
    tok_list = parse_tokens(tokens)
    if not tok_list:
        await ctx.reply("❌ Token không hợp lệ."); return
    try: cid = int(channel_id)
    except ValueError:
        await ctx.reply("❌ ID kênh không hợp lệ."); return

    delay = 3.0
    parts = list(args)
    if parts:
        try:
            maybe = float(parts[0])
            delay = max(0.5, maybe); parts = parts[1:]
        except ValueError:
            pass
    content = " ".join(parts).strip()
    if not content:
        await ctx.reply(f"⚠️ Cú pháp: `{ctx.prefix}spam <tokens> <channel_id> <count> [delay] <nội dung>`")
        return

    stop = asyncio.Event()
    spam_stop_flags[cid] = stop

    async def run_one(tok):
        sent = 0
        while not stop.is_set():
            if count > 0 and sent >= count: return
            await send_token_message(tok, cid, content)
            sent += 1
            await asyncio.sleep(max(0.5, delay + delay*random.uniform(-0.15, 0.15)))

    for tok in tok_list:
        asyncio.create_task(run_one(tok))

    try: await ctx.message.delete()
    except Exception: pass
    try:
        await ctx.author.send(
            f"🚀 Đã bắt đầu spam kênh `{cid}` với {len(tok_list)} token | "
            f"count={count} (0=vô hạn) | delay={delay}s | content=`{content[:80]}`")
    except Exception:
        await ctx.reply("🚀 Bắt đầu spam.")

    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel,
        f"{ctx.prefix}spam <tokens:{len(tok_list)}> {channel_id} {count} {delay} {content}",
        f"Tokens: `{len(tok_list)}` | Channel: `{cid}` | Count: `{count}` | Delay: `{delay}s`"))

@bot.command(name="leave")
async def prefix_leave(ctx: commands.Context):
    if not _prefix_guard(ctx): return
    if ctx.guild is None:
        await ctx.reply("⚠️ Chỉ dùng trong server."); return
    name, gid = ctx.guild.name, ctx.guild.id
    await ctx.reply(f"👋 Rời `{name}`...")
    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel, f"{ctx.prefix}leave", f"Rời guild `{gid}`"))
    try: await ctx.guild.leave()
    except Exception as e: log.error(f"prefix leave: {e}")

# ============================ READY ============================
@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[{OWNER_NAME.upper()}] ✅ Logged in as {bot.user} ({bot.user.id}){Style.RESET_ALL}")
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.CYAN}[{OWNER_NAME.upper()}] ✅ Synced {len(synced)} slash commands{Style.RESET_ALL}")
    except Exception as e:
        log.error(f"sync: {e}")
    try:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{OWNER_NAME} PANEL"),
            status=discord.Status.dnd)
    except Exception: pass
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 🎭 Bot sẵn sàng — owner: {OWNER_NAME}{Style.RESET_ALL}")
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")

# ============================ RUN ============================
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise SystemExit("❌ Thiếu DISCORD_TOKEN trong .env")
    if not LOG_WEBHOOK_URL:
        print("⚠️ Chưa cấu hình LOG_WEBHOOK_URL trong .env — sẽ không gửi log lệnh.")

    clear_console()
    print_banner(OWNER_NAME)

    XA_DIR.mkdir(exist_ok=True)
    bot.run(BOT_TOKEN)
