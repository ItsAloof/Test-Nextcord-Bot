from http import client
import nextcord
from nextcord.ext import commands
import os
import questionary

from dotenv import load_dotenv

load_dotenv(dotenv_path="./secrets.env")
print("File name: {}".format(__name__))
TESTING_GUILD_ID = [951325774139494450, 396329225206104064]  # Replace with your guild ID
activity = nextcord.Activity(name="you sleep 👀", type=nextcord.ActivityType.watching)
client = commands.Bot(command_prefix='t.', description='Test Bot', intents = nextcord.Intents.all(), activity=activity)
admin_users = [192730242673016832]
default_options = {'color': 0xd4af37, 'auth': admin_users}
modules = {
'games': [{'cmd': "interactivestory", 'options': default_options}, {'cmd': "fakeperson", 'options': default_options}, {'cmd': "command", 'options': default_options}], 
'utils': [{'cmd': "movie", 'options': default_options}], 'admin': []}
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


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
        for command in module:
            print(command)
            # client.load_extension(f'commands.{command}', extras = command['options'])
    client.load_extension('commands.movie')
    client.run(os.getenv(pickBot()))
