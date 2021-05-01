from tools.client_init import *

# custom imports for example there
# ..

@client.command(aliases = ['hello'])
async def __hello (ctx):
    await ctx.send('World!')

def on_ready_event():
    print('ready_event triggered in file hello_world')