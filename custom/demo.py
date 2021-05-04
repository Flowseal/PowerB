# THIS FILE WON'T BE IMPORTED!

# default imports
from tools.client_init import *

# custom imports for example there
# ..


# add commands in dict

# user commands list
settings.commands['Fun']['hello'] = 'Print hello world!'

# admin commands list
settings.admin_commands['Fun']['set_hello'] = 'Set the greeting message'


# admin command etc
@client.command(aliases = ['set_hello'])
async def __set_hello (ctx):
    pass

# default command etc
@client.command(aliases = ['hello'])
async def __hello (ctx):
    await ctx.send('World!')

# custom event
def on_ready_event():
    print('ready_event triggered in file demo.py')

# custom event
async def on_message(message):
    if (message.content == 'ping'):
        await message.channel.send('pong!')