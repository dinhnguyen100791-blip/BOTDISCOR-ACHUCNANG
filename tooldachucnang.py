# main.py — HARIDWG PANEL v4.0
# Bot Discord + Web Dashboard + WebSocket realtime — chạy trên Render
# Fix /dungtreo: dừng cả spam + treongon + treo room
# /treongon mới: delay + channel_id + server_id + tokens + file (autocomplete hoặc upload)
# /spam: gửi nội dung giữ nguyên định dạng (emoji, xuống dòng, dấu)
# /customrpl: đổi tên panel
# Auto-tạo ngontreo_1.txt → ngontreo_4.txt khi khởi động
import os, json, asyncio, random, time, aiohttp, base64, re, unicodedata, logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from aiohttp import web as aioweb

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
except ImportError:
    class Fore: RED=GREEN=CYAN=WHITE=YELLOW=MAGENTA=RESET=""
    class Style: BRIGHT=RESET_ALL=""

load_dotenv()
os.system("")

# ══════════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════════
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_banner(panel_name: str = "HARIDWG PANEL", owner_name: str = "haridwg"):
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
    print(f"{CYAN}          ║{WHITE}       🎭  {panel_name}  •  v4.0  🎭          {CYAN}║{RESET}")
    print(f"{CYAN}          ║{WHITE}       Owner: {DARK_RED}{owner_name}{WHITE} — Multitool Discord     {CYAN}║{RESET}")
    print(f"{CYAN}          ╚═══════════════════════════════════════════════════╝{RESET}")
    print()
    print(f"{DARK_RED}{'─'*70}{RESET}")
    print(f"{BLOOD}  [•] Panel          : {WHITE}{panel_name}{RESET}")
    print(f"{BLOOD}  [•] Owner          : {WHITE}{owner_name}{RESET}")
    print(f"{BLOOD}  [•] Prefix         : {WHITE}t?help  t?spam  t?treongon{RESET}")
    print(f"{BLOOD}  [•] Web Dashboard  : {WHITE}ENABLED{RESET}")
    print(f"{BLOOD}  [•] WebSocket      : {WHITE}ENABLED /ws?secret=***{RESET}")
    print(f"{BLOOD}  [•] Auto-file      : {WHITE}ngontreo_1→4 + ngonnhay_1→6{RESET}")
    print(f"{BLOOD}  [•] Status         : {WHITE}ĐANG KHỞI ĐỘNG...{RESET}")
    print(f"{DARK_RED}{'─'*70}{RESET}")
    print()

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
BOT_TOKEN        = os.getenv("DISCORD_TOKEN")
LOG_WEBHOOK_URL  = os.getenv("LOG_WEBHOOK_URL", "").strip()
OWNER_NAME       = "haridwg"
DEFAULT_OWNER_IDS = {1504134318698660000, 1511259341532041368}
COOLDOWN         = 5.0
DEFAULT_PREFIX   = "t?"
PREFIX_FILE      = "prefixes.json"
INVITE_FILE      = "invites.json"
OWNERS_FILE      = "owners.json"
USERS_FILE       = "users.json"
PANEL_FILE       = "panel.json"
MSG_FILE         = "noidung.txt"
XA_DIR           = Path("Xả")
FFMPEG           = os.getenv("FFMPEG_PATH", "ffmpeg")

NGON_PREFIXES    = ("ngontreo", "ngonnhay")

PORT             = int(os.getenv("PORT", "8080"))
WS_SECRET        = os.getenv("WS_SECRET", "haridwg_secret_2025")
BOT_START_TIME   = time.time()
connected_ws_clients: set = set()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("haridwg")

# ══════════════════════════════════════════════════════════════
#  STORAGE
# ══════════════════════════════════════════════════════════════
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
extra_owners:   set              = set(_load(OWNERS_FILE, []))
extra_users:    set              = set(_load(USERS_FILE, []))
panel_config:   dict             = _load(PANEL_FILE, {"name": "HARIDWG PANEL"})

def get_panel_name() -> str:
    return str(panel_config.get("name", "HARIDWG PANEL"))

def set_panel_name(name: str):
    panel_config["name"] = name
    _save(PANEL_FILE, panel_config)

user_cooldowns: Dict[int, float] = {}
active_voice_workers: List = []

# 🆕 Registry tất cả stop events (dùng cho /dungtreo)
_active_stop_events: List[asyncio.Event] = []

def register_stop() -> asyncio.Event:
    evt = asyncio.Event()
    _active_stop_events.append(evt)
    return evt

def unregister_stop(evt: asyncio.Event):
    try: _active_stop_events.remove(evt)
    except ValueError: pass

# ══════════════════════════════════════════════════════════════
#  PERMISSION
# ══════════════════════════════════════════════════════════════
def is_owner(uid: int) -> bool:
    return uid in DEFAULT_OWNER_IDS or uid in extra_owners

def is_user(uid: int) -> bool:
    return is_owner(uid) or uid in extra_users

# ══════════════════════════════════════════════════════════════
#  TOKEN PARSER + SANITIZE
# ══════════════════════════════════════════════════════════════
def parse_tokens(raw) -> List[str]:
    if not raw: return []
    if isinstance(raw, list):
        raw = ",".join(str(x) for x in raw)
    parts = re.split(r"[\s,;]+", str(raw).strip())
    return [t for t in parts if len(t) > 20]

def read_messages() -> List[str]:
    if not os.path.exists(MSG_FILE): return []
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        return [l.rstrip("\r\n") for l in f if l.strip()]

def sanitize(text: str, max_len: int = 2000) -> str:
    """
    Chỉ loại bỏ ký tự GÂY CRASH khi gửi Discord API:
      - Surrogate (U+D800–U+DFFF): không hợp lệ UTF-8
      - Null byte (\x00): Discord từ chối
    GIỮ NGUYÊN: newline (\n), tab, emoji, tiếng Việt có dấu, mọi ký tự khác.
    """
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[\ud800-\udfff]', '', text)
    text = text.replace('\x00', '')
    if not text:
        text = " "
    if len(text) > max_len:
        text = text[:max_len-3] + "..."
    return text

# ══════════════════════════════════════════════════════════════
#  NGON — File scanner + parser + auto-create
# ══════════════════════════════════════════════════════════════
def find_ngon_files() -> List[Path]:
    """Quét file có tên bắt đầu bằng 'ngontreo' hoặc 'ngonnhay'."""
    results = []
    try:
        for f in Path(".").iterdir():
            try:
                if f.is_file():
                    name_lower = f.name.lower()
                    if any(name_lower.startswith(p) for p in NGON_PREFIXES):
                        results.append(f)
            except Exception:
                continue
    except Exception as e:
        log.warning(f"find_ngon_files: {e}")
    return sorted(results, key=lambda p: p.name.lower())

