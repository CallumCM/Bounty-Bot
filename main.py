print(f'\033[0;34mInitializing Bot...\033[0m')

from dotenv import load_dotenv

load_dotenv()

__version__ = '0.0.0'

import os
import time
import json
import util
import nextcord
from console import fg
from pathlib import Path
from nextcord.ext import commands

intents = nextcord.Intents.none()
intents.guilds = True

activity = nextcord.Activity(
    type=nextcord.ActivityType.watching,
    name='replit.com/bounties',
)

bot = commands.Bot(
    intents=intents,
    activity=activity,
    case_insensitive=True,
    chunk_guilds_at_startup=False,
)

# Remove the default help command
bot.remove_command('help')

bot.__version__ = __version__


@bot.event
async def on_ready():
    print(f'Bot Version: {fg.lightgreen}{__version__}{fg.default}')
    print(f'Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}')
    print(f'Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}')
    print(
        f'I\'m in {fg.blue}{str(len(bot.guilds))}{fg.default} server{"s" if len(bot.guilds) > 1 else ""}!'
    )
    
    Path('./guilds.json').write_text(
        json.dumps(bot.guilds, indent=2))

util.load_directory(bot, 'extensions')
util.load_directory(bot, 'commands')

while True:
    try:
        bot.run(os.getenv('TOKEN'))
    except nextcord.errors.HTTPException as err:

        # Catch ratelimits
        if err.status == 429:

            util.clear_terminal()

            print(f'{fg.red}Rate limit exceeded.{fg.default}')
            retry_after = err.response.headers['Retry-After']

            print(
                f'{fg.green}Retrying in {retry_after} seconds...{fg.default}')

            time.sleep(int(retry_after))
            continue