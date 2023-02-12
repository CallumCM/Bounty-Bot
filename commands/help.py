import nextcord
from nextcord.ext import commands
from constants import TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name='help',
        description='Why am I here?',
        guild_ids=TESTING_GUILD_ID,
        force_global=SLASH_COMMANDS_GLOBAL,
    )
    async def help_command(self, interaction: nextcord.Interaction):
        await interaction.send(
            "I'll let you know when there's new Replit bounties. I look for a channel called either `replit-bounties`, or `bounties` and I will send updates there. If you have any questions, please contact callum@geekveggie.dev"
        )


def setup(bot):
    bot.add_cog(HelpCommand(bot))
