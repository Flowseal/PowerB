from tools.imports import *
from config import settings

intents = discord.Intents.all()
prefix = settings.settings['PREFIX']

client = commands.Bot(command_prefix=prefix, intents=intents)