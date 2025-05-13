from discord_token import DISCORD_TOKEN
from discord.ext import commands
import discord


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


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
    print("Logged out!")
