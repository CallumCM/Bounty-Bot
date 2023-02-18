from nextcord.ext import commands
import nextcord
import util
from constants import VALID_CHANNEL_NAMES, SPECIFIC_CHANNEL_WELCOME
import bounty


class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def write_serverlist(self):
        servers = []
        for i in self.bot.guilds:
            servers.append(i.name + '\n')
        with open("./servers.txt", "w") as serverlist:
            serverlist.writelines(servers)

    @commands.Cog.listener()
    async def on_ready(self):
        self.write_serverlist()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.write_serverlist()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.write_serverlist()

        channel = util.find_channel(VALID_CHANNEL_NAMES, guild)

        # Create the channel if able to + it doesn't already exist
        if not channel and util.bot_has_permission(guild, 'manage_channels'):
            overwrites = {
                guild.me:
                nextcord.PermissionOverwrite(send_messages=True,
                                             view_channel=True)
            }
            channel = await guild.create_text_channel('replit-bounties',
                                                      overwrites=overwrites)

        if channel:
            await channel.send(SPECIFIC_CHANNEL_WELCOME)

            first_bounty = bounty.most_recent_bounty()
            await channel.send(embed=bounty.create_bounty_embed(first_bounty))


def setup(bot):
    bot.add_cog(Greet(bot))
