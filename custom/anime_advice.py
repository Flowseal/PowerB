from requests.api import head
from tools.client_init import *
from bs4 import BeautifulSoup
import requests

headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.285' }

def page_count(url):
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.content, 'html.parser')
  pagination = soup.find('div', class_='pagination')
  total = pagination.find('span', class_='link-total')

  if total:
    return int(total.text)
  else:
    return 1

def generate_link(type_genre, genre, type, status, rating, year):
  if genre and type_genre:
    url = f'https://shikimori.one/animes/kind/{type}/status/{status}/season/{year}/genre/{type_genre},{genre}/rating/r,pg_13,pg,g/score/{rating}'
  elif genre:
    url = f'https://shikimori.one/animes/kind/{type}/status/{status}/season/{year}/genre/{genre}/rating/r,pg_13,pg,g/score/{rating}'
  elif type_genre:
    url = f'https://shikimori.one/animes/kind/{type}/status/{status}/season/{year}/genre/{type_genre}/rating/r,pg_13,pg,g/score/{rating}'
  else:
    url = f'https://shikimori.one/animes/kind/{type}/status/{status}/season/{year}/rating/r,pg_13,pg,g/score/{rating}'

  page_total = page_count(url)
  page = '1'
  if page_total > 1:
    page = str(random.randint(1, page_total))
  url += f'/page/{page}'

  return url

def get_anime_link(url):
  req = requests.get(url, headers=headers)
  soup = BeautifulSoup(req.content, 'html.parser')

  anime_block = soup.find('div', class_='cc-entries')
  animes = anime_block.find_all('article')
  if len(animes) == 0:
    return False

  anime = random.choice(animes)
  link = anime.find('a')["href"]
  return link

async def parse_anime(url):
  req = requests.get(url, headers=headers)

  retries = 0
  ok = True
  while not req.ok:
    retries += 1
    if retries % 3 == 0:
      req = requests.get(url, headers=headers)

    if retries > 15:
      ok = False
      break

    await asyncio.sleep(0.3)

  if not ok:
    return False, False, False, False, False, False, False, False, False


  soup = BeautifulSoup(req.content, 'html.parser')

  name = ''.join(soup.find('h1').find_all(text=True))

  rating = soup.find('div', class_='b-rate').find('div', class_='text-score').find('div').text

  info_block = soup.find('div', class_='b-entry-info')
  info = info_block.find_all('div', class_='line-container')

  form = info[0].find('div', class_='value').text
  episodes = info[1].find('div', class_='value').text

  if info_block.find('span', class_='b-anime_status_tag released'):
    status = 'Вышло ' + info_block.find('span', class_='b-anime_status_tag released').parent.text.replace('\xa0', '')
  else:
    status = 'Выходит ' + info_block.find('span', class_='b-anime_status_tag ongoing').parent.text.replace('\xa0', '')

  genres_block = info_block.find('div', class_='key', text='Жанры:').parent.find('div', class_='value')
  genres_all = genres_block.find_all('span', class_='b-tag')
  genres = [s.find('span', class_='genre-ru').text for s in genres_all]

  image = soup.find('div', class_='c-poster').find('img')["src"]

  desc_block = soup.find('div', class_='text', itemprop='description').find('div', class_='b-text_with_paragraphs')
  desc = ''

  is_footer = False

  tags = desc_block.find_all(text=True)
  for tag in tags:
    if tag.parent.name == 'a':
      desc += '[' + tag.parent.text + ']' + '(' + tag.parent["href"] + ')'
    else:
      desc += tag
  
  if len(desc) > 1024:
    desc = ''
    for tag in tags:
      if tag.parent.name == 'a':
        desc += '**' + tag.parent.text + '**'
      else:
        desc += tag

  if len(desc) > 1024:
    desc = ''
    for tag in tags:
      desc += tag

  if len(desc) > 1024 and len(desc) <= 2048:
    is_footer = True
  elif len(desc) > 2048:
    d_cut = desc[:1024]
    d_words = d_cut.split()[:-5]
    desc = ' '.join(d_words)
    desc += '...'

  return name, rating, form, episodes, status, genres, image, desc, is_footer

settings.commands['Anime']['anime advice'] = False

