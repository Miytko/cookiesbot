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
    msg = f"Total time spent in vc: {hours}h{total_minutes[interaction.user.name] % 60:02}m"
    await interaction.response.send_message(msg)


@bot.tree.command(name="vcleaderboard", description="Top 5 users by total time spent in vc")
async def vcleaderboard(interaction: discord.Interaction):
    total_minutes = vc_utils.process_log()
    sorted_hours = dict(sorted(total_minutes.items(), key=lambda item: item[1], reverse=True))

    msg = f"Top 5 unemployed:\n"

    index = 0
    for user, value in enumerate(sorted_hours.items()):
        if index < 5:
            hours = math.floor(value / 60)
            usermsg = f"{user} - {hours}h{value%60:02}m\n"
            msg += usermsg
        else:
            break
    
    await interaction.response.send_message(msg)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("syncd")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    print("Logged out!")
