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
    gameSpecificState: dict = field(default_factory=dict)

    def get_player_array(self):
        player_array = []
        for player in self.players:
            player_array.append(player.to_dict())
        return player_array

    def get_player(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return None

games = {}

def create_room_with_player(room, user):
    if room in games.keys():
        return 'Room id already exists!'
    if len(games) >= MAX_GAMES:
        return 'Room quantity exceeded!'
    games[room] = GameSession(room)
    games[room].players.append(Player(user, True))
    return ''

def create_player_in_room(room, user):
    if room not in games.keys():
        return "Room doesn't exist!"
    for player in games[room].players:
        if player.name == user:
            return 'Player name is taken!'
    games[room].players.append(Player(user, False))
    return ''

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
    if games[room].gameState != 'lobby':
        return "Can't choose the game mode while playing!"
    games[room].gameType = game
    # TODO: Validate game type
    return ''

def start_game(json):
    room = json['room']
    name = json['name']
    if room not in games.keys():
        return "Room doesn't exist!";
    player = games[room].get_player(name)
    if player == None:
        return "Player doesn't exist in room!"
    if player.isOwner == False:
        return "Player isn't an owner!"
    if games[room].gameState != 'lobby':
        return "Can't start the game while already playing!"
    games[room].gameState = 'playing'
    return ''

def get_gamestate(room):
    if room not in games.keys():
        return None
    res = {}
    res['room'] = room
    res['gameType'] = games[room].gameType
    res['gameState'] = games[room].gameState
    res['players'] = games[room].get_player_array()
    return res

def get_server_status():
    result = {}
    result['maxRooms'] = MAX_GAMES
    result['rooms'] = []
    for game in games.values():
        entry = {}
        entry['sessionId'] = game.room
        entry['userCount'] = len(game.players)
        result['rooms'].append(entry)
    return result

def can_create_new_game():
    return len(games) < MAX_GAMES

def init_game(room):
    pass