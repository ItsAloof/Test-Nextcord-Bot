class UserData():
    def __init__(self, user_id: int, created_at: str, username: str, mutual_guilds: list[int]):
        self._user_id = user_id
        self.created_at = created_at
        self.username = username
        self.mutual_guilds = mutual_guilds
    
    @property
    def getUserID(self):
        return self._user_id
    
    def getCreatedAt(self):
        return self.created_at
    
    def getUsername(self):
        return self.username
    
    def getUserData(self):
        guilds = []
        for guild in self.mutual_guilds:
            guilds.append({'guild_id': guild.id, 'guild_name': guild.name})
        return {
            "user_id": self._user_id,
            "created_at": self.created_at,
            "username": self.username,
            "mutual_guilds": guilds
        }