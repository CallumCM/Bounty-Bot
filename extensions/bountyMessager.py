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
        self.update_bounty.start()

    @tasks.loop(minutes=30)
    async def update_bounty(self):
        bounty_updates = bounty.check_for_updates()
        if bounty_updates:
            embed = nextcord.Embed(title=bounty_updates['title'],
                                   url=bounty_updates["url"],
                                   description=bounty_updates["description"],
                                   color=0xe75f0a)
            #embed.set_author(name='@' + bounty_updates["author"])
            embed.add_field(
                name="Pays...",
                value=
                f'{bounty_updates["dollars"]} ({bounty_updates["cycles"]} Cycles)'
            )
            embed.add_field(name='Due in...', value=bounty_updates['due_in'])

            print(bounty_updates)

            await self.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(BountyMessager(bot))
