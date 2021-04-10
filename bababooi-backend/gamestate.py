from dataclasses import dataclass, field

@dataclass
class Player:
    name: str
    isOwner: bool = False
    def to_dict(self):
        return {"name": self.name, "isOwner": self.isOwner}

@dataclass
class GameSession:
    room: str
    players: list = field(default_factory=list)
    gameType: str = ""

    def get_player_array(self):
        player_array = []
        for player in self.players:
            player_array.append(player.to_dict())
        return player_array

games = {}

def add_player(json):
    room = json['room']
    name = json['name']
    isOwner = False
    if room not in games.keys():
        games[room] = GameSession(room)
        isOwner = True
    for player in games[room].players:
        if player.name == name:
            return True
    games[room].players.append(Player(name, isOwner))
    return False

def remove_player(json):
    room = json['room']
    name = json['name']
    if room not in games.keys():
        return
    game = games[room]
    isOwner = False
    for i in range(0, len(game.players)):
        if game.players[i].name == name:
            isOwner = game.players[i].isOwner
            game.players.pop(i)
            break
    if isOwner and len(game.players) > 0:
        game.players[0].isOwner = True
    elif len(game.players) == 0:
        games.pop(room)
        return False
    return True

def get_players(room):
    if room in games.keys():
        return games[room].get_player_array()
    return []
