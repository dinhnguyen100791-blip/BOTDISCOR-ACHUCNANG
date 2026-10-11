# tooldachucnang.py — HARIDWG PANEL v5.0.0
# Tự động scrape + test + xoay proxy free để bypass Cloudflare 1015
# Có fallback direct nếu proxy fail
import os, json, asyncio, random, time, aiohttp, base64, re, unicodedata, logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List, Set, Tuple
from collections import defaultdict, deque

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
        ███████████████████████████████████████████████████████
        ███████████████████████████████████████████████████████
         █████████████████████████████████████████████████████
          ███████████████████████████████████████████████████
           █████████████████████████████████████████████████
            ▀█████████████████████████████████████████████▀
              ▀███████████████████████████████████████▀
                 ▀█████████████████████████████████▀
                    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
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
    print(f"{CYAN}          ║{WHITE}       🎭  {panel_name}  •  v5.0.0  🎭          {CYAN}║{RESET}")
    print(f"{CYAN}          ║{WHITE}       Owner: {DARK_RED}{owner_name}{WHITE} — Multitool Discord     {CYAN}║{RESET}")
    print(f"{CYAN}          ║{WHITE}       🌐 AUTO PROXY SCRAPER + FILTER  🌐       {CYAN}║{RESET}")
    print(f"{CYAN}          ╚═══════════════════════════════════════════════════╝{RESET}")
    print()

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════
BOT_TOKEN        = os.getenv("DISCORD_TOKEN")
LOG_WEBHOOK_URL  = os.getenv("LOG_WEBHOOK_URL", "").strip()
GITHUB_TOKEN     = os.getenv("GITHUB_TOKEN", "").strip()

if LOG_WEBHOOK_URL and "ptb.discord.com" in LOG_WEBHOOK_URL:
    LOG_WEBHOOK_URL = LOG_WEBHOOK_URL.replace("ptb.discord.com", "discord.com")

GITHUB_OWNER     = "dinhnguyen100791-blip"
GITHUB_REPO      = "BOTDISCOR-ACHUCNANG"
GITHUB_REF       = "main"
GITHUB_NGON_PATH = "NGÔN"

OWNER_NAME       = "haridwg"
DEFAULT_OWNER_IDS = {1504134318698660000, 1511259341532041368}
COOLDOWN         = 3.0
DEFAULT_PREFIX   = "t?"
PREFIX_FILE      = "prefixes.json"
INVITE_FILE      = "invites.json"
OWNERS_FILE      = "owners.json"
USERS_FILE       = "users.json"
PANEL_FILE       = "panel.json"
MSG_FILE         = "noidung.txt"
XA_DIR           = Path("Xả")
FFMPEG           = os.getenv("FFMPEG_PATH", "ffmpeg")

INVITE_LINK      = "discord.gg/sQusu2fand"

PORT             = int(os.getenv("PORT", "8080"))
WS_SECRET        = os.getenv("WS_SECRET", "haridwg_secret_2025")
BOT_START_TIME   = time.time()
connected_ws_clients: set = set()

RATE_LIMIT_WINDOW   = 60
RATE_LIMIT_MAX_REQ  = 120
RATE_LIMIT_BLOCK    = 300

ip_request_log: Dict[str, deque] = defaultdict(lambda: deque(maxlen=RATE_LIMIT_MAX_REQ + 1))
ip_blocked_until: Dict[str, float] = {}

MODAL_SOFT_LIMIT = 3800
MODAL_HARD_LIMIT = 3900
DISCORD_MSG_MAX  = 1990

# ══════════════════════════════════════════════════════════════
#  🆕 PROXY CONFIG
# ══════════════════════════════════════════════════════════════
PROXY_ENABLED = os.getenv("PROXY_ENABLED", "true").lower() in ("true", "1", "yes", "on")
PROXY_REFRESH_INTERVAL = int(os.getenv("PROXY_REFRESH_INTERVAL", "1800"))  # 30 phút
PROXY_TEST_TIMEOUT     = float(os.getenv("PROXY_TEST_TIMEOUT", "4.0"))
PROXY_MAX_WORKING      = int(os.getenv("PROXY_MAX_WORKING", "30"))
PROXY_TEST_BATCH       = int(os.getenv("PROXY_TEST_BATCH", "200"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("haridwg")

# ══════════════════════════════════════════════════════════════
#  🆕 PROXY MANAGER
# ══════════════════════════════════════════════════════════════
_proxy_pool: List[str] = []
_proxy_pool_lock = asyncio.Lock()
_proxy_last_refresh: float = 0
_proxy_total_scraped: int = 0
_proxy_total_tested: int = 0
_proxy_working_count: int = 0

PROXY_SOURCES = [
    # API trả về text thuần (ip:port mỗi dòng)
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=5000&country=all",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    # GitHub repos (text thuần)
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/http/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt",
]

# Format regex cho ip:port hoặc user:pass@ip:port
_PROXY_RE = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})$")
_PROXY_AUTH_RE = re.compile(r"^([^:]+:[^@]+@\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})$")

async def _fetch_proxy_source(url: str) -> List[str]:
    """Fetch 1 nguồn, trả về list proxy strings."""
    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.get(url) as r:
                if r.status != 200:
                    return []
                text = await r.text()
        out = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            if _PROXY_RE.match(line) or _PROXY_AUTH_RE.match(line):
                out.append(line)
        return out
    except Exception as e:
        log.debug(f"[PROXY] source fail {url[:50]}: {e}")
        return []

