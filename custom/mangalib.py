from tools.client_init import *
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession
from pisces import Pisces

headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285', 'cookie': 'XSRF-TOKEN=eyJpdiI6InZLZFR4Qi80a2tJWVJnQ1prUW4yU0E9PSIsInZhbHVlIjoiQ0VRTzhmZjl5V0cxNXEza3Q0d1RNbVFwTHhmUm1VWmFGbnh5VlNJOVE1SzI4NWZORU9zUHJQOWk1UE5TZGNCbXkxL1lpRDFDclZjZzFwUlFLN0p0SThhcXpjTUpUMWFucFVDL2g1SjRCeVppN2F5anBhUklQdC92TnR4ZU1pZE0iLCJtYWMiOiI1Y2M3YzIxOGUzODFiMzA3NjM3ZDA2NjI3ZDE2M2I3Y2E2OWJlOWU1YmExNTBmOWI4MDhkY2FhYzE4MjFjNGY3In0%3D; _ym_uid=1623941422937038083; _ym_d=1623941422; _ym_isad=2; _ym_visorc=w' }

def get_chapter_info(soup):
    chapter_block = soup.find('div', class_='media-section media-chapters-list').find('div', class_='media-chapter')
    chapter = int(chapter_block["data-id"])
    
    info = chapter_block.find('div', class_='media-chapter__name')
    link = 'https://mangalib.me' + str(info.find('a')["href"])
    name = info.find('a').text

    author = chapter_block.find('div', class_='media-chapter__username').find('a').text
    date = chapter_block.find('div', class_='media-chapter__date').text

    manga = soup.find('div', class_='media-name__main').text

    return manga, chapter, link, name.strip(), author.strip(), date.strip()

async def on_ready():
    client.loop.create_task(__listen())

async def __listen():
    while True:
        with open('files/manga.json', 'r') as f:
            table = json.load(f)

        for manga in table:
            if 'translators' in table[manga]:
                for trans in table[manga]['translators']:

                    url = f'https://mangalib.me/{manga}?section=chapters&bid={trans}'
                    session = AsyncHTMLSession()
                    req = await session.get(url, headers=headers)
                    await req.html.arender()

                    if req.status_code not in [503, 200]:
                        continue

                    soup = BeautifulSoup(req.html.html, 'html.parser')

                    if 'Not Found 404' in soup.find('title').text:
                        continue

                    chapters = soup.find('div', class_='media-section media-chapters-list')

                    if not chapters:
                        continue

                    manga_name, chapter, link, name, author, date = get_chapter_info(soup)

                    if 'chapter' not in table[manga]['translators'][trans]:
                        table[manga]['translators'][trans]['chapter'] = chapter
                    elif table[manga]['translators'][trans]['chapter'] != chapter:
                        table[manga]['translators'][trans]['chapter'] = chapter

                        users = table[manga]['translators'][trans]['subs']
                        await notify(users, manga_name, link, name, author, date)

                    await asyncio.sleep(2)
            
            else:

                url = f'https://mangalib.me/{manga}?section=chapters'
                session = AsyncHTMLSession()
                req = await session.get(url, headers=headers)
                await req.html.arender()

                if req.status_code not in [503, 200]:
                    continue

                soup = BeautifulSoup(req.html.html, 'html.parser')

                if 'Not Found 404' in soup.find('title').text:
                    continue

                chapters = soup.find('div', class_='media-section media-chapters-list')

                if not chapters:
                    continue

                manga_name, chapter, link, name, author, date = get_chapter_info(soup)

                if 'chapter' not in table[manga]:
                    table[manga]['chapter'] = chapter
                elif table[manga]['chapter'] != chapter:
                    table[manga]['chapter'] = chapter
                    
                    users = table[manga]['subs']
                    await notify(users, manga_name, link, name, author, date)
                    
                await asyncio.sleep(2)


        with open('files/manga.json', 'w') as f:
            json.dump(table, f)

        await asyncio.sleep(30)

async def notify(users, manga, link, name, author, date):
    for user in users:
        obj = await client.fetch_user(user)
        await obj.create_dm()

        emb = discord.Embed( title = manga, description = name, colour = discord.Color.orange() )

        emb.add_field(name='🙍‍♂️ Автор', value=f'`{author}`', inline=True)
        emb.add_field(name='📅 Дата', value=f'`{date}`', inline=True)
        emb.add_field(name='🔗 Читать', value=f'[Нажмите, чтобы прочитать]({link})', inline=False)

        emb.set_thumbnail(url='https://icons.iconarchive.com/icons/graphicloads/colorful-long-shadow/128/Book-icon.png')

        await obj.dm_channel.send(content='Вышла новая глава в вашем списке!', embed=emb)

        await asyncio.sleep(1)



