import telebot
import random
import time
import logging

# Replace with your bot token
bot_token = '7897622625:AAH-DA4CVm6hJUABcD1Ft6kt4Mf87vrXkkM'
bot = telebot.TeleBot(bot_token)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Store user data (In a real scenario, use a database)
users = {}
last_command_times = {}

# Helper function to get user's balance
def get_balance(user_id):
    return users.get(user_id, 0)

# Helper function to update user's balance
def update_balance(user_id, amount):
    if user_id in users:
        users[user_id] = max(users[user_id] + amount, 0)  # Balance can't go below 0
    else:
        users[user_id] = max(amount, 0)

# Helper function to log actions
def log_action(action, user_id, info=""):
    user = f"User {user_id}"
    logger.info(f"{action}: {user}. {info}")

# Helper function to enforce cooldown (2 seconds delay)
def enforce_cooldown(user_id, command, cooldown=2):
    current_time = time.time()
    if user_id in last_command_times:
        last_used = last_command_times[user_id].get(command, 0)
        if current_time - last_used < cooldown:
            return False
    if user_id not in last_command_times:
        last_command_times[user_id] = {}
    last_command_times[user_id][command] = current_time
    return True

# Only allow bot in group chats
def check_group(message):
    return message.chat.type in ['group', 'supergroup']

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    welcome_message = (
        "🐹 Welcome to the Scamster Gank fun Bot! 🐹💰\n\n"
        "Join the anti-scam revolution with fun games and big rewards, all while staying safe from the crypto wilderness! 🚀💎\n\n"
        "🎮 Here’s what you can do:\n"
        "- /steal – Test your luck and steal some coins from fellow Ganksters!\n"
        "- /Gank_points – Check your balance and see how much $$ you’ve racked up!\n"
        "- /spin_slots – Spin the slots for a chance to hit big winnings!\n"
        "- /roll_dice – Roll the dice and see where fortune takes you.\n"
        "- /flip_coin – A simple coin flip could change your fortune.\n"
        "- /raffle – Enter the raffle and win some $$!\n"
        "- /leaderboard – Check out the top Ganksters dominating the game.\n"
        "- /invite – Spread the Gank movement and earn rewards for inviting friends.\n\n"
        "🚀 Ready to take down the scams and have fun? Type /spin_slots to get started!\n\n"
        "May the Gank be with you, and fortune in your favor! 🐹💸"
    )
    bot.send_message(message.chat.id, welcome_message)

# /steal command
@bot.message_handler(commands=['steal'])
def steal(message):
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    user_id = message.from_user.id
    if not enforce_cooldown(user_id, 'steal'):
        bot.reply_to(message, "Please wait before trying again!")
        return
    if random.random() < 0.75:  # 75% chance of success
        reward = random.choice([1000, 1500, 2000, 2500, 3000, 5000])
        update_balance(user_id, reward)
        bot.reply_to(message, f"😈 Successful steal Gank 😈, you got {reward} Gank points!")
        log_action("Steal Success", user_id, f"Reward: {reward}")
    else:
        if get_balance(user_id) > 0:
            update_balance(user_id, -1000)
            bot.reply_to(message, "Failed! Sorry Gank, You lost 1000 Gank points.")
            log_action("Steal Fail", user_id, "Lost: 1000 points")
        else:
            bot.reply_to(message, "Failed! Sorry Gank, You have no points to lose.")
            log_action("Steal Fail", user_id, "No points to lose")

# /Gank_points command
@bot.message_handler(commands=['Gank_points'])
def Gank_points(message):
    user_id = message.from_user.id
    balance = get_balance(user_id)
    bot.reply_to(message, f"You have {balance} Gank points!")
    log_action("Checked Balance", user_id, f"Balance: {balance}")

# /spin_slots command
@bot.message_handler(commands=['spin_slots'])
def spin_slots(message):
    user_id = message.from_user.id
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    if not enforce_cooldown(user_id, 'spin_slots'):
        bot.reply_to(message, "Please wait before trying again!")
        return
    if random.random() < 0.50:  # 50% chance of winning
        update_balance(user_id, 1500)
        bot.reply_to(message, "❤❤❤, Congrats Gank it's a win! +1500 Gank points!")
        log_action("Slot Win", user_id, "+1500 points")
    else:
        if get_balance(user_id) > 0:
            update_balance(user_id, -1000)
            bot.reply_to(message, "❌😢💔, Sorry, it's a loss! -1000 Gank points!")
            log_action("Slot Loss", user_id, "-1000 points")
        else:
            bot.reply_to(message, "❌😢💔, Sorry, you have no points to lose!")
            log_action("Slot Loss", user_id, "No points to lose")

