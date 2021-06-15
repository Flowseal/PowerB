# module imports and client init
from tools.client_init import *

# remove debug messages
youtube_dl.utils.bug_reports_message = lambda: ''

# add modules in folder custom
impext.do('custom')

# to optimize checks
custom_modules = impext.get_modules()

@client.event
async def on_ready():
    print (f"{client.user.name} | Ready")

    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_ready')()
        except:
            pass

@client.event
async def on_message(message):
    if (message.author.bot):
        return False

    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_message')(message)
        except:
            pass

    if (len(message.content) > 0):
        is_command = message.content[0] == prefix

        if is_command:
            mes = message.content.lower()[1:]
            for table in settings.commands:
                    for command in settings.commands[table]:
                        if mes.startswith(command.lower()) and settings.commands[table][command]:
                            if not message.author.guild_permissions.administrator:
                                return False


    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_command_error')(ctx, error)
        except:
            pass

    if isinstance(error, CommandNotFound):
        return
    raise error

@client.event
async def on_member_join(member):
    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_member_join')(member)
        except:
            pass

@client.event
async def on_voice_state_update(member, before, after):
    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_voice_state_update')(member, before, after)
        except:
            pass

# run that shit
client.run (settings.settings['token'])