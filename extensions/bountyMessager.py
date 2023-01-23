import bounty
import nextcord
from nextcord.ext import tasks, commands


class BountyMessager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None

    def cog_unload(self):
        self.update_bounty.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = await self.bot.fetch_channel(1061902826533568564)
        bounty.init()
        self.update_bounty.start()

    @tasks.loop(minutes=5)
    async def update_bounty(self):
        new_bounties = bounty.check_for_updates()
        if new_bounties:
            for new_bounty in new_bounties:
                embed = nextcord.Embed(
                    title=new_bounty['title'],
                    url=new_bounty["url"],
                    description=new_bounty["descriptionPreview"],
                    color=0xe75f0a)

                embed.add_field(
                    name="Pays",
                    value=
                    f'{new_bounty["dollars"]} ({new_bounty["cycles"]} Cycles)')

                embed.add_field(name='Deadline', value=new_bounty['timestamp'])

                await self.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(BountyMessager(bot))
