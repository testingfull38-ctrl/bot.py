from flask import Flask
import telebot
from sympy import sympify, symbols, solve, SympifyError
import time
import threading

# Initialize Flask app (required for Replit Web template)
app = Flask(__name__)

# Your Telegram bot token and channel ID
TOKEN = '8482581885:AAFcl4wGWC8E_-LlUh5yzB8Bpn1op1rXZT0'
CHANNEL_ID = '-1002978355160'

# Initialize bot
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "Bot is running!", 200

@bot.message_handler(commands=['start', 'help'])
def start(message):
    response = "Hi! I'm your math solver bot 🤖\nSend me an expression like '2 + 3 * sin(pi/2)' to evaluate 🔢\nOr 'solve x**2 - 4 = 0' to solve equations ✅"
    bot.reply_to(message, response)
    log_message = f"User @{message.from_user.username} (ID: {message.from_user.id}) started the bot 🚀\nBot replied: {response}"
    bot.send_message(CHANNEL_ID, log_message)

@bot.message_handler(func=lambda message: True)
def handle_math(message):
    user_input = message.text.strip()
    try:
        if user_input.lower().startswith('solve'):
            eq_str = user_input[5:].strip()
            x = symbols('x')
            eq = sympify(eq_str.replace('=', '-(') + ')')
            solution = solve(eq, x)
            response = f"Solution: {solution} ✅"
        else:
            expr = sympify(user_input)
            result = expr.evalf()
            response = f"Result: {result} 🔢"
        
        bot.reply_to(message, response)
        log_message = f"User @{message.from_user.username} (ID: {message.from_user.id}) sent: {user_input} 📩\nBot replied: {response}"
        bot.send_message(CHANNEL_ID, log_message)
    
    except SympifyError:
        error_response = "Invalid expression! Try again ❌ (e.g., use ** for power, sin() for sine)"
        bot.reply_to(message, error_response)
        log_message = f"User @{message.from_user.username} (ID: {message.from_user.id}) sent invalid: {user_input} ⚠️\nBot replied: {error_response}"
        bot.send_message(CHANNEL_ID, log_message)
    except Exception as e:
        error_response = f"Error: {str(e)} ❌"
        bot.reply_to(message, error_response)
        log_message = f"User @{message.from_user.username} (ID: {message.from_user.id}) caused error: {user_input} 🚨\nError: {str(e)}\nBot replied: {error_response}"
        bot.send_message(CHANNEL_ID, log_message)

def run_bot():
    bot.polling(none_stop=True)

def keep_alive():
    while True:
        print("Bot is alive! 🕒")  # Keeps Replit active
        time.sleep(600)  # Ping every 10 minutes

# Start bot and keep-alive in threads
threading.Thread(target=run_bot, daemon=True).start()
threading.Thread(target=keep_alive, daemon=True).start()

# Run Flask app (required by Replit)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
