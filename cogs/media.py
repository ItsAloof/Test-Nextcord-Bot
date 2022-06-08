import enum
import time
from random import choices
from discord import SlashOption
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
from typing import List

from utils.embed_builder import Embed, Colors

from main import TESTING_GUILD_ID, tmdb
from utils.MediaTypes import MediaType
from utils.userdata import UserData


class Media(commands.Cog):
    time_format = '%Y-%m-%d'
    new_time_format = '%B %e, %Y'
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth
    def formatDate(date: str):
        return time.strftime(Media.new_time_format, time.strptime(date, Media.time_format))

    def create_media_embed(mediaType: MediaType, results: list, index: int):
        if mediaType == MediaType.movie:
            return Media.create_movie_embed(results=results, index=index)
        elif mediaType == MediaType.tv:
            return Media.create_tv_embed(results=results, index=index)
        elif mediaType == MediaType.person:
            return Media.create_person_embed(results=results, index=index)
        else:
            return Embed.make_embed(title="Error", description="Invalid media type", color=Colors.red)

    def create_movie_embed(results: list, index: int):
        movie = tmdb.getMovie(results[index]['id'])
        pages = len(results)
        genres = []
        for genre in movie['genres']:
            genres.append(f"{genre['name']}")
        embed = Embed.make_embed(title=movie['title'], description=movie['overview'], image_url=tmdb.getImage(movie['poster_path'], "original"), footer_text=f"Page {index+1}/{pages}", fields=[{'name': "Genres", 'value': ", ".join(genres), 
        'inline':True},{'name':"Runtime", 'value':f"{int(movie['runtime'] / 60)}h {movie['runtime'] % 60}m", 
        'inline':True}, {'name':"Release Date", 'value':Media.formatDate(date=movie['release_date']), 'inline': True},
        {'name':"Rating", 'value':f"{movie['vote_average']}/10 | {movie['vote_count']} votes", 'inline':True}, {'name':"Budget", 'value':f"${movie['budget']:,}", 'inline':True}, {'name':"Revenue", 'value':f"${movie['revenue']:,}", 'inline':True}], color=Colors.light_green) 
        return embed

    def create_tv_embed(results: list, index: int):
        tv = tmdb.getTVShow(results[index]['id'])
        pages = len(results)
        genres = []
        networks = []
        for genre in tv['genres']:
            genres.append(f"{genre['name']}")
        for network in tv['networks']:
            networks.append(f"{network['name']}")

        embed = Embed.make_embed(title=tv['name'], description=tv['overview'], image_url=tmdb.getImage(tv['poster_path'], "original"), 
        footer_text=f"Page {index+1}/{pages}", fields=[{'name': "Genres", 'value': ", ".join(genres), 
        'inline':True},{'name':f"{tv['number_of_seasons']} Seasons", 'value':f"{tv['number_of_episodes']} Episodes", 'inline':True}, 
        {'name':"Release Date", 'value':Media.formatDate(date=tv['first_air_date']), 'inline': True},
        {'name':"Rating", 'value':f"{tv['vote_average']}/10 | {tv['vote_count']} votes", 'inline':True}, 
        {'name':"Networks", 'value':", ".join(networks), 'inline':True}, 
        {'name':"Status", 'value':tv['status'], 'inline':True}], 
        color=Colors.light_green) 
        return embed
    
    def create_person_embed(results: list, index: int):
        person = tmdb.getPerson(results[index]['id'])
        pages = len(results)
        fields=[{'name': "Born", 'value':Media.formatDate(date=person['birthday']), 'inline':True}, {'name':"Birthplace", 'value':person['place_of_birth'], 'inline':True}]
        if person['deathday'] is not None:
            fields.append({'name':"Died", 'value':Media.formatDate(date=person['deathday']), 'inline':True})
        embed = Embed.make_embed(title=person['name'], description=person['biography'], image_url=tmdb.getImage(person['profile_path'], "original"), footer_text=f"Page {index+1}/{pages}", 
        fields=fields, color=Colors.light_green)
        
        return embed

        

    @nextcord.slash_command(name="media", description="Search for Movies or TV shows", guild_ids=TESTING_GUILD_ID)
    async def media(self, interaction: Interaction): pass


    @media.subcommand(name="movies", description="Search for Movies")
    async def movie(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the movie you are searching for"), year: int = SlashOption(required=False, name="year", description="What year to search for movies in", verify=True), 
    ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,})):
        results = tmdb.searchMovie(query, year)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Media.create_movie_embed(results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.movie), ephemeral=bool(ephemeral))

    @media.subcommand(name="shows", description="Search for TV shows")
    async def tv(self, interaction: Interaction, query: str = SlashOption(required=True, name="name", description="The name of the show you are searching for") ,year: int = SlashOption(required=False, name="year", description="Year to search for first air dates in", 
    verify=True), ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,}, verify=True)):
        results = tmdb.searchTVShow(query, year)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Media.create_tv_embed(results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.tv), ephemeral=bool(ephemeral))

    @media.subcommand(name="people", description="Search for People in films and TV")
    async def people(self, interaction: Interaction, name: str = SlashOption(required=True, name="name", description="Name of the person to search for", verify=True), 
    ephemeral: int = SlashOption(required=False, name="hidden", description="Set whether the response should be visible to only you or everyone", choices={"yes": 1, "no": 0,}, verify=True)):
        results = tmdb.searchPeople(name)
        if(results['total_results'] == 0):
            await interaction.send(content="No results found", ephemeral=True)
            return
        embed = Media.create_person_embed(results['results'], index=0)
        await interaction.send(embed=embed, view=ResultsView(results=results['results'], starting_page=0, interaction=interaction, mediaType=MediaType.person), ephemeral=bool(ephemeral))

    @media.subcommand(name="movielist", description="Get a list of movies you have saved")
    async def movielist(self, interaction: Interaction):
        userdata = UserData(interaction.user, interaction.guild)
        movielist: list[int] = userdata.getMovieList()
        if movielist is None or len(movielist) == 0:
            await interaction.send(content="You have no movies saved", ephemeral=True)
            return
        else:
            movie_list = "Your Movies:\n"
            index = 1
            for movie in movielist:
                movie_list += f"{index}.) {movie['movie_name']}\n"
                index += 1
            await interaction.send(content=movie_list, ephemeral=True)
        

