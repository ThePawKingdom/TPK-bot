import discord
import asyncio
import config
import traceback
import datetime
import asyncpg

from settings import cogs
from discord.ext import commands


async def run():
    db = await asyncpg.create_pool(**config.DB_CONN_INFO)

    bot = Bot(database=db)
    bot.loop = asyncio.get_event_loop()

    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.now()
    try:
        await db.execute('CREATE TABLE IF NOT EXISTS blacklist (id BIGINT PRIMARY KEY, reason TEXT)')
        await db.execute("CREATE TABLE IF NOT EXISTS balance (user_id BIGINT, guild_id BIGINT, money BIGINT, CONSTRAINT CompKey_ID_NAME PRIMARY KEY (user_id, guild_id))")
        await db.execute("CREATE TABLE IF NOT EXISTS moneylogs (guild_id BIGINT PRIMARY KEY, channel_id BIGINT)")
        await db.execute("CREATE TABLE IF NOT EXISTS guildprefix (guild_id BIGINT PRIMARY KEY, prefix TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS moneytype (guild_id BIGINT PRIMARY KEY, currency TEXT)")
        res = await db.fetch('SELECT * FROM blacklist')
        for the_id in res:
            bot.blacklist[the_id['id']] = the_id['reason']
            print("Loaded blacklist")

        await bot.start(config.token)
    except KeyboardInterrupt:
        await db.close()
        await bot.close()


async def get_prefix(bot, message):
    results = await bot.database.fetchval(f"SELECT prefix FROM guildprefix WHERE guild_id = $1", message.guild.id)
    prefixes = [";"] if not results else [f"{results}"]

    return commands.when_mentioned_or(*prefixes)(bot, message)


class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.playing, name='With wolves'),
            reconnect=True,
            allowed_mentions=discord.AllowedMentions.none(),
            max_messages=10000,
            intents=discord.Intents.all(),
            slash_commands=True
        )

        for extension in cogs.extensions:
            try:
                self.load_extension(extension)
                print(f'[extension] {extension} was loaded successfully!')
            except Exception as e:
                tb = traceback.format_exception(type(e), e, e.__traceback__)
                tbe = "".join(tb) + ""
                print(f'[WARNING] Could not load extension {extension}: {tbe}')

        self.database = kwargs.pop('database', None)
        self.lockdown = True
        self.blacklist = {}

    async def on_ready(self):
        print('Bot has started successfully.')

    async def on_message(self, message):
        if message.author.bot:
            return
        try:
            ctx = await self.get_context(message)
            if ctx.valid:
                await self.invoke(ctx)
        except Exception as e:
            print(e)
            return


loop = asyncio.get_event_loop()
loop.run_until_complete(run())