import math
import asyncio
from datetime import datetime, timedelta
from telegram.ext import CommandHandler
from Grabber import application, user_collection
import math
import random
import time

async def balance(update, context):
    user_id = update.effective_user.id

    user_data = await user_collection.find_one({'id': user_id})

    if user_data:
        balance_amount = user_data.get('balance', 0)
        bank_balance = math.floor(bank_balance)
        balance_message = f"Your Current Balance Is :  $ `{balance_amount}` Gold coins!!"    
    else:
        balance_message = "You are not eligible To be a Hunter 🍂"

    await update.message.reply_text(balance_message)

pay_cooldown = {}

async def pay(update, context):
    sender_id = update.effective_user.id

    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply To a Hunter to /pay.")
        return
    
    if update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.id == sender_id:
        await update.message.reply_text("You can't give $ Gold coins To Yourself!")
        return

    # Check if the user has executed /pay recently and enforce cooldown
    if sender_id in pay_cooldown:
        last_execution_time = pay_cooldown[sender_id]
        if (datetime.utcnow() - last_execution_time) < timedelta(minutes=30):
            await update.message.reply_text("You can pay /pay again after 30 Minutes!!...")
            return

    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply a Hunter to /pay.")
        return

    recipient_id = update.message.reply_to_message.from_user.id
    recipient_first_name = update.message.reply_to_message.from_user.first_name
    recipient_username = update.message.reply_to_message.from_user.username

    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        await update.message.reply_text("Invaild amount, use /pay <amount>")
        return
      
    if amount < 0:
        await update.message.reply_text("Amount must be positive BKL !!!")
        return
    elif amount > 1000000:
        await update.message.reply_text("You can pay upto $ `10,00,000` Gold coins in one payment !!")
        return

    sender_data = await user_collection.find_one({'id': sender_id})
    if not sender_data or sender_data.get('balance', 0) < amount:
        await update.message.reply_text("insufficient amount to pay !!.")
        return

    await user_collection.update_one(
        {'id': sender_id},
        {'$inc': {'balance': -amount}}
    )
    await user_collection.update_one(
        {'id': recipient_id},
        {'$inc': {'balance': amount}}
    )

    pay_cooldown[sender_id] = datetime.utcnow()

    recipient_link = f"https://t.me/{recipient_username}" if recipient_username else f"https://t.me/user{recipient_id}"
    success_message = f"success ! You paid $ `{amount}` Gold coins to [{recipient_first_name}]!"

    await update.message.reply_markdown(success_message)

async def mtop(update, context):
    # Retrieve the top 10 users with the highest balance
    top_users = await user_collection.find({}, projection={'id': 1, 'first_name': 1, 'last_name': 1, 'balance': 1}).sort('balance', -1).limit(10).to_list(10)

    # Create a message with the top users
    top_users_message = "Top 10 Rich Hunters data.\n\n"
    for i, user in enumerate(top_users, start=1):
        first_name = user.get('first_name', 'Unknown')
        last_name = user.get('last_name', '')
        user_id = user.get('id', 'Unknown')

        full_name = f"{first_name} {last_name}" if last_name else first_name

        top_users_message += f"{i}. <a href='tg://user?id={user_id}'>{full_name}</a>, $ `{user.get('balance', 0)}` Gold Coins\n"

    photo_path = 'https://telegra.ph/file/07283c3102ae87f3f2833.png'
    await update.message.reply_photo(photo=photo_path, caption=top_users_message, parse_mode='HTML')


from datetime import datetime, timedelta

async def format_time_delta(delta):
    seconds = delta.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

async def daily_reward(update, context):
    user_id = update.effective_user.id
    user_data = await user_collection.find_one({'id': user_id}, projection={'last_daily_reward': 1, 'balance': 1})

    if user_data:
        last_claimed_date = user_data.get('last_daily_reward')

        if last_claimed_date and last_claimed_date.date() == datetime.utcnow().date():
            remaining_time = timedelta(days=1) - (datetime.utcnow() - last_claimed_date)
            formatted_time = await format_time_delta(remaining_time)
            await update.message.reply_text(f"Soory ! hunter but you already claimed . Next reward in: `{formatted_time}`.")
            return

    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': 2000}, '$set': {'last_daily_reward': datetime.utcnow()}}
    )

    await update.message.reply_text("Congratulations! You claim $ `2000` Gold coins as a daily reward.")

async def roll(update, context):
    user_id = update.effective_user.id
    try:
        amount = int(context.args[0])
        choice = context.args[1].upper()  # Assuming the second argument is ODD or EVEN
    except (IndexError, ValueError):
        await update.message.reply_text("Invalid usage, please use /roll <amount> <ODD/EVEN>")
        return

    if amount < 0:
        await update.message.reply_text("Amount must be positive.")
        return

    user_data = await user_collection.find_one({'id': user_id})
    if not user_data:
        await update.message.reply_text("User data not found.")
        return

    balance_amount = user_data.get('balance', 0)
    if amount < balance_amount * 0.07:
        await update.message.reply_text("You can bet more than 7% of your balance.")
        return

    if balance_amount < amount:
        await update.message.reply_text("Insufficient balance to place the bet.")
        return

    # Send the dice emoji
    dice_message = await context.bot.send_dice(update.effective_chat.id, "🎲")

    # Extract the dice value
    dice_value = dice_message.dice.value

    # Check if the dice roll is odd or even
    dice_result = "ODD" if dice_value % 2 != 0 else "EVEN"

    xp_change = 0  # Initialize XP change

    if choice == dice_result:
        # User wins, update balance and add XP
        xp_change = 4
        await user_collection.update_one(
            {'id': user_id},
            {'$inc': {'balance': amount, 'user_xp': xp_change}}
        )
        await update.message.reply_text(f"Dice roll: {dice_value}\nYou won! Your balance increased by {amount * 2}.")
    else:
        # User loses, deduct bet amount from balance and subtract XP
        xp_change = -2
        await user_collection.update_one(
            {'id': user_id},
            {'$inc': {'balance': -amount, 'user_xp': xp_change}}
        )
        await update.message.reply_text(f"Dice roll: {dice_value}\nYou lost! {amount} deducted from your balance.")

    # Notify user about XP change
    await update.message.reply_text(f"XP change: {xp_change}")

application.add_handler(CommandHandler("roll", roll, block=False))

async def xp(update, context):
    user_id = update.effective_user.id
    user_data = await user_collection.find_one({'id': user_id})

    if not user_data:
        await update.message.reply_text("User data not found.")
        return

    xp = user_data.get('user_xp', 0)
    level = math.floor(math.sqrt(xp / 100)) + 1

    if level > 100:
        level = 100

    ranks = {1: "E", 10: "D", 30: "C", 50: "B", 70: "A", 90: "S"}
    rank = next((rank for xp_limit, rank in ranks.items() if level <= xp_limit), None)

    message = f"Your current level is `{level}`\nand your rank is `{rank}`."

    await update.message.reply_text(message)

application.add_handler(CommandHandler("xp", xp, block=False))
application.add_handler(CommandHandler("roll", roll, block=False))
application.add_handler(CommandHandler("bal", balance, block=False))
application.add_handler(CommandHandler("pay", pay, block=False))

application.add_handler(CommandHandler("Tophunters", mtop, block=False))
application.add_handler(CommandHandler("claim", daily_reward, block=False))
