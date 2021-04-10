from dataclasses import dataclass, field

MAX_GAMES = 10

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
    gameType: str = "bababooi"
    gameState: str = "lobby"

    def get_player_array(self):
        player_array = []
        for player in self.players:
            player_array.append(player.to_dict())
        return player_array

    def get_player(name):
        for player in self.players:
            if player.name == name:
                return player
        return None

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
            return 'Player name is taken!'
    games[room].players.append(Player(name, isOwner))
    return ''

def remove_player(json):
    room = json['room']
    name = json['name']
    if room not in games.keys():
        return False
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

def choose_game(json):
    room = json['room']
    name = json['name']
    game = json['game']
    if room not in games.keys():
        return "Room doesn't exist!";
    player = games[room].get_player(name)
    if player == None:
        return "Player doesn't exist in room!"
    if player.isOwner == False:
        return "Player isn't an owner!"
    games[room].gameState = game
    # TODO: Validate game
    return ''

def get_players(room):
    if room in games.keys():
        return games[room].get_player_array()
    return []

def can_create_new_game():
    return len(games) < MAX_GAMES