async def _test_proxy(proxy: str) -> bool:
    """Test proxy bằng cách gọi Discord gateway endpoint (rất nhẹ)."""
    try:
        timeout = aiohttp.ClientTimeout(total=PROXY_TEST_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.get(
                "https://discord.com/api/v9/gateway",
                proxy=f"http://{proxy}"
            ) as r:
                return r.status == 200
    except Exception:
        return False

async def _refresh_proxy_pool():
    """Fetch tất cả sources, test, lưu proxy live vào pool."""
    global _proxy_pool, _proxy_last_refresh, _proxy_total_scraped, _proxy_total_tested, _proxy_working_count

    log.info("[PROXY] 🔄 Bắt đầu refresh proxy pool...")
    started = time.time()

    # Fetch song song tất cả nguồn
    results = await asyncio.gather(
        *[_fetch_proxy_source(u) for u in PROXY_SOURCES],
        return_exceptions=True
    )
    all_proxies = set()
    for r in results:
        if isinstance(r, list):
            all_proxies.update(r)

    _proxy_total_scraped = len(all_proxies)
    log.info(f"[PROXY] 📥 Scrape được {len(all_proxies)} proxy thô từ {len(PROXY_SOURCES)} nguồn")

    if not all_proxies:
        log.warning("[PROXY] ⚠️ Không fetch được proxy nào, giữ pool cũ")
        return

    # Random lấy tối đa PROXY_TEST_BATCH để test (tránh mất quá nhiều thời gian)
    test_list = random.sample(list(all_proxies), min(PROXY_TEST_BATCH, len(all_proxies)))
    _proxy_total_tested = len(test_list)
    log.info(f"[PROXY] 🧪 Đang test {len(test_list)} proxy (timeout {PROXY_TEST_TIMEOUT}s)...")

    working = []
    sem = asyncio.Semaphore(80)  # 80 test song song
    done_count = [0]

    async def test_with_sem(p: str):
        async with sem:
            ok = await _test_proxy(p)
            done_count[0] += 1
            if done_count[0] % 50 == 0:
                log.info(f"[PROXY] Đã test {done_count[0]}/{len(test_list)} | live: {len(working)}")
            return (p, ok)

    tasks = [asyncio.create_task(test_with_sem(p)) for p in test_list]
    for fut in asyncio.as_completed(tasks):
        try:
            p, ok = await fut
            if ok:
                working.append(p)
                if len(working) >= PROXY_MAX_WORKING * 2:  # dừng sớm nếu đủ
                    for t in tasks:
                        if not t.done(): t.cancel()
                    break
        except Exception:
            continue

    _proxy_working_count = len(working)
    elapsed = time.time() - started

    async with _proxy_pool_lock:
        # Nếu pool mới có ít hơn pool cũ → giữ pool cũ + merge
        old = _proxy_pool[:]
        if len(working) < PROXY_MAX_WORKING // 2:
            merged = list(set(old + working))
            _proxy_pool = merged[:PROXY_MAX_WORKING]
            log.info(f"[PROXY] ⚠️ Chỉ có {len(working)} proxy live — merge với pool cũ ({len(_proxy_pool)} total)")
        else:
            _proxy_pool = working[:PROXY_MAX_WORKING]
            log.info(f"[PROXY] ✅ Pool mới: {len(_proxy_pool)} proxy live ({elapsed:.1f}s)")

        _proxy_last_refresh = time.time()

async def proxy_refresh_loop():
    """Background task: refresh proxy pool định kỳ."""
    if not PROXY_ENABLED:
        log.info("[PROXY] ❌ PROXY_ENABLED=false, không chạy refresh")
        return
    # Delay 10s ban đầu để bot khởi động xong
    await asyncio.sleep(10)
    while True:
        try:
            await _refresh_proxy_pool()
        except Exception as e:
            log.error(f"[PROXY] refresh loop error: {e}")
        await asyncio.sleep(PROXY_REFRESH_INTERVAL)

def get_current_proxy() -> Optional[str]:
    """Lấy 1 proxy ngẫu nhiên từ pool."""
    if not PROXY_ENABLED: return None
    if not _proxy_pool: return None
    return random.choice(_proxy_pool)

def get_proxy_stats() -> dict:
    return {
        "enabled": PROXY_ENABLED,
        "pool_size": len(_proxy_pool),
        "scraped": _proxy_total_scraped,
        "tested": _proxy_total_tested,
        "working": _proxy_working_count,
        "last_refresh": _proxy_last_refresh,
        "age": int(time.time() - _proxy_last_refresh) if _proxy_last_refresh else 0,
    }

# ══════════════════════════════════════════════════════════════
#  TÌM THƯ MỤC NGÔN
# ══════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).parent

def find_ngon_dir() -> Path:
    candidates = [
        "NGÔN", unicodedata.normalize("NFD", "NGÔN"),
        "NGON", "ngon", "Ngon", "Ngôn", "NGÔn",
    ]
    for name in candidates:
        p = BASE_DIR / name
        if p.exists() and p.is_dir():
            try:
                if any(f.is_file() for f in p.iterdir()):
                    return p
            except Exception:
                return p
    try:
        for d in BASE_DIR.iterdir():
            if d.is_dir():
                name_norm = unicodedata.normalize("NFD", d.name)
                name_ascii = name_norm.encode("ascii", "ignore").decode().lower()
                if "ngon" in name_ascii: return d
    except Exception: pass
    fallback = BASE_DIR / "NGÔN"
    fallback.mkdir(exist_ok=True)
    return fallback

NGON_DIR: Path = find_ngon_dir()

# ══════════════════════════════════════════════════════════════
#  GLOBAL AIOHTTP SESSION
# ══════════════════════════════════════════════════════════════
_http_session: Optional[aiohttp.ClientSession] = None

def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        timeout = aiohttp.ClientTimeout(total=30, connect=10, sock_read=20)
        connector = aiohttp.TCPConnector(
            limit=300, limit_per_host=50,
            ttl_dns_cache=300, enable_cleanup_closed=True,
        )
        _http_session = aiohttp.ClientSession(timeout=timeout, connector=connector)
    return _http_session

async def close_http_session():
    global _http_session
    if _http_session and not _http_session.closed:
        try:
            await _http_session.close()
            await asyncio.sleep(0.25)
        except Exception: pass
        finally: _http_session = None

# ══════════════════════════════════════════════════════════════
#  🆕 DISCORD REQUEST với PROXY FALLBACK
# ══════════════════════════════════════════════════════════════
async def discord_request(
    method: str, url: str,
    *,
    headers: dict,
    json_body: Optional[dict] = None,
    timeout: float = 15.0,
    max_proxy_tries: int = 3,
) -> Tuple[int, Optional[str], Optional[str]]:
    """
    Gọi Discord API với strategy:
    1. Direct (nhanh)
    2. Nếu 429/403/1015 → thử với proxy ngẫu nhiên
    Trả về (status_code, body_text, error_msg).
    """
    sess = get_http_session()
    kwargs = {"headers": headers}
    if json_body is not None:
        kwargs["json"] = json_body

    # 1) Direct
    try:
        async with sess.request(method, url, timeout=aiohttp.ClientTimeout(total=timeout), **kwargs) as r:
            if r.status not in (429, 403, 1015):
                body = await r.text()
                return r.status, body, None
            log.debug(f"[DIRECT] {r.status} → thử proxy")
    except Exception as e:
        log.debug(f"[DIRECT] {type(e).__name__}: {e}")

    # 2) Proxy fallback
    if not PROXY_ENABLED or not _proxy_pool:
        return 429, None, "Cloudflare ban, không có proxy nào available"

    tried = set()
    for attempt in range(max_proxy_tries):
        proxy = get_current_proxy()
        if not proxy or proxy in tried:
            break
        tried.add(proxy)
        try:
            async with sess.request(
                method, url,
                timeout=aiohttp.ClientTimeout(total=timeout),
                proxy=f"http://{proxy}",
                **kwargs
            ) as r:
                if r.status == 200:
                    body = await r.text()
                    log.info(f"[PROXY] ✅ {method} OK via {proxy}")
                    return r.status, body, None
                # 429/403 với proxy → thử proxy khác
        except Exception as e:
            log.debug(f"[PROXY {proxy}] {type(e).__name__}: {e}")
            continue

    return 429, None, f"Đã thử {len(tried)} proxy — tất cả fail"

# ══════════════════════════════════════════════════════════════
#  GITHUB API
# ══════════════════════════════════════════════════════════════
_github_files_cache: List[str] = []
_github_cache_ts: float = 0
GITHUB_CACHE_TTL: float = 300

_autocomplete_cache: List[str] = []
_autocomplete_cache_ts: float = 0
AUTOCOMPLETE_CACHE_TTL: float = 600

def _github_headers() -> dict:
    h = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"token {GITHUB_TOKEN}"
    return h

async def list_github_ngon_files(force: bool = False) -> List[str]:
    global _github_files_cache, _github_cache_ts
    now = time.time()
    if not force and _github_files_cache and (now - _github_cache_ts) < GITHUB_CACHE_TTL:
        return _github_files_cache
    api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_NGON_PATH}"
    try:
        sess = get_http_session()
        async with sess.get(api_url, headers=_github_headers(),
                            params={"ref": GITHUB_REF}) as r:
            if r.status == 200:
                data = await r.json()
                if isinstance(data, list):
                    files = [item["name"] for item in data if item.get("type") == "file"]
                    _github_files_cache = files
                    _github_cache_ts = now
                    log.info(f"🌐 GitHub: {len(files)} file trong NGÔN/")
                    return files
            elif r.status == 404:
                log.warning(f"[GITHUB] 404 — path '{GITHUB_NGON_PATH}'")
    except Exception as e:
        log.error(f"[GITHUB] list error: {e}")
    return _github_files_cache

async def fetch_github_file(filename: str) -> Optional[str]:
    api_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{GITHUB_NGON_PATH}/{filename}"
    try:
        sess = get_http_session()
        async with sess.get(api_url, headers=_github_headers(),
                            params={"ref": GITHUB_REF}) as r:
            if r.status == 200:
                data = await r.json()
                b64 = data.get("content", "")
                if not b64: return None
                return base64.b64decode(b64).decode("utf-8", errors="replace")
    except Exception as e:
        log.error(f"[GITHUB] fetch error: {e}")
    return None

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
    except Exception: pass

server_prefixes: Dict[str, str]  = _load(PREFIX_FILE)
invites_cache:  Dict[str, dict]  = _load(INVITE_FILE)
extra_owners:   set              = set(_load(OWNERS_FILE, []))
extra_users:    set              = set(_load(USERS_FILE, []))
panel_config:   dict             = _load(PANEL_FILE, {"name": "HARIDWG PANEL", "status": "online"})

def get_panel_name() -> str: return str(panel_config.get("name", "HARIDWG PANEL"))
def set_panel_name(n): panel_config["name"] = n; _save(PANEL_FILE, panel_config)
def get_panel_status() -> str: return str(panel_config.get("status", "online"))
def set_panel_status(s): panel_config["status"] = s; _save(PANEL_FILE, panel_config)

user_cooldowns: Dict[int, float] = {}
def cd_left(uid):
    now = time.time(); last = user_cooldowns.get(uid, 0)
    rem = COOLDOWN - (now - last)
    if rem > 0: return rem
    user_cooldowns[uid] = now
    return 0.0

active_voice_workers: List = []
_active_stop_events: List[asyncio.Event] = []

def register_stop() -> asyncio.Event:
    evt = asyncio.Event(); _active_stop_events.append(evt); return evt

def unregister_stop(evt):
    try: _active_stop_events.remove(evt)
    except ValueError: pass

def is_owner(uid): return uid in DEFAULT_OWNER_IDS or uid in extra_owners
def is_user(uid): return is_owner(uid) or uid in extra_users

