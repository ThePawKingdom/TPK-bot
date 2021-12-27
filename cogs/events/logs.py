import discord
from discord.ext import commands
from datetime import datetime
from utils import default
from settings import links, colors, emotes

class Logs(commands.Cog, name="Logs"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} - {ctx.guild.name} | {ctx.author} > {ctx.message.clean_content}")
        else:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} - Direct Messages | {ctx.author} > {ctx.message.clean_content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """ Tries to re-run a command when a message gets edited! """
        if after.author.bot or before.content == after.content:
            return
        prefixes = commands.when_mentioned_or('>>')(self.bot, after)
        if after.content.startswith(tuple(prefixes)):
            ctx = await self.bot.get_context(after)
            msg = await self.bot.invoke(ctx)

def setup(bot):
    bot.add_cog(Logs(bot))
