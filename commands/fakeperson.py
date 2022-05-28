from ast import Str
import re
import shutil
from nextcord.ext import commands
import nextcord
from nextcord import Interaction
import requests
from typing import List

from main import TESTING_GUILD_ID

class User(commands.Cog):
    TESTING_GUILD_ID = 0
    def __init__(self, client, color, auth):
        self.client = client
        self.color = color
        self.auth = auth

    @nextcord.slash_command(name="randomuser", description="Generate a random user profile", guild_ids=TESTING_GUILD_ID)
    async def randomuser(self, interaction: Interaction):
        r = requests.get('https://randomuser.me/api/?nat=us')
        data = r.json()
        user = data['results'][0]
        embed = nextcord.Embed(title="", color=0x2bff00)
        embed.set_author(name=user['name']['first'] + " " + user['name']['last'])
        embed.set_image(url=user['picture']['large'])
        embed.set_footer(text="Generated by randomuser.me")
        embed.add_field(name="Phone Number", value=user["phone"], inline=False)
        embed.add_field(name="Email", value=user["email"], inline=False)
        embed.add_field(name="Address", value=f'{user["location"]["street"]["number"]} {user["location"]["street"]["name"]}, {user["location"]["city"]}, {user["location"]["state"]}, {user["location"]["postcode"]}', inline=False)
        embed.set_thumbnail(url="https://patch.com/img/cdn20/users/22973312/20190703/111508/styles/patch_image/public/green-check-point-patch___03111500060.jpg?width=695&height=695&fit=crop&crop=faces&auto=format&q=100")
        await interaction.send(embed=embed)

    @nextcord.slash_command(name="fakeperson", description="Generate a fake person", guild_ids=TESTING_GUILD_ID)
    async def fakeperson(self, interaction: Interaction):
        r = requests.get('https://boredhumans.com/api_faces.php');
        data = r._content.decode('utf-8')
        pattern = "https:\/\/boredhumans\.b-cdn\.net\/faces\/[0-9]+\.jpg"
        url = re.findall(pattern, data)
        msg = "No faces found" if (url.count == 0) else url[0]
        await interaction.send(msg)
    
    @nextcord.slash_command(name="fakeperson2", description="Generate a fake person that looks more realistic", guild_ids=TESTING_GUILD_ID)
    async def fakepersontwo(self, interaction: Interaction):
        r = requests.get('https://boredhumans.com/api_faces2.php');
        data = r._content.decode('utf-8')
        pattern = "https:\/\/boredhumans\.b-cdn\.net\/faces2\/[0-9]+\.jpg"
        url = re.findall(pattern, data)
        msg = "No faces found" if (url.count == 0) else url[0]
        await interaction.send(msg)


   

def setup(client, **kwargs):
    print(f"Loaded command: {__name__}")
    client.add_cog(User(client, **kwargs))

    