import sys
import random
import datetime
from isort import file
import orjson

fake_firstnames = ['Its', 'Itz', 'xxx', 'XxX', 'Warrior', 'wy', 'impos', 'Int', 'Rye', 'Kid', 'World', 'Wonder']
fake_lastnames = ['Oif', 'Oof', 'Zed' ,'zed', 'Pilot', 'War', 'est', 'Sky', 'zone', 'fitz', 'accord', 'Warlord', 'Tension']

class User():
    def __init__(self, ) -> None: pass
    
    def getUserData(username: str, id: int, created_at: str, mutual_guilds: list[int]):
        return {'user_id': id, 'created_at': created_at, 'username': username, 'mutual_guilds': mutual_guilds}

def generateUsers(amount):
    users = []
    for i in range(amount):
        users.append(User.getUserData(username="".join(random.choice(fake_firstnames) + random.choice(fake_lastnames)), id=random.randint(10000000000, 99999999999), created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mutual_guilds=[random.randint(10000000000, 99999999999)]))
    return users

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        users = generateUsers(int(args[1]))
        open("users.json", "wb").write(orjson.dumps(users, option=orjson.OPT_INDENT_2))



