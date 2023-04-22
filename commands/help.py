import nextcord
from nextcord.ext import commands
from constants import (TESTING_GUILD_ID, SLASH_COMMANDS_GLOBAL,
                       VALID_CHANNEL_NAMES, WELCOME_MESSAGE,
                       SPECIFIC_CHANNEL_WELCOME)
import util
import bounty


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name='help',
        description='Get the welcome message and the most recent bounty',
        guild_ids=TESTING_GUILD_ID,
        force_global=SLASH_COMMANDS_GLOBAL,
    )
    async def help_command(self, interaction: nextcord.Interaction):
        channel = util.find_channel(VALID_CHANNEL_NAMES, interaction.guild)

        try:
            if channel:
                await channel.send(SPECIFIC_CHANNEL_WELCOME)

                first_bounty = bounty.most_recent_bounty()
                await channel.send(
                    embed=bounty.create_bounty_embed(first_bounty))

            await interaction.send(WELCOME_MESSAGE, ephemeral=True)
        except:
            pass


def setup(bot):
    bot.add_cog(HelpCommand(bot))