def read_ngon_file(path: Path) -> List[str]:
    """Đọc file — giữ NGUYÊN mọi dòng không trống (kể cả dòng `#`)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.rstrip("\r\n") for l in f]
        return [l for l in lines if l.strip()]
    except Exception as e:
        log.error(f"read_ngon_file {path}: {e}")
        return []

def parse_ngon_source(nguon: str) -> List[str]:
    """Nếu là file có thật → đọc file. Ngược lại coi là text tự viết."""
    if not nguon:
        return []
    p = Path(nguon)
    if p.exists() and p.is_file():
        return read_ngon_file(p)
    for ext in (".txt", ".md", ".ngon", ""):
        cand = Path(nguon + ext)
        if cand.exists() and cand.is_file():
            return read_ngon_file(cand)
    text = nguon.strip()
    if "\n" in text:
        parts = [l.strip() for l in text.split("\n")]
    elif "|" in text:
        parts = [l.strip() for l in text.split("|")]
    else:
        parts = [text]
    return [l for l in parts if l]

# ─── File mặc định tự tạo khi khởi động ─────────────────────
DEFAULT_NGON_FILES = {
    "ngontreo_1.txt": """Xin chào, mình là haridwg
Chúc bạn một ngày tốt lành 🌸
Đừng quên uống nước nhé 💧
HARIDWG PANEL đã online
""",
    "ngontreo_2.txt": """# Comment vẫn được gửi
Hôm nay trời đẹp ghê
# Dòng này cũng gửi luôn
Cảm ơn đã đọc hết
""",
    "ngontreo_3.txt": """Chúc bạn ngủ ngon 🌙
Ngày mai lại cố gắng nhé
Yêu thương nhiều 💕
Mơ đẹp nha
""",
    "ngontreo_4.txt": """Bot đang hoạt động bình thường ✅
Mọi người có thể dùng lệnh /help
Nhớ tuân thủ nội quy server
Cảm ơn đã ủng hộ
""",
    # Giữ ngonnhay_* cho tương thích ngược
    "ngonnhay_1.txt": """Xin chào
Chúc ngày tốt lành 🌸
""",
    "ngonnhay_2.txt": """Test ngonnhay 2
Dòng 2
""",
    "ngonnhay_3.txt": """Test ngonnhay 3
""",
    "ngonnhay_4.txt": """Test ngonnhay 4
""",
    "ngonnhay_5.txt": """Test ngonnhay 5
""",
    "ngonnhay_6.txt": """Test ngonnhay 6
