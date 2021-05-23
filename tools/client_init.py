from tools.imports import *
from tools.checks import *
from config import settings

intents = discord.Intents.all()
prefix = '/'

client = commands.Bot(command_prefix=prefix, intents=intents)
slash = SlashCommand(client, sync_commands=True)

client.remove_command('help')