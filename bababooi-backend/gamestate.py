import math
import random
import requests

from dataclasses import dataclass, field
from datetime import datetime, timezone

MAX_GAMES = 10

@dataclass
class Player:
    name: str
    isOwner: bool = False
    gameScore: int = 0
    totalScore: int = 0
    def to_dict(self):
        return {"name": self.name, "isOwner": self.isOwner}

@dataclass
class GameSession:
    room: str
    players: list = field(default_factory=list)
    gameType: str = "bababooi"
    gameState: str = "lobby"
    gameSpecificData: dict = field(default_factory=dict)
    roundNo: int = 0
    roundLimit: int = 3 # can be changed per-game

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

    def reset(self):
        for p in self.players:
            p.gameScore = 0
        self.gameSpecificData = {}
        self.roundNo = 0
        self.gameState = "lobby"

games = {}
bababooi_data = {}
masked_feud_data = {}

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
        return "Room doesn't exist!"
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

def init_game(room):
    if room not in games.keys():
        return "Room doesn't exist!"
    game = games[room]
    mode = game.gameType

    if mode == 'bababooi':
        game.roundLimit = 3
        bababooi_init_round(game)
    elif mode == 'masked_feud':
        game.roundLimit = 3
        masked_feud_init_round(game)
    else:
        return "Game doesn't exist"

    return None

def masked_feud_init_round(game):
    state = game.gameSpecificData

    # Select our prompts for this game
    state['prompts'] = random.sample(masked_feud_data['prompts'], game.roundLimit)
    state['prompt_answers'] = []

    p = random.choice(game.players)
    state['current_player'] = p.name
    state['current_player_index'] = game.players.index(p)

    for p in state['prompts']:
        json = requests.post('http://127.0.0.1:5001/nlpfeud', json=p).json()

        state['prompt_answers'].append({})
        for k, v in json['probs']:
            worth = math.ceil(v * 100)
            state['prompt_answers'][-1][k] = {
                'worth' : worth,
                'revealed' : False
            }


def bababooi_init_round(game):
    state = game.gameSpecificData
    num_classes = len(bababooi_data['info']['class_names'])
    classes = random.sample(range(0, num_classes), 2)
    startClassName = bababooi_data['info']['class_names'][classes[0]]
    img_idx = random.randint(0, len(bababooi_data['img'][startClassName]))
    state['startingClassIdx'] = classes[0]
    state['targetClassIdx'] = classes[1]
    state['startingClassName'] = bababooi_data['info']['proper_names'][classes[0]]
    state['targetClassName'] = bababooi_data['info']['proper_names'][classes[1]]
    state['startingImg'] = bababooi_data['img'][startClassName][img_idx]['drawing']
    state['startingTime'] = str(datetime.now(timezone.utc).isoformat())

def bababooi_score_round(game):
    pass

def start_game(json):
    room = json['room']
    name = json['name']
    if room not in games.keys():
        return "Room doesn't exist!"
    player = games[room].get_player(name)
    if player == None:
        return "Player doesn't exist in room!"
    if player.isOwner == False:
        return "Player isn't an owner!"
    if games[room].gameState != 'lobby':
        return "Can't start the game while already playing!"
    # Clear player prev round scores
    for player in games[room].players:
        player.gameScore = 0
    games[room].gameState = 'playing'
    result = init_game(room)
    return '' if result is None else result


def get_gamestate(room):
    if room not in games.keys():
        return None
    res = {}
    game = games[room]
    res['room'] = room
    res['gameType'] = game.gameType
    res['gameState'] = game.gameState
    res['gameSpecificData'] = game.gameSpecificData
    res['players'] = game.get_player_array()
    return res

def submit_image(json):
    room = json['room']
    name = json['name']
    img = json['data'] # TODO: decode img
    game = games[room]


def submit_text(json):
    name, room, text = json['name'], json['room'], json['text']
    game = games[room]

    if game.gameType == 'masked_feud':
        return handle_masked_feud_submit_text(game, text)
    else:
        return "Current game doesn't support submit text"



def handle_masked_feud_submit_text(game, text):
    state = game.gameSpecificData

    round_over = False
    game_over = False
    prompt_answers = state['prompt_answers'][game.roundNo]

    # The text is an answer and was not revealed yet
    if text in prompt_answers and not prompt_answers[text]['revealed']:
        # Answer is now revealed
        prompt_answers[text]['revealed'] = True

        # Get current player and set their score
        player = game.players[state['current_player_index']]
        player.gameScore += prompt_answers[text]['worth']

        round_over = all([prompt_answers[k]['revealed'] for k in prompt_answers])

        if round_over:
            game.roundNo += 1
            game_over = game.roundNo == game.roundLimit

    if game_over:
        # If the game is over, determine who won this game and return us to the lobby
        winning_player = max(game.players, key=lambda p : p.gameScore)
        winning_player.totalScore += 1
        game.reset()
    else:
        # If the game isn't over, just choose whoever is next
        state['current_player_index'] = (state['current_player_index'] + 1) % len(game.players)
        state['current_player'] = game.players[state['current_player_index']].name

    return ''


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
