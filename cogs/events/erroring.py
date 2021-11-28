import asyncio
import discord
import traceback
from datetime import datetime
from utils import checks
from settings import emotes, links, colors
from discord.ext import commands


class Erroring(commands.Cog, name="Erroring"):
    def __init__(self, bot):
        self.bot = bot

    async def bot_check(self, ctx):
        if await checks.lockdown(ctx):
            return False
        return True

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound):
            return

        if isinstance(err, commands.MissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.send(f"{emotes.crossmark} **You are missing permissions - `{perms}`**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.BotMissingPermissions):
            perms = "`" + '`, `'.join(err.missing_permissions) + "`"
            return await ctx.send(f"{emotes.crossmark} **I am missing permissions - `{perms}`**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.MissingRequiredArgument):
            return await ctx.send(f"{emotes.crossmark} **You are missing required arguments - `{err.param.name}`**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.CommandOnCooldown):
            await ctx.send(f":warning: **{ctx.command.qualified_name} is on cooldown for {err.retry_after:.0f} seconds.**", delete_after=5, ephemeral=True)
            logchannel = self.bot.get_channel(links.errors)
            print(f"{datetime.now().__format__('%a %d %b %y, %H:%M')} [COOLDOWN] - {ctx.author} experienced {err.retry_after:.0f} seconds of cooldown.")
            return await logchannel.send(f":warning: **{ctx.author} ({ctx.author.id}) had a {err.retry_after:.0f} second cooldown at {datetime.now().__format__('%a %d %b %y, %H:%M')}.**")

        if isinstance(err, commands.NotOwner):
            return await ctx.send(f"**{emotes.crossmark} Only BadWolf team members can use this command.**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.UserNotFound):
            return await ctx.send(f"**:warning: I could not find the specified user - {err.argument}**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.MemberNotFound):
            return await ctx.send(f"**:warning: I could not find the specified member - {err.argument}**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.ChannelNotFound):
            return await ctx.send(f"**:warning: I could not find the specified channel - {err.argument}**", delete_after=5, ephemeral=True)

        if isinstance(err, commands.NoPrivateMessage):
            return await ctx.send(f"**{emotes.crossmark} This command can only be used in guilds.**", delete_after=5, ephemeral=True)

        else:
            elog = self.bot.get_channel(links.errors)
            le = discord.Embed(color=colors.red)
            le.description = f"\n```py\n{''.join(traceback.format_exception(type(err), err, err.__traceback__))}\n```"
            le.add_field(name="__**Additional information**__",
                         value=f"""
                         **Command:** {ctx.message.clean_content}
                         **Author:** {ctx.author} ({ctx.author.id})
                         **Guild:** {ctx.guild} ({ctx.guild.id})
                         **Channel:** {ctx.channel} ({ctx.channel.id})
                               """)
            await elog.send(embed=le)
            print(err.__traceback__)

            e = discord.Embed(title=":warning: An error occurred", color=colors.red)
            e.description = f"```py\n{err}\n```"
            e.set_footer(text="Full error has been sent to my developers.")
            await ctx.reply(embed=e)

def setup(bot):
    bot.add_cog(Erroring(bot))
