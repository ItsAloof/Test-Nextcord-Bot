from http import client
import nextcord
from nextcord.ext import commands


print("File name: {}".format(__name__))
TESTING_GUILD_ID = [951325774139494450, 396329225206104064]  # Replace with your guild ID
client = commands.Bot(command_prefix='t.', description='Test Bot', intents = nextcord.Intents.all())
admin_users = [192730242673016832]
cmds = ['command', 'fakeperson', 'interactivestory']
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    


if __name__ == "__main__":
    for cmd in cmds:
        client.load_extension(f'commands.{cmd}', extras = {'color': 0xd4af37, 'auth': admin_users})

    client.run('OTI3MzczOTE0NTA4Nzc1NTI1.GoycLK.jksd0v_vPtrwYXHjnQcpJDPSAGvkXRsZf_LVkk')