async def subscribe(member, manga:str, translator_id:str):
    with open('files/manga.json', 'r') as f:
        table = json.load(f)

    if manga not in table:
        table[manga] = {}
        
    if translator_id:
        if 'translators' not in table[manga]:
            table[manga]['translators'] = {}

        if translator_id not in table[manga]['translators']:
            table[manga]['translators'][translator_id] = {}
            table[manga]['translators'][translator_id]['subs'] = []

        if member.id in table[manga]['translators'][translator_id]['subs']:
            return False
        
        table[manga]['translators'][translator_id]['subs'].append(member.id)

    else:
        if 'subs' not in table[manga]:
            table[manga]['subs'] = []

        if member.id in table[manga]['subs']:
            return False

        table[manga]['subs'].append(member.id)
    
    with open('files/manga.json', 'w') as f:
        json.dump(table, f)

    return True
        
    

async def unsubscribe(member, manga:str, translator_id:str):
    with open('files/manga.json', 'r') as f:
        table = json.load(f)

    if manga not in table:
        return False

    if translator_id:
        if 'translators' not in table[manga]:
            return False

        if translator_id not in table[manga]['translators']:
            return False

        if member.id not in table[manga]['translators'][translator_id]['subs']:
            return False

        table[manga]['translators'][translator_id]['subs'].remove(member.id)
        if len(table[manga]['translators'][translator_id]['subs']) == 0:
            del table[manga]['translators'][translator_id]
    
    else:
        if 'subs' not in table[manga]:
            return False

        if member.id not in table[manga]['subs']:
            return False

        table[manga]['subs'].remove(member.id)
        if len(table[manga]['subs']) == 0:
            del table[manga]
    
    with open('files/manga.json', 'w') as f:
        json.dump(table, f)

    return True
        

async def check(id:str, translator_id:str):
    if id.find('https://') != -1:
        return False

    if id.find('mangalib') != -1:
        return False

    url = f'https://mangalib.me/{id}?section=chapters'
    if translator_id:
        url += f'&bid={translator_id}'

    session = AsyncHTMLSession()
    req = await session.get(url, headers=headers)
    await req.html.arender()

    if req.status_code not in [503, 200]:
        return False

    soup = BeautifulSoup(req.html.html, 'html.parser')

    if 'Not Found 404' in soup.find('title').text:
        return False

    chapters = soup.find('div', class_='media-section media-chapters-list')

    if not chapters:
        return 'translator'

    return True

settings.commands['Anime']['mangalib'] = False

@slash.slash(name="mangalib",
             description="Subscribe/Unsub for manga chapters updates",
             options=[
                create_option(
                    name="id",
                    description="mangalib.me/[ID] <--- Manga id",
                    option_type=SlashCommandOptionType.STRING,
                    required=True
                ),
                create_option(
                    name="command",
                    description="Subscribe/Unsubscribe for manga updates",
                    option_type=SlashCommandOptionType.STRING,
                    required=True,
                    choices=[
                        create_choice(name='Subscribe', value='sub'),
                        create_choice(name='Unsubcribe', value='unsub'),
                    ],
                ),
                create_option(
                    name="translator_id",
                    description="mangalib.me/..?bid=[ID] <--- Translator id",
                    option_type=SlashCommandOptionType.STRING,
                    required=False
                ),
             ])

async def mangalib (ctx, id:str, command:str, translator_id:str=''):
    await ctx.defer()
    out = await check(id, translator_id)

    if not out:
        emb = discord.Embed( title = '❌ Wrong manga id or problems with mangalib', description = '', colour = discord.Color.red() )
        await ctx.send(embed=emb)
        return False

    if out == 'translator':
        emb = discord.Embed( title = '❗ You should add translator id for this manga', description = '', colour = discord.Color.orange() )
        await ctx.send(embed=emb)
        return False

    if command == 'sub':
        result = await subscribe(ctx.author, id, translator_id)
    else:
        result = await unsubscribe(ctx.author, id, translator_id)

    if not result:
        emb = discord.Embed( title = '❌ Failure. Probably, you have already (un)subscribed to the manga', description = '', colour = discord.Color.red() )
        await ctx.send(embed=emb)
    else:
        if command == 'sub':
            emb = discord.Embed( title = '✅ Successful! I will PM you, when the new chapter comes out', description = '', colour = discord.Color.green() )
        else:
            emb = discord.Embed( title = '✅ Successful! I unsubscribed you from getting updates', description = '', colour = discord.Color.green() )
        await ctx.send(embed=emb)

    