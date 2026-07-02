from discord.ext import commands
import discord
import datetime
import os
import csv
from pathlib import Path


MAIN_PATH = Path(__file__).resolve().parent.parent.parent
DB_FILE = os.path.join(MAIN_PATH, "db/vc_activity.csv")


class VoiceTracker(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        # message = f"Something else happened. Error? member: {member}, before: {before}, after: {after}"
        timestamp = datetime.datetime.now()
        time_txt = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        fields = ["date", "user", "action",
                "previous_server", "previous_channel",
                "current_server", "current_channel"]


        user = member
        action = ""
        previous_server = ""
        previous_channel = ""
        current_server = ""
        current_channel = ""

        if before.channel is None and after.channel is not None:
            action = "join"
            current_server = after.channel.guild
            current_channel = after.channel
            # message = f"{member} has joined {after.channel} ({after.channel.guild})"

        if before.channel is not None and after.channel is None:
            action = "leave"
            previous_server = before.channel.guild
            previous_channel = before.channel
            # message = f"{member} has left {before.channel} ({before.channel.guild})"

        if before.channel is not None and after.channel is not None:
            action = "switch"
            current_server = after.channel.guild
            current_channel = after.channel
            previous_server = before.channel.guild
            previous_channel = before.channel
            # message = f"{member} has switched from {before.channel} ({before.channel.guild}) " \
            #         f"to {after.channel} ({after.channel.guild})"

        data = [
            [time_txt, user, action,
            previous_server, previous_channel,
            current_server, current_channel]
        ]
            
        with open(DB_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)


async def setup(bot):
    await bot.add_cog(VoiceTracker(bot))
