from tools.client_init import *

buttons_list = {'en': 'English', 'ru': 'Russian'}

def create_buttons(lang='en'):
        buttons = [
            create_button(
                style = ButtonStyle.blurple if lang == key else ButtonStyle.gray,
                label = buttons_list[key],
                custom_id = key
            ) for key in buttons_list
        ]
        buttons.append(
            create_button(
                style = ButtonStyle.URL,
                label = 'Github',
                url='https://github.com/Flowseal/PowerB'
            )
        )
        component = create_actionrow(*buttons)
        return component

def create_page(lang='en'):
    embed = discord.Embed(title = 'Handmade Bot', color = discord.Color.magenta())

    if 'en' in lang:
        embed.description = '\n'.join((
            'It\'s self-coded discord bot using *Python3* and *Discord.py* library',
            'Base source that everyone can easily edit and use as his own is free and uploaded to **Github**',
            '*You can visit Github by clicking the button "Github"*',
            '\nThe bot also uses slash-commands library, that provide cute commands-display by typing "/" symbol in channel',
            'If you have suggestions about the commands feel free to create **issues** or **pull** requests'
        ))
    else:
        embed.description = '\n'.join((
            'Это самописный бот для discord, написанный на языке *Python* с использованием библиотеки *Discord.py*',
            'Базовый код бота, который любой желающий может изменить и использовать, бесплатен и залит на **Github**',
            '*Вы можете перейти на страницу Github нажатием соответствующей кнопки*',
            '\nБот также использует библиотеку slash-commands, которая добавляет красивое изображение комманд при написании символа "/"',
            'Если у вас есть какие-либо предложения, то вы можете создать **issue** или **pull** запрос'
        ))

    embed.set_footer(text='by SAAC')
    embed.set_thumbnail(url = "https://icons.iconarchive.com/icons/alecive/flatwoken/128/Apps-Help-icon.png")
    return embed


@slash.slash(name="help",
             description="Prints information about the Bot")
async def help (ctx):
    components = create_buttons()
    await ctx.send(embed=create_page(), components=[components], hidden=True)

@slash.component_callback()
async def ru(ctx: ComponentContext):
    components = create_buttons('ru')
    await ctx.edit_origin(embed=create_page('ru'), components=[components])

@slash.component_callback()
async def en(ctx: ComponentContext):
    components = create_buttons('en')
    await ctx.edit_origin(embed=create_page('en'), components=[components])