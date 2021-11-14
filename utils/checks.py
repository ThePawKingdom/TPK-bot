import discord

from settings import colors, links


async def lockdown(ctx):
    if ctx.bot.lockdown:
        if ctx.author.id == 809057677716094997 or 345457928972533773:
            return False
        else:
            e = discord.Embed(color=colors.red)
            e.description = f"BadWolf is currently undergoing maintenance. Please stand by and wait." \
                            f" If you wanna see what's going on or stay updated on the maintenance," \
                            f" you are free to join [our support server]({links.support})"
            await ctx.send(embed=e)
            return True
    return False