@slash.subcommand(base="anime", name="advice",
description="Advice you the anime",
options=[
  create_option(
    name="type_genre",
    description="Anime type genre",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
       create_choice(name='Сёнэн', value='27-Shounen'),
       create_choice(name='Сёдзё', value='25-Shoujo'),
       create_choice(name='Сейнэн', value='42-Seinen'),
       create_choice(name='Сёнэн-ай', value='28-Shounen-Ai'),
       create_choice(name='Сёдзе-ай', value='26-Shoujo-Ai'),
       create_choice(name='Дзёсей', value='43-Josei')
    ],
  ),
  create_option(
    name="genre",
    description="Anime genre",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
       create_choice(name='Романтика', value='22-Romance'),
       create_choice(name='Драма', value='8-Drama'),
       create_choice(name='Комедия', value='4-Comedy'),
       create_choice(name='Повседневность', value='36-Slice-of-Life'),
       create_choice(name='Школа', value='23-School'),

       create_choice(name='Экшен', value='1-Action'),
       create_choice(name='Фэнтези', value='10-Fantasy'),
       create_choice(name='Игры', value='11-Game'),
       create_choice(name='Фантастика', value='24-Sci-Fi'),
       create_choice(name='Гарем', value='35-Harem'),
       create_choice(name='Спорт', value='30-Sports'),
       create_choice(name='Детектив', value='7-Mystery'),
       create_choice(name='Музыка', value='19-Music'),
       create_choice(name='Ужасы', value='14-Horror'),
       create_choice(name='Психология', value='40-Psychological'),
       create_choice(name='Приключения', value='2-Adventure'),
       create_choice(name='Триллер', value='41-Thriller'),
       create_choice(name='Суперспособности', value='31-Super-Power'),
       create_choice(name='Меха', value='18-Mecha'),
    ],
  ),
  create_option(
    name="type",
    description="Anime type",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
       create_choice(name='Сериал', value='tv'),
       create_choice(name='Фильм', value='movie'),
    ],
  ),
  create_option(
    name="status",
    description="Anime status",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
       create_choice(name='Вышло', value='released'),
       create_choice(name='Выходит', value='ongoing'),
    ],
  ),
  create_option(
    name="rating",
    description="Anime rating",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
       create_choice(name='8+', value='8'),
       create_choice(name='7+', value='7'),
       create_choice(name='6+', value='6'),
    ],
  ),
  create_option(
    name="year",
    description="Anime release year",
    option_type=SlashCommandOptionType.STRING,
    required=False,
    choices=[
      create_choice(name='2021', value='2021'),
      create_choice(name='2020', value='2020'),
      create_choice(name='2018-2019', value='2018_2019'),
      create_choice(name='2013-2017', value='2013_2017'),
      create_choice(name='2000-2012', value='2000_2012'),
      create_choice(name='1990-1999', value='199x'),
      create_choice(name='1980-1989', value='198x'),
    ],
  )
])

async def anime_advice (ctx, type_genre:str='', genre:str='', type:str='movie,tv', status:str='released,ongoing', rating:str='8', year:str='2021,2020,2018_2019,2013_2017,2000_2012,199x'):
    await ctx.defer()
    
    link = get_anime_link(generate_link(type_genre, genre, type, status, rating, year))
    if not link:
      emb = discord.Embed( title = '🐽 Sorry, I cant advice you anything now', description = '', colour = discord.Color.red() )
      await ctx.send(embed=emb)
      return False
    
    name, rating, form, episodes, status, genres, image, desc, is_footer = await parse_anime(link)
    if not name:
      emb = discord.Embed( title = '🐽 Sorry, I cant advice you anything now', description = '', colour = discord.Color.red() )
      await ctx.send(embed=emb)
      return False

    emb = discord.Embed( title = name, description = f'*{form}* - *{status}*', colour = discord.Color.purple() )

    emb.add_field( name = '⭐ Рейтинг', value = f'`{rating}`', inline=True)

    if form == 'Фильм':
      emb.add_field( name = '🎬 Длительность', value = f'`{episodes}`', inline=True)
    else:
      emb.add_field( name = '🎬 Эпизоды', value = f'`{episodes}`', inline=True)
    
    gen = ', '.join(genres)
    emb.add_field( name = '🌀 Жанры', value = f'`{gen}`', inline=False)

    if desc:
      if not is_footer:
        emb.add_field( name = '💬 Описание', value = f'{desc}', inline=False)
      else:
        emb.set_footer(text=desc)

    emb.set_thumbnail(url = image)

    await ctx.send(embed=emb)