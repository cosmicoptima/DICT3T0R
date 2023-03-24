import dbm

db = dbm.open("db", "c")

class DbUser:
    def __init__(self, id: int):
        self.discord_id = int