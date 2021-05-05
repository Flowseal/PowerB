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
    print (f"{client.user.name} | Ready")

    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_ready')()
        except:
            pass

@client.event
async def on_message(message):
    is_command = message.content[0] == prefix

    if '_help' in message.content and is_command:
        cmd = message.content.replace('_help', '')
        cmd = cmd.replace(prefix, '')

        for table in settings.commands:
            for command in settings.commands[table]:
                if command.lower() == cmd.lower():
                    await message.channel.send(f'> {cmd.lower()}\n' + settings.commands[table][command])

    for module in custom_modules:
        try:
            await getattr(custom_modules[module], 'on_message')(message)
        except:
            pass

    if is_command:
        mes = message.content.lower()[1:]
        for table in settings.admin_commands:
                for command in settings.admin_commands[table]:
                    if mes.startswith(command.lower()):
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

# run that shit
client.run (settings.settings['token'])