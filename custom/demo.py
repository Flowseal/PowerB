# THIS FILE WON'T BE IMPORTED!

# default imports
from tools.client_init import *

# custom imports from custom folder
impext.do('custom/demo')

'''
You also can define your needed imports there
'''


# command
@slash.slash(name="hello",
             description="demo hello")
async def hello (ctx):
    pass

# admin command (for example, you also can use permissions-based commands from lib)
@slash.slash(name="hello_admin",
             description="demo hello for admins")
async def hello_admin (ctx):
    if not await is_admin_notify(ctx):
        return False
    pass


# on_ready event trigger
def on_ready():
    print('ready_event triggered in file demo.py')

# on_message event trigger
async def on_message(message):
    if (message.content == 'ping'):
        await message.channel.send('pong!')