""",
}

def ensure_ngon_files():
    """Tạo file ngontreo_1..4 + ngonnhay_1..6 nếu chưa có. KHÔNG ghi đè file có sẵn."""
    created, skipped = [], []
    for name, content in DEFAULT_NGON_FILES.items():
        p = Path(name)
        if p.exists():
            skipped.append(name); continue
        try:
            with open(p, "w", encoding="utf-8") as f: f.write(content)
            created.append(name)
        except Exception as e:
            log.error(f"Không tạo được {name}: {e}")
    if created:
        log.info(f"📁 Đã tạo {len(created)} file mẫu: {', '.join(created)}")
    if skipped:
        log.info(f"📁 Đã có sẵn {len(skipped)} file (bỏ qua)")
    return created, skipped

# ─── Autocomplete ────────────────────────────────────────────
async def ngon_autocomplete(interaction: discord.Interaction, current: str):
    files = find_ngon_files()
    cur = (current or "").lower()
    return [
        app_commands.Choice(name=f.name, value=f.name)
        for f in files if cur in f.name.lower()
    ][:25]

# ══════════════════════════════════════════════════════════════
#  COOLDOWN
# ══════════════════════════════════════════════════════════════
def cd_left(uid: int) -> float:
    now = time.time()
    last = user_cooldowns.get(uid, 0)
    rem = COOLDOWN - (now - last)
    if rem > 0: return rem
    user_cooldowns[uid] = now
    return 0.0

# ══════════════════════════════════════════════════════════════
#  INVITE + WEBHOOK
# ══════════════════════════════════════════════════════════════
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
    if not LOG_WEBHOOK_URL: return
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
        "title": f"📋 [{get_panel_name()}] LỆNH VỪA SỬ DỤNG",
        "color": 0xE7000B,
        "fields": fields,
        "footer": {"text": f"{get_panel_name()} • v4.0"},
    }
    try:
        async with aiohttp.ClientSession() as s:
            await s.post(LOG_WEBHOOK_URL, json={"embeds": [embed]})
    except Exception as e: log.error(f"webhook: {e}")

# ══════════════════════════════════════════════════════════════
#  TOKEN HTTP (send message via user token)
# ══════════════════════════════════════════════════════════════
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

async def send_token_message(token: str, channel_id: int, content: str) -> bool:
    """Gửi 1 message qua user token. Nội dung đã được sanitize ở ngoài."""
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

# ══════════════════════════════════════════════════════════════
#  VOICE WORKER
# ══════════════════════════════════════════════════════════════
class VoiceWorker:
    def __init__(self, token: str, guild_id: int, channel_id: int,
                 mute: bool = False, deaf: bool = True, stream: bool = False):
        self.token = token
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.mute = mute; self.deaf = deaf; self.stream = stream
        self.ws = None; self.session = None
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
                    except asyncio.TimeoutError: break
                    except Exception: break
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

def stop_all_activity() -> dict:
    """🆕 Dừng TẤT CẢ: voice workers + spam/treongon tasks."""
    global active_voice_workers
    n_voice = len(active_voice_workers)
    for w in active_voice_workers:
        try: w.stop()
        except Exception: pass
    active_voice_workers.clear()

    n_events = len(_active_stop_events)
    for evt in _active_stop_events:
        try: evt.set()
        except Exception: pass

    return {"voice": n_voice, "tasks": n_events}

# ══════════════════════════════════════════════════════════════
#  BOT SETUP
# ══════════════════════════════════════════════════════════════
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

async def slash_owner_guard(inter) -> bool:
    if not is_owner(inter.user.id):
        await inter.response.send_message("⛔ Chỉ **owner** dùng được lệnh này.", ephemeral=True)
        return False
    rem = cd_left(inter.user.id)
    if rem > 0:
        await inter.response.send_message(f"⏳ Chờ **{rem:.1f}s**.", ephemeral=True)
        return False
    return True

async def slash_user_guard(inter) -> bool:
    if not is_user(inter.user.id):
        await inter.response.send_message("⛔ Bạn không có quyền dùng lệnh này.", ephemeral=True)
        return False
    rem = cd_left(inter.user.id)
    if rem > 0:
        await inter.response.send_message(f"⏳ Chờ **{rem:.1f}s**.", ephemeral=True)
        return False
    return True

def prefix_owner_guard(ctx: commands.Context) -> bool:
    return is_owner(ctx.author.id) and cd_left(ctx.author.id) == 0

def prefix_user_guard(ctx: commands.Context) -> bool:
    return is_user(ctx.author.id) and cd_left(ctx.author.id) == 0

# ══════════════════════════════════════════════════════════════
#  PREFIX COMMANDS
# ══════════════════════════════════════════════════════════════
@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.CommandNotFound): return
    log.error(f"cmd error: {error}")

@bot.command(name="help")
async def prefix_help(ctx: commands.Context):
    if not prefix_user_guard(ctx): return
    p = ctx.prefix
    e = discord.Embed(
        title=f"📖 {get_panel_name()} — Danh sách lệnh",
        description=f"Prefix server này: `{p}` • Cooldown: `{int(COOLDOWN)}s`",
        color=0xE7000B,
    )
    e.add_field(name="👤 USER", value=(
        f"`{p}help` — Danh sách lệnh\n"
        f"`{p}spam <tokens> <channel_id> <count> [delay] <nội dung>`\n"
        f"`{p}treongon <channel_id> <tokens> <số_lần> [delay|_] [nguon]`"
    ), inline=False)
    e.add_field(name="👑 OWNER", value=(
        f"`{p}adduser` / `{p}addowner` — Thêm quyền\n"
        f"`{p}removeuser` / `{p}removeowner` — Xoá quyền\n"
        f"`{p}listperm` — Xem phân quyền\n"
        f"`{p}leave` — Rời server\n"
        f"`{p}addprefix <prefix>` — Đổi prefix\n"
        f"`{p}dungtreoall` — Dừng tất cả token + spam"
    ), inline=False)
    e.add_field(name="⚡ SLASH", value=(
        "`/help` `/treoroom` `/treongon` `/spam` `/xa`\n"
        "`/dungtreo` `/addprefix` `/leave`\n"
        "`/adduser` `/addowner` `/customrpl`"
    ), inline=False)
    e.set_footer(text=f"{get_panel_name()} • v4.0")
    await ctx.reply(embed=e, mention_author=False)
    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel, f"{p}help"))

@bot.command(name="spam")
async def prefix_spam(ctx: commands.Context, tokens: str, channel_id: str, count: int, *args):
    if not prefix_user_guard(ctx): return
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
            delay = max(0.5, float(parts[0])); parts = parts[1:]
        except ValueError: pass
    content = " ".join(parts).strip()
    if not content:
        await ctx.reply(f"⚠️ Cú pháp: `{ctx.prefix}spam <tokens> <channel_id> <count> [delay] <nội dung>`")
        return

    content = sanitize(content)
    stop = register_stop()

    async def run_one(tok):
        sent = 0
        while not stop.is_set():
            if count > 0 and sent >= count: return
            await send_token_message(tok, cid, content)
            sent += 1
            await asyncio.sleep(max(0.5, delay + delay*random.uniform(-0.15, 0.15)))

    async def run_all():
        tasks = [asyncio.create_task(run_one(tok)) for tok in tok_list]
        try: await asyncio.gather(*tasks)
        except Exception as e: log.error(f"prefix_spam: {e}")
        finally: unregister_stop(stop)

    asyncio.create_task(run_all())
    try: await ctx.message.delete()
    except Exception: pass
    try:
        await ctx.author.send(f"🚀 Spam `{cid}` với {len(tok_list)} token | count={count} | delay={delay}s")
    except Exception:
        await ctx.reply("🚀 Bắt đầu spam.")

    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel,
        f"{ctx.prefix}spam <tokens:{len(tok_list)}> {channel_id} {count} {delay} {content}",
        f"Tokens: `{len(tok_list)}` | Channel: `{cid}` | Count: `{count}` | Delay: `{delay}s`"))

@bot.command(name="treongon")
async def prefix_treongon(ctx: commands.Context, channel_id: str, tokens: str,
                          so_lan: int = 1, *args):
    if not prefix_user_guard(ctx): return
    tok_list = parse_tokens(tokens)
    if not tok_list:
        await ctx.reply("❌ Token không hợp lệ."); return
    try: cid = int(channel_id)
    except ValueError:
        await ctx.reply("❌ ID kênh không hợp lệ."); return

    delay = 3.0
    nguon_text = ""
    parts = list(args)
    if parts:
        first = parts[0]
        if first == "_":
            nguon_text = " ".join(parts[1:]).strip()
        else:
            try:
                delay = float(first); nguon_text = " ".join(parts[1:]).strip()
            except ValueError:
                nguon_text = " ".join(parts).strip()
    if delay < 3.0: delay = 3.0

    lines = parse_ngon_source(nguon_text)
    used_from = ""
    if lines:
        p = Path(nguon_text)
        if p.exists() and p.is_file():
            used_from = f"file `{p.name}`"
        else:
            for ext in (".txt", ".md", ".ngon"):
                if Path(nguon_text + ext).exists():
                    used_from = f"file `{nguon_text}{ext}`"
                    break
        if not used_from:
            used_from = "text tự viết"
    if not lines:
        lines = read_messages()
        if lines: used_from = f"file mặc định `{MSG_FILE}`"
    if not lines:
        await ctx.reply("❌ Không có nội dung để gửi."); return

    stop = register_stop()
    async def _token_loop(tok):
        for _ in range(so_lan if so_lan > 0 else 10**9):
            if stop.is_set(): return
            for line in lines:
                if stop.is_set(): return
                ok = await send_token_message(tok, cid, sanitize(line))
                if not ok: await asyncio.sleep(2)
                else: await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))

    async def run_all():
        tasks = [asyncio.create_task(_token_loop(tok)) for tok in tok_list]
        try: await asyncio.gather(*tasks)
        except Exception as e: log.error(f"prefix_treongon: {e}")
        finally: unregister_stop(stop)

    asyncio.create_task(run_all())
    try: await ctx.message.delete()
    except Exception: pass
    await ctx.reply(f"🚀 Gửi {used_from} ({len(lines)} câu), delay `{delay}s`, loops={so_lan}")

    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel,
        f"{ctx.prefix}treongon {channel_id} <tokens:{len(tok_list)}> {so_lan} {delay} {nguon_text[:80]}",
        f"Channel: `{cid}` | Tokens: `{len(tok_list)}` | Loops: `{so_lan}` | Delay: `{delay}s` | Nguồn: {used_from}"))

@bot.command(name="adduser")
async def prefix_adduser(ctx: commands.Context, target: str):
    if not prefix_owner_guard(ctx): return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ Cần **ID** hoặc **@mention**."); return
    uid = int(m.group(1))
    if uid in extra_users: await ctx.reply(f"ℹ️ Đã có."); return
    if is_owner(uid): await ctx.reply(f"ℹ️ Đã là owner."); return
    extra_users.add(uid); _save(USERS_FILE, sorted(extra_users))
    await ctx.reply(f"✅ Đã thêm <@{uid}> vào **USER**.")

@bot.command(name="addowner")
async def prefix_addowner(ctx: commands.Context, target: str):
    if not prefix_owner_guard(ctx): return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ Cần **ID** hoặc **@mention**."); return
    uid = int(m.group(1))
    if is_owner(uid): await ctx.reply(f"ℹ️ Đã là owner."); return
    extra_owners.add(uid); extra_users.discard(uid)
    _save(OWNERS_FILE, sorted(extra_owners)); _save(USERS_FILE, sorted(extra_users))
    await ctx.reply(f"✅ Đã thêm <@{uid}> vào **OWNER**.")

@bot.command(name="removeuser")
async def prefix_removeuser(ctx: commands.Context, target: str):
    if not prefix_owner_guard(ctx): return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID không hợp lệ."); return
    uid = int(m.group(1))
    if uid in extra_users:
        extra_users.discard(uid); _save(USERS_FILE, sorted(extra_users))
        await ctx.reply(f"🗑️ Đã xoá <@{uid}>.")
    else: await ctx.reply("ℹ️ Không có trong danh sách.")

@bot.command(name="removeowner")
async def prefix_removeowner(ctx: commands.Context, target: str):
    if not prefix_owner_guard(ctx): return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID không hợp lệ."); return
    uid = int(m.group(1))
    if uid in DEFAULT_OWNER_IDS: await ctx.reply("🚫 Không xoá được owner gốc."); return
    if uid in extra_owners:
        extra_owners.discard(uid); _save(OWNERS_FILE, sorted(extra_owners))
        await ctx.reply(f"🗑️ Đã xoá <@{uid}>.")
    else: await ctx.reply("ℹ️ Không có trong danh sách.")

@bot.command(name="listperm")
async def prefix_listperm(ctx: commands.Context):
    if not prefix_owner_guard(ctx): return
    e = discord.Embed(title=f"🔐 Phân quyền — {get_panel_name()}", color=0xE7000B)
    e.add_field(name=f"👑 OWNER GỐC ({len(DEFAULT_OWNER_IDS)})",
                value="\n".join(f"• <@{u}>" for u in sorted(DEFAULT_OWNER_IDS)) or "—", inline=False)
    e.add_field(name=f"👑 OWNER THÊM ({len(extra_owners)})",
                value="\n".join(f"• <@{u}>" for u in sorted(extra_owners)) or "—", inline=False)
    e.add_field(name=f"👤 USER ({len(extra_users)})",
                value="\n".join(f"• <@{u}>" for u in sorted(extra_users)) or "—", inline=False)
    await ctx.reply(embed=e)

@bot.command(name="addprefix")
async def prefix_addprefix(ctx: commands.Context, new_prefix: str):
    if not prefix_owner_guard(ctx): return
    if ctx.guild is None: await ctx.reply("⚠️ Chỉ dùng trong server."); return
    if not new_prefix or len(new_prefix) > 5: await ctx.reply("❌ Prefix 1-5 ký tự."); return
    server_prefixes[str(ctx.guild.id)] = new_prefix
    _save(PREFIX_FILE, server_prefixes)
    await ctx.reply(f"✅ Đã đổi prefix thành `{new_prefix}`.")

@bot.command(name="leave")
async def prefix_leave(ctx: commands.Context):
    if not prefix_owner_guard(ctx): return
    if ctx.guild is None: await ctx.reply("⚠️ Chỉ dùng trong server."); return
    name, gid = ctx.guild.name, ctx.guild.id
    await ctx.reply(f"👋 Rời `{name}`...")
    asyncio.create_task(report(ctx.author, ctx.guild, ctx.channel, f"{ctx.prefix}leave", f"Rời guild `{gid}`"))
    try: await ctx.guild.leave()
    except Exception as e: log.error(f"leave: {e}")

@bot.command(name="dungtreoall")
async def prefix_dungtreoall(ctx: commands.Context):
    if not prefix_owner_guard(ctx): return
    r = stop_all_activity()
    await ctx.reply(f"🛑 Đã dừng **{r['voice']}** voice + **{r['tasks']}** task spam/treongon.")

# ══════════════════════════════════════════════════════════════
#  SLASH COMMANDS
# ══════════════════════════════════════════════════════════════
@bot.tree.command(name="help", description="Danh sách lệnh slash")
async def slash_help(inter: discord.Interaction):
    if not await slash_user_guard(inter): return
    e = discord.Embed(title=f"⚡ {get_panel_name()} — Slash", color=0xE7000B)
    e.add_field(name="👤 USER", value=(
        "`/help` — Danh sách lệnh\n"
        "`/treoroom` — Treo voice (DM bot)\n"
        "`/treongon` — Nhắn từ file/text\n"
        "`/spam` — Spam nội dung giữ nguyên định dạng\n"
        "`/xa` — Phát nhạc trong voice"
    ), inline=False)
    e.add_field(name="👑 OWNER", value=(
        "`/dungtreo` — Dừng tất cả (voice + spam)\n"
        "`/addprefix` `/leave`\n"
        "`/adduser` `/addowner`\n"
        "`/customrpl` — Đổi tên panel"
    ), inline=False)
    await inter.response.send_message(embed=e, ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/help"))

# 🆕 /customrpl
@bot.tree.command(name="customrpl", description="Đổi tên panel hiển thị (owner)")
@app_commands.describe(name="Tên mới muốn hiển thị")
async def slash_customrpl(inter: discord.Interaction, name: str):
    if not await slash_owner_guard(inter): return
    name = name.strip()
    if not name or len(name) > 60:
        await inter.response.send_message("❌ Tên phải từ 1-60 ký tự.", ephemeral=True); return
    old = get_panel_name()
    set_panel_name(name)
    await inter.response.send_message(f"✅ Đã đổi tên panel:\n• Cũ: `{old}`\n• Mới: `{name}`", ephemeral=True)
    try:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=name),
            status=discord.Status.dnd)
    except Exception: pass
    asyncio.create_task(report(inter.user, inter.guild, inter.channel,
        f"/customrpl {name}", f"Panel name: `{old}` → `{name}`"))

@bot.tree.command(name="addprefix", description="Đổi prefix server (owner)")
@app_commands.describe(prefix="Prefix mới")
async def slash_addprefix(inter: discord.Interaction, prefix: str):
    if not await slash_owner_guard(inter): return
    if inter.guild is None:
        await inter.response.send_message("⚠️ Chỉ trong server.", ephemeral=True); return
    server_prefixes[str(inter.guild.id)] = prefix
    _save(PREFIX_FILE, server_prefixes)
    await inter.response.send_message(f"✅ Đổi prefix thành `{prefix}`.", ephemeral=True)

@bot.tree.command(name="adduser", description="Thêm user (owner)")
async def slash_adduser(inter: discord.Interaction, user: discord.User):
    if not await slash_owner_guard(inter): return
    if user.id in extra_users:
        await inter.response.send_message(f"ℹ️ Đã có.", ephemeral=True); return
    if is_owner(user.id):
        await inter.response.send_message(f"ℹ️ Đã là owner.", ephemeral=True); return
    extra_users.add(user.id); _save(USERS_FILE, sorted(extra_users))
    await inter.response.send_message(f"✅ Thêm {user.mention} vào **USER**.", ephemeral=True)

@bot.tree.command(name="addowner", description="Thêm owner (owner)")
async def slash_addowner(inter: discord.Interaction, user: discord.User):
    if not await slash_owner_guard(inter): return
    if is_owner(user.id):
        await inter.response.send_message(f"ℹ️ Đã là owner.", ephemeral=True); return
    extra_owners.add(user.id); extra_users.discard(user.id)
    _save(OWNERS_FILE, sorted(extra_owners)); _save(USERS_FILE, sorted(extra_users))
    await inter.response.send_message(f"✅ Thêm {user.mention} vào **OWNER**.", ephemeral=True)

class TreoRoomModal(discord.ui.Modal, title="🎙️ TREO ROOM"):
    f_token   = discord.ui.TextInput(label="Token (1 hoặc nhiều, phẩy)", style=discord.TextStyle.paragraph,
                                     required=True, max_length=4000)
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
            gid = int(str(self.f_server.value).strip())
            cid = int(str(self.f_channel.value).strip())
        except ValueError:
            await interaction.response.send_message("❌ ID không hợp lệ.", ephemeral=True); return
        mute   = str(self.f_mic.value).strip().lower()   == "on"
        deaf   = not (str(self.f_head.value).strip().lower() == "on")
        stream = str(self.f_stream.value).strip().lower() == "on"
        await interaction.response.send_message(
            f"⏳ Đang treo **{len(tokens)}** token vào `{cid}`...", ephemeral=True)
        await start_treo_room(tokens, gid, cid, mute, deaf, stream,
                              lambda m: interaction.followup.send(m, ephemeral=True))
        asyncio.create_task(report(interaction.user, interaction.guild, interaction.channel,
            "/treoroom", f"Tokens: `{len(tokens)}` | Server: `{gid}` | Channel: `{cid}`"))

@bot.tree.command(name="treoroom", description="Mở form treo token vào voice")
async def slash_treoroom(inter: discord.Interaction):
    if not await slash_user_guard(inter): return
    if inter.guild is not None:
        try:
            await inter.user.send("⚠️ Vì bảo mật, hãy dùng `/treoroom` trong **DM với bot**.")
        except Exception: pass
    await inter.response.send_modal(TreoRoomModal())

# 🆕 /dungtreo (alias /dungtreoall) — FIX hoạt động đúng
@bot.tree.command(name="dungtreo", description="Dừng TẤT CẢ: voice + spam + treongon (owner)")
async def slash_dungtreo(inter: discord.Interaction):
    if not await slash_owner_guard(inter): return
    r = stop_all_activity()
    await inter.response.send_message(
        f"🛑 **Đã dừng tất cả:**\n"
        f"• Voice workers: **{r['voice']}**\n"
        f"• Task spam/treongon: **{r['tasks']}**",
        ephemeral=True)
    log.info(f"[DUNGTREO] voice={r['voice']} tasks={r['tasks']}")
    asyncio.create_task(report(inter.user, inter.guild, inter.channel,
        "/dungtreo", f"Voice: {r['voice']} | Tasks: {r['tasks']}"))

@bot.tree.command(name="dungtreoall", description="Alias của /dungtreo (owner)")
async def slash_dungtreoall(inter: discord.Interaction):
    if not await slash_owner_guard(inter): return
    r = stop_all_activity()
    await inter.response.send_message(
        f"🛑 Đã dừng **{r['voice']}** voice + **{r['tasks']}** task.", ephemeral=True)

# 🆕 /treongon — syntax mới: delay + channel_id + server_id + tokens + file/nguon
@bot.tree.command(name="treongon", description="Nhắn nội dung từ file ngontreo* hoặc text (user)")
@app_commands.describe(
    delay="Delay giây giữa các tin (tối thiểu 3)",
    channel_id="ID kênh cần nhắn",
    server_id="ID server (guild)",
    tokens="1 hoặc nhiều token, ngăn bởi dấu phẩy",
    so_lan="Số lần lặp lại (0 = vô hạn, mặc định 1)",
    file="Upload file (nếu không dùng file có sẵn)",
    nguon="Chọn file 'ngontreo*' / 'ngonnhay*' có sẵn (autocomplete)",
)
@app_commands.autocomplete(nguon=ngon_autocomplete)
async def slash_treongon(inter: discord.Interaction,
                         delay: float,
                         channel_id: str,
                         server_id: str,
                         tokens: str,
                         so_lan: int = 1,
                         file: Optional[discord.Attachment] = None,
                         nguon: Optional[str] = None):
    if not await slash_user_guard(inter): return

    tok_list = parse_tokens(tokens)
    if not tok_list:
        await inter.response.send_message("❌ Token không hợp lệ.", ephemeral=True); return

    try: cid = int(channel_id)
    except ValueError:
        await inter.response.send_message("❌ `channel_id` không hợp lệ.", ephemeral=True); return

    try: sid = int(server_id)
    except ValueError:
        await inter.response.send_message("❌ `server_id` không hợp lệ.", ephemeral=True); return

    if delay is None or delay < 3.0: delay = 3.0
    if so_lan is None: so_lan = 1

    # Ưu tiên: upload > chọn file > fallback
    lines: List[str] = []
    used_from = ""

    if file is not None:
        # Lưu vào thư mục với prefix ngontreo_
        fname = file.filename
        if not any(fname.lower().startswith(p) for p in NGON_PREFIXES):
            fname = f"ngontreo_{int(time.time())}_{fname}"
        save_path = Path(fname)
        try:
            await file.save(save_path)
            lines = read_ngon_file(save_path)
            used_from = f"file upload `{save_path.name}`"
        except Exception as e:
            await inter.response.send_message(f"❌ Không lưu được file: {e}", ephemeral=True); return
    elif nguon:
        lines = parse_ngon_source(nguon)
        used_from = f"file có sẵn `{nguon}`"
    else:
        lines = read_messages()
        if lines: used_from = f"file mặc định `{MSG_FILE}`"

    if not lines:
        await inter.response.send_message(
            "❌ Không có nội dung nào để gửi.\n"
            "• Chọn file `ngontreo*` ở ô **nguon**\n"
            "• Hoặc upload file ở ô **file**\n"
            "• Hoặc tạo file `noidung.txt`", ephemeral=True)
        return

    stop = register_stop()

    async def _token_loop(tok):
        for _ in range(so_lan if so_lan > 0 else 10**9):
            if stop.is_set(): return
            for line in lines:
                if stop.is_set(): return
                ok = await send_token_message(tok, cid, sanitize(line))
                if not ok: await asyncio.sleep(2)
                else:      await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))

    async def run_all():
        tasks = [asyncio.create_task(_token_loop(tok)) for tok in tok_list]
        try: await asyncio.gather(*tasks)
        except Exception as e: log.error(f"treongon: {e}")
        finally: unregister_stop(stop)

    asyncio.create_task(run_all())

    preview = " | ".join(lines[:3])[:120] + (" ..." if len(lines) > 3 else "")
    await inter.response.send_message(
        f"🚀 **/treongon**\n"
        f"• Server: `{sid}` | Kênh: `{cid}`\n"
        f"• Tokens: `{len(tok_list)}` | Lặp: `{so_lan if so_lan>0 else '∞'}` | Delay: `{delay}s`\n"
        f"• Nguồn: {used_from} ({len(lines)} câu)\n"
        f"• Preview: {preview}",
        ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/treongon",
        f"Server: `{sid}` | Channel: `{cid}` | Tokens: `{len(tok_list)}` | Loops: `{so_lan}` | "
        f"Delay: `{delay}s` | Nguồn: {used_from}"))

# 🆕 /spam — gửi nội dung giữ nguyên định dạng, dùng admin bot
@bot.tree.command(name="spam", description="Spam nội dung (giữ nguyên emoji, xuống dòng, dấu)")
@app_commands.describe(
    channel_id="ID kênh cần spam",
    server_id="ID server (guild)",
    delay="Delay giây (tối thiểu 3)",
    content="Nội dung (giữ nguyên mọi ký tự: emoji, xuống dòng, dấu tiếng Việt...)",
    so_lan="Số lần gửi (mặc định 1, 0 = vô hạn)",
)
async def slash_spam(inter: discord.Interaction,
                     channel_id: str,
                     server_id: str,
                     delay: float,
                     content: str,
                     so_lan: int = 1):
    if not await slash_user_guard(inter): return

    try: cid = int(channel_id)
    except ValueError:
        await inter.response.send_message("❌ `channel_id` không hợp lệ.", ephemeral=True); return
    try: sid = int(server_id)
    except ValueError:
        await inter.response.send_message("❌ `server_id` không hợp lệ.", ephemeral=True); return

    if delay is None or delay < 3.0: delay = 3.0
    if so_lan is None: so_lan = 1

    # Lấy channel qua admin bot
    target_channel = bot.get_channel(cid)
    if target_channel is None:
        try: target_channel = await bot.fetch_channel(cid)
        except Exception as e:
            await inter.response.send_message(f"❌ Không tìm thấy kênh: {e}", ephemeral=True); return

    # Sanitize nhưng GIỮ NGUYÊN nội dung
    msg_content = sanitize(content, 2000)

    stop = register_stop()

    async def spam_loop():
        sent = 0
        try:
            while not stop.is_set():
                if so_lan > 0 and sent >= so_lan: break
                try:
                    await target_channel.send(msg_content)
                    sent += 1
                except discord.HTTPException as e:
                    log.warning(f"spam send error: {e}")
                    await asyncio.sleep(2)
                if stop.is_set(): break
                await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))
        except Exception as e:
            log.error(f"spam loop: {e}")
        finally:
            unregister_stop(stop)

    asyncio.create_task(spam_loop())

    preview = msg_content[:100].replace("\n", "\\n")
    await inter.response.send_message(
        f"🚀 **/spam**\n"
        f"• Server: `{sid}` | Kênh: `{cid}`\n"
        f"• Delay: `{delay}s` | Lần: `{so_lan if so_lan>0 else '∞'}`\n"
        f"• Preview: `{preview}{'...' if len(msg_content)>100 else ''}`",
        ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/spam",
        f"Server: `{sid}` | Channel: `{cid}` | Delay: `{delay}s` | Loops: `{so_lan}` | "
        f"Content: `{msg_content[:200]}`"))

@bot.tree.command(name="leave", description="Bot rời server (owner)")
async def slash_leave(inter: discord.Interaction):
    if not await slash_owner_guard(inter): return
    if inter.guild is None:
        await inter.response.send_message("⚠️ Chỉ trong server.", ephemeral=True); return
    name, gid = inter.guild.name, inter.guild.id
    await inter.response.send_message(f"👋 Rời `{name}`...", ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/leave", f"Rời `{gid}`"))
    try: await inter.guild.leave()
    except Exception as e: log.error(f"leave: {e}")

@bot.tree.command(name="xa", description="Phát nhạc trong voice (user)")
@app_commands.describe(
    tokens="1 hoặc nhiều token",
    channel_id="ID kênh voice",
    user="User nhận thông báo",
    file="Upload file nhạc",
    so_thu_tu="Số thứ tự file trong Xả/",
)
async def slash_xa(inter: discord.Interaction, tokens: str, channel_id: str,
                   user: discord.User,
                   file: Optional[discord.Attachment] = None,
                   so_thu_tu: Optional[int] = None):
    if not await slash_user_guard(inter): return
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
            await inter.response.send_message(f"❌ Lưu file lỗi: {e}", ephemeral=True); return
    elif so_thu_tu is not None:
        for ext in (".mp3", ".wav", ".ogg", ".m4a"):
            c = XA_DIR / f"{so_thu_tu}{ext}"
            if c.exists(): target_path = c; break
        if target_path is None:
            await inter.response.send_message(f"❌ Không có file `{so_thu_tu}` trong `Xả/`.", ephemeral=True); return
    else:
        await inter.response.send_message("❌ Cần upload hoặc `so_thu_tu`.", ephemeral=True); return

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

    await inter.response.send_message(f"🎶 Đã treo **{started}** token vào `{cid}` với `{target_path.name}`.", ephemeral=True)
    asyncio.create_task(report(inter.user, inter.guild, inter.channel, "/xa",
        f"Tokens: `{len(tok_list)}` | Channel: `{cid}` | File: `{target_path.name}`"))

# ══════════════════════════════════════════════════════════════
#  WEB SERVER + WEBSOCKET
# ══════════════════════════════════════════════════════════════
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{PANEL_NAME}} — Status</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a0a;color:#fff;font-family:'Consolas','Monaco',monospace;
    min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px;
    background-image:radial-gradient(circle at 50% 0%,rgba(255,0,0,.18),transparent 60%);}
  .mask{font-size:70px;margin-bottom:12px;filter:drop-shadow(0 0 25px rgba(255,0,0,.6));animation:float 3s ease-in-out infinite}
  @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
  .header{font-size:30px;color:#ff0000;text-shadow:0 0 12px #ff0000;letter-spacing:5px;margin-bottom:6px;text-align:center}
  .subtitle{color:#888;font-size:11px;margin-bottom:35px;letter-spacing:3px}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:20px;width:100%;max-width:960px}
  .card{background:linear-gradient(145deg,#1a0000,#0d0000);border:1px solid #ff0000;border-radius:12px;padding:24px;
    box-shadow:0 0 25px rgba(255,0,0,.2);position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s}
  .card:hover{transform:translateY(-4px);box-shadow:0 0 35px rgba(255,0,0,.4)}
  .card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,#ff0000,#ff5555,#ff0000)}
  .card-label{font-size:11px;color:#ff5555;text-transform:uppercase;letter-spacing:3px;margin-bottom:14px}
  .card-value{font-size:34px;font-weight:bold;color:#fff;text-shadow:0 0 10px rgba(255,0,0,.6);display:flex;align-items:center;gap:10px}
  .card-sub{font-size:11px;color:#666;margin-top:10px;letter-spacing:1px}
  .status-online{color:#00ff88!important;text-shadow:0 0 15px #00ff88!important;font-size:26px!important}
  .status-offline{color:#ff0000!important;text-shadow:0 0 15px #ff0000!important;font-size:26px!important}
  .dot{display:inline-block;width:12px;height:12px;border-radius:50%;flex-shrink:0;animation:pulse 2s infinite}
  .dot.online{background:#00ff88;box-shadow:0 0 15px #00ff88}
  .dot.offline{background:#ff0000;box-shadow:0 0 15px #ff0000;animation:none}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
  .footer{margin-top:40px;color:#333;font-size:10px;letter-spacing:3px;text-align:center}
  .footer a{color:#ff0000;text-decoration:none}
  .ws-status{position:fixed;top:14px;right:14px;font-size:10px;color:#555;padding:6px 12px;border:1px solid #333;border-radius:20px;background:#000;letter-spacing:1px}
  .ws-status.on{color:#00ff88;border-color:#00ff88}
  .ws-status.off{color:#ff0000;border-color:#ff0000}
  .glow{animation:glow 2s infinite}
  @keyframes glow{0%,100%{filter:drop-shadow(0 0 5px rgba(255,0,0,.5))}50%{filter:drop-shadow(0 0 20px rgba(255,0,0,1))}}
</style>
</head>
<body>
<div class="ws-status off" id="wsStat">● WS: KẾT NỐI...</div>
<div class="mask glow">🎭</div>
<div class="header">{{PANEL_NAME}}</div>
<div class="subtitle">● REALTIME MONITORING ●</div>
<div class="grid">
  <div class="card"><div class="card-label">Trạng thái Bot</div>
    <div class="card-value"><span class="dot offline" id="dot"></span>
      <span class="status-offline" id="status-text">Đang tải...</span></div>
    <div class="card-sub" id="bot-info">—</div></div>
  <div class="card"><div class="card-label">Số Server Bot Ở</div>
    <div class="card-value" id="guilds">—</div><div class="card-sub">guild</div></div>
  <div class="card"><div class="card-label">Số Câu Lệnh</div>
    <div class="card-value" id="cmds">—</div><div class="card-sub" id="cmd-sub">slash + prefix</div></div>
  <div class="card"><div class="card-label">Voice Đang Treo</div>
    <div class="card-value" id="voice">—</div><div class="card-sub">worker</div></div>
  <div class="card"><div class="card-label">Task Đang Chạy</div>
    <div class="card-value" id="tasks">—</div><div class="card-sub">spam / treongon</div></div>
  <div class="card"><div class="card-label">Uptime</div>
    <div class="card-value" id="uptime">—</div><div class="card-sub">kể từ khởi động</div></div>
</div>
<div class="footer">{{PANEL_NAME}} • v4.0 • WebSocket Realtime<br>
<a href="/api/status">/api/status</a> • <a href="/health">/health</a> • /ws</div>
<script>
let ws, rt;
function fmtUp(s){s=Math.floor(s);const d=Math.floor(s/86400),h=Math.floor((s%86400)/3600),
  m=Math.floor((s%3600)/60),x=s%60;if(d)return d+'d '+h+'h '+m+'m';if(h)return h+'h '+m+'m';
  if(m)return m+'m '+x+'s';return x+'s';}
function ui(d){const on=d.bot_status==='ONLINE';
  document.getElementById('dot').className='dot '+(on?'online':'offline');
  const st=document.getElementById('status-text');
  st.textContent=on?'ONLINE':'OFFLINE';
  st.className=on?'status-online':'status-offline';
  document.getElementById('bot-info').textContent=d.bot_name+' • ID '+(d.bot_id||'—');
  document.getElementById('guilds').textContent=d.guild_count;
  document.getElementById('cmds').textContent=d.slash_count+d.prefix_count;
  document.getElementById('cmd-sub').textContent=d.slash_count+' slash + '+d.prefix_count+' prefix';
  document.getElementById('voice').textContent=d.voice_workers;
  document.getElementById('tasks').textContent=d.active_tasks||0;
  document.getElementById('uptime').textContent=fmtUp(d.uptime);}
function setWs(s){const el=document.getElementById('wsStat');
  el.className='ws-status '+(s==='on'?'on':'off');
  el.textContent=s==='on'?'● WS: ONLINE':'● WS: RECONNECT...';}
function conn(){const p=location.protocol==='https:'?'wss':'ws';
  const sec=new URLSearchParams(location.search).get('secret')||'';
  ws=new WebSocket(p+'://'+location.host+'/ws?secret='+encodeURIComponent(sec));
  ws.onopen=()=>setWs('on');
  ws.onmessage=e=>{try{const m=JSON.parse(e.data);if(m.type==='status')ui(m.data);}catch(_){}};
  ws.onclose=()=>{setWs('off');clearTimeout(rt);rt=setTimeout(conn,5000);};
  ws.onerror=()=>setWs('off');}
conn();
setInterval(async()=>{if(ws&&ws.readyState===WebSocket.OPEN)return;
  try{const r=await fetch('/api/status');ui(await r.json());}catch(_){}},10000);
</script>
</body>
</html>
"""

