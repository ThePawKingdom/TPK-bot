def next_level(ctx):
    if str(ctx.guild.premium_tier) == "0":
        count = int(2 - ctx.guild.premium_subscription_count)
        txt = f'Next level in **{count}** boosts'
        return txt
