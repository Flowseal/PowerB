from tools.client_init import *

settings.commands['Information']['help'] = 'Print infromation about commands'
settings.commands['Information']['ahelp'] = 'Print infromation about admin commands'

@client.command(aliases = ['help'])
async def __help (ctx):
    
    member = ctx.message.author
    await ctx.send(f'<@{member.id}>, I sent you commands list in PM 👍')

    emb = discord.Embed( title = 'Commands list:', description = '', colour = discord.Color.light_grey() )
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

    for table in settings.commands:
        commands = ''
        for cmd in settings.commands[table]:
            commands += f'`{prefix}{cmd}` '
        
        emb.add_field( name = f'{table}', value = commands, inline=False)

    emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/alecive/flatwoken/128/Apps-Help-icon.png")
    emb.set_footer(text='Type *command*_help to see infromation about command')

    dm = await member.create_dm()
    await dm.send(embed=emb)


@client.command(aliases = ['ahelp'])
async def __ahelp (ctx):
    
    member = ctx.message.author
    await ctx.send(f'<@{member.id}>, I sent you commands list in PM 👍')

    emb = discord.Embed( title = 'Commands list:', description = '', colour = discord.Color.light_grey() )
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

    for table in settings.admin_commands:
        commands = ''
        for cmd in settings.admin_commands[table]:
            commands += f'`{prefix}{cmd}` '
        
        emb.add_field( name = f'{table}', value = commands, inline=False)

    emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/alecive/flatwoken/128/Apps-Help-icon.png")
    emb.set_footer(text='Type *command*_help to see infromation about command')

    dm = await member.create_dm()
    await dm.send(embed=emb)