# /roll_dice command
@bot.message_handler(commands=['roll_dice'])
def roll_dice(message):
    user_id = message.from_user.id
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    if not enforce_cooldown(user_id, 'roll_dice'):
        bot.reply_to(message, "Please wait before trying again!")
        return
    dice_roll = random.randint(1, 12)
    if dice_roll == 6:
        update_balance(user_id, 2000)
        bot.reply_to(message, f"{dice_roll}, SMOOOOOTH, you win! +2000 Gank points!")
        log_action("Dice Win", user_id, "+2000 points")
    else:
        if get_balance(user_id) > 0:
            update_balance(user_id, -200)
            bot.reply_to(message, f"{dice_roll}, you lose! -200 Gank points.")
            log_action("Dice Loss", user_id, "-200 points")
        else:
            bot.reply_to(message, f"{dice_roll}, you lose! But you have no points to lose.")
            log_action("Dice Loss", user_id, "No points to lose")

# /flip_coin command
@bot.message_handler(commands=['flip_coin'])
def flip_coin(message):
    user_id = message.from_user.id
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    if not enforce_cooldown(user_id, 'flip_coin'):
        bot.reply_to(message, "Please wait before trying again!")
        return
    coin_flip = random.choice(['Heads', 'Tails'])
    if coin_flip == 'Heads':
        update_balance(user_id, 2500)
        bot.reply_to(message, "Heads, you win! +2500 Gank points!")
        log_action("Coin Win", user_id, "+2500 points")
    else:
        if get_balance(user_id) > 0:
            update_balance(user_id, -2500)
            bot.reply_to(message, "Tails, you lose! -2500 Gank points.")
            log_action("Coin Loss", user_id, "-2500 points")
        else:
            bot.reply_to(message, "Tails, you lose! But you have no points to lose.")
            log_action("Coin Loss", user_id, "No points to lose")

# /raffle command
raffle_participants = []

@bot.message_handler(commands=['raffle'])
def raffle(message):
    user_id = message.from_user.id
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    user_name = message.from_user.first_name
    
    if not enforce_cooldown(user_id, 'raffle'):
        bot.reply_to(message, "Please wait before trying again!")
        return

    if user_id in raffle_participants:
        bot.reply_to(message, "🐹 You're already in the raffle!")
    else:
        raffle_participants.append(user_id)
        bot.reply_to(message, f"🐹 {user_name}, you've entered the raffle! Good luck! 🎟")
        log_action("Entered Raffle", user_id)

    # Raffle triggers when 5 participants are reached
    if len(raffle_participants) >= 5:
        winner_id = random.choice(raffle_participants)
        winner_name = bot.get_chat(winner_id).first_name
        bot.send_message(message.chat.id, f"🎉 The winner is {winner_name}! +5000 Gank points!")
        update_balance(winner_id, 5000)
        raffle_participants.clear()
        log_action("Raffle Winner", winner_id, "Won 5000 points")

# /invite command
@bot.message_handler(commands=['invite'])
def invite(message):
    user_id = message.from_user.id
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    user_name = message.from_user.first_name
    
    if not enforce_cooldown(user_id, 'invite'):
        bot.reply_to(message, "Please wait before trying again!")
        return

    invite_link = f"https://t.me/+7upY1zsKXXs0NjZl?start={user_id}"
    invite_message = (
        f"🔥 {user_name}, share this link to invite friends: {invite_link}\n"
        "You’ll earn 8000 Gank points for every successful invite! 🎉"
    )
    bot.reply_to(message, invite_message)
    log_action("Invite", user_id)

# /leaderboard command
@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    if not check_group(message):
        bot.reply_to(message, "This bot only works in group chats.")
        return
    leaderboard = sorted(users.items(), key=lambda x: x[1], reverse=True)
    top_users = "\n".join([f"{bot.get_chat(user_id).first_name}: {balance} Gank points" for user_id, balance in leaderboard[:5]])
    bot.reply_to(message, f"🏆 Top Ganksters 🏆\n{top_users}")
    log_action("Checked Leaderboard", message.from_user.id)

# Start polling the bot
if __name__ == '__main__':
    print("Bot is starting...")  # Start message in terminal
    bot.polling()
  