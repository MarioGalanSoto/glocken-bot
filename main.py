import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

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
intents.voice_states = True
intents.guilds = True
intents.members = True  # Ensure that member intents are enabled to receive member join events

bot = commands.Bot(command_prefix="!", intents=intents)

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

bot.run(TOKEN)
