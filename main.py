from discord_token import DISCORD_TOKEN
from discord.ext import commands
import discord
import datetime


class CookieBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


intents = discord.Intents.default()
intents.message_content = True
bot = CookieBot(command_prefix="!", intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send("hi")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    message = f"Something else happened. Error? member: {member}, before: {before}, after: {after}"
    timestamp = datetime.datetime.now()
    time_txt = timestamp.strftime("[%Y-%m-%d %H:%M:%S] ")
    if before.channel is None and after.channel is not None:
        message = f"{member} has joined {after.channel} ({after.channel.guild})"
    if before.channel is not None and after.channel is None:
        message = f"{member} has left {before.channel} ({before.channel.guild})"
    if before.channel is not None and after.channel is not None:
        message = f"{member} has switched from {before.channel} ({before.channel.guild}) " \
                  f"to {after.channel} ({after.channel.guild})"
    log_msg = time_txt + message + "\n"
    with open("db/log.txt", "a") as f:
        f.write(log_msg)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    print("Logged out!")