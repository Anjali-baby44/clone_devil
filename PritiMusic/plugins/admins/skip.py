import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

import config
from PritiMusic import app
from PritiMusic.core.call import Lucky
from PritiMusic.misc import db

# ✅ Imports Updated
from PritiMusic.utils.database import get_loop
from PritiMusic.cplugin.utils.decorators.admins import AdminRightsCheck
from PritiMusic.utils.inline import close_markup
from PritiMusic.utils.stream.autoclear import auto_clean
from config import BANNED_USERS

@Client.on_message(
    filters.command(["skip", "cskip", "next", "cnext"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.group 
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip_comm(cli: Client, message: Message, _, chat_id):
    
    # 🛑 THE CLASH FIX: Agar command Main Bot par aayi hai, toh Clone wala code chup rahega!
    try:
        if cli.me.id == app.id:
            return
    except Exception:
        pass
        
    # 🟢 BULLETPROOF ADMIN CHECK
    user_id = message.from_user.id
    if user_id not in SUDOERS: 
        try:
            member = await cli.get_chat_member(chat_id, user_id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await message.reply_text("❌ **You don't have permission to use this command. Only Admins can skip.**")
        except Exception:
            return await message.reply_text("❌ **You don't have permission to use this command. Only Admins can skip.**")

    # 1. Queue check
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
    
    # 2. Loop check (Agar loop on hai, toh skip allow nahi hoga)
    loop = await get_loop(chat_id)
    if loop != 0:
        return await message.reply_text(_["admin_8"])

    # 3. Multi-skip logic (e.g., /skip 3)
    skip_count = 1
    if len(message.command) > 1:
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            if 1 <= state <= len(check):
                skip_count = state
            else:
                return await message.reply_text(_["admin_11"].format(len(check)))
        else:
            return await message.reply_text(_["admin_11"].format(len(check)-1))

    # 4. Actual Skip Logic
    try:
        # Pehle (skip_count - 1) songs ko queue se nikal kar clean up karo
        if skip_count > 1:
            for x in range(skip_count - 1):
                try:
                    popped = check.pop(0)
                    if popped:
                        await auto_clean(popped)
                except:
                    pass
        
        # Sahi PyTgCalls client (assistant) get karo safely
        pytgcalls_client = Lucky.one
        try:
            if hasattr(Lucky, "get_active_clients"):
                clients = await Lucky.get_active_clients(chat_id)
                pytgcalls_client = clients[0] if clients else Lucky.one
            elif hasattr(Lucky, "active_clients") and chat_id in Lucky.active_clients:
                val = Lucky.active_clients[chat_id]
                pytgcalls_client = val[0] if isinstance(val, list) and val else val
        except Exception:
            pass
            
        # change_stream call karo. 
        await Lucky.change_stream(pytgcalls_client, chat_id)
        
        # Skip confirmation
        await message.reply_text(f"➻ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ 🎄\n└ʙʏ : {message.from_user.mention}")
        
    except Exception as e:
        # Agar error aaya toh gracefully handle karo
        try:
            await message.reply_text(
                text=_["admin_6"].format(message.from_user.mention, message.chat.title),
                reply_markup=close_markup(_)
            )
            await Lucky.stop_stream(chat_id)
        except:
            pass
