import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from alicex import LOGGER, app, userbot
from alicex.core.call import alice
from alicex.misc import sudo
from alicex.plugins import ALL_MODULES
from alicex.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("alicex.plugins" + all_module)
    LOGGER("alicex.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await alice.start()
    try:
        await alice.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("alicex").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await alice.decorators()
    LOGGER("alicex").info(
        "\x41\x6c\x69\x63\x65\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x74\x68\x61\x6e\x6f\x73\x5f\x70\x72\x6f"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("alicex").info("Stopping alice Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
