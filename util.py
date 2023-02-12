from console import fg
import os
from traceback import extract_tb
import subprocess
from nextcord import Guild


def bot_has_permission(guild: Guild, permission: str):
    return getattr(guild.me.guild_permissions, permission)


def find_channel(names, guild: Guild):
    """
    Find a channel by an array of names, with the first name being the highest priority
    """
    for name in names:
        for channel in guild.channels:
            if channel.name == name:
                return channel

    return None


def clear_terminal():
    """
    Clear the terminal
    """

    # If we're on Windows the command is "cls," otherwise it's "clear"
    subprocess.Popen('cls' if os.name == 'nt' else 'clear',
                     shell=True).communicate()


def load_directory(bot, directory_name):
    """
    Recursively walk through every Python file in `directory_name`, and load each as a Cog UNLESS the file name starts with lib
    """
    all_files = []

    for root, dirs, files in os.walk(directory_name):
        for file in files:
            if file.endswith(".py") and not file.startswith("lib"):
                all_files.append(file)

    all_files = sorted(all_files)
    for file in all_files:
        print(
            f"{fg.t_5865f2}Loading {fg.yellow}{directory_name}.{file[:-3]}{fg.default}"
        )

        try:
            bot.load_extension(f"{directory_name}.{file[:-3]}")
        except Exception as error:

            stack = extract_tb(error.original.__traceback__)

            print(fg.red + f"Error: {str(error.original)}")
            for i in stack.format():
                print(i)
            print("\n\nEnd of Stacktrace\n\n" + "_" * 50 + "\n\n" + fg.default)