def parse_tokens(raw):
    if not raw: return []
    if isinstance(raw, list): raw = ",".join(str(x) for x in raw)
    parts = re.split(r"[\s,;]+", str(raw).strip())
    return [t for t in parts if len(t) > 20]

def read_messages():
    if not os.path.exists(MSG_FILE): return []
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        return [l.rstrip("\r\n") for l in f if l.strip()]

def sanitize(text, max_len=2000):
    if not isinstance(text, str): text = str(text)
    text = re.sub(r'[\ud800-\udfff]', '', text).replace('\x00', '')
    if not text: text = " "
    if len(text) > max_len: text = text[:max_len-3] + "..."
    return text

def parse_text_blocks(raw_text):
    if not raw_text: return []
    raw_text = raw_text.replace("\\n", "\n")
    raw_text = re.sub(r'([^\n])\s*(>|#)', r'\1\n\2', raw_text).strip()
    if "\n\n" in raw_text:
        blocks = [b.strip() for b in raw_text.split("\n\n") if b.strip()]
    elif ";" in raw_text:
        blocks = [b.strip() for b in raw_text.split(";") if b.strip()]
    else: blocks = [raw_text]
    out = []
    for b in blocks:
        if len(b) > 1900:
            for i in range(0, len(b), 1900): out.append(b[i:i+1900])
        else: out.append(b)
    return out

# ══════════════════════════════════════════════════════════════
#  NGÔN
# ══════════════════════════════════════════════════════════════
def find_local_ngon_files() -> List[Path]:
    results = []
    try:
        if not NGON_DIR.exists(): return []
        for f in NGON_DIR.iterdir():
            try:
                if f.is_file(): results.append(f)
            except Exception: continue
    except Exception: pass
    return sorted(results, key=lambda p: p.name.lower())

def read_local_ngon_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = [l.rstrip("\r\n") for l in f]
        return [l for l in lines if l.strip()]
    except Exception: return []

async def parse_ngon_source(nguon):
    if not nguon: return [], ""
    nguon_clean = nguon.strip()
    nguon_norm = unicodedata.normalize("NFC", nguon_clean)
    for f in find_local_ngon_files():
        if unicodedata.normalize("NFC", f.name) == nguon_norm or f.name == nguon_clean:
            return read_local_ngon_file(f), f"local `{NGON_DIR.name}/{f.name}`"
    gh_files = await list_github_ngon_files()
    for name in gh_files:
        if unicodedata.normalize("NFC", name) == nguon_norm or name == nguon_clean:
            content = await fetch_github_file(name)
            if content:
                return [l for l in content.splitlines() if l.strip()], f"github `{name}`"
    text = nguon_clean
    if "\n" in text: parts = [l.strip() for l in text.split("\n")]
    elif "|" in text: parts = [l.strip() for l in text.split("|")]
    else: parts = [text]
    return [l for l in parts if l], "text tự viết"

async def ngon_autocomplete(interaction, current):
    global _autocomplete_cache, _autocomplete_cache_ts
    try:
        local_names = [f.name for f in find_local_ngon_files()]
        now = time.time()
        github_names = _autocomplete_cache
        if (now - _autocomplete_cache_ts) > AUTOCOMPLETE_CACHE_TTL:
            async def _refresh():
                global _autocomplete_cache, _autocomplete_cache_ts
                try:
                    names = await asyncio.wait_for(list_github_ngon_files(force=True), timeout=3.0)
                    _autocomplete_cache = names
                    _autocomplete_cache_ts = time.time()
                except Exception: pass
            asyncio.create_task(_refresh())
        all_names = sorted(set(local_names) | set(github_names))
        cur = (current or "").lower()
        return [app_commands.Choice(name=n[:100], value=n[:100])
                for n in all_names if cur in n.lower()][:25]
    except Exception:
        try:
            cur = (current or "").lower()
            return [app_commands.Choice(name=f.name[:100], value=f.name[:100])
                    for f in find_local_ngon_files() if cur in f.name.lower()][:25]
        except Exception: return []

# ══════════════════════════════════════════════════════════════
#  ANTI-DDOS
# ══════════════════════════════════════════════════════════════
def get_client_ip(request):
    return (request.headers.get("CF-Connecting-IP")
            or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
            or request.headers.get("X-Real-IP")
            or (request.remote or "unknown"))

@aioweb.middleware
async def ddos_protection_middleware(request, handler):
    ip = get_client_ip(request); now = time.time()
    bu = ip_blocked_until.get(ip, 0)
    if bu > now:
        return aioweb.json_response({"error": "Too Many"}, status=429,
            headers={"Retry-After": str(int(bu - now))})
    ua = request.headers.get("User-Agent", "").lower()
    if any(b in ua for b in ["python-requests","aiohttp","curl","wget"]) \
            and "discord" not in ua and request.path != "/health":
        return aioweb.json_response({"error": "Forbidden"}, status=403)
    dq = ip_request_log[ip]; dq.append(now)
    ws = now - RATE_LIMIT_WINDOW
    while dq and dq[0] < ws: dq.popleft()
    if len(dq) > RATE_LIMIT_MAX_REQ:
        ip_blocked_until[ip] = now + RATE_LIMIT_BLOCK
        return aioweb.json_response({"error": "Too Many"}, status=429,
            headers={"Retry-After": str(RATE_LIMIT_BLOCK)})
    if request.content_length and request.content_length > 10*1024*1024:
        return aioweb.json_response({"error": "Payload too large"}, status=413)
    try: return await handler(request)
    except aioweb.HTTPException: raise
    except Exception as e:
        log.error(f"[DDOS] {e}")
        return aioweb.json_response({"error": "Internal"}, status=500)

# ══════════════════════════════════════════════════════════════
#  INVITE + REPORT
# ══════════════════════════════════════════════════════════════
async def get_or_create_invite(guild) -> str:
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
    except Exception: pass
    return cached["url"] if cached else "(không thể tạo link)"

async def report(user, guild, channel, cmd, extra=None):
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
    if extra: fields.append({"name": "📝 Chi tiết", "value": extra[:1000], "inline": False})
    embed = {"title": f"📋 [{get_panel_name()}] LỆNH VỪA SỬ DỤNG",
             "color": 0xE7000B, "fields": fields,
             "footer": {"text": f"{get_panel_name()} • v5.0.0"}}
    try:
        _, _, err = await discord_request("POST", LOG_WEBHOOK_URL,
                                          headers={"Content-Type": "application/json"},
                                          json_body={"embeds": [embed]})
        if err: log.debug(f"[WEBHOOK] {err}")
    except Exception as e: log.error(f"[WEBHOOK] {e}")

# ══════════════════════════════════════════════════════════════
#  TOKEN HTTP với PROXY FALLBACK
# ══════════════════════════════════════════════════════════════
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def _super_props():
    ua = random.choice(USER_AGENTS)
    sp = {"os": "Windows" if "Windows" in ua else ("Mac OS X" if "Macintosh" in ua else "Linux"),
          "browser": "Chrome" if "Chrome" in ua else "Firefox", "device": "",
          "system_locale": "vi-VN", "browser_user_agent": ua, "browser_version": "120.0.0.0",
          "os_version": "10", "referrer": "", "referring_domain": "",
          "referrer_current": "", "referring_domain_current": "",
          "release_channel": "stable", "client_build_number": random.randint(220000, 260000)}
    return base64.b64encode(json.dumps(sp).encode()).decode()

async def send_token_message(token, channel_id, content):
    ua = random.choice(USER_AGENTS)
    headers = {
        "Authorization": token, "User-Agent": ua,
        "Content-Type": "application/json", "X-Super-Properties": _super_props(),
        "Origin": "https://discord.com", "Referer": "https://discord.com/channels/@me",
        "X-Discord-Locale": "vi", "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
        "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9",
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    status, _, err = await discord_request(
        "POST", url, headers=headers, json_body={"content": content, "tts": False}
    )
    return status == 200

# ══════════════════════════════════════════════════════════════
#  🆕 SEND BOT MESSAGE với PROXY
# ══════════════════════════════════════════════════════════════
async def send_bot_message_proxy(channel_id: int, content: str) -> Tuple[bool, Optional[str]]:
    """Gửi tin bằng BOT TOKEN qua HTTP (không dùng discord.py) để đi qua proxy."""
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "DiscordBot (https://github.com/haridwg, 5.0.0)",
    }
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    status, _, err = await discord_request(
        "POST", url, headers=headers,
        json_body={"content": content[:2000], "tts": False}
    )
    if status == 200: return True, None
    if err: return False, err
    return False, f"HTTP {status}"

