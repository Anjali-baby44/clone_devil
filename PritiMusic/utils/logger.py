from pyrogram import enums
from pyrogram.enums import ParseMode, ButtonStyle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

from PritiMusic import app
from PritiMusic.utils.database import is_on_off
from config import LOGGER_ID

# 🔥 PREMIUM EMOJIS LIST 🔥
PREMIUM_EMOJIS = [
    "5422831825178206894", 
    "5368324170673489600",
    "5206607081334906820",
    "5206380668048496464"
]

# ====================================================
# HELPER FUNCTION: To Fetch Group Owner
# ====================================================
async def get_owner(client, chat_id):
    try:
        async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if member.status == enums.ChatMemberStatus.OWNER:
                return member.user.mention
    except:
        pass
    return "Unknown"


async def play_logs(message, streamtype):
    if await is_on_off(2):
        try:
            query = message.text.split(None, 1)[1]
        except:
            query = "Link/File or Reply"

        # Fetch Total Members & Owner
        try:
            members_count = await app.get_chat_members_count(message.chat.id)
        except:
            members_count = "Unknown"
            
        owner = await get_owner(app, message.chat.id)

        # Generate Link for Button
        chat_link = None
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        else:
            try:
                chat_link = await app.export_chat_invite_link(message.chat.id)
            except:
                pass

        logger_text = f"""
<blockquote><b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ : {message.from_user.mention}</b>
<b>• ǫᴜᴇʀʏ : {query}</b>
<b>• ᴄʜᴀᴛ : {message.chat.title} [<code>{message.chat.id}</code>]</b>
<b>• ᴏᴡɴᴇʀ : {owner}</b>
<b>• ᴍᴇᴍʙᴇʀs : {members_count}</b></blockquote>
"""
        # Create Button Markup with Kaurigram Styles
        reply_markup = None
        if chat_link:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=chat_link, style=ButtonStyle.PRIMARY, icon_custom_emoji_id=random.choice(PREMIUM_EMOJIS))]]
            )

        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup
                )
            except:
                pass
        return


async def clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype):
    # 1. Data Extract kar lete hain
    bot = await client.get_me()
    try:
        query = message.text.split(None, 1)[1]
    except:
        query = "Link/File or Reply"

    # ====================================================
    # CASE 1: Clone Bot Owner ke Logger me bhejna (Simple Old Style)
    # ====================================================
    if clone_logger_id:
        owner_log_text = f"""
<b>{bot_mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ :</b> {message.from_user.mention}
<b>• ǫᴜᴇʀʏ :</b> {query}
<b>• ᴄʜᴀᴛ :</b> {message.chat.title} [<code>{message.chat.id}</code>]
"""
        if message.chat.id != int(clone_logger_id):
            try:
                await client.send_message(
                    chat_id=int(clone_logger_id),
                    text=owner_log_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"[ERROR] Sending to Clone Owner Log Failed: {e}")

    # ====================================================
    # CASE 2: Aapke (Main Admin) Logger me bhejna (With Link Button & Members)
    # ====================================================
    if LOGGER_ID:
        try:
            members_count = await client.get_chat_members_count(message.chat.id)
        except:
            members_count = "Unknown"
            
        owner = await get_owner(client, message.chat.id)

        chat_link = None
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        else:
            try:
                chat_link = await client.export_chat_invite_link(message.chat.id)
            except:
                pass

        admin_log_text = f"""
<blockquote><b>🤖 ᴄʟᴏɴᴇ ʙᴏᴛ ʟᴏɢ : @{bot.username}</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ : {message.from_user.mention}</b>
<b>• ǫᴜᴇʀʏ : {query}</b>
<b>• ᴄʜᴀᴛ : {message.chat.title} [<code>{message.chat.id}</code>]</b>
<b>• ᴏᴡɴᴇʀ : {owner}</b>
<b>• ᴍᴇᴍʙᴇʀs : {members_count}</b></blockquote>
"""
        reply_markup = None
        if chat_link:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=chat_link, style=ButtonStyle.PRIMARY, icon_custom_emoji_id=random.choice(PREMIUM_EMOJIS))]]
            )

        # Ye Main Bot (app) bhejega aapke group me
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=admin_log_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"[ERROR] Sending to Main Admin Log Failed: {e}")


