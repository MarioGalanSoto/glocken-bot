#main.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import re
import random
#add jokes api : https://v2.jokeapi.dev/joke/Miscellaneous,Dark,Pun
# Load .env file
load_dotenv()

# Check for required environment variables and raise an error if missing
required_vars = ['DISCORD_TOKEN']
missing_vars = [var for var in required_vars if os.getenv(var) is None]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Get the token from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent to listen to messages
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix=">", intents=intents)
# Initialize bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("discord bot is running...")

# Event to greet new members when they join the server
@bot.event
async def on_member_join(member):
    greetings = [
        f"Welcome to the server, {member.mention}! We're glad to have you here.",
        f"Hey {member.mention}, welcome aboard! Make yourself at home.",
        f"{member.mention} just joined us! Welcome to the community.",
        f"Hello {member.mention}! We're excited to see you here.",
        f"What's up, {member.mention}? Welcome to the server!",
        f"Hi {member.mention}, welcome! We hope you enjoy your stay.",
        f"{member.mention}, welcome to our server!",
        f"Great to have you with us, {member.mention}! Welcome!",
        f"Welcome, {member.mention}! We're so happy you could join us.",
        f"Hey {member.mention}, welcome! We're looking forward to getting to know you.",
        f"We hope you brought pizza {member.mention}."
    ]

    # Create an embed for a styled welcome message
    embed = discord.Embed(
        title=f"Welcome to the server, {member.name}",
        description=random.choice(greetings)+ "  🎉\n\nIf you have any questions, don't hesitate to ask. Enjoy your stay! 🌟",
        color=discord.Color.blue()  # You can choose any color you like
    )

    # Add the member's avatar as a thumbnail (medium-sized profile picture)
    embed.set_thumbnail(url=member.avatar.url)

    # Add the name and discriminator (e.g., User#1234)
    # embed.add_field(name="Member", value=f"{member.name}#{member.discriminator}", inline=True)
    # Find the welcome channel
    channel = discord.utils.get(member.guild.text_channels, name='welcome-channel')  # Adjust channel name as needed

    if channel:
        await channel.send(embed=embed)
@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == bot.user:
        return

    # Check if the message starts with ">timer"
    if message.content.startswith(">timer"):
        # Remove the command prefix ">timer" and strip any leading/trailing whitespace
        command_content = message.content[len(">timer"):].strip()

        # Check if the remaining content matches the expected timer format (e.g., "30s break!")
        pattern = re.compile(r'(?P<time>\d+[smhd])\s+(?P<reminder>.+)')
        match = pattern.match(command_content)

        if match:
            time_str = match.group('time')
            reminder = match.group('reminder')

            time_seconds = convert_time_to_seconds(time_str)

            if time_seconds is not None:
                # Confirm the timer has been set
                await message.channel.send(f"Timer set for {time_str}. I'll remind you when it's time!")

                # Wait for the specified duration
                await asyncio.sleep(time_seconds)

                # Send the reminder mentioning the user
                await message.channel.send(f"{message.author.mention}, {reminder}")
            else:
                await message.channel.send("I couldn't understand the time format. Please use something like `1m`, `5m`, `2h`, etc.")
        else:
            await message.channel.send("Please use the correct format: `>timer <time> <reminder>`.")

    # Process other commands if any
    await bot.process_commands(message)

def convert_time_to_seconds(time_str):
    pattern = re.compile(r'(?P<value>\d+)(?P<unit>[smhd])')
    matches = pattern.findall(time_str)

    if not matches:
        return None

    total_seconds = 0
    for value, unit in matches:
        value = int(value)
        if unit == 's':  # seconds
            total_seconds += value
        elif unit == 'm':  # minutes
            total_seconds += value * 60
        elif unit == 'h':  # hours
            total_seconds += value * 3600
        elif unit == 'd':  # days
            total_seconds += value * 86400

    return total_seconds

bot.run(TOKEN)
