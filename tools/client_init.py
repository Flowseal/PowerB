from tools.imports import *
from tools.checks import *
from config import settings

# impext used for import all modules from folder
# etc: impext.do("custom")
from modules import impext

intents = discord.Intents.all()
prefix = '/'

client = commands.Bot(command_prefix=prefix, intents=intents)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

client.remove_command('help')