# ====================================================
# NEW FUNCTION: Bot Removed (Kicked/Left) Logs
# ====================================================
async def bot_removed_logs(client, message, is_clone=False):
    """
    Isko aap left_chat_member ya ChatMemberUpdated handler me call kar sakte ho.
    Example call: await bot_removed_logs(client, message, is_clone=True)
    """
    try:
        bot = await client.get_me()
        
        # Jisne bot ko nikala uska profile mention (link automatically ban jayega)
        if message.from_user:
            kicked_by = message.from_user.mention
        else:
            kicked_by = "<b>Unknown User</b>"
        
        try:
            members_count = await client.get_chat_members_count(message.chat.id)
        except:
            members_count = "Unknown"
            
        owner = await get_owner(client, message.chat.id)

        # Note: Bot nikal jane ke baad private group ka link nikalna API me allowed nahi hai.
        # Isliye agar username public hai tabhi button aayega.
        chat_link = None
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"

        # Alag-alag formatting Clone aur Main bot ke liye
        if is_clone:
            header_text = "⚠️ ᴄʟᴏɴᴇ ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ"
            bot_details = f"@{bot.username}"
        else:
            header_text = "⚠️ ᴍᴀɪɴ ʙᴏᴛ ʀᴇᴍᴏᴠᴇᴅ"
            bot_details = app.mention

        remove_log_text = f"""
<blockquote><b>{header_text}</b>

<b>• ʙᴏᴛ : {bot_details}</b>
<b>• ʀᴇᴍᴏᴠᴇᴅ ʙʏ : {kicked_by}</b>
<b>• ᴄʜᴀᴛ : {message.chat.title} [<code>{message.chat.id}</code>]</b>
<b>• ᴏᴡɴᴇʀ : {owner}</b>
<b>• ᴍᴇᴍʙᴇʀs : {members_count}</b></blockquote>
"""
        reply_markup = None
        if chat_link:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=chat_link, style=ButtonStyle.DANGER, icon_custom_emoji_id=random.choice(PREMIUM_EMOJIS))]]
            )

        if LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=remove_log_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    reply_markup=reply_markup
                )
            except Exception as e:
                print(f"[ERROR] Sending Remove Log Failed: {e}")
    except Exception as e:
        print(f"[ERROR] Bot Removed Log Generation Failed: {e}")


# ====================================================
# NEW FUNCTION: Autoplay Logs
# ====================================================
async def autoplay_log(client, chat_id, query, is_clone=False):
    """
    Isko aap `core/call.py` mein jahan autoplay gaana add hota hai wahan call kar sakte hain.
    Example: await autoplay_log(client, chat_id, next_track["title"], is_clone=False)
    """
    if not await is_on_off(2):
        return
        
    try:
        bot = await client.get_me()
        bot_mention = bot.mention
    except:
        return

    try:
        chat = await client.get_chat(chat_id)
        chat_title = chat.title
        chat_username = chat.username
    except:
        chat_title = "Unknown Chat"
        chat_username = None

    try:
        members_count = await client.get_chat_members_count(chat_id)
    except:
        members_count = "Unknown"
        
    owner = await get_owner(client, chat_id)

    chat_link = None
    if chat_username:
        chat_link = f"https://t.me/{chat_username}"
    else:
        try:
            chat_link = await client.export_chat_invite_link(chat_id)
        except:
            pass

    if is_clone:
        header_text = f"🤖 <b>ᴄʟᴏɴᴇ ᴀᴜᴛᴏᴘʟᴀʏ ʟᴏɢ : @{bot.username}</b>"
    else:
        header_text = f"<b>{bot_mention} ᴀᴜᴛᴏᴘʟᴀʏ ʟᴏɢ</b>"

    logger_text = f"""
<blockquote>{header_text}

<b>• ᴀᴄᴛɪᴏɴ : ᴀᴜᴛᴏᴘʟᴀʏ ᴛʀɪɢɢᴇʀᴇᴅ 🔄</b>
<b>• ᴛʀᴀᴄᴋ : {query}</b>
<b>• ᴄʜᴀᴛ : {chat_title} [<code>{chat_id}</code>]</b>
<b>• ᴏᴡɴᴇʀ : {owner}</b>
<b>• ᴍᴇᴍʙᴇʀs : {members_count}</b></blockquote>
"""
    reply_markup = None
    if chat_link:
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("ɢʀᴏᴜᴘ ʟɪɴᴋ", url=chat_link, style=ButtonStyle.SUCCESS, icon_custom_emoji_id=random.choice(PREMIUM_EMOJIS))]]
        )

    if chat_id != LOGGER_ID:
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"[ERROR] Sending Autoplay Log Failed: {e}")
