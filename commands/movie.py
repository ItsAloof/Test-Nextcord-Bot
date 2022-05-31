from ast import Str
import json
from random import choices
import re
from secrets import choice
import shutil
from discord import SlashOption
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import requests
from typing import List
from bs4 import BeautifulSoup
import orjson

from main import TESTING_GUILD_ID

class Movies(commands.Cog):
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth
    
    @nextcord.slash_command(name="movie", description="Search for a movie", guild_ids=TESTING_GUILD_ID)
    async def movie(self, interaction: Interaction):
        await interaction.send("Searching for a movie...")


def setup(client, **kwargs):
    print(f"Loaded command: {__name__}")
    f = open("example_movie.json")
    data = orjson.loads(f.buffer.read())
    for jsonMovie in data['results']:
        print(f'Title: {jsonMovie["title"]}\nOverview:\n{jsonMovie["overview"]}\nRelease Date: {jsonMovie["release_date"]}\n')
    # client.add_cog(Movies(client, **kwargs))

    