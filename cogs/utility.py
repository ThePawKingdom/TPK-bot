import platform
import time
import discord
import aiohttp
import re
import typing

import psutil as psutil
from settings import links, colors
from utils import times, default
from collections import Counter
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
                    discord_ms = f"**{round((discord_end - discord_start) * 1000)}**ms"
                else:
                    discord_ms = "fucking dead"
                await ctx.send(f"<a:loading:908629364378325023> Ping | {discord_ms}")

    @commands.command(alias=["botinfo"])
    async def about(self, ctx):
        """
        Information about BadWolf
        """
        chtypes = Counter(type(c) for c in self.bot.get_all_channels())
        voice = chtypes[discord.channel.VoiceChannel]
        text = chtypes[discord.channel.TextChannel]
        cpup = psutil.cpu_percent()
        core = psutil.cpu_count()
        mem = psutil.virtual_memory().total >> 20
        mem_usage = psutil.virtual_memory().used >> 20
        storage_free = psutil.disk_usage('/').free >> 30
        storage = psutil.disk_usage('/').total >> 30
        boottime = psutil.boot_time()
        joshua = await self.bot.fetch_user(links.joshua)
        etile = await self.bot.fetch_user(links.etile)
        users = sum(x.member_count for x in self.bot.guilds)

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_thumbnail(url=self.bot.user.avatar.url)
        e.title = f"{self.bot.user.name} information"
        e.description = f"""
__**General information**__
Developers:
- **[{etile}](https://discord.com/users/{links.etile})**
- **[{joshua}](https://discord.com/users/{links.joshua})**

Library: [Enhanced-discord.py {discord.__version__}](https://github.com/iDevision/enhanced-discord.py)
Links: [support server]({links.support}) | [Invite me]({links.invite}) | [github]({links.github})

__**System**__
System Software: `{platform.system()} {platform.release()}`
CPU Usage: `{cpup}`%
RAM: `{mem_usage}`/`{mem}` MB
Storage `{storage_free}` / `{storage}` GB
Cores: `{core}`
Boot time: <t:{re.sub(".[0-9]$", '', f'{boottime}')}:R>

__**Statistics**__
`{len(self.bot.guilds)}` guilds
`{users}` bot users
`{len([c for c in set(self.bot.walk_commands())])}` commands
`{voice:,}` voice channels
`{text:,}` text channels
"""
        await ctx.send(embed=e)

    @commands.command(alias=["si"])
    async def serverinfo(self, ctx):
        """
        Display information about this server
        """
        human = sum(not member.bot for member in ctx.guild.members)
        bots = sum(member.bot for member in ctx.guild.members)
        features = ", ".join(ctx.guild.features).lower().replace('_', ' ').title() if len(ctx.guild.features) != 0 else None
        verification = str(ctx.guild.verification_level).capitalize()
        nitromsg = f"This server has **{ctx.guild.premium_subscription_count}** boosts"
        nitromsg += f"\n{default.next_level(ctx)}"
        num = sum(1 for user in ctx.guild.members if (ctx.channel.permissions_for(user).kick_members or ctx.channel.permissions_for(user).ban_members) and not user.bot)
        bans = ''
        if ctx.channel.permissions_for(ctx.guild.me).ban_members:
            bans += f"**Banned:** {len(await ctx.guild.bans()):,}"

        e = discord.Embed(color=colors.green)
        e.set_author(icon_url=ctx.guild.icon.url if ctx.guild.icon else self.bot.user.display_avatar.url, name="About " + ctx.guild.name)
        e.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else self.bot.user.display_avatar.url)
        e.add_field(
            name="General Information:",
            value=f"""
**Name:** {ctx.guild.name}
**ID:** {ctx.guild.id}
**Created on** {times.discord_time_format(ctx.guild.created_at)}
**Verification level:** {verification}

**Owner:** {ctx.guild.owner}
**Owner ID:** {ctx.guild.owner.id}

**Nitro status:** 
{nitromsg}
""",
            inline=True)

        e.add_field(
            name="Other Information:",
            value=f"""
**Members:** {ctx.guild.member_count:,}
**Humans:** {human} | **Bots:** {bots}
**Staff:** {num}
{bans}
""",
            inline=True)
        e.add_field(name="Features:", value=features, inline=False)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Utility(bot))
