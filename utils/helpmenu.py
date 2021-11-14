import discord, config, asyncio
from discord.ext import commands, menus
from utils.paginator import Pages
from settings import links, emotes


def safe_get(list, index, default=None):
    try:
        return list[index]
    except IndexError:
        return default


class GroupHelpSource(menus.ListPageSource):
    def __init__(self, group, data):
        super().__init__(data, per_page=5)
        self.group = group

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=str(self.group),
                              color=discord.Color.dark_teal())

        for index, command in enumerate(entries, start=offset):
            embed.add_field(name=command.qualified_name,
                            value=(
                                f"[{' | '.join([alias for alias in command.aliases])}] \n" if command.aliases else ""
                                                                                                                   f"{command.help or 'None'}"
                            ))

        embed.set_footer(text=f"Page {menu.current_page + 1} / {self.get_max_pages()}" if
        self.get_max_pages() > 0 else "Page 0/0")
        return embed


class CogHelpSource(menus.ListPageSource):
    def __init__(self, cog, data):
        super().__init__(data, per_page=6)
        self.cog = cog

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(title=self.cog.qualified_name,
                              color=discord.Color.dark_teal())

        for index, command in enumerate(entries, start=offset):
            embed.add_field(
                name=f"**{str(command)}** [{' | '.join(alias for alias in command.aliases)}]" if command.aliases else f"**{str(command)}**",
                value=(
                        f"{command.help}" or "None"
                ), inline=False
            )

        embed.set_footer(text=f"Page {menu.current_page + 1} / {self.get_max_pages()}"
        if self.get_max_pages() > 0 else "Page 0/0")

        return embed


class CogHelpPages(menus.MenuPages):
    def __init__(self, source):
        super().__init__(source, delete_message_after=True)


class PenguinHelp(commands.HelpCommand):
    def __init__(self):
        self.owner_cogs = ['Jishaku', 'Devishaku']
        self.admin_cogs = ['Admin']
        self.ignore_cogs = ['Error', 'DLP', 'Slash', 'Logs', 'Admin', 'Devishaku', 'Jishaku', 'HelpMenu']
        self.help_icon = '<:store:729571108260675604>'
        super().__init__(command_attrs={
            # "cooldown": commands.Cooldown(1, 5, commands.BucketType.user),
            "help": "The help command",
            "aliases": ["h"]
        })

    async def command_not_found(self, string):
        return f"The command `{string}` was not found."

    async def send_bot_help(self, mapping):
        """ See bot help """
        ctx = self.context

        Josh = await self.context.bot.fetch_user(843866750131109909)

        support = links.support
        invite = links.invite
        prefixes = "`>>`"
        s = "Support"
        i = "Bot invite"
        boats = "[discord.boats](https://discord.boats/bot/620990340630970425)"
        privacy = "[Privacy Policy](https://psychops.tk/legal.php#privacy)"

        emb = discord.Embed(color=discord.Color.dark_teal())
        emb.description = (f"[{s}]({support}) | [{i}]({invite}) "
                           f"| {boats} | {privacy}\n\n**Made by:** {Josh}\nPrefix: {prefixes}\n\n")

        def check(r, u):
            return u.id in [self.context.author.id, 843866750131109909] and r.message.id == msg.id

        exts = []
        to_react = []
        for extension in set(self.context.bot.cogs.values()):
            if extension.qualified_name in self.ignore_cogs:
                continue
            if extension.qualified_name == ["Jishaku", "Devishaku"]:
                continue
            if extension.qualified_name in self.owner_cogs and not await self.context.bot.is_owner(self.context.author):
                continue
            # if extension.qualified_name in self.admin_cogs and not await self.context.bot.is_admin(self.context.author):
            #    continue
            # if extension.qualified_name in self.booster_cogs and not await self.context.bot.is_booster(self.context.author):
            #    continue
            # if await checks.cog_disabled(self.context, str(extension.qualified_name)):
            #    continue
            exts.append(f"{extension.help_icon} **{extension.qualified_name}**")
            to_react.append(f"{extension.help_icon}")

        # emb.set_author(icon_url=self.context.bot.user.avatar.url, name=self.context.bot.user.name)
        emb.set_thumbnail(url=self.context.bot.user.avatar.url)
        emb.add_field(name="Categories:", value="\n".join(exts) + "\n\u200b")

        if ctx.guild:
            emb.set_footer(text="You can also click on the reactions below to view commands in each category.")

        msg = await ctx.send(embed=emb)
        try:
            if ctx.guild:
                for reaction in to_react:
                    await msg.add_reaction(reaction)
                await msg.add_reaction('\U000023f9')

                cog_emojis = {
                    "<:Discovery:845656527347777548>": 'Utility',
                    "<:banhammer:908419238249787412>": 'Moderation',
                    "👑": 'Admin',
                    "💰": 'Currency',
                    "<:Hug:839603884716589066>": 'Social',
                    "<:cog:908418457203265536>": 'Management',
                    "<:slash:833803136199032882>": 'Slash',
                    "\U000023f9": 'Stop'
                }
                react, user = await self.context.bot.wait_for('reaction_add', check=check, timeout=300.0)
                if str(react) in cog_emojis:
                    pass
                elif str(react) not in cog_emojis:
                    return
                await msg.delete()
                await self.context.send_help(self.context.bot.get_cog(cog_emojis[str(react)]))

        except asyncio.TimeoutError:
            try:
                await msg.clear_reactions()
            except Exception:
                return
        except Exception:
            await self.context.send(content="Failed to add reactions")

    async def send_cog_help(self, cog):
        commands = []
        for command in cog.get_commands():
            commands.append(f"`{command.qualified_name}` - **{command.short_doc}**\n")

        paginator = Pages(self.context,
                          title=f"{cog.qualified_name} help",
                          entries=commands,
                          thumbnail=None,
                          per_page=10,
                          embed_color=discord.Color.dark_teal(),
                          show_entry_count=True)
        await paginator.paginate()

    async def send_command_help(self, command):
        aliases = '`' + '`, `'.join(command.aliases) + "`"
        if aliases == "``" or aliases == '`':
            aliases = f" {emotes.crossmark} No aliases found"
        embed = discord.Embed(title=f"[{command.cog.qualified_name}] {command.qualified_name}",
                              color=discord.Color.dark_teal())
        # title= command.qualified_name + " | " + " | ".join([f"{alias}" for alias in command.aliases]),
        embed.description = command.help or f"`{command.qualified_name}` does not have a description."
        embed.set_thumbnail(url=self.context.bot.user.avatar.url)

        command = (await self.filter_commands([command]))

        command = command[0] if len(command) == 1 else None

        if not command:
            return await self.get_destination().send(embed=embed)

        embed.add_field(name="Usage",
                        value=f"{self.clean_prefix}{command.qualified_name} {command.signature}")
        embed.add_field(name="Aliases",
                        value=aliases,
                        inline=True)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group: commands.Group):
        menu = CogHelpPages(source=GroupHelpSource(group, await self.filter_commands(group.commands)))
        await menu.start(self.context)