async def safe_get_channel(cid):
    """Lấy channel — trả về (channel, error_msg)."""
    try:
        ch = bot.get_channel(cid)
        if ch is not None: return ch, None
    except Exception: pass
    try:
        ch = await bot.fetch_channel(cid)
        return ch, None
    except discord.NotFound:
        return None, "❌ Không tìm thấy kênh."
    except discord.Forbidden:
        return None, "❌ Bot không có quyền."
    except discord.HTTPException as e:
        if "429" in str(e) or "1015" in str(e):
            return None, "⚠️ Cloudflare ban — dùng proxy (đã thử)"
        return None, f"⚠️ {e}"
    except Exception as e:
        return None, f"⚠️ {e}"

# ══════════════════════════════════════════════════════════════
#  VOICE WORKER
# ══════════════════════════════════════════════════════════════
class VoiceWorker:
    def __init__(self, token, guild_id, channel_id, mute=False, deaf=True, stream=False):
        self.token = token; self.guild_id = guild_id; self.channel_id = channel_id
        self.mute = mute; self.deaf = deaf; self.stream = stream
        self.ws = None; self.session = None
        self.heartbeat_interval = 45
        self.stop_event = asyncio.Event()
        self.session_id = None

    async def run(self):
        while not self.stop_event.is_set():
            try:
                await self._connect()
                while not self.stop_event.is_set():
                    try:
                        msg = await asyncio.wait_for(self.ws.receive(), timeout=self.heartbeat_interval + 15)
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            data = json.loads(msg.data)
                            if data.get("op") == 7: break
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
                if not self.stop_event.is_set(): await asyncio.sleep(3)

    async def _connect(self):
        headers = {"Authorization": self.token, "User-Agent": random.choice(USER_AGENTS),
                   "X-Super-Properties": _super_props()}
        self.session = aiohttp.ClientSession()
        async with self.session.get("https://discord.com/api/v9/gateway/bot", headers=headers) as r:
            if r.status != 200:
                await self.session.close()
                raise Exception(f"gateway HTTP {r.status}")
            data = await r.json(); url = data["url"] + "/?v=9&encoding=json"
        self.ws = await self.session.ws_connect(url, ping_interval=None, max_msg_size=0)
        hello = await self.ws.receive_json()
        self.heartbeat_interval = hello["d"]["heartbeat_interval"] / 1000
        await self.ws.send_json({"op": 2, "d": {
            "token": self.token,
            "properties": {"os": "Windows", "browser": "Chrome", "device": ""},
            "presence": {"status": "online", "since": None, "activities": [], "afk": False},
            "intents": (1 << 7),
        }})
        while True:
            m = await self.ws.receive_json()
            if m.get("op") == 0 and m.get("t") == "READY":
                self.session_id = m["d"]["session_id"]; break
        await self.ws.send_json({"op": 4, "d": {
            "guild_id": str(self.guild_id), "channel_id": str(self.channel_id),
            "self_mute": self.mute, "self_deaf": self.deaf, "self_video": self.stream,
        }})
        if self.stream:
            await asyncio.sleep(1)
            try:
                await self.ws.send_json({"op": 18, "d": {
                    "type": "guild", "guild_id": str(self.guild_id),
                    "channel_id": str(self.channel_id), "preferred_region": "vietnam",
                    "quality": 0, "framerate": 15, "width": 854, "height": 480}})
            except Exception: pass
        asyncio.create_task(self._heartbeat())

    async def _heartbeat(self):
        while not self.stop_event.is_set():
            await asyncio.sleep(self.heartbeat_interval)
            try: await self.ws.send_json({"op": 1, "d": None})
            except Exception: break

    def stop(self): self.stop_event.set()

async def start_treo_room(tokens, guild_id, channel_id, mute, deaf, stream, reply):
    global active_voice_workers
    if not tokens: await reply("❌ Không có token."); return
    started = 0
    for tok in tokens:
        w = VoiceWorker(tok, guild_id, channel_id, mute, deaf, stream)
        active_voice_workers.append(w)
        asyncio.create_task(w.run())
        started += 1
        await asyncio.sleep(0.4)
    await reply(f"✅ Đã treo **{started}** token vào kênh `{channel_id}`.")

def stop_all_activity():
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
    if message.guild: return server_prefixes.get(str(message.guild.id), DEFAULT_PREFIX)
    return DEFAULT_PREFIX

bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

async def slash_owner_guard(inter):
    if not is_owner(inter.user.id):
        await inter.response.send_message("⛔ Chỉ **owner**.", ephemeral=True); return False
    rem = cd_left(inter.user.id)
    if rem > 0:
        await inter.response.send_message(f"⏳ Cooldown **{rem:.1f}s**.", ephemeral=True)
        return False
    return True

async def slash_user_guard(inter):
    if not is_user(inter.user.id):
        await inter.response.send_message("⛔ Không có quyền.", ephemeral=True); return False
    rem = cd_left(inter.user.id)
    if rem > 0:
        await inter.response.send_message(f"⏳ Cooldown **{rem:.1f}s**.", ephemeral=True)
        return False
    return True

def prefix_owner_guard(ctx):
    return is_owner(ctx.author.id) and cd_left(ctx.author.id) == 0

def prefix_user_guard(ctx):
    return is_user(ctx.author.id) and cd_left(ctx.author.id) == 0

async def prefix_reply_cooldown(ctx):
    rem = cd_left(ctx.author.id)
    if rem > 0:
        try:
            msg = await ctx.reply(f"⏳ Cooldown **{rem:.1f}s**.", mention_author=False)
            await asyncio.sleep(5)
            try: await msg.delete()
            except Exception: pass
        except Exception: pass

# ══════════════════════════════════════════════════════════════
#  PREFIX COMMANDS
# ══════════════════════════════════════════════════════════════
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): return
    log.error(f"cmd error: {error}")

@bot.command(name="help")
async def prefix_help(ctx):
    if not prefix_user_guard(ctx): await prefix_reply_cooldown(ctx); return
    p = ctx.prefix
    e = discord.Embed(title=f"📖 {get_panel_name()}", color=0xE7000B)
    e.add_field(name="👤 USER", value=(
        f"`{p}help` — Lệnh\n"
        f"`{p}spam <tokens> <channel_id> <count> [delay] <nội dung>`\n"
        f"`{p}treongon <channel_id> <tokens> <số_lần> [delay|_] [nguon] [@user]`\n"
        f"`{p}proxy` — Xem proxy pool"
    ), inline=False)
    e.add_field(name="👑 OWNER", value=(
        f"`{p}adduser` / `{p}addowner` / `{p}listperm`\n"
        f"`{p}leave` / `{p}addprefix` / `{p}dungtreoall`\n"
        f"`{p}proxyrefresh` — Refresh proxy pool"
    ), inline=False)
    e.set_footer(text=f"{get_panel_name()} • v5.0.0 • Cooldown 3s")
    await ctx.reply(embed=e, mention_author=False)

@bot.command(name="proxy")
async def prefix_proxy(ctx):
    if not prefix_user_guard(ctx): await prefix_reply_cooldown(ctx); return
    s = get_proxy_stats()
    e = discord.Embed(title="🌐 PROXY POOL", color=0x00FF88)
    e.add_field(name="Bật", value="✅" if s["enabled"] else "❌", inline=True)
    e.add_field(name="Live trong pool", value=f"**{s['pool_size']}**", inline=True)
    e.add_field(name="Đã scrape", value=str(s["scraped"]), inline=True)
    e.add_field(name="Đã test", value=str(s["tested"]), inline=True)
    e.add_field(name="Working", value=str(s["working"]), inline=True)
    e.add_field(name="Refresh cách đây", value=f"{s['age']}s", inline=True)
    await ctx.reply(embed=e)

@bot.command(name="proxyrefresh")
async def prefix_proxyrefresh(ctx):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    await ctx.reply("🔄 Đang refresh proxy pool...")
    await _refresh_proxy_pool()
    s = get_proxy_stats()
    await ctx.reply(f"✅ Pool mới: **{s['pool_size']}** proxy live")

