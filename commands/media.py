import time
from random import choices
from discord import SlashOption
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
from typing import List

from utils import Embed

from main import TESTING_GUILD_ID, tmdb


class Media(commands.Cog):
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth

    @nextcord.slash_command(name="media", description="Search for Movies or TV shows", guild_ids=TESTING_GUILD_ID)
    async def media(self, interaction: Interaction): pass


    @media.subcommand(name="movies", description="Search for Movies")
    async def movie(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the movie you are searching for"), year: int = SlashOption(required=False, name="year", description="What year to search for movies in", verify=True)):
        # start = time.time()
        results = tmdb.searchMovie(query, year)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found")
            return
        # await interaction.send(content="Searching for movies...")
        embed = Embed.create_movie_embed(self, results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction), ephemeral=True)

    @media.subcommand(name="tv", description="Search for TV shows")
    async def tv(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the show you are searching for") ,year: int = SlashOption(required=False, name="year", description="Year to search for first air dates in", verify=True)):
        await interaction.send("Searching for TV shows...")
    

    @media.subcommand(name="people", description="Search for People in films and TV")
    async def people(self, interaction: Interaction, name: str = SlashOption(required=True, name="name", description="Name of the person to search for", verify=True)):
        await interaction.send("Searching for people...")
class ResultsButton(nextcord.ui.Button["ResultsView"]):
    def __init__(self, results: list, current_page:int, next_button: bool, label: str):
        super().__init__(style=nextcord.ButtonStyle.blurple, label=label, row=1)
        self.results = results
        self.current_page = current_page
        self.next_button = next_button
        if not next_button:
            self.disabled = True

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: ResultsView = self.view
        if self.next_button:
            if self.current_page == len(view.results)-1:
                return
            else:
                self.current_page += 1
            embed = self.next_page()
        elif self.next_button is False:
            if self.current_page == 0:
                return
            else:
                self.current_page -= 1
            embed = self.prev_page()

        self.updateButtons(current_page=self.current_page)


        await interaction.response.edit_message(embed=embed, view=view)
    
    def disableButton(self):
        if self.next_button:
            if self.current_page == len(self.results)-1:
                self.disabled = True
            else:
                self.disabled = False
        elif self.next_button is False:
            if self.current_page == 0:
                self.disabled = True
            else:
                self.disabled = False

    def next_page(self):
        if self.current_page == len(self.view.results):
            return None
        else:
            print('index: ', self.current_page)
            return Embed.create_movie_embed(self, self.results, self.current_page)
    
    def prev_page(self):
        if self.current_page < 0:
            return None
        else:
            print('index: ', self.current_page)
            return Embed.create_movie_embed(self, self.results, self.current_page)

    def updateButtons(self, current_page: int):
        for child in self.view.children:
            child.current_page = current_page
            child.disableButton()
    
class ResultsView(nextcord.ui.View):
    children: List[ResultsButton]
    def __init__(self, results: list, starting_page: int, interaction: Interaction):
        super().__init__()
        self.results = results
        self.starting_page = starting_page
        self.add_item(ResultsButton(results, starting_page, False, label="Prev"))
        self.add_item(ResultsButton(results, starting_page, True, label="Next"))
def setup(client, **kwargs):
    client.add_cog(Media(client, **kwargs))

    