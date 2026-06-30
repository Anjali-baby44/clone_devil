import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ----------------- TELEGRAM CREDENTIALS -----------------
API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH", "")

BOT_TOKEN = getenv("BOT_TOKEN", "")
BOT_ID = getenv("BOT_ID", "")

# ----------------- API RACING CONFIGURATION -----------------
# 1. Shruti API
API_URL = getenv("API_URL", "https://api.shrutibots.site")
API_KEY = getenv("API_KEY", "ShrutiBotsC0WH1GowF2HkGoKv4F3y")

# 2. Xbit API
YTPROXY_URL = getenv("YTPROXY_URL", "https://tgapi.xbitcode.com")
YT_API_KEY = getenv("YT_API_KEY" , "xbit_B4TNnBAoe6uoSM7NLFz-dk6X7GibJ6Bh")

# 3. Worker API
WORKER_FALLBACK_API_URL = getenv("WORKER_FALLBACK_API_URL", "https://youtubenewapi.skybotsdeveloper.workers.dev")
WORKER_FALLBACK_API_KEY = getenv("WORKER_FALLBACK_API_KEY", "itsmesid")

# 4. Inflex API
INFLEX_API_URL = getenv("INFLEX_API_URL", "https://teaminflex.xyz")
INFLEX_API_KEY = getenv("INFLEX_API_KEY", "INFLEX40920628D")

# ----------------- BOT DETAILS -----------------
OWNER_USERNAME = getenv("OWNER_USERNAME", "")
BOT_USERNAME = getenv("BOT_USERNAME", "")
BOT_NAME = getenv("BOT_NAME", "")
ASSUSERNAME = getenv("ASSUSERNAME", "")
BOT_LINK = getenv("BOT_LINK", "https://t.me/clone_MUSICrobot")

MONGO_DB_URI = getenv("MONGO_DB_URI", "")

# ----------------- LOGGING & IDS -----------------
LOGGER_ID = int(getenv("LOGGER_ID", "0"))
CLONE_LOGGER = LOGGER_ID
CLONE_LOGGER_2 = int(getenv("CLONE_LOGGER_2", "-1003255930328")) # ✅ Naya Log Group 2

OWNER_ID = int(getenv("OWNER_ID", "0"))

 SUDOERS = [8418584090, 8723235165]


# ----------------- SERVER & DEPLOYMENT -----------------
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", "")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", "")

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/THE-SHIV-OFFICIAL/CLONE-TRIAL")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", "")

# ----------------- LINKS & SUPPORT -----------------
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/betabot_hub")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/betabot_support")
GITHUB = getenv("GITHUB", "https://t.me/sukoon_s")

# ----------------- ASSISTANT LIMITS -----------------
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))

# ----------------- DURATION LIMITS -----------------
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "17000"))
SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

# ----------------- SPOTIFY API -----------------
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))
PLAYLIST_ID = -1003812209413

# ----------------- FILE SIZE LIMITS -----------------
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

# ----------------- STRING SESSIONS -----------------
STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)

# ----------------- DICTS & LISTS -----------------
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

# ----------------- IMAGES & THUMBNAILS -----------------
START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/n22tbs.jpg").split()
HELP_IMG_URL = getenv("HELP_IMG_URL", "https://files.catbox.moe/zbl2i7.jpg").split()
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/zbl2i7.jpg").split()

PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://files.catbox.moe/6r97s4.jpg https://files.catbox.moe/huqcbp.jpg https://files.catbox.moe/gbx3h3.jpg https://files.catbox.moe/6f5azl.jpg").split()
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://files.catbox.moe/6r97s4.jpg")
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://files.catbox.moe/6r97s4.jpg").split()
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://i.ibb.co/S4sPf3q8/soundcloud.jpg").split()
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://files.catbox.moe/6r97s4.jpg").split()
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()

# ----------------- CHECKS & VALIDATIONS -----------------
if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL url must start with https://")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT url must start with https://")

# ----------------- UI ELEMENTS -----------------
CMBOT = [
    "💞", "🥂", "🔍", "🧪", "⚡️", "🔥", "🦋", "🎩", "🌈", "🍷",
    "🥃", "🥤", "🕊️", "💌", "🧨", "✨", "💥", "💯", "🌟", "⚡️",
    "❤️", "😍", "🥰", "😘", "😂", "🤣", "😱", "😡", "👏", "🙏",
    "🎉", "🎊", "🎶", "🎵", "🎧", "🎸", "🎹", "🥁", "🎺", "🎷",
    "🔥", "⚡️", "💫", "🌙", "☀️", "🌈", "❄️", "🌸", "🌺", "🌹",
    "🦋", "🕊️", "🐍", "🐯", "🦁", "🐺", "🐉", "🦅", "🦄", "🐎"
]

EFFECT_ID = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]