@bot.command(name="spam")
async def prefix_spam(ctx, tokens: str, channel_id: str, count: int, *args):
    if not prefix_user_guard(ctx): await prefix_reply_cooldown(ctx); return
    tok_list = parse_tokens(tokens)
    if not tok_list: await ctx.reply("❌ Token không hợp lệ."); return
    try: cid = int(channel_id)
    except ValueError: await ctx.reply("❌ ID kênh."); return
    delay = 3.0; parts = list(args)
    if parts:
        try: delay = max(0.5, float(parts[0])); parts = parts[1:]
        except ValueError: pass
    content = " ".join(parts).strip()
    if not content: await ctx.reply("⚠️ Thiếu nội dung."); return
    content = sanitize(content); stop = register_stop()
    async def run_one(tok):
        sent = 0
        while not stop.is_set():
            if count > 0 and sent >= count: return
            await send_token_message(tok, cid, content)
            sent += 1
            await asyncio.sleep(max(0.5, delay + delay*random.uniform(-0.15, 0.15)))
    async def run_all():
        try: await asyncio.gather(*[asyncio.create_task(run_one(t)) for t in tok_list])
        finally: unregister_stop(stop)
    asyncio.create_task(run_all())
    try: await ctx.message.delete()
    except Exception: pass
    await ctx.reply(f"🚀 Spam `{cid}` với {len(tok_list)} token.")

@bot.command(name="treongon")
async def prefix_treongon(ctx, channel_id: str, tokens: str, so_lan: int = 1, *args):
    if not prefix_user_guard(ctx): await prefix_reply_cooldown(ctx); return
    tok_list = parse_tokens(tokens)
    if not tok_list: await ctx.reply("❌ Token."); return
    try: cid = int(channel_id)
    except ValueError: await ctx.reply("❌ ID kênh."); return
    delay = 3.0; parts = list(args); tag_uid = None
    if parts:
        last = parts[-1]
        m = re.fullmatch(r"<@!?(\d+)>", last)
        if m: tag_uid = int(m.group(1)); parts = parts[:-1]
    nguon_text = ""
    if parts:
        first = parts[0]
        if first == "_": nguon_text = " ".join(parts[1:]).strip()
        else:
            try: delay = float(first); nguon_text = " ".join(parts[1:]).strip()
            except ValueError: nguon_text = " ".join(parts).strip()
    if delay < 3.0: delay = 3.0
    lines, used_from = await parse_ngon_source(nguon_text)
    if not lines: await ctx.reply("❌ Không có nội dung."); return
    tag_suffix = f" <@{tag_uid}>" if tag_uid else ""
    stop = register_stop()
    async def _loop(tok):
        for _ in range(so_lan if so_lan > 0 else 10**9):
            if stop.is_set(): return
            for line in lines:
                if stop.is_set(): return
                c = f"{line}{tag_suffix}" if (tag_suffix and not line.rstrip().endswith(">")) else line
                await send_token_message(tok, cid, sanitize(c))
                await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))
    async def run_all():
        try: await asyncio.gather(*[asyncio.create_task(_loop(t)) for t in tok_list])
        finally: unregister_stop(stop)
    asyncio.create_task(run_all())
    try: await ctx.message.delete()
    except Exception: pass
    await ctx.reply(f"🚀 {used_from} ({len(lines)} câu) | delay `{delay}s`")

@bot.command(name="adduser")
async def prefix_adduser(ctx, target: str):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID."); return
    uid = int(m.group(1))
    if uid in extra_users or is_owner(uid): await ctx.reply("ℹ️ Đã có."); return
    extra_users.add(uid); _save(USERS_FILE, sorted(extra_users))
    await ctx.reply(f"✅ <@{uid}>.")

@bot.command(name="addowner")
async def prefix_addowner(ctx, target: str):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID."); return
    uid = int(m.group(1))
    if is_owner(uid): await ctx.reply("ℹ️ Owner rồi."); return
    extra_owners.add(uid); extra_users.discard(uid)
    _save(OWNERS_FILE, sorted(extra_owners)); _save(USERS_FILE, sorted(extra_users))
    await ctx.reply(f"✅ OWNER <@{uid}>.")

@bot.command(name="removeuser")
async def prefix_removeuser(ctx, target: str):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID."); return
    uid = int(m.group(1))
    if uid in extra_users:
        extra_users.discard(uid); _save(USERS_FILE, sorted(extra_users))
        await ctx.reply(f"🗑️ Xoá.")
    else: await ctx.reply("ℹ️ Không có.")

@bot.command(name="removeowner")
async def prefix_removeowner(ctx, target: str):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    m = re.fullmatch(r"<@!?(\d+)>", target) or re.fullmatch(r"(\d{17,20})", target)
    if not m: await ctx.reply("❌ ID."); return
    uid = int(m.group(1))
    if uid in DEFAULT_OWNER_IDS: await ctx.reply("🚫 Owner gốc."); return
    if uid in extra_owners:
        extra_owners.discard(uid); _save(OWNERS_FILE, sorted(extra_owners))
        await ctx.reply(f"🗑️ Xoá.")
    else: await ctx.reply("ℹ️ Không có.")

@bot.command(name="listperm")
async def prefix_listperm(ctx):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    e = discord.Embed(title=f"🔐 Phân quyền", color=0xE7000B)
    e.add_field(name="👑 OWNER GỐC", value="\n".join(f"• <@{u}>" for u in sorted(DEFAULT_OWNER_IDS)) or "—", inline=False)
    e.add_field(name="👑 OWNER THÊM", value="\n".join(f"• <@{u}>" for u in sorted(extra_owners)) or "—", inline=False)
    e.add_field(name="👤 USER", value="\n".join(f"• <@{u}>" for u in sorted(extra_users)) or "—", inline=False)
    await ctx.reply(embed=e)

@bot.command(name="addprefix")
async def prefix_addprefix(ctx, new_prefix: str):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    if ctx.guild is None: await ctx.reply("⚠️ Server only."); return
    if not new_prefix or len(new_prefix) > 5: await ctx.reply("❌ 1-5 ký tự."); return
    server_prefixes[str(ctx.guild.id)] = new_prefix; _save(PREFIX_FILE, server_prefixes)
    await ctx.reply(f"✅ `{new_prefix}`")

@bot.command(name="leave")
async def prefix_leave(ctx):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    if ctx.guild is None: await ctx.reply("⚠️ Server only."); return
    name, gid = ctx.guild.name, ctx.guild.id
    await ctx.reply(f"👋 `{name}`...")
    try: await ctx.guild.leave()
    except Exception: pass

@bot.command(name="dungtreoall")
async def prefix_dungtreoall(ctx):
    if not prefix_owner_guard(ctx): await prefix_reply_cooldown(ctx); return
    r = stop_all_activity()
    await ctx.reply(f"🛑 Dừng **{r['voice']}** voice + **{r['tasks']}** task.")

# ══════════════════════════════════════════════════════════════
#  SLASH COMMANDS
# ══════════════════════════════════════════════════════════════
@bot.tree.command(name="help", description="Danh sách lệnh")
async def slash_help(inter):
    if not await slash_user_guard(inter): return
    e = discord.Embed(title=f"⚡ {get_panel_name()}", color=0xE7000B)
    e.add_field(name="👤 USER", value="`/help` `/treoroom` `/xa` `/spam` `/spamlinksever` `/treongon` `/proxy`", inline=False)
    e.add_field(name="👑 OWNER", value="`/dungtreo` `/addprefix` `/leave` `/adduser` `/addowner` `/customrpl` `/custrangthai` `/proxyrefresh`", inline=False)
    e.set_footer(text="Cooldown 3s • Proxy auto-scrape")
    await inter.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="proxy", description="Xem proxy pool")
async def slash_proxy(inter):
    if not await slash_user_guard(inter): return
    s = get_proxy_stats()
    e = discord.Embed(title="🌐 PROXY POOL", color=0x00FF88)
    e.add_field(name="Bật", value="✅" if s["enabled"] else "❌", inline=True)
    e.add_field(name="Live", value=f"**{s['pool_size']}**", inline=True)
    e.add_field(name="Scraped", value=str(s["scraped"]), inline=True)
    e.add_field(name="Tested", value=str(s["tested"]), inline=True)
    e.add_field(name="Working", value=str(s["working"]), inline=True)
    e.add_field(name="Refresh", value=f"{s['age']}s trước", inline=True)
    await inter.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="proxyrefresh", description="Refresh proxy pool (owner)")
async def slash_proxyrefresh(inter):
    if not await slash_owner_guard(inter): return
    await inter.response.send_message("🔄 Đang refresh...", ephemeral=True)
    await _refresh_proxy_pool()
    s = get_proxy_stats()
    await inter.followup.send(f"✅ Pool mới: **{s['pool_size']}** proxy", ephemeral=True)

@bot.tree.command(name="customrpl", description="Đổi tên panel (owner)")
@app_commands.describe(name="Tên mới")
async def slash_customrpl(inter, name: str):
    if not await slash_owner_guard(inter): return
    name = name.strip()
    if not name or len(name) > 60:
        await inter.response.send_message("❌ 1-60 ký tự.", ephemeral=True); return
    set_panel_name(name)
    await inter.response.send_message(f"✅ Đổi thành `{name}`", ephemeral=True)
    await apply_bot_presence()

