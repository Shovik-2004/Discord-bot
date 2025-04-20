import discord
import os
import requests
import json
import random
import time
from dotenv import load_dotenv
from replit import db  # Replit database
import sys
from monitoring import MESSAGES_RECEIVED, ABUSIVE_MESSAGES, COMMANDS_TRIGGERED, start_metrics_server
import logging


# List of abusive words to filter
abusive_words = {"sex", "fuck", "bitch", "fucker", "suicide", "bully", "fat", "fucked", "mother fucker", "bitch"}

# Function to check if a message contains abusive language
def is_abusive(text):
    words = set(text.lower().split())  # Convert text to lowercase and split into words
    return any(word in words for word in abusive_words)

# List of sad words for encouragement
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

if "responding" not in db.keys():
  db["responding"] = True

# Function to get an inspirational quote
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote
    except Exception:
        return "Stay strong! You're amazing! 😊"

# Function to update encouragements
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]

# Function to delete encouragement messages
def delete_encouragement(index):
    if "encouragements" in db.keys():
        encouragements = list(db["encouragements"])
        if 0 <= index < len(encouragements):
            del encouragements[index]
            db["encouragements"] = encouragements
            return "Encouragement deleted."
        else:
            return "Invalid index."
    return "No encouragements to delete."

# Backup happiness messages
happy_messages = [
    "Happiness depends upon ourselves. -Aristotle",
    "Smile, it's free therapy. -Douglas Horton",
    "Happiness is not something ready-made. It comes from your own actions. -Dalai Lama",
    "Do what makes your soul shine! 😊",
    "Every day is a new beginning, take a deep breath and start again!"
]

# Function to get a happiness-boosting message
def get_happy_message():
    url = "https://zenquotes.io/api/random"
    for _ in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            json_data = json.loads(response.text)
            return json_data[0]['q'] + " -" + json_data[0]['a']
        except requests.exceptions.RequestException:
            time.sleep(2)
    return random.choice(happy_messages)

# Load environment variables from .env file
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.message_content = True  

# Initialize bot client with intents
client = discord.Client(intents=intents)

# Bot login event
@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

# Message event listener
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    msg = message.content.lower()

    # Check for abusive language and delete the message if detected
    if is_abusive(msg):
        await message.delete()
        await message.channel.send(f"⚠️ {message.author.mention}, your message was removed due to inappropriate content.")
        return  # Stop further processing for this message

    # Greet the user
    if msg.startswith('$hello'):
        await message.channel.send('Hello! How can I help you today? 😊')

    # Send an inspirational quote
    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    # Respond with a happiness-boosting message if a sad word is detected
    if any(word in msg for word in sad_words):
        happy_message = get_happy_message()
        await message.channel.send(happy_message)

    # Respond to "thanks"
    if "thanks" in msg or "thank you" in msg:
        await message.channel.send("You're welcome! 😊")

    # Add a new encouragement message
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("✅ New encouraging message added!")

    # Delete an encouragement message
    if msg.startswith("$del"):
        try:
            index = int(msg.split("$del ", 1)[1])
            result = delete_encouragement(index)
            await message.channel.send(result)
        except ValueError:
            await message.channel.send("⚠️ Please provide a valid number.")

# Fetch bot token from environment variable
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Ensure token is set
if not TOKEN:
    raise ValueError("❌ No token found! Set DISCORD_BOT_TOKEN in the .env file.")

# Run the bot


# Run the bot only if NOT in a testing environment
if __name__ == "__main__" and "pytest" not in sys.modules:
    client.run(TOKEN)

