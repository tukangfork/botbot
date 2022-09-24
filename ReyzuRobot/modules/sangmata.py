from telethon.errors.rpcerrorlist import YouBlockedUserError
from ReyzuRobot import telethn as tbot
from ReyzuRobot.events import register
from ReyzuRobot import ubot2 as ubot
from asyncio.exceptions import TimeoutError


@register(pattern="^/sg ?(.*)")
async def lastname(steal):
    steal.pattern_match.group(1)
    puki = await steal.reply("```Mengambil informasi pengguna..```")
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await puki.edit("```Harap balas ke pesan pengguna.```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await puki.edit("```Balas pesan pengguna asli.```")
        return
    await puki.edit("```Tunggu sebentar...```")
    try:
        async with ubot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                r = await conv.get_response()
                response = await conv.get_response()
            except YouBlockedUserError:
                await steal.reply(
                    "```Error, lapor ke @ReyzuSupport```"
                )
                return
            if r.text.startswith("Name"):
                respond = await conv.get_response()
                await puki.edit(f"`{r.message}`")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id, respond.id]
                ) 
                return
            if response.text.startswith("No records") or r.text.startswith(
                "No records"
            ):
                await puki.edit("```Saya tidak dapat menemukan informasi pngguna ini, oengguna ini belum pernah mengubah namanya.```")
                await ubot.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id]
                )
                return
            else:
                respond = await conv.get_response()
                await puki.edit(f"```{response.message}```")
            await ubot.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id, respond.id]
            )
    except TimeoutError:
        return await puki.edit("`Aku lelah, maaf 🙏 ...`")