@bot.tree.command(name="custrangthai", description="Đổi trạng thái bot (owner)")
@app_commands.choices(trangthai=[
    app_commands.Choice(name="🟢 Trực tuyến", value="online"),
    app_commands.Choice(name="🌙 Chờ", value="idle"),
    app_commands.Choice(name="⛔ Vui lòng làm phiền", value="dnd"),
    app_commands.Choice(name="⚪ Vô hình", value="invisible"),
])
async def slash_custrangthai(inter, trangthai: app_commands.Choice[str]):
    if not await slash_owner_guard(inter): return
    set_panel_status(trangthai.value)
    await apply_bot_presence()
    em = {"online": "🟢", "idle": "🌙", "dnd": "⛔", "invisible": "⚪"}
    await inter.response.send_message(f"✅ {em.get(trangthai.value,'')} **{trangthai.name}**", ephemeral=True)

@bot.tree.command(name="addprefix", description="Đổi prefix server (owner)")
async def slash_addprefix(inter, prefix: str):
    if not await slash_owner_guard(inter): return
    if inter.guild is None: await inter.response.send_message("⚠️ Server only.", ephemeral=True); return
    server_prefixes[str(inter.guild.id)] = prefix; _save(PREFIX_FILE, server_prefixes)
    await inter.response.send_message(f"✅ `{prefix}`", ephemeral=True)

@bot.tree.command(name="adduser", description="Thêm user (owner)")
async def slash_adduser(inter, user: discord.User):
    if not await slash_owner_guard(inter): return
    if user.id in extra_users or is_owner(user.id):
        await inter.response.send_message("ℹ️ Có rồi.", ephemeral=True); return
    extra_users.add(user.id); _save(USERS_FILE, sorted(extra_users))
    await inter.response.send_message(f"✅ {user.mention}", ephemeral=True)

@bot.tree.command(name="addowner", description="Thêm owner (owner)")
async def slash_addowner(inter, user: discord.User):
    if not await slash_owner_guard(inter): return
    if is_owner(user.id): await inter.response.send_message("ℹ️ Owner.", ephemeral=True); return
    extra_owners.add(user.id); extra_users.discard(user.id)
    _save(OWNERS_FILE, sorted(extra_owners)); _save(USERS_FILE, sorted(extra_users))
    await inter.response.send_message(f"✅ {user.mention} OWNER", ephemeral=True)

class TreoRoomModal(discord.ui.Modal, title="🎙️ TREO ROOM"):
    f_token = discord.ui.TextInput(label="Token (nhiều, dấu phẩy)", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    f_server = discord.ui.TextInput(label="ID Server", required=True, max_length=32)
    f_channel = discord.ui.TextInput(label="ID Kênh Voice", required=True, max_length=32)
    f_voice_mode = discord.ui.TextInput(label="Mic + Tai nghe (on/off, on/off)", default="off,on", required=True, max_length=15)
    f_stream = discord.ui.TextInput(label="Stream (on/off)", default="off", required=True, max_length=3)

    async def on_submit(self, interaction):
        tokens = parse_tokens(str(self.f_token.value))
        if not tokens: await interaction.response.send_message("❌ Token.", ephemeral=True); return
        try: gid = int(str(self.f_server.value).strip()); cid = int(str(self.f_channel.value).strip())
        except ValueError: await interaction.response.send_message("❌ ID.", ephemeral=True); return
        parts = [p.strip() for p in str(self.f_voice_mode.value).strip().lower().split(",") if p.strip()]
        mic_val = parts[0] if len(parts) > 0 else "off"
        head_val = parts[1] if len(parts) > 1 else "on"
        mute = mic_val == "on"; deaf = head_val != "on"
        stream = str(self.f_stream.value).strip().lower() == "on"
        await interaction.response.send_message(
            f"⏳ Treo **{len(tokens)}** | Mic **{mic_val}** | Tai nghe **{head_val}** | Stream **{stream}**",
            ephemeral=True)
        await start_treo_room(tokens, gid, cid, mute, deaf, stream,
                              lambda m: interaction.followup.send(m, ephemeral=True))

@bot.tree.command(name="treoroom", description="Treo token vào voice")
async def slash_treoroom(inter):
    if not await slash_user_guard(inter): return
    if inter.guild is not None:
        try: await inter.user.send("⚠️ Dùng trong DM bot.")
        except Exception: pass
    await inter.response.send_modal(TreoRoomModal())

@bot.tree.command(name="dungtreo", description="Dừng TẤT CẢ (owner)")
async def slash_dungtreo(inter):
    if not await slash_owner_guard(inter): return
    r = stop_all_activity()
    await inter.response.send_message(f"🛑 **{r['voice']}** voice + **{r['tasks']}** task", ephemeral=True)

@bot.tree.command(name="dungtreoall", description="Alias (owner)")
async def slash_dungtreoall(inter):
    if not await slash_owner_guard(inter): return
    r = stop_all_activity()
    await inter.response.send_message(f"🛑 **{r['voice']}** voice + **{r['tasks']}** task", ephemeral=True)

@bot.tree.command(name="treongon", description="Nhắn từ file local/GitHub")
@app_commands.autocomplete(nguon=ngon_autocomplete)
async def slash_treongon(inter, delay: float, channel_id: str, server_id: str,
                         tokens: str, so_lan: int = 1,
                         user: Optional[discord.User] = None,
                         file: Optional[discord.Attachment] = None,
                         nguon: Optional[str] = None):
    if not await slash_user_guard(inter): return
    tok_list = parse_tokens(tokens)
    if not tok_list: await inter.response.send_message("❌ Token.", ephemeral=True); return
    try: cid = int(channel_id)
    except ValueError: await inter.response.send_message("❌ Kênh.", ephemeral=True); return
    try: sid = int(server_id)
    except ValueError: await inter.response.send_message("❌ Server.", ephemeral=True); return
    if delay is None or delay < 3.0: delay = 3.0
    if so_lan is None: so_lan = 1
    lines = []; used_from = ""
    if file is not None:
        NGON_DIR.mkdir(exist_ok=True)
        save_path = NGON_DIR / file.filename
        try:
            await file.save(save_path)
            lines = read_local_ngon_file(save_path)
            used_from = f"upload `{save_path.name}`"
        except Exception as e:
            await inter.response.send_message(f"❌ {e}", ephemeral=True); return
    elif nguon:
        lines, used_from = await parse_ngon_source(nguon)
    else:
        lines = read_messages()
        if lines: used_from = f"`{MSG_FILE}`"
    if not lines:
        await inter.response.send_message(
            f"❌ Không có nội dung.\nLocal: {len(find_local_ngon_files())} file\nGitHub: {len(_github_files_cache)} file",
            ephemeral=True); return
    tag_suffix = f" <@{user.id}>" if user else ""
    stop = register_stop()
    async def _loop(tok):
        for _ in range(so_lan if so_lan > 0 else 10**9):
            if stop.is_set(): return
            for line in lines:
                if stop.is_set(): return
                c = f"{line}{tag_suffix}" if (tag_suffix and not line.rstrip().endswith(">")) else line
                await send_token_message(tok, cid, sanitize(c))
                await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))
    async def run_all():
        try: await asyncio.gather(*[asyncio.create_task(_loop(t)) for t in tok_list])
        finally: unregister_stop(stop)
    asyncio.create_task(run_all())
    preview = f"{lines[0]}{tag_suffix}"[:100] if lines else ""
    await inter.response.send_message(
        f"🚀 Server `{sid}` Kênh `{cid}`\n"
        f"• Tokens `{len(tok_list)}` | Lặp `{so_lan if so_lan>0 else '∞'}` | Delay `{delay}s`\n"
        f"• Nguồn: {used_from} ({len(lines)} câu)\n"
        f"• Preview: `{preview}`", ephemeral=True)

