import bounty
from nextcord.ext import tasks, commands
import util
from constants import VALID_CHANNEL_NAMES


class BountyMessager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_unload(self):
        self.update_bounty.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        bounty.init()
        self.update_bounty.start()

    @tasks.loop(minutes=5)
    async def update_bounty(self):
        new_bounties = bounty.check_for_updates()
        if new_bounties:
            channels = [
                util.find_channel(VALID_CHANNEL_NAMES, guild)
                for guild in self.bot.guilds
            ]

            for channel in channels:
                for new_bounty in new_bounties:
                    await channel.send(
                        embed=bounty.create_bounty_embed(new_bounty))


def setup(bot):
    bot.add_cog(BountyMessager(bot))
