# THIS FILE WON'T BE IMPORTED!

# default imports
from tools.client_init import *

# custom imports for example there
# ..



# add an user command
settings.commands['Fun']['hello'] = False

# add an admin command (only admins will avaliable to call it)
settings.commands['Fun']['hello_admin'] = True

# dict command value is a boolean (True - for admins ; False - for all)


# user command
@slash.slash(name="hello",
             description="demo hello")
async def hello (ctx):
    pass

# admin command
@slash.slash(name="hello_admin",
             description="demo hello for admins")
async def hello_admin (ctx):
    pass



# on_ready event trigger
def on_ready():
    print('ready_event triggered in file demo.py')

# on_message event trigger
async def on_message(message):
    if (message.content == 'ping'):
        await message.channel.send('pong!')