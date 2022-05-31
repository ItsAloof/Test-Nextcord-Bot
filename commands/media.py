import time
from random import choices
import re
from secrets import choice
import shutil
from discord import SlashOption
from matplotlib.pyplot import title
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import requests
from typing import List
from bs4 import BeautifulSoup
import orjson


from main import TESTING_GUILD_ID, tmdb


class Media(commands.Cog):
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth
    
    
    @nextcord.slash_command(name="media", description="Search for Movies or TV shows", guild_ids=TESTING_GUILD_ID)
    async def media(self, interaction: Interaction): pass


    @media.subcommand(name="movie", description="Search for Movies")
    async def movie(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the movie you are searching for"), year: int = SlashOption(required=False, name="year", description="What year to search for movies in", verify=True)):
        await interaction.send("Searching for movies...")
        start = time.time()
        results = tmdb.searchMovie(query, year)
        if(results['total_results'] == 0):
            await interaction.edit_original_message(content="No results found")
            return
        firstMovieDetails = tmdb.getMovie(results['results'][0]['id'])
        movie = firstMovieDetails

        embed = nextcord.Embed(title=f"{movie['title']} ({movie['release_date'][:4]})", description=movie['overview'], color=0x15fc00)
        end = time.time()
        embed.set_image(url=tmdb.getImage(movie['poster_path'], "original"))
        embed.set_footer(text=f"{movie['vote_average']}/10 | {movie['vote_count']} votes | Response Time = {end - start:.2f}s")
        genres = []
        for genre in movie['genres']:
            genres.append(f"{genre['name']}")
        embed.add_field(name="Genres", value=", ".join(genres), inline=True)
        embed.add_field(name="Runtime", value=f"{int(movie['runtime'] / 60)}h {movie['runtime'] % 60}m", inline=True)
        embed.add_field(name="Budget", value=f"${movie['budget']:,}", inline=False)
        embed.add_field(name="Revenue", value=f"${movie['revenue']:,}", inline=True)
        await interaction.edit_original_message(content="", embed=embed)

    @media.subcommand(name="tv", description="Search for TV shows")
    async def tv(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the show you are searching for") ,year: int = SlashOption(required=False, name="year", description="Year to search for first air dates in", verify=True)):
        await interaction.send("Searching for TV shows...")
    

    @media.subcommand(name="people", description="Search for People in films and TV")
    async def people(self, interaction: Interaction, name: str = SlashOption(required=True, name="name", description="Name of the person to search for", verify=True)):
        await interaction.send("Searching for people...")

def setup(client, **kwargs):
    # print(f"Loaded command: {__name__}")
    # f = open("example_movie.json")
    # data = orjson.loads(f.buffer.read())
    # for jsonMovie in data['results']:
    #     print(f'Title: {jsonMovie["title"]}\nOverview:\n{jsonMovie["overview"]}\nRelease Date: {jsonMovie["release_date"]}\n')
    client.add_cog(Media(client, **kwargs))

    