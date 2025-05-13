from discord.ext import commands
import discord
import datetime
import os
from pathlib import Path


MAIN_PATH = Path(__file__).resolve().parent.parent.parent
DB_FILE = os.path.join(MAIN_PATH, "db/log.txt")


class VoiceTracker(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
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
        with open(DB_FILE, "a") as f:
            f.write(log_msg)


async def setup(bot):
    await bot.add_cog(VoiceTracker(bot))
