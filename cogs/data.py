from nextcord.ext import commands
import nextcord
from nextcord import Interaction, Message
from utilities.mongodb import MongoDB
from utilities.userdata import UserData

class DataCog(commands.Cog):
    def __init__(self, client: commands.Bot, mongodb: MongoDB, modules: list[dict]):
        self.client = client
        self.mongodb = mongodb
        self.modules = modules
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.client.user}\nWatching over {len(self.client.users)} in {len(self.client.guilds)} guilds.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name}")
        self.mongodb.insertGuild(guild_id=guild.id, data={'name': guild.name, 'owner_id': guild.owner_id, 'modules_enabled': self.modules})
        for member in guild.members:
            if member.bot:
                continue

            user = UserData(user_id=member.id, created_at=member.created_at, username=member.name, mutual_guilds=member.mutual_guilds)
            self.mongodb.insertUser(user_id=member.id, data=user.getUserData())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            await guild.system_channel.send(f"Welcome {member.mention} to {guild.name}")
        if member.bot:
            for role in guild.roles:
                if role.name == "Bot":
                    await member.add_roles(role, reason="Automated role assignment: Member was a bot")
        userdata = UserData(user_id=member.id, created_at=member.created_at, username=member.name, mutual_guilds=member.mutual_guilds)
        data = self.mongodb.getUser(user_id=member.id)
        if data is None:
            data = userdata.getUserData()
            self.mongodb.insertUser(user_id=member.id, data=data)
        else:
            data['mutual_guilds'].append({'guild_id': guild.id, 'name': guild.name})
            self.mongodb.updateUser(user_id=member.id, data=data)

def setup(client, **kwargs):
    print("Loaded command: {}".format(__name__))
    client.add_cog(DataCog(client, **kwargs))