# 🆕 /spam dùng send_bot_message_proxy (không cần Channel object)
@bot.tree.command(name="spam", description="Spam 1 nội dung (dùng proxy)")
async def slash_spam(inter, channel_id: str, server_id: str, delay: float, content: str, so_lan: int = 1):
    if not await slash_user_guard(inter): return
    try: cid = int(channel_id)
    except ValueError: await inter.response.send_message("❌ Kênh.", ephemeral=True); return
    if delay is None or delay < 3.0: delay = 3.0
    content = sanitize(content, 2000)
    stop = register_stop()
    async def loop():
        sent = 0; fail = 0
        try:
            while not stop.is_set():
                if so_lan > 0 and sent >= so_lan: break
                ok, err = await send_bot_message_proxy(cid, content)
                if ok: sent += 1; fail = 0
                else:
                    fail += 1
                    if fail >= 3:
                        log.warning(f"[SPAM] Fail 3 lần liên tiếp: {err}")
                        break
                    await asyncio.sleep(3)
                    continue
                await asyncio.sleep(max(3.0, delay + delay * random.uniform(-0.1, 0.1)))
        finally: unregister_stop(stop)
    asyncio.create_task(loop())
    await inter.response.send_message(
        f"🚀 Spam `{cid}` | Delay `{delay}s` | Lần `{so_lan if so_lan>0 else '∞'}`\n"
        f"• Proxy pool: **{len(_proxy_pool)}** live", ephemeral=True)

class SpamLinkSeverModal(discord.ui.Modal, title="📨 SPAM LINK SEVER"):
    f_server = discord.ui.TextInput(label="ID Server", required=True, max_length=32)
    f_channel = discord.ui.TextInput(label="ID Kênh", required=True, max_length=32)
    f_tokens = discord.ui.TextInput(label="Token (dấu phẩy)", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    f_content = discord.ui.TextInput(label="Nội dung (dòng trống = khối mới)", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    f_delay = discord.ui.TextInput(label="Delay giây (mặc định 2)", default="2", required=False, max_length=10)

    async def on_submit(self, interaction):
        try: sid = int(str(self.f_server.value).strip())
        except ValueError: await interaction.response.send_message("❌ Server.", ephemeral=True); return
        try: cid = int(str(self.f_channel.value).strip())
        except ValueError: await interaction.response.send_message("❌ Kênh.", ephemeral=True); return
        tok_list = parse_tokens(str(self.f_tokens.value))
        if not tok_list: await interaction.response.send_message("❌ Token.", ephemeral=True); return
        try: delay = float(str(self.f_delay.value).strip() or "2")
        except ValueError: delay = 2.0
        if delay < 2.0: delay = 2.0
        blocks = parse_text_blocks(str(self.f_content.value))
        if not blocks: await interaction.response.send_message("❌ Rỗng.", ephemeral=True); return
        total_chars = sum(len(b) for b in blocks)
        if total_chars > MODAL_HARD_LIMIT:
            NGON_DIR.mkdir(exist_ok=True)
            fname = f"auto_{int(time.time())}.txt"
            try:
                with open(NGON_DIR / fname, "w", encoding="utf-8") as f: f.write("\n\n".join(blocks))
                await interaction.response.send_message(
                    f"⚠️ Dài ({total_chars}). Đã lưu `{NGON_DIR.name}/{fname}`\n"
                    f"👉 `/treongon nguon:{fname}`", ephemeral=True)
                return
            except Exception as e:
                await interaction.response.send_message(f"❌ {e}", ephemeral=True); return
        stop = register_stop()
        async def _loop(tok):
            while not stop.is_set():
                for b in blocks:
                    if stop.is_set(): return
                    await send_token_message(tok, cid, sanitize(b))
                    await asyncio.sleep(max(2.0, delay + delay * random.uniform(-0.05, 0.05)))
        async def run_all():
            try: await asyncio.gather(*[asyncio.create_task(_loop(t)) for t in tok_list])
            finally: unregister_stop(stop)
        asyncio.create_task(run_all())
        await interaction.response.send_message(
            f"🚀 Server `{sid}` Kênh `{cid}` | Tokens `{len(tok_list)}`\n"
            f"• Khối `{len(blocks)}` ({total_chars} ký tự) | Delay `{delay}s`", ephemeral=True)

@bot.tree.command(name="spamlinksever", description="Spam nhiều khối")
async def slash_spamlinksever(inter):
    if not await slash_user_guard(inter): return
    await inter.response.send_modal(SpamLinkSeverModal())

@bot.tree.command(name="leave", description="Bot rời server (owner)")
async def slash_leave(inter):
    if not await slash_owner_guard(inter): return
    if inter.guild is None: await inter.response.send_message("⚠️ Server.", ephemeral=True); return
    name, gid = inter.guild.name, inter.guild.id
    await inter.response.send_message(f"👋 `{name}`...", ephemeral=True)
    try: await inter.guild.leave()
    except Exception: pass

@bot.tree.command(name="xa", description="Phát nhạc")
async def slash_xa(inter, tokens: str, channel_id: str, user: discord.User,
                   file: Optional[discord.Attachment] = None, so_thu_tu: Optional[int] = None):
    if not await slash_user_guard(inter): return
    tok_list = parse_tokens(tokens)
    if not tok_list: await inter.response.send_message("❌ Token.", ephemeral=True); return
    try: cid = int(channel_id)
    except ValueError: await inter.response.send_message("❌ Kênh.", ephemeral=True); return
    target = None
    if file is not None:
        XA_DIR.mkdir(exist_ok=True); target = XA_DIR / file.filename
        try: await file.save(target)
        except Exception as e: await inter.response.send_message(f"❌ {e}", ephemeral=True); return
    elif so_thu_tu is not None:
        for ext in (".mp3", ".wav", ".ogg", ".m4a"):
            c = XA_DIR / f"{so_thu_tu}{ext}"
            if c.exists(): target = c; break
        if target is None: await inter.response.send_message("❌ Không có file.", ephemeral=True); return
    else: await inter.response.send_message("❌ Upload hoặc số.", ephemeral=True); return
    started = 0
    for tok in tok_list:
        w = VoiceWorker(tok, inter.guild_id or 0, cid, mute=True, deaf=False, stream=False)
        active_voice_workers.append(w); asyncio.create_task(w.run()); started += 1; await asyncio.sleep(0.4)
    await inter.response.send_message(f"🎶 **{started}** token vào `{cid}` với `{target.name}`", ephemeral=True)

# ══════════════════════════════════════════════════════════════
#  PRESENCE
# ══════════════════════════════════════════════════════════════
async def apply_bot_presence():
    try:
        sm = {"online": discord.Status.online, "idle": discord.Status.idle,
              "dnd": discord.Status.dnd, "invisible": discord.Status.invisible}
        status = sm.get(get_panel_status(), discord.Status.online)
        activity = discord.Activity(type=discord.ActivityType.watching, name=get_panel_name())
        await bot.change_presence(status=status, activity=activity)
    except Exception as e: log.error(f"presence: {e}")

# ══════════════════════════════════════════════════════════════
#  WEB SERVER
# ══════════════════════════════════════════════════════════════
HTML_PAGE = r"""<!DOCTYPE html>
<html lang="vi"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{PANEL_NAME}} — Status</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#fff;font-family:'Consolas',monospace;
min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px;
background-image:radial-gradient(circle at 50% 0%,rgba(255,0,0,.18),transparent 60%)}
.mask{font-size:70px;margin-bottom:12px;filter:drop-shadow(0 0 25px rgba(255,0,0,.6));animation:float 3s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.header{font-size:30px;color:#f00;text-shadow:0 0 12px #f00;letter-spacing:5px;margin-bottom:6px;text-align:center}
.subtitle{color:#888;font-size:11px;margin-bottom:35px;letter-spacing:3px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;width:100%;max-width:960px}
.card{background:linear-gradient(145deg,#1a0000,#0d0000);border:1px solid #f00;border-radius:12px;padding:28px;
box-shadow:0 0 25px rgba(255,0,0,.2);transition:transform .2s}
.card:hover{transform:translateY(-4px);box-shadow:0 0 35px rgba(255,0,0,.4)}
.card-label{font-size:11px;color:#ff5555;text-transform:uppercase;letter-spacing:3px;margin-bottom:14px}
.card-value{font-size:36px;font-weight:bold;color:#fff;text-shadow:0 0 10px rgba(255,0,0,.6)}
.card-sub{font-size:11px;color:#666;margin-top:10px}
.card-value a{color:#0f8;text-decoration:none;text-shadow:0 0 12px #0f8;font-size:22px}
.footer{margin-top:40px;color:#333;font-size:10px;letter-spacing:3px;text-align:center}
.footer a{color:#f00;text-decoration:none}
.ws-status{position:fixed;top:14px;right:14px;font-size:10px;color:#555;padding:6px 12px;border:1px solid #333;border-radius:20px;background:#000}
.ws-status.on{color:#0f8;border-color:#0f8}
.ws-status.off{color:#f00;border-color:#f00}
</style></head><body>
<div class="ws-status off" id="wsStat">● WS: KẾT NỐI...</div>
<div class="mask">🎭</div>
<div class="header">{{PANEL_NAME}}</div>
<div class="subtitle">● {{INVITE_LINK}} ●</div>
<div class="grid">
<div class="card"><div class="card-label">Số Câu Lệnh</div>
<div class="card-value" id="cmds">—</div><div class="card-sub" id="cmd-sub">slash + prefix</div></div>
<div class="card"><div class="card-label">Số Server Bot Ở</div>
<div class="card-value" id="guilds">—</div><div class="card-sub">guild</div></div>
<div class="card"><div class="card-label">Proxy Live</div>
<div class="card-value" id="proxy">—</div><div class="card-sub" id="proxy-sub">pool</div></div>
<div class="card"><div class="card-label">Link Server Bot</div>
<div class="card-value"><a href="https://{{INVITE_LINK}}" target="_blank">🔗 {{INVITE_LINK}}</a></div>
<div class="card-sub">nhấn để tham gia</div></div>
</div>
<div class="footer">{{PANEL_NAME}} • v5.0.0<br>
<a href="/api/status">/api/status</a> • <a href="/health">/health</a> • /ws</div>
<script>
let ws,rt;
function ui(d){
document.getElementById('cmds').textContent=d.slash_count+d.prefix_count;
document.getElementById('cmd-sub').textContent=d.slash_count+' slash + '+d.prefix_count+' prefix';
document.getElementById('guilds').textContent=d.guild_count;
document.getElementById('proxy').textContent=d.proxy_pool;
document.getElementById('proxy-sub').textContent='live • '+d.proxy_scraped+' scraped';
}
function setWs(s){const e=document.getElementById('wsStat');
e.className='ws-status '+(s==='on'?'on':'off');
e.textContent=s==='on'?'● WS: ONLINE':'● WS: RECONNECT...'}
function conn(){const p=location.protocol==='https:'?'wss':'ws';
const sec=new URLSearchParams(location.search).get('secret')||'';
ws=new WebSocket(p+'://'+location.host+'/ws?secret='+encodeURIComponent(sec));
ws.onopen=()=>setWs('on');
ws.onmessage=e=>{try{const m=JSON.parse(e.data);if(m.type==='status')ui(m.data)}catch(_){}};
ws.onclose=()=>{setWs('off');clearTimeout(rt);rt=setTimeout(conn,5000)};
ws.onerror=()=>setWs('off')}
conn();
setInterval(async()=>{if(ws&&ws.readyState===WebSocket.OPEN)return;
try{const r=await fetch('/api/status');ui(await r.json())}catch(_){}},10000);
</script></body></html>"""

def get_status_dict():
    online = bot.is_ready() and bot.user is not None
    s = get_proxy_stats()
    return {
        "panel_name": get_panel_name(),
        "bot_status": "ONLINE" if online else "OFFLINE",
        "bot_name": str(bot.user) if bot.user else "—",
        "guild_count": len(bot.guilds),
        "slash_count": len(bot.tree.get_commands()),
        "prefix_count": len([c for c in bot.commands]),
        "voice_workers": len(active_voice_workers),
        "active_tasks": len(_active_stop_events),
        "ngon_local": len(find_local_ngon_files()),
        "ngon_github": len(_github_files_cache),
        "proxy_pool": s["pool_size"],
        "proxy_scraped": s["scraped"],
        "proxy_working": s["working"],
        "uptime": time.time() - BOT_START_TIME,
    }

async def handle_index(request):
    html = HTML_PAGE.replace("{{PANEL_NAME}}", get_panel_name()).replace("{{INVITE_LINK}}", INVITE_LINK)
    return aioweb.Response(text=html, content_type="text/html")

async def handle_health(request):
    return aioweb.json_response({"ok": True})

async def handle_status(request):
    return aioweb.json_response(get_status_dict())

async def handle_ws(request):
    ws = aioweb.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)
    if request.query.get("secret", "") != WS_SECRET:
        await ws.send_json({"type": "error", "message": "Invalid secret"})
        await ws.close(); return ws
    connected_ws_clients.add(ws)
    await ws.send_json({"type": "status", "data": get_status_dict()})
    try:
        async for msg in ws:
            if msg.type == aioweb.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data); await handle_ws_command(ws, data)
                except Exception as e:
                    await ws.send_json({"type": "error", "message": str(e)})
    finally:
        connected_ws_clients.discard(ws)
    return ws

