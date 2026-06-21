from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

import config
from PritiMusic import app
from PritiMusic.core.call import Lucky
from PritiMusic.utils.database import is_music_playing, music_on
from PritiMusic.utils.decorators import AdminRightsCheck
from PritiMusic.utils.inline import close_markup
from config import BANNED_USERS

@Client.on_message(
    filters.command(["resume", "cresume"], prefixes=["/", "!", "#"]) 
    & filters.group 
    & ~BANNED_USERS
)
@AdminRightsCheck
async def resume_admin(cli: Client, message: Message, _, chat_id):
    
    # BULLETPROOF ADMIN CHECK
    if message.from_user.id not in config.SUDOERS:
        try:
            member = await cli.get_chat_member(chat_id, message.from_user.id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await message.reply_text("❌ **Sirf Admins he is command ko use kar sakte hain!**")
        except Exception:
            return await message.reply_text("❌ **Error: Admin rights verify nahi ho paye.**")

    # Queue status check
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
        
    # Database update
    await music_on(chat_id)
    
    # Stream resume
    await Lucky.resume_stream(chat_id)
    
    # Success message
    await message.reply_text(
        _["admin_4"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
