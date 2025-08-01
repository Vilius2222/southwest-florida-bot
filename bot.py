import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Your server (guild) ID
GUILD_ID = 1400050793037566096

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@tree.command(name="startup", description="Start session with reactions (1–5)")
@app_commands.describe(slot="Choose a slot number from 1 to 5")
async def startup(interaction: discord.Interaction, slot: int):
    if not (1 <= slot <= 5):
        await interaction.response.send_message("❌ Please provide a slot number between 1 and 5.", ephemeral=True)
        return

    embed = discord.Embed(
        title="SFF | Server Startup",
        description=(
            f"<@&1400414055113424907>\n"
            f"{interaction.user.mention} has started a session!\n\n"
            "**To begin, this session requires 5 ✅ reactions.**\n"
            "Get ready to have fun!"
        ),
        color=discord.Color.blurple()
    )
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1400062111824220200/1400480581665427466/e331ec21-dfc6-4d1a-a76b-ee781183ce32.jpg")
    embed.set_footer(text="Southwest Florida Federation")

    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")

    try:
        await msg.edit(allowed_mentions=discord.AllowedMentions.none())
    except Exception:
        pass


@tree.command(name="ea", description="Share Early Access link with embed and role tags")
@app_commands.describe(link="Paste the EA session link")
async def ea(interaction: discord.Interaction, link: str):
    embed = discord.Embed(
        title="🚦 Early Access Session Started!",
        description="You may now join the session by clicking the link below:",
        color=discord.Color.green()
    )
    embed.add_field(name="🔗 Link", value=link, inline=False)
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/1400062111824220200/1400765179309854832/e9dee22e-dc46-4e31-944c-373e4c9da1f7.jpg")
    embed.set_footer(text="Southwest Florida Federation • EA")

    role_mentions = "<@&1400414401760067594> <@&1400424755546292325> <@&1400425039114928128>"
    await interaction.response.send_message(content=role_mentions, embed=embed)


@tree.command(name="release", description="Release info: pt, status, frp, drift")
@app_commands.describe(link="Paste the release link")
async def release(interaction: discord.Interaction, link: str):
    await interaction.response.send_message(
        f"""📤 **Release Details**:
**Link:** {link}
**PT:** on/off  
**Status:** ...  
**FRP:** 75 or 80  
**Drift:** Corners or Fully on"""
    )


@tree.command(name="reinvites", description="Send reinvite link")
@app_commands.describe(link="Paste the reinvite link")
async def reinvites(interaction: discord.Interaction, link: str):
    await interaction.response.send_message(f"🔁 Reinvite Link: {link}")


@tree.command(name="over", description="End session & provide minutes")
@app_commands.describe(minutes="Enter the number of minutes")
async def over(interaction: discord.Interaction, minutes: int):
    await interaction.response.send_message(f"✅ Session ended. Total time: **{minutes} minutes**.")


@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced_global = await tree.sync()
        print(f"🌍 Globally synced {len(synced_global)} commands.")
    except Exception as e:
        print(f"⚠️ Global sync failed: {e}")

    try:
        guild = discord.Object(id=GUILD_ID)
        synced_guild = await tree.sync(guild=guild)
        print(f"🏠 Synced {len(synced_guild)} commands to guild {GUILD_ID}")
    except Exception as e:
        print(f"⚠️ Guild sync failed: {e}")

bot.run(TOKEN)
