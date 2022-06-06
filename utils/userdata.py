from discord import Guild, Member

from main import mongodb

class UserData():
    def __init__(self, user: Member, guild: Guild = None, starting_balance: int = 0):
        self._user = user
        self.guild = guild
        self._data = mongodb.getUser(user_id=user.id)
        self.starting_balance = starting_balance
        if self._data is not None and guild is not None:
            self.addGuildData(guild, starting_balance)
        elif self._data is None and guild is not None:
            self.save()
        elif self._data is None and guild is None:
            self.guild = user.guild
            self.save()


    
    @property
    def user(self) -> Member:
        return self._user
    
    def getCreatedAt(self) -> str:
        return self.created_at
    
    def getUsername(self) -> str:
        return self.username

    def addGuildData(self, guild: Guild, balance: int) -> dict:
        """
        Add guild data to the user data
        """
        if self._data is None:
            self.createData()
        elif self.containsGuild(self.guild) is False:
            self._data['guild_data'][f'{guild.id}'] = {'guild_name': guild.name, 'balance': balance}

    def containsGuild(self, guild: Guild) -> bool:
        """
        Check if the user data contains the specified guild
        """
        if self._data is None:
            return False
        for guild_id in self._data['guild_data']:
            if int(guild_id) == guild.id:
                return True
        return False
    
    def getGuildData(self) -> dict:
        if self.containsGuild(self.guild):
            return self._data['guild_data'][f'{self.guild.id}']

    def createData(self) -> None:
        if self.guild is None:
            self.guild = self._user.guild
        self._data = {
            "user_id": self._user.id,
            "created_at": self._user.created_at,
            "username": self._user.name,
            "guild_data": {f'{self.guild.id}': {'guild_name': self.guild.name, 'balance': 0}}
        }
    
    def deposit(self, amount: int = 0) -> None:
        """
        Deposit money to players balance on specified guild

        Parameters
        ----------
        amount : :class:`int`
            The amount of money to deposit
        """
        if self._data is None:
            self.createData()
        self._data['guild_data'][f'{self.guild.id}']['balance'] += amount
        self.save()
    
    def setBalance(self, balance: int) -> None:
        """
        Set the balance of the user on the specified guild

        Parameters
        ----------
        balance : :class:`int`
            The amount of money to set the balance to
        """
        if self._data is None:
            self.createData()
        self._data['guild_data'][f'{self.guild.id}']['balance'] = balance
        self.save(update={f'guild_data.{self.guild.id}': self._data['guild_data'][f'{self.guild.id}']})
    
    def getBalance(self) -> int:
        """
        Get the balance of the user on the specified guild
        """
        if self._data is None:
            return None
        return self._data['guild_data'][f'{self.guild.id}']['balance']
    
    def save(self, update: dict = None) -> None:
        """
        Save the user data given to the database

        Formatting is handled automatically within :class:`UserData` class

        Parameters
        ----------
        update : :class:`dict`
            What data should be updated within the userdata in the database
        """
        if self._data is None:
            self.createData()
            mongodb.insertUser(user_id=self._user.id, data=self._data)
        elif update is None:
            mongodb.updateUser(self._user.id, self._data)
        else:
            mongodb.updateUser(self._user.id, update)

        
    
    @property
    def data(self) -> dict:
        return self.data