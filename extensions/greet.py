from nextcord.ext import commands
import util
from constants import VALID_CHANNEL_NAMES
import bounty


class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = util.find_channel(VALID_CHANNEL_NAMES, guild)
        await channel.send(
            'Hello! I will post new Replit bounties in this channel. If this is the incorrect channel, make sure the correct one is named "replit-bounties" or "bounties".\nSource Code on GitHub: https://github.com/CallumCM/Bounty-Bot\nDevelopment Repl: https://replit.com/@CallumCM/Bounty-Bot'
        )
        first_bounty = bounty.most_recent_bounty()
        await channel.send(embed=bounty.create_bounty_embed(first_bounty))


def setup(bot):
    bot.add_cog(Greet(bot))
