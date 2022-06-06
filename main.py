from http import client
from unicodedata import name
import nextcord
from nextcord.ext import commands
import os
import questionary

from tmdb3 import tmdb_api

from dotenv import load_dotenv

from utilities.mongodb import MongoDB


load_dotenv(dotenv_path="./secrets.env")

tmdb = tmdb_api(api_key=os.getenv("TMDB_API_KEY"))

mongodb = MongoDB(connection_url=os.getenv("MONGODB_URI"))

TESTING_GUILD_ID = [951325774139494450, 396329225206104064, 982358070896234588]  # Replace with your guild ID
# "you sleep 👀"
client = commands.Bot(command_prefix='mo.', description='Test Bot', intents = nextcord.Intents.all(), activity=nextcord.Activity(name=f"netflix and chill", type=nextcord.ActivityType.streaming, url="https://www.youtube.com/watch?v=0J2QdDbelmY&list=RD0J2QdDbelmY&start_radio=1"))


admin_users = [192730242673016832]
default_options = {'color': 0xd4af37, 'auth': admin_users}
modules = {
'games': [{'cmd': "interactivestory", 'options': default_options}, {'cmd': "economy", 'options': default_options}, {'cmd': "fakeperson", 'options': default_options}, {'cmd': "command", 'options': default_options}], 
'utils': [{'cmd': "media", 'options': default_options}], 'admin': []}


def pickBot():
    choice1 = questionary.Choice(title="Mako Test Bot", value="MAKO_TEST_BOT_TOKEN")
    choice2 = questionary.Choice(title="Interaction Test Bot", value="INTERACTION_BOT_TOKEN")
    return questionary.select("Select which bot to use:", choices=[choice1, choice2]).ask()

def load_modules():
    games = questionary.Choice(title="Games", value="games", checked=True)
    utils = questionary.Choice(title="Utils", value="utils", checked=True)
    admin = questionary.Choice(title="Admin", value="admin", checked=False, disabled=True)
    return questionary.checkbox("Select which modules to load:", choices=[games, utils, admin]).ask()


if __name__ == "__main__":
    
    for module in load_modules():
        for command in modules[module]:
            client.load_extension(f"cogs.{command['cmd']}", extras=command['options'])
    client.load_extension("cogs.data", extras={'mongodb': mongodb, 'modules': modules})
    client.run(os.getenv(pickBot()))
