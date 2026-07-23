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


def format_time_msg(minutes):
    return f"{math.floor(minutes/60)}h {minutes%60:02}m"


@bot.tree.command(name="vcleaderboard", description="Top 5 users by total time spent in vc")
async def vcleaderboard(interaction: discord.Interaction):
    total_minutes = vc_utils.process_log()
    sorted_hours = sorted(total_minutes.items(), key=lambda item: item[1], reverse=True)

    msg = f"Top 5 unemployed:\n"

    invoker_name = interaction.user.name
    invoker_rank = None
    invoker_minutes = total_minutes.get(invoker_name)


    for index, (user, minutes) in enumerate(sorted_hours):
        rank = index + 1

        if user == invoker_name:
            invoker_rank = rank

        if index < 5:
            msg += f"{rank}. {user} - {format_time_msg(minutes)}\n"


    if invoker_rank is not None and invoker_rank > 5:
        msg += f"...{invoker_rank}. {invoker_name} - {format_time_msg(invoker_minutes)}\n"

    
    await interaction.response.send_message(msg)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    print("syncd")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    print("Logged out!")
