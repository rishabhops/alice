import random
from telegram.ext import CommandHandler, CallbackContext
from Grabber import application, user_collection
from datetime import datetime, timedelta

# Define a cooldown duration in seconds (1 minute in this case)
COOLDOWN_DURATION = 73
COMMAND_BAN_DURATION = 600  # Set the ban duration in seconds (10 minutes)

# Create a dictionary to store the last command time and the command count for each user
last_command_time = {}
user_cooldowns = {}  # Dictionary to track user cooldowns

async def random_daily_reward(update, context):
    # Check if the command is used in a group
    if update.message.chat.type == "private":
        await update.message.reply_text("This command can only be used in group chats.")
        return

    user_id = update.effective_user.id

    # Check if the command is a reply to a message
    if update.message.reply_to_message:
        await update.message.reply_text("This command cannot be used as a reply to someone else's message.")
        return

    # Check if the user is banned from the command
    if user_id in user_cooldowns and (datetime.utcnow() - user_cooldowns[user_id]) < timedelta(seconds=COOLDOWN_DURATION):
        remaining_time = COOLDOWN_DURATION - (datetime.utcnow() - user_cooldowns[user_id]).total_seconds()
        await update.message.reply_text(f"You must wait {int(remaining_time)} seconds before using sexplore again.")
        return

    # Check if the user has enough balance to pay the fee
    user_data = await user_collection.find_one({'id': user_id}, projection={'balance': 1})
    user_balance = user_data.get('balance', 0)
    crime_fee = 300

    if user_balance < crime_fee:
        await update.message.reply_text("You need at least 500 tokens to use explore.")
        return

    # Deduct the crime fee from the user's balance
    await user_collection.update_one({'id': user_id}, {'$inc': {'balance': -crime_fee}})

    # Generate a random token reward between 500 and 1000
    random_reward = random.randint(600, 1000)

    # Generate a random congratulatory message
    congratulatory_messages = ["Explore a dungeon", "Explore a dark forest", "Explore ruins", "Explore an elvish village", "Explore a goblin nest", "Explore an orc den"]
    random_message = random.choice(congratulatory_messages)

    # Update the user's balance with the random reward and record the last command time
    await user_collection.update_one(
        {'id': user_id},
        {'$inc': {'balance': random_reward}}
    )
    last_command_time[user_id] = datetime.utcnow()

    # Set the user cooldown
    user_cooldowns[user_id] = datetime.utcnow()

    await update.message.reply_text(f"You {random_message} and got {random_reward} tokens.🤫")

async def clear_command_ban(context: CallbackContext):
    user_id = context.job.context
    if user_id in user_cooldowns:
        del user_cooldowns[user_id]

# Add the new command handler for random_daily_reward
application.add_handler(CommandHandler("daily", random_daily_reward, block=True))
