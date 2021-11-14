from discord.ext import commands


class Management(commands.Cog, name="Management"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = '<:cog:908418457203265536>'  # Set the help menu emote.

    @commands.group()
    @commands.guild_only()
    async def prefix(self, ctx):
        """ Set the bot's prefix """
        if ctx.invoked_subcommand is None:
            prefix = await self.bot.database.fetchval(f"SELECT prefix FROM guildprefix WHERE guild_id = $1", ctx.guild.id)

            if prefix is None:
                prefix = '>>'

            await ctx.send(f"My current prefix is `{prefix}`\nYou can change it using `{ctx.prefix}prefix set <prefix>`")

    @prefix.command(name="set", aliases=["change"])
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def prefix_set(self, ctx, prefix: str):
        if len(prefix) > 10:
            return await ctx.send("Your prefix can not be longer than 10 characters!")

        else:
            query = """
            INSERT INTO guildprefix VALUES($1, $2)
            ON CONFLICT (guild_id) DO UPDATE
            SET prefix = $2
            WHERE guildprefix.guild_id = $1
                    """

            await self.bot.database.execute(query, ctx.guild.id, prefix)
            await ctx.send(f"The prefix has successfully changed to `{prefix}`.")


def setup(bot):
    bot.add_cog(Management(bot))
