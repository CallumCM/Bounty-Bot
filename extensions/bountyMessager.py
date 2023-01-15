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

    @tasks.loop(minutes=15)
    async def update_bounty(self):
        bounty_updates = bounty.check_for_updates()
        if bounty_updates:
            for bounty_item in bounty_updates:
                embed = nextcord.Embed(
                    title=bounty_item['title'],
                    url=bounty_item["url"],
                    description=bounty_item["descriptionPreview"],
                    color=0xe75f0a)

                #embed.set_author(name='@' + bounty_item["author"])

                embed.add_field(
                    name="Pays",
                    value=
                    f'{bounty_item["dollars"]} ({bounty_item["cycles"]} Cycles)'
                )

                embed.add_field(name='Deadline',
                                value=bounty_item['timestamp'])

                await self.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(BountyMessager(bot))
