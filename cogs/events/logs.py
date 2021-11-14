import discord
from discord.ext import commands
from datetime import datetime
from utils import default
from settings import links, colors, emotes

class Logs(commands.Cog, name="Logs"):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if ctx.author.id == 843866750131109909:  # bluewy
            return True  # even if gets blacklisted can't be blocked from the bot

        try:
            blacklist_check = self.bot.blacklist[ctx.author.id]
            if blacklist_check:
                return False  # they're blacklisted.
        except Exception:
            return True

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.guild:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} - {ctx.guild.name} | {ctx.author} > {ctx.message.clean_content}")
        else:
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} - Direct Messages | {ctx.author} > {ctx.message.clean_content}")


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        results = await self.bot.database.fetchval(f"SELECT * FROM blacklist WHERE id = $1", guild.id)

        log = self.bot.get_channel(links.guildlog)
        if not results:
            owner = await self.bot.fetch_user(guild.owner_id)
            owner = str(owner)

            l = discord.Embed(color=colors.green, title="New guild joined")
            l.set_author(name=guild, icon_url=guild.icon.url)
            l.set_footer(text=f"Now in {len(self.bot.guilds)} guilds")
            l.description = f"""
Guild **{guild}** ({guild.id})
Owner: **{owner}** ({guild.owner_id})
Created on **{default.date(guild.created_at)}**
Approximately **{guild.member_count}** members
**{len(guild.text_channels)}** text & **{len(guild.voice_channels)}** voice channels
Icon url: **[Click here]({guild.icon.url})** 
"""

            return await log.send(guild.id, embed=l)

        else:
            print(f"{guild} ({guild.id} tried adding me, but was blacklisted.")
            await log.send(f"{emotes.crossmark} {guild.name} ({guild.id}) tried adding me, but this guild is blacklisted.")
            return await guild.leave()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        log = self.bot.get_channel(links.guildlog)
        owner = await self.bot.fetch_user(guild.owner_id)
        owner = str(owner)
        results = await self.bot.database.fetchval(f"SELECT * FROM blacklist WHERE id = $1", guild.id)

        if not results:
            l = discord.Embed(color=colors.orange, title="Old guild left")
        elif results:
            l = discord.Embed(color=colors.red, title="Blacklisted guild left")
        l.set_author(name=guild, icon_url=guild.icon.url)
        l.set_footer(text=f"Now in {len(self.bot.guilds)} guilds")
        l.description = f"""
        Guild **{guild}** ({guild.id})
        Owner: **{owner}** ({guild.owner_id})
        Created on **{default.date(guild.created_at)}**
        Approximately **{guild.member_count}** members
        **{len(guild.text_channels)}** text & **{len(guild.voice_channels)}** voice channels
        Icon url: **[Click here]({guild.icon.url})** 
        """

        await log.send(embed=l)

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