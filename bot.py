import discord
from discord.ext import commands, tasks
import os
from datetime import datetime

TOKEN = os.getenv("TOKEN")

PROMPT_CHANNEL_ID = 1520819535836352603
BOT_DATA_CHANNEL_ID = 1521158662402347018

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

prompts = [
"Draw an abandoned lighthouse covered in vines.",
"Draw a floating island held up by giant roots.",
"Draw a cat wearing a space helmet exploring Mars.",
"Draw a forest where the trees glow at night.",
"Draw a knight resting under a giant mushroom.",
"Draw a cozy cabin during a heavy rainstorm.",
"Draw a whale swimming through the clouds.",
"Draw a robot gardener taking care of flowers.",
"Draw a hidden village inside a hollow mountain.",
"Draw a library where books float in the air.",
"Draw a fox made entirely of stars.",
"Draw a train traveling through the sky.",
"Draw a magical-looking (but non-magical) glowing door in a forest.",
"Draw a sleepy dragon curled around a campfire.",
"Draw a city built on the back of a giant turtle.",
"Draw a lantern festival at night.",
"Draw a jellyfish floating through space.",
"Draw a deer with glowing antlers in the dark woods.",
"Draw a floating bakery in the clouds.",
"Draw a small house inside a giant tree stump.",
"Draw a storm forming inside a glass bottle.",
"Draw a penguin explorer in icy ruins.",
"Draw a garden growing on an old piano.",
"Draw a castle made of ice in the ocean.",
"Draw a traveler meeting a friendly spirit of nature (symbolic).",
"Draw a bridge between two floating islands.",
"Draw a cat sleeping on top of a stack of books.",
"Draw a forest filled with glowing fireflies.",
"Draw a dragon protecting a small village.",
"Draw a mysterious doorway in an alleyway.",
"Draw a giant snail carrying a tiny village.",
"Draw a moon reflected in a still lake.",
"Draw a warrior resting after a long journey.",
"Draw a waterfall flowing into the sky.",
"Draw a fox hiding inside a pumpkin-shaped house.",
"Draw a space station orbiting a giant flower.",
"Draw a peaceful forest in winter.",
"Draw a crow delivering letters across a village.",
"Draw a tree growing through an old ruin.",
"Draw a fish flying through the air.",
"Draw a clock tower in the middle of the ocean.",
"Draw a sleepy village at sunrise.",
"Draw a dragon reading a book.",
"Draw a child building a sandcastle that becomes huge.",
"Draw a hidden cave filled with glowing crystals.",
"Draw a floating marketplace in the sky.",
"Draw a rabbit wearing an adventurers backpack.",
"Draw a mountain with a glowing heart-shaped cave.",
"Draw a star falling into a lake.",
"Draw a knight made of shadows (silhouette design).",
"Draw a forest where everything is upside down.",
"Draw a cat chasing glowing butterflies.",
"Draw a village inside a giant snow globe.",
"Draw a river flowing through the sky.",
"Draw a traveler with a floating mechanical staff.",
"Draw a city made of paper structures.",
"Draw a fox sitting on a crescent moon.",
"Draw a giant book opening into a world of cities.",
"Draw a castle surrounded by thick fog.",
"Draw a dragon sleeping under cherry blossoms.",
"Draw a glowing cave under the ocean.",
"Draw a robot exploring an ancient temple.",
"Draw a lighthouse guiding ships through storm clouds.",
"Draw a tree that grows glowing seeds.",
"Draw a small island with one lighthouse.",
"Draw a cat walking through a dreamlike landscape.",
"Draw a traveler crossing a glowing desert.",
"Draw a forest that is always autumn.",
"Draw a dragon made of flowing water.",
"Draw a city inside a giant snowflake.",
"Draw a mysterious key floating above a table.",
"Draw a bookstore at midnight.",
"Draw a fox running through glowing grass.",
"Draw a bridge made of vines over a river.",
"Draw a painter creating a world on a giant canvas.",
"Draw a hidden kingdom under the sea.",
"Draw a mountain floating above clouds.",
"Draw a glowing sword stuck in stone.",
"Draw a village protected by giant wolves.",
"Draw a starry sky reflected in black ink water.",
"Draw a robot learning to paint a landscape.",
"Draw a cat sitting in a sunflower field.",
"Draw a dragon guarding a crystal cave.",
"Draw a floating train station in the sky.",
"Draw a forest that is always night.",
"Draw a lantern floating into space.",
"Draw a tiny house inside a snowflake.",
"Draw a glowing river at night.",
"Draw a city built inside a giant tree.",
"Draw a fox wearing a crown in an old ruined kingdom.",
"Draw a portal shaped like a mirror to another world.",
"Draw a traveler meeting their future self in peace.",
"Draw a floating island shaped like a whale.",
"Draw a dragon sleeping in a volcano.",
"Draw a castle hidden inside clouds.",
"Draw a world inside a glass orb.",
"Draw a cat watching stars fall.",
"Draw a forest that changes seasons in one day."
]


# ---------------- STATE (DISCORD STORAGE) ----------------

async def get_state():
    channel = await bot.fetch_channel(BOT_DATA_CHANNEL_ID)
    messages = [m async for m in channel.history(limit=1)]

    if not messages:
        msg = await channel.send("0|none")
        return 0, "none", msg

    msg = messages[0]

    try:
        index, last_date = msg.content.split("|")
        return int(index), last_date, msg
    except:
        await msg.edit(content="0|none")
        return 0, "none", msg


async def save_state(index, date_str, msg):
    await msg.edit(content=f"{index}|{date_str}")


# ---------------- DAILY POST ----------------

@tasks.loop(minutes=1)
async def daily_prompt():
    channel = await bot.fetch_channel(PROMPT_CHANNEL_ID)

    index, last_date, msg = await get_state()

    today = datetime.now().strftime("%Y-%m-%d")

    # ONLY ONE POST PER DAY
    if last_date == today:
        return

    if index >= len(prompts):
        return

    await channel.send(
        f"🎨 Daily Drawing Prompt\n\n{prompts[index]}"
    )

    index += 1
    await save_state(index, today, msg)


# ---------------- COMMAND ----------------

@bot.command()
async def prompt(ctx):
    index, _, _ = await get_state()

    if index >= len(prompts):
        await ctx.send("You've completed every prompt! 🎉")
        return

    await ctx.send(f"🎨 Current Prompt\n\n{prompts[index]}")


# ---------------- START ----------------

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    if not daily_prompt.is_running():
        daily_prompt.start()


bot.run(TOKEN)
