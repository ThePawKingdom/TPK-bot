import discord

from prettytable import PrettyTable
from settings import links, colors
from discord.ext import commands
from utils.paginator import TextPages

class Admin(commands.Cog, name="Admin"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = '👑'  # Set the help menu emote.

    @commands.group()
    @commands.is_owner()
    async def suggestion(self, ctx):
        """ Deny/Approve a suggestion """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @suggestion.command()
    @commands.is_owner()
    async def approve(self, ctx, msg_id: int, *, reason: commands.clean_content):
        """ Approve a suggestion """
        suggestion = await self.bot.database.fetch("SELECT * FROM suggestions WHERE msg_id = $1", msg_id)

        if not suggestion:
            return await ctx.author.send(":warning: This suggestion does not seem to exist. Are you sure you are providing a message ID?")

        user = await self.bot.fetch_user(suggestion[0]['user_id'])
        suggestion_content = f"{suggestion[0]['suggestion']}"
        suggestion_message = suggestion[0]['msg_id']

        message = await self.bot.get_guild(links.mainguild).get_channel(links.suggestions).fetch_message(suggestion_message)
        embed = message.embeds[0]

        embed.color = colors.green
        embed.add_field(name="Suggestion Approved:", value=reason, inline=False)
        embed.set_footer(text=f"Approved by {ctx.author}")
        await message.clear_reactions()
        await message.edit(embed=embed)

        e = discord.Embed(color=colors.green)
        e.description = f"Your suggestion has been approved by {ctx.author}:\n**Approved with reason:** {reason}\n\n**suggestion:**\n{suggestion_content}"
        e.set_author(name=f"Suggested by {user}", icon_url=user.avatar.url if user.avatar else user.display_avatar.url)
        try:
            await user.send(embed=e)
        except Exception:
            pass

    @suggestion.command()
    @commands.is_owner()
    async def deny(self, ctx, msg_id: int, *, reason: commands.clean_content):
        """ Deny a suggestion """
        suggestion = await self.bot.database.fetch("SELECT * FROM suggestions WHERE msg_id = $1", msg_id)

        if not suggestion:
            return await ctx.send(":warning: This suggestion does not seem to exist. Are you sure you are providing a message ID?")

        user = await self.bot.fetch_user(suggestion[0]['user_id'])
        suggestion_content = f"{suggestion[0]['suggestion']}"
        suggestion_message = suggestion[0]['msg_id']

        message = await self.bot.get_guild(links.mainguild).get_channel(links.suggestions).fetch_message(suggestion_message)
        embed = message.embeds[0]

        embed.color = colors.red
        embed.add_field(name="Suggestion denied:", value=reason, inline=False)
        embed.set_footer(text=f"Denied by {ctx.author}")
        await message.clear_reactions()
        await message.edit(embed=embed)

        e = discord.Embed(color=colors.red)
        e.description = f"Your suggestion has been denied by {ctx.author}:\n**Denied with reason:** {reason}\n\n**suggestion:**\n{suggestion_content}"
        e.set_author(name=f"Suggested by {user}", icon_url=user.avatar.url if user.avatar else user.display_avatar.url)
        try:
            await user.send(embed=e)
        except Exception:
            pass

    @commands.command(name="sql")
    @commands.is_owner()
    async def sql(self, ctx, *, query):
        """ Execute psql query """
        try:
            if query.__contains__('guild.id'):
                query = query.replace('guild.id', str(ctx.guild.id))
            if query.__contains__('author.id'):
                query = query.replace('author.id', str(ctx.author.id))
            if query.__contains__('channel.id'):
                query = query.replace('channel.id', str(ctx.channel.id))

            if not query.lower().startswith("select"):
                data = await self.bot.database.execute(query)
                return await ctx.send(data)

            data = await self.bot.database.fetch(query)
            if not data:
                return await ctx.send("Table seems to be empty!")
            columns = []
            values = []
            for k in data[0].keys():
                columns.append(k)

            for y in data:
                rows = []
                for v in y.values():
                    rows.append(v)
                values.append(rows)

            x = PrettyTable(columns)
            for d in values:
                x.add_row(d)

            pages = TextPages(ctx,
                              text=f'\n{x}')
            return await pages.paginate()
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Admin(bot))