def get_status_dict() -> dict:
    online = bot.is_ready() and bot.user is not None
    return {
        "panel_name": get_panel_name(),
        "bot_status": "ONLINE" if online else "OFFLINE",
        "bot_name": str(bot.user) if bot.user else "—",
        "bot_id": bot.user.id if bot.user else 0,
        "latency_ms": round(bot.latency * 1000, 1) if online else 0,
        "guild_count": len(bot.guilds),
        "slash_count": len(bot.tree.get_commands()),
        "prefix_count": len([c for c in bot.commands]),
        "voice_workers": len(active_voice_workers),
        "active_tasks": len(_active_stop_events),
        "uptime": time.time() - BOT_START_TIME,
    }

async def handle_index(request):
    html = HTML_PAGE.replace("{{PANEL_NAME}}", get_panel_name())
    return aioweb.Response(text=html, content_type="text/html")

async def handle_health(request):
    return aioweb.json_response({"ok": True, "status": "running"})

async def handle_status(request):
    return aioweb.json_response(get_status_dict())

async def handle_ws(request):
    ws = aioweb.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)
    secret = request.query.get("secret", "")
    if secret != WS_SECRET:
        await ws.send_json({"type": "error", "message": "Invalid secret"})
        await ws.close(); return ws
    connected_ws_clients.add(ws)
    log.info(f"[WS] +client (tổng: {len(connected_ws_clients)})")
    await ws.send_json({"type": "status", "data": get_status_dict()})
    try:
        async for msg in ws:
            if msg.type == aioweb.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    await handle_ws_command(ws, data)
                except json.JSONDecodeError:
                    await ws.send_json({"type": "error", "message": "JSON không hợp lệ"})
                except Exception as e:
                    await ws.send_json({"type": "error", "message": str(e)})
    finally:
        connected_ws_clients.discard(ws)
        log.info(f"[WS] -client (còn: {len(connected_ws_clients)})")
    return ws

