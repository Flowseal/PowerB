from tools.client_init import *

# custom imports for example there
# ..

# add commands in dict
settings.commands['Fun']['hello'] = 'Print hello world!'
settings.admin_commands['Fun']['set_hello'] = 'Set the greeting message'

# admin command etc
@client.command(aliases = ['set_hello'])
async def __set_hello (ctx):
    pass

# default command
@client.command(aliases = ['hello'])
async def __hello (ctx):
    await ctx.send('World!')

# custom event
def on_ready_event():
    print('ready_event triggered in file demo.py')