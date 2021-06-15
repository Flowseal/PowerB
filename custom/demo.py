# THIS FILE WON'T BE IMPORTED!

# default imports
from tools.client_init import *

# custom imports from custom folder
impext.do('custom/demo')

'''
You also can define your needed imports there
'''

settings.commands['Fun']['hello'] = False # c1
settings.commands['Fun']['hello_admin'] = True #c2

'''
In that case:
c1 command in help list can see everyone
c2 command in help list can see only roles with admin priv

So: False - Everyone; True - Admins
'''


# user command
@slash.slash(name="hello",
             description="demo hello")
async def hello (ctx):
    pass

# admin command
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