async def handle_ws_command(ws, data: dict):
    action = data.get("action")
    if action == "status":
        await ws.send_json({"type": "status", "data": get_status_dict()}); return
    if action == "treo":
        tokens = parse_tokens(data.get("tokens", ""))
        if not tokens:
            await ws.send_json({"type": "error", "message": "Không có token"}); return
        try:
            gid = int(data.get("guild_id")); cid = int(data.get("channel_id"))
        except (TypeError, ValueError):
            await ws.send_json({"type": "error", "message": "ID không hợp lệ"}); return
        mute = bool(data.get("mute", False)); deaf = bool(data.get("deaf", True)); stream = bool(data.get("stream", False))
        async def _reply(m):
            try: await ws.send_json({"type": "info", "message": m})
            except Exception: pass
        asyncio.create_task(start_treo_room(tokens, gid, cid, mute, deaf, stream, _reply))
        await ws.send_json({"type": "ok", "message": f"Treo {len(tokens)} token..."}); return
    if action in ("stop_all", "dungtreo"):
        r = stop_all_activity()
        await ws.send_json({"type": "ok", "message": f"Đã dừng voice={r['voice']} task={r['tasks']}"}); return
    if action == "spam":
        tokens = parse_tokens(data.get("tokens", ""))
        if not tokens:
            await ws.send_json({"type": "error", "message": "Không có token"}); return
        try: cid = int(data.get("channel_id"))
        except (TypeError, ValueError):
            await ws.send_json({"type": "error", "message": "channel_id không hợp lệ"}); return
        content = str(data.get("content", ""))
        count = int(data.get("count", 1)); delay = float(data.get("delay", 3.0))
        if not content.strip():
            await ws.send_json({"type": "error", "message": "Nội dung rỗng"}); return
        msg_content = sanitize(content)
        stop_evt = register_stop()
        async def run_one(tok):
            sent = 0
            while not stop_evt.is_set():
                if count > 0 and sent >= count: return
                await send_token_message(tok, cid, msg_content)
                sent += 1
                await asyncio.sleep(max(0.5, delay + delay*random.uniform(-0.15, 0.15)))
        async def run_all():
            try: await asyncio.gather(*[asyncio.create_task(run_one(t)) for t in tokens])
            finally: unregister_stop(stop_evt)
        asyncio.create_task(run_all())
        await ws.send_json({"type": "ok", "message": f"Spam {cid} với {len(tokens)} token"}); return
    await ws.send_json({"type": "error", "message": f"Action không hỗ trợ: {action}"})