async def handle_ws_command(ws, data):
    a = data.get("action")
    if a == "status":
        await ws.send_json({"type": "status", "data": get_status_dict()}); return
    if a in ("stop_all", "dungtreo"):
        r = stop_all_activity()
        await ws.send_json({"type": "ok", "message": f"Đã dừng {r['voice']}+{r['tasks']}"}); return
    if a == "refresh_proxy":
        asyncio.create_task(_refresh_proxy_pool())
        await ws.send_json({"type": "ok", "message": "Đang refresh proxy..."}); return
    await ws.send_json({"type": "error", "message": "Unsupported"})

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

async def cleanup_rate_limit_store():
    while True:
        await asyncio.sleep(3600)
        now = time.time()
        for ip in [ip for ip, t in ip_blocked_until.items() if t <= now]:
            ip_blocked_until.pop(ip, None)
        ws = now - RATE_LIMIT_WINDOW
        for ip in list(ip_request_log.keys()):
            dq = ip_request_log[ip]
            while dq and dq[0] < ws: dq.popleft()
            if not dq: ip_request_log.pop(ip, None)

async def start_web_server():
    app = aioweb.Application(middlewares=[ddos_protection_middleware])
    app.router.add_get("/",           handle_index)
    app.router.add_get("/health",     handle_health)
    app.router.add_get("/api/status", handle_status)
    app.router.add_get("/ws",         handle_ws)
    runner = aioweb.AppRunner(app); await runner.setup()
    site = aioweb.TCPSite(runner, "0.0.0.0", PORT); await site.start()
    log.info(f"🌐 Web: http://0.0.0.0:{PORT}")
    log.info(f"🌐 Proxy: {'ON' if PROXY_ENABLED else 'OFF'} | refresh {PROXY_REFRESH_INTERVAL}s")
    asyncio.create_task(broadcast_status_loop())
    asyncio.create_task(cleanup_rate_limit_store())
    while True: await asyncio.sleep(3600)

# ══════════════════════════════════════════════════════════════
#  READY
# ══════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    global _autocomplete_cache, _autocomplete_cache_ts
    print(f"{Fore.GREEN}[{OWNER_NAME.upper()}] ✅ {bot.user}{Style.RESET_ALL}")
    try:
        synced = await bot.tree.sync()
        print(f"{Fore.CYAN}[{OWNER_NAME.upper()}] ✅ {len(synced)} slash{Style.RESET_ALL}")
    except Exception as e: log.error(f"sync: {e}")
    await apply_bot_presence()
    gh_files = await list_github_ngon_files(force=True)
    _autocomplete_cache = gh_files or []
    _autocomplete_cache_ts = time.time()
    s = get_proxy_stats()
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 🎭 {get_panel_name()}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 🌐 Proxy: {'✅ ON' if PROXY_ENABLED else '❌ OFF'} | Pool: {s['pool_size']}{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] 📂 NGÔN: {len(find_local_ngon_files())} local + {len(gh_files)} github{Style.RESET_ALL}")
    print(f"{Fore.RED}[{OWNER_NAME.upper()}] ⏱️ Cooldown: {COOLDOWN}s{Style.RESET_ALL}")
    print(f"{Fore.RED}{'━'*60}{Style.RESET_ALL}")

# ══════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════
async def _run_all():
    tasks = [asyncio.create_task(start_web_server())]
    if PROXY_ENABLED:
        tasks.append(asyncio.create_task(proxy_refresh_loop()))

    log.info("⏳ Chờ 30s trước khi login Discord...")
    await asyncio.sleep(30)

    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            log.info(f"🔐 Login lần {attempt}/{max_retries}...")
            await bot.start(BOT_TOKEN)
            break
        except Exception as e:
            err = str(e); wait = min(60 * attempt, 300)
            if "429" in err or "1015" in err:
                log.warning(f"⚠️ Cloudflare limit lần {attempt}. Chờ {wait}s...")
            else:
                log.error(f"❌ Login lỗi: {e}")
            if attempt >= max_retries: break
            await asyncio.sleep(wait)

    try:
        await asyncio.gather(*tasks)
    finally:
        await close_http_session()

if __name__ == "__main__":
    if not BOT_TOKEN: raise SystemExit("❌ Thiếu DISCORD_TOKEN trong .env")
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    clear_console()
    print_banner(get_panel_name(), OWNER_NAME)
    XA_DIR.mkdir(exist_ok=True)
    try: asyncio.run(_run_all())
    except KeyboardInterrupt: log.info("Đã dừng.")
