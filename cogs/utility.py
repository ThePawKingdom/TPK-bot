import asyncio
import platform
import time
import discord
import aiohttp
import re
import typing

import psutil as psutil
from settings import links, colors, emotes
from utils import times, default
from collections import Counter
from discord.ext import commands


class Utility(commands.Cog, name="Utility"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = '<:Discovery:845656527347777548>'  # Set the help menu emote.

    @commands.command()
    async def ping(self, ctx):
        """ See TPKBot's latency to discord """
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
        """ Information about TPKBot """
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
        users = sum(x.member_count for x in self.bot.guilds)

        e = discord.Embed(color=discord.Color.dark_teal())
        e.set_thumbnail(url=self.bot.user.avatar.url)
        e.title = f"{self.bot.user.name} information"
        e.description = f"""
__**General information**__
Developers:
- **[{joshua}](https://discord.com/users/{links.joshua})**

Library: [Enhanced-discord.py {discord.__version__}](https://github.com/iDevision/enhanced-discord.py)
Links: [support server]({links.support}) | [github]({links.github})

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
        """ Display information about this server """
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

    @commands.command(alias=["ui"])
    async def userinfo(self, ctx, user: typing.Union[discord.User, str] = None):
        """ Get info about users on discord """
        if user is None:
            user = ctx.author

        user = await default.find_user(ctx, user)

        if not user:
            return await ctx.reply(':warning: I could not find this user!')

        e = discord.Embed(color=colors.green)
        e.set_author(icon_url=user.avatar.url, name="About " + user.name)

        member = ctx.guild.get_member(user.id)

        if member:
            uroles = [role.mention for role in member.roles if not role.is_default()]
            uroles.reverse()
            if len(uroles) > 15:
                uroles = [f"{', '.join(uroles[:10])} (+{len(member.roles) - 11})"]
            user_roles = f' **({len(member.roles) - 1} Total)**' if uroles != [] else 'No roles'

            if times.discord_time_format(member.joined_at):
                join = times.discord_time_format(member.joined_at)
            else:
                join = 'Unknown'

            e.add_field(name="General Information:", value=f"""
{user.name}

**User ID:** {user.id}
**Created on** {times.discord_time_format(user.created_at)}


""",
                        inline=False)
            e.add_field(name="Server Information:", value=f"""
**Nickname:** {user.display_name}
**Joined At:** {join}
**Roles:** {', '.join(uroles) + user_roles}
""",
                        inline=False)
        else:
            e.add_field(name="General Information:", value=f"""
{user.name}

**User ID:** {user.id}
**Created on:** {times.discord_time_format(user.created_at)}
""",
                        inline=False)

            avatar = user.avatar or user.display_avatar
            if not avatar.is_animated():
                e.set_thumbnail(url=avatar.with_format('png').url)
            elif avatar.is_animated():
                e.set_thumbnail(url=avatar.with_format('gif').url)
            else:
                e.set_thumbnail(url=user.avatar.url if user.avatar else user.display_avatar.url)

        await ctx.send(embed=e)

    @commands.command()
    async def roleinfo(self, ctx, role: discord.Role):
        """ Get information about a role """
        position = len(ctx.guild.roles) - role.position
        permissions = dict(role.permissions)
        perms = []
        for perm in permissions.keys():
            if permissions[perm] is True and not role.permissions.administrator:
                perms.append(perm.lower().replace('_', ' ').title())

        if role.permissions.administrator:
            perms.append("Administrator")

        rolemembers = []

        if not role.members:
            rolemembers.append("None")

        for member in role.members:
            rolemembers.append(member.name)

        if len(rolemembers) > 10:
            rolemembers = [f"{', '.join(rolemembers[:10])} (+{len(role.members) - 11})"]

        e = discord.Embed(title="About " + role.name, color=role.color)
        e.add_field(name="General Information:", value=f"""
**Role name:** {role.name}
**Role ID:** {role.id}
**Role mention:** {role.mention}
""",
                    inline=False)
        e.add_field(name="Other Information:", value=f"""
**Is Integration:** {role.is_integration()}
**Hoisted:** {role.hoist}
**Position:** {position}
**Color:** {role.color}
**Created:** {times.discord_time_format(role.created_at)}
""",
                    inline=False)
        e.add_field(name="Permissions:", value=', '.join(perms), inline=False)
        e.add_field(name="Members:", value=', '.join(rolemembers), inline=False)

        await ctx.send(embed=e)

    @commands.command()
    async def privacy(self, ctx):
        """ Get the privacy policy for TPKbot """
        e = discord.Embed(description=f"You can check out our privacy policy [here](https://psychops.tk/legal.php#collected).", color=colors.green)
        await ctx.send(embed=e)

    @commands.command()
    async def avatar(self, ctx, *, user: discord.User = None):
        """ Show someone's avatar """
        if user is None:
            user = ctx.author

        embed = discord.Embed(color=colors.green)
        embed.set_author(name=f"{user}'s Profile Picture!",
                         icon_url=user.avatar.url if user.avatar else user.display_avatar.url)
        png = user.avatar.with_format('png').url if user.avatar else user.display_avatar.with_format('png').url
        jpg = user.avatar.with_format('jpg').url if user.avatar else user.display_avatar.with_format('jpg').url
        webp = user.avatar.with_format('webp').url if user.avatar else user.display_avatar.with_format('webp').url
        gif = user.avatar.with_format(
            'gif').url if user.avatar and user.avatar.is_animated() else user.display_avatar.with_format(
            'gif').url if user.display_avatar.is_animated() else None
        display = user.display_avatar.with_format(
            'gif').url if user.display_avatar.is_animated() else user.display_avatar.with_format('png').url
        embed.description = f"[png]({png}) | [jpg]({jpg}) | [webp]({webp}){f' | [gif]({gif})' if gif else ''}"
        embed.set_image(url=display)
        await ctx.send(embed=embed)

    # @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    # async def suggest(self, ctx, *, suggestion):
    #     """ Make a suggestion for BadWolf """
    #     channel = await self.bot.fetch_channel(907617618180075580)
    
    #     if len(suggestion) > 1000:
    #         return await ctx.send(":warning: Suggestions can not be more then 1000 characters.")

    #     embed = discord.Embed(color=colors.orange, title='New suggestion')
    #     embed.set_author(icon_url=ctx.author.avatar.url, name=ctx.author.name + f' ({ctx.author.id} ')
    #     embed.description = suggestion
    #     msg = await channel.send(embed=embed)
    #     await msg.add_reaction('👍')
    #     await msg.add_reaction('👎')
    #     await self.bot.database.execute("INSERT INTO suggestions(suggestion, user_id, msg_id) VALUES($1, $2, $3)", suggestion, ctx.author.id, msg.id)

    #     e = discord.Embed(color=colors.orange)
    #     e.description = f'Your suggestion has been sent to [our support server]({links.support})'
    #     await ctx.send(embed=e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def announce(self, ctx, channel: discord.TextChannel, *, desc):
        """ Announce something """
        if not channel:
            return await ctx.send('Please provide a channel to use.')
        if len(desc) > 2000:
            return await ctx.send('Please make your announcement shorter then 2000 characters.')
        if len(desc) < 2000:
            e = discord.Embed(color=discord.Color.dark_teal())
            e.description = "Do you want the message embedded?"

            def check(r, u):
                return u.id == ctx.author.id and r.message.id == checkmsg.id

            try:
                checkmsg = await ctx.send(embed=e)
                await checkmsg.add_reaction(emotes.checkmark)
                await checkmsg.add_reaction(emotes.crossmark)
                react, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)

                if str(react) == emotes.checkmark:
                    try:
                        await checkmsg.clear_reactions()
                    except Exception:
                        pass
                    e = discord.Embed(color=discord.Color.random(), description=desc)
                    await channel.send(embed=e)

                    embed = discord.Embed(color=discord.Color.green(), description=f"Sent embedded announcement in **{channel}**.")
                    await checkmsg.edit(embed=embed)
                    return

                if str(react) == emotes.crossmark:
                    try:
                        await checkmsg.clear_reactions()
                    except Exception:
                        pass
                    await channel.send(desc)

                    embed2 = discord.Embed(color=discord.Color.green(), description=f"Sent plain announcement in **{channel}**.")
                    await checkmsg.edit(embed=embed2)
                    return

            except asyncio.TimeoutError:
                try:
                    await checkmsg.clear_reactions()
                except Exception:
                    pass
                etimeout = discord.Embed(color=discord.Color.dark_red(), description="Command timed out, canceling...")
                return await checkmsg.edit(embed=etimeout)

def setup(bot):
    bot.add_cog(Utility(bot))
