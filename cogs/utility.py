import time
import aiohttp

from discord.ext import commands


class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = '<:Discovery:845656527347777548>'  # Set the help menu emote.

    @commands.command()
    async def ping(self, ctx):
        """
        See BadWolf's latency to discord
        """
        discord_start = time.monotonic()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com') as r:
                if r.status == 200:
                    discord_end = time.monotonic()
                    discord_ms = f"{round((discord_end - discord_start) * 1000)}ms"
                else:
                    discord_ms = "fucking dead"
                await ctx.send(f"\U0001f3d3 Pong   |   {discord_ms}")


def setup(bot):
    bot.add_cog(Utility(bot))