class SaveResultButton(nextcord.ui.Button["ResultsView"]):
    def __init__(self, interaction: Interaction, mediaType: MediaType, movie_id: int, movie_name: str):
        super().__init__(style=nextcord.ButtonStyle.success, label="Save", row=1)
        self.interaction = interaction
        self.mediaType = mediaType
        self.color = Colors.light_green
        self.movie_id = movie_id
        self.movie_name = movie_name

    async def callback(self, interaction: Interaction):
        if(self.mediaType == MediaType.movie):
            userdata = UserData(interaction.user, interaction.guild)
            movies = userdata.getMovieList()
            if movies is None:
                userdata.addMovie(self.movie_id, self.movie_name)
                await interaction.send(content="Movie added to your list", ephemeral=True)
            for movie in movies:
                if movie['movie_id'] == self.movie_id:
                    await interaction.send(content="Movie already in your list", ephemeral=True)
                    return
            userdata.addMovie(self.movie_id, self.movie_name)
            await interaction.send(content="Movie added to your list", ephemeral=True)
    
class ResultsButton(nextcord.ui.Button["ResultsView"]):
    def __init__(self, results: list, current_page:int, next_button: bool, label: str, mediaType: MediaType):
        super().__init__(style=nextcord.ButtonStyle.primary, label=label, row=1)
        self.results = results
        self.current_page = current_page
        self.next_button = next_button
        self.mediaType = mediaType
        if not next_button:
            self.disabled = True
        if len(results) - 1 == 0:
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
        self.updateSaveButton(movie_id=view.results[self.current_page]['id'], movie_name=view.results[self.current_page]['title'])

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
            return Media.create_media_embed(mediaType=self.mediaType, results=self.results, index=self.current_page)
    
    def prev_page(self):
        if self.current_page < 0:
            return None
        else:
            return Media.create_media_embed(mediaType=self.mediaType, results=self.results, index=self.current_page)

    def updateSaveButton(self, movie_id: int, movie_name: str):
        for child in self.view.children:
            if isinstance(child, SaveResultButton):
                child.movie_id = movie_id
                child.movie_name = movie_name
                break
    
    def updateButtons(self, current_page: int):
        for child in self.view.children:
            if isinstance(child, ResultsButton):
                child.current_page = current_page
                child.disableButton()
    
class ResultsView(nextcord.ui.View):
    children: List[ResultsButton]
    def __init__(self,mediaType: MediaType, results: list, starting_page: int, interaction: Interaction):
        super().__init__()
        self.results = results
        self.starting_page = starting_page
        self.add_item(ResultsButton(results, starting_page, False, label="Prev", mediaType=mediaType))
        self.add_item(SaveResultButton(interaction, mediaType, movie_id=results[starting_page]['id'], movie_name=results[starting_page]['title']))
        self.add_item(ResultsButton(results, starting_page, True, label="Next", mediaType=mediaType))
def setup(client, **kwargs):
    print(f'Loaded command: {__name__}')
    client.add_cog(Media(client, **kwargs))


