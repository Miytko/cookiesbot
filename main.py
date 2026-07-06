from discord_token import DISCORD_TOKEN
from discord.ext import commands
import discord
import vc_utils
import math

EXTENSIONS = ["cogs.tests.vc_track"]


class CookieBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        for extension in EXTENSIONS:
            await self.load_extension(extension)


intents = discord.Intents.default()
intents.message_content = True
bot = CookieBot(command_prefix="!", intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send("hi")


@bot.tree.command(name="vctime", description="See how much time you've spent in vc")
async def vctime(interaction: discord.Interaction):
    total_minutes = vc_utils.process_log()
    hours = math.floor(total_minutes[interaction.user.name] / 60)
    msg = f"Total time spent in vc: {hours}h{total_minutes[interaction.user.name] % 60:02}"
    await interaction.response.send_message(msg)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("syncd")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    print("Logged out!")
