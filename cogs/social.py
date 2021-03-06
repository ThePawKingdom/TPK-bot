import discord
from settings import gifs
from discord.ext import commands
from utils import default as functions


class Social(commands.Cog, name="Social"):
    def __init__(self, bot):
        self.bot = bot
        self.help_icon = "<:Hug:839603884716589066>"

    @commands.command(brief="Snuggle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snuggle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Snuggle the specified people"""
        await functions.interactions(ctx, members, "snuggled", 'snuggle', gifs.snuggle, reason)

    @commands.command(brief="Hug someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        await functions.interactions(ctx, members, "hugged", 'hug', gifs.hug, reason, 'hug')

    @commands.command(brief="Boop someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boop(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Boop the specified people"""
        await functions.interactions(ctx, members, "booped", 'boop', gifs.boop, reason)

    @commands.command(brief="Smooch someone", aliases=["kiss"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smooch(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Smooch the specified people"""
        await functions.interactions(ctx, members, "smooched", 'smooch', gifs.smooch, reason)

    @commands.command(brief="Lick someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lick(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Lick the specified people"""
        await functions.interactions(ctx, members, "licked", 'lick', gifs.lick, reason)

    @commands.command(brief="Give bellyrubs!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bellyrub(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give bellyrubs to the specified people"""
        await functions.interactions(ctx, members, "bellyrubbed", 'rub the belly of', gifs.bellyrub, reason)

    @commands.command(brief="Nuzzle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuzzle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Nuzzle the specified people"""
        await functions.interactions(ctx, members, "nuzzled", 'nuzzles', gifs.nuzzle, reason)

    @commands.command(brief="Cuddle someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuddle(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Cuddle the specified people"""
        await functions.interactions(ctx, members, "cuddled", 'cuddle', gifs.cuddle, reason)

    @commands.command(brief="Feed someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feed(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Feed the specified people"""
        await functions.interactions(ctx, members, "fed", 'feed', gifs.feed, reason)

    @commands.command(brief="Glomp someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glomp(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Glomp on the specified people"""
        await functions.interactions(ctx, members, "glomped", 'glomp', gifs.glomp, reason)

    @commands.command(brief="Highfive someone")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Highfive the specified people"""
        await functions.interactions(ctx, members, "highfived", 'hivefive', gifs.highfive, reason)

    @commands.command(brief="Rawrrrr")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rawr(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Rawr at the specified people"""
        await functions.interactions(ctx, members, "rawred at", 'rawr at', gifs.rawr, reason)

    @commands.command(brief="Howl to the moon, or someone", aliases=["howl"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def awoo(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Howl at the specified people"""
        await functions.interactions(ctx, members, "howled at", 'howl at', gifs.awoo, reason)

    @commands.command(brief="pat someone!", aliases=["pet"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Pat the specified people"""
        await functions.interactions(ctx, members, "patted", 'pat', gifs.pet, reason, 'pat')

    @commands.command(brief="Gib cookie")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cookie(self, ctx, members: commands.Greedy[discord.Member], *, reason=None):
        """Give cookies to the specified people"""
        await functions.interactions(ctx, members, "gave a cookie to", 'give a cookie to', gifs.cookie, reason)

    @commands.command(brief="Blushies!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, members: commands.Greedy[discord.Member]):
        """Blush (optionally because of specified people)"""
        await functions.feelings(ctx, members, "blushes", gifs.blush)

    @commands.command(brief="Be happy")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def happy(self, ctx, members: commands.Greedy[discord.Member]):
        """Be happy (optionally because of specified people)"""
        await functions.feelings(ctx, members, "smiles", gifs.happy)

    @commands.command(brief="wag yer tail")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wag(self, ctx, members: commands.Greedy[discord.Member]):
        """Wag your tail (Optionally because of specified people)"""
        await functions.feelings(ctx, members, "wags their tail", gifs.wag)


def setup(bot):
    bot.add_cog(Social(bot))
