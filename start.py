# impext used for import all modules from folder
# etc: impext.do("custom")
from modules import impext

# module imports and client init
from tools.client_init import *

# import custom user modules
custom_modules = impext.do('custom')

# remove debug messages
youtube_dl.utils.bug_reports_message = lambda: ''

@client.event
async def on_ready():
    print('Ready')

    for module in custom_modules:
        try:
            getattr(custom_modules[module], 'on_ready_event')()
        except:
            pass
    

# run that shit
client.run (settings.settings['TOKEN'])