from tools.imports import *
from config import settings

intents = discord.Intents.all()
prefix = settings.settings['prefix']

client = commands.Bot(command_prefix=prefix, intents=intents)

client.remove_command('help')