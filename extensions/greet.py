from nextcord.ext import commands
import util
from constants import VALID_CHANNEL_NAMES, SPECIFIC_CHANNEL_WELCOME
import bounty


class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = util.find_channel(VALID_CHANNEL_NAMES, guild)
        await channel.send(SPECIFIC_CHANNEL_WELCOME)

        first_bounty = bounty.most_recent_bounty()
        await channel.send(embed=bounty.create_bounty_embed(first_bounty))


def setup(bot):
    bot.add_cog(Greet(bot))
