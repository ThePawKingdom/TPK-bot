from discord.ext import commands
from utils.helpmenu import PenguinHelp

class HelpCog(commands.Cog, name="HelpMenu"):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = PenguinHelp()
        bot.help_command.cog = self
        # self.help_icon = '<:Discovery:845656527347777548>' # Not relevant as this is for the help menu that this cog allows usage of.

def setup(bot):
    bot.add_cog(HelpCog(bot))
