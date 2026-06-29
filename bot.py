import discord
from discord.ext import commands, tasks
import os
import json
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1520819535836352603

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

DAY_FILE = "day.json"

prompts = [
    # (your full list stays EXACTLY the same here)
]

def load_day():
    if os.path.exists(DAY_FILE):
        with open(DAY_FILE, "r") as f:
            return json.load(f)["day"]
    return 0

def save_day(day):
    with open(DAY_FILE, "w") as f:
        json.dump({"day": day}, f)

current_day = load_day()


# 🟢 DAILY AUTO POST
@tasks.loop(minutes=1)
async def daily_prompt():
    global current_day

    now = datetime.now()

    if now.hour == 0 and now.minute == 0:
        channel = await bot.fetch_channel(CHANNEL_ID)

        if channel and current_day < len(prompts):
            await channel.send(
                f"🎨 Daily Drawing Prompt (Day {current_day + 1}):\n\n"
                + prompts[current_day]
            )

            current_day += 1
            save_day(current_day)


# 🟢 SLASH COMMAND (simple version = prefix command)
@bot.command()
async def prompt(ctx):
    day = load_day()

    if day < len(prompts):
        await ctx.send(
            f"🎨 Today’s Prompt (Day {day + 1}):\n\n"
            + prompts[day]
        )
    else:
        await ctx.send("All prompts are completed 🎉")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    daily_prompt.start()


bot.run(TOKEN)
