from random import random
import time
import nextcord
import enum
from main import tmdb

class Colors(enum.Enum):
    aqua = 0x1ff0b0
    blue = 0x027FFC
    red = 0xFF4932
    air_force_blue = 0x5d8aa8
    dark_green = 0x006400
    dark_blue = 0x00008b
    dark_red = 0x8b0000
    dark_orange = 0xff8c00
    purple = 0xf709f7
    dark_purple = 0x800080
    dark_yellow = 0x808000
    gold = 0xffd700
    light_green = 0x39ff14
    white = 0xffffff
    black = 0x000000
    gray = 0x808080
    light_gray = 0xD3D3D3
    dark_gray = 0xA9A9A9
    yellow = 0xffff00

class Embed():
    time_format = '%Y-%m-%d'
    new_time_format = '%B %e, %Y'
    def __init__(self):
        pass

    def make_embed(self, title: str = "", author: str = None, description=None, color: Colors = Colors.black, 
    image_url=None, thumbnail = None, 
    footer_text=None, footer_icon=None, 
    fields: list=None, 
    random_color: bool = False):
        if random_color:
            color = random.choice(list(Colors))
        embed = nextcord.Embed(title=title, description=description, color=color.value)
        if fields is not None:
            for field in fields:
                name = field['name']
                value = field['value']
                try:
                    inline = field['inline']
                except IndexError:
                    inline = False
                embed.add_field(name=name, value=value, inline=inline)
        
        if author is not None:
            embed.set_author(name=author)
        if image_url is not None:
            embed.set_image(url=image_url)
        if footer_text is not None:
            embed.set_footer(text=footer_text)
            if(footer_icon is not None):
                embed.set_footer(text=footer_text ,icon_url=footer_icon)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        return embed

    def formatDate(date: str):
        return time.strftime(Embed.new_time_format, time.strptime(date, Embed.time_format))

    def create_movie_embed(self, results: list, index: int):
        movie = tmdb.getMovie(results[index]['id'])
        pages = len(results)
        embed = nextcord.Embed(title=f"{movie['title']} ({movie['release_date'][:4]})", description=movie['overview'], color=0x15fc00)
        embed.set_image(url=tmdb.getImage(movie['poster_path'], "original"))
        embed.set_footer(text=f"Page {index+1}/{pages}")
        genres = []
        for genre in movie['genres']:
            genres.append(f"{genre['name']}")
        embed.add_field(name="Genres", value=", ".join(genres), inline=True)
        embed.add_field(name="Runtime", value=f"{int(movie['runtime'] / 60)}h {movie['runtime'] % 60}m", inline=True)
        embed.add_field(name="Release Date", value=Embed.formatDate(date=movie['release_date']), inline=True)
        embed.add_field(name="Rating", value=f"{movie['vote_average']}/10 | {movie['vote_count']} votes", inline=True)
        embed.add_field(name="Budget", value=f"${movie['budget']:,}", inline=True)
        embed.add_field(name="Revenue", value=f"${movie['revenue']:,}", inline=True)
        return embed
        