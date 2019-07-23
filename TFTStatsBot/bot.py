from discord.ext import commands
import asyncio
import discord

COGS = ["cogs.champions", "cogs.classes"]

async def run():
    bot = TFTStatsBot()

    try:
        await bot.start("TOKEN")
    except KeyboardInterrupt:
        await bot.logout()
        print("Connection closed!")


class TFTStatsBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="tb.",
            description="StatsBot for TeamFight Tactics"
        )

        for ext in COGS:
            try:
                self.load_extension(ext)
            except Exception as e:
                print(f"Cant load {ext}")
                raise e

    async def on_ready(self):
        print(f"Logged in as {self.user.name}")
        print(discord.utils.oauth_url(self.user.id))
      

loop = asyncio.get_event_loop()
loop.run_until_complete(run()) 