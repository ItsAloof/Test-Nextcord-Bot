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
cmds = ['command', 'fakeperson', 'interactivestory']
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


def pickBot():
    choice1 = questionary.Choice(title="Mako Test Bot", value="MAKO_TEST_BOT_TOKEN")
    choice2 = questionary.Choice(title="Interaction Test Bot", value="INTERACTION_BOT_TOKEN")
    return questionary.select("Select which bot to use:", choices=[choice1, choice2]).ask()

if __name__ == "__main__":
    for cmd in cmds:
        client.load_extension(f'commands.{cmd}', extras = {'color': 0xd4af37, 'auth': admin_users})
    client.run(os.getenv(pickBot()))
