import discord

def next_level(ctx):
    if str(ctx.guild.premium_tier) == "0":
        count = int(2 - ctx.guild.premium_subscription_count)
        txt = f'Next level in **{count}** boosts'
        return txt

async def find_user(ctx, user):
    user = user or ctx.author
    if isinstance(user, discord.User):
        pass
    elif isinstance(user, str):
        if not user.isdigit():
            return None
        try:
            user = await ctx.bot.fetch_user(user)
        except Exception:
            return None

    return user