async def broadcast_status_loop():
    while True:
        await asyncio.sleep(5)
        if not connected_ws_clients: continue
        payload = {"type": "status", "data": get_status_dict()}
        dead = []
        for ws in list(connected_ws_clients):
            try: await ws.send_json(payload)
            except Exception: dead.append(ws)
        for ws in dead: connected_ws_clients.discard(ws)

async def start_web_server():
    app = aioweb.Application()
    app.router.add_get("/",            handle_index)
    app.router.add_get("/health",      handle_health)
    app.router.add_get("/api/status",  handle_status)
    app.router.add_get("/ws",          handle_ws)
    runner = aioweb.AppRunner(app); await runner.setup()
    site = aioweb.TCPSite(runner, "0.0.0.0", PORT); await site.start()
    log.info(f"🌐 Web Server: http://0.0.0.0:{PORT}")
    log.info(f"🔌 WebSocket : ws://0.0.0.0:{PORT}/ws?secret=***")
    asyncio.create_task(broadcast_status_loop())
    while True: await asyncio.sleep(3600)

# ══════════════════════════════════════════════════════════════
#  READY
# ══════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"{Fore.GREEN}[{OWNER_NAME.upper()}] ✅ Logged in as {bot.user} ({bot.user.id}){Style.RESET_ALL}")
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.CYAN}[{OWNER_NAME.upper()}] ✅ Synced {len(synced)} slash commands{Style.RESET_ALL}")
    except Exception as e: log.error(f"sync: {e}")
    try:
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=get_panel_name()),
            status=discord.Status.dnd)
    except Exception: pass
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 🎭 Panel: {get_panel_name()}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 👑 Owner gốc: {sorted(DEFAULT_OWNER_IDS)}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 👑 Owner thêm: {sorted(extra_owners) or '—'}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 👤 User thêm : {sorted(extra_users) or '—'}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 📁 File ngon  : {[f.name for f in find_ngon_files()] or '—'}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 🌐 Dashboard : http://0.0.0.0:{PORT}{Style.RESET_ALL}")
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")

# ══════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════
async def _run_all():
    await asyncio.gather(start_web_server(), bot.start(BOT_TOKEN))

if __name__ == "__main__":
    if not BOT_TOKEN:
        raise SystemExit("❌ Thiếu DISCORD_TOKEN trong .env")
    if not LOG_WEBHOOK_URL:
        print("⚠️ Chưa cấu hình LOG_WEBHOOK_URL.")

    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    clear_console()
    print_banner(get_panel_name(), OWNER_NAME)
    XA_DIR.mkdir(exist_ok=True)
    ensure_ngon_files()   # 👈 Tự tạo ngontreo_1→4 + ngonnhay_1→6

    try:
        asyncio.run(_run_all())
    except KeyboardInterrupt:
        log.info("Đã dừng bot.")
