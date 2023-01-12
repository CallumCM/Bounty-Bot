# Usage/Running the Bot
Supply a Discord bot token in the `TOKEN` environment variable, and press run!

# Adding new commands/features
The way the bot is currently organized, each command is in it's own `Cog` located 
in a Python file in the `commands` folder, and each non-command feature is the same 
in the `extensions` folder. For information on Cogs, slash commands, etc. check out 
the Nextcord documentation at [docs.nextcord.dev/en/stable](https://docs.nextcord.dev/en/stable/)

# Premade Features:

## util.py

### `@admin()` - Admin Command Decorator

Allow only users with admin to run this slash command.
<br>
Example:
```py
@util.admin()
@nextcord.slash_command(
  name="admin",
  description="Manage bot administrators."
)
async def admin_command(self, interaction: nextcord.Interaction):
  await interaction.send("You are an admin!")
```
### `@owner()` - Owner Command Decorator
Same as above, but only lets the person with the ID in the `OWNER` variable in `constants.py` run the command.

### `get_message()` - Get Message from Language File

`lang.json` is a file which stores a bunch of key-value pairs, 
so that you can easily write/edit messages and have them update 
in multiple places. You can also use template strings to make customizable messages.
<br>
Example `lang.json`
```json
{
  "error.wikipedia_failed": "An issue was encountered fetching the wikipedia page for {page}."
}
```
Example `cog.py`:
```py
@nextcord.slash_command(
  name="pear",
  description="Get information from Wikipedia about pears"
)
async def pear_command(self, interaction: nextcord.Interaction):
  try:
    pear_data = get_wikipedia_page("Pear")
    await interaction.send(pear_data)
  except Exception as e:
    await interaction.send(get_message("error.wikipedia_failed", page="Pears"))
```

## constants.py
`DEVELOPMENT_FEATURES` - configure an environment variable with this name to say
"True" or "False," so that some features of the bot only run in development, 
and can be disabled in production.
-- --
Because of the way Discord's slash command system functions,
new slash commands can take a few hours to update/appear which
is (obviously) not ideal for development, so you provide the server
ID of your testing server(s) in the array called `TESTING_GUILD_ID` and Discord 
will instantly update the slashcommand in that/those server(s).
When you're ready for everyone to try your slash commands,
set an environment variable called `SLASH_COMMANDS_GLOBAL` to "True"

## Config
This is a library written to easily support server-specific config for 
theoretically unlimited servers. `default_config.json` stores the default config values 
for each server, and any new server will automatically get these config values. If you get 
an error about a config value not existing, make sure it exists in `default_config.json`. 
`global_config.json` contains config that users cannot access, and that is persistant across 
all servers. Config arrays that exist in `global_config.json` and `default_config.json` will 
have the global values appended.
-- --
`config.read(guild_id, option)` - Read a specific config value for a server
`config.fetch(guild_id, array)` - Read a specific config array for a server
`config.load(guild_id)` - Read the entire config for a server
`config.write(guild_id, option, value)` - Set a config option to a value for a server
`config.append(guild_id, list, value)` - Append a value to an array that exists in config. (Global config values must be added manually and cannot be added through this)
`config.remove(guild_id, list, value)` - Remove a value to an array that exists in config. (Global config values must be added manually and cannot be added through this)
`config.backup()` - Backs up every single server's config into one file (`backup.json`)
`config.revert()` - Restores every single server's config from `backup.json`