from telegram.ext import CommandHandler, CallbackContext
from Grabber import collection, user_collection, application

async def sell(update, context):
    user_id = update.effective_user.id

    # Check if the command includes a character ID
    if not context.args or len(context.args) != 1:
        await update.message.reply_text('Please provide a valid Character ID to sell.')
        return

    character_id = context.args[0]

    # Retrieve the character from the harem based on the provided ID
    character = await collection.find_one({'id': character_id})
    if not character:
        await update.message.reply_text('ғᴜᴄᴋ ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴏɴ ᴛʜɪs ɪᴅ ɴᴜᴍʙᴇʀ')
        return

    # Check if the user has the character in their harem
    user = await user_collection.find_one({'id': user_id})
    if not user or 'characters' not in user:
        await update.message.reply_text('bC you dont have character on this id')
        return

    # Check if the character is present in the user's harem and get its count
    character_count = sum(1 for char in user.get('characters', []) if char['id'] == character_id)

    if character_count == 0:
        await update.message.reply_text('ғᴜᴄᴋ ʏᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴏɴ ᴛʜɪs ɪᴅ ɴᴜᴍʙᴇʀ')
        return

    # Determine the coin value based on the rarity of the character
    rarity_coin_mapping = {
       "🟢 Common": 20000,
        "🔵 Medium": 40000,
        "🟠 Rare": 80000,
        "🟡 Legendary": 15000,
        "🪽 celestial": 200000,
        "💮 Exclusive": 30000,
        "🥴 Spacial": 400000,
        "💎 Premium": 60000000,
        "🔮 Limited": 2000000,
    }

    rarity = character.get('rarity', 'Unknown Rarity')
    coin_value = rarity_coin_mapping.get(rarity, 0)

    if coin_value == 0:
        await update.message.reply_text('Invalid rarity. Cannot determine the coin value.')
        return

    # Find the specific character instance to sell (only the first one)
    character_to_sell = next((char for char in user.get('characters', []) if char['id'] == character_id), None)

    if character_to_sell:
        # Remove the sold character from the user's harem
        await user_collection.update_one(
            {'id': user_id},
            {'$pull': {'characters': {'id': character_id}}, '$inc': {'count': -1}}
        )

        # Add coins to the user's balance
        await user_collection.update_one({'id': user_id}, {'$inc': {'balance': coin_value}})
        await update.message.reply_text(f"congratulations you selled a new waifu {character_to_sell['name']} now you get¸ {coin_value} Tokens⚡")
    else:
        await update.message.reply_text("fuck waifu is not found! 🙃...")

sell_handler = CommandHandler("wsell", sell, block=False)
application.add_handler(sell_handler)
