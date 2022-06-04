import random
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
    def __init__(self):
        pass

    def make_embed(title: str = "", author: str = None, description: str = None, color: Colors = Colors.black, 
    image_url = None, thumbnail = None, 
    footer_text = None, footer_icon = None, 
    fields: list = None, 
    random_color: bool = False):
        if random_color:
            color = random.choice(list(Colors))
        if description is None:
            embed = nextcord.Embed(title=title,  color=color.value)
        else:
            embed = nextcord.Embed(title=title, description=description, color=color.value)
        if fields is not None:
            for field in fields:
                if field['name'] == None or field['name'] == "":
                    name = "N/A"
                else:
                    name = field['name']
                if field['value'] == None or field['value'] == "":
                    value = "N/A"
                else:
                    value = field['value']
                try:
                    inline = field['inline'] if field['inline'] is not None else False
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

    