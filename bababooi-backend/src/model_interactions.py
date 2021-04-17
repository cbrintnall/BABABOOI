import os, boto3, json
import gamestate

def load_data_local():
    data_path = os.environ.get("DATA_PATH")
    info_file = os.environ.get("INFO_FILENAME", "info.json")

    with open(f"{data_path}/{info_file}", "r") as f:
        gamestate.bababooi_data["info"] = json.loads(f.read())
        gamestate.bababooi_data["img"] = {}

        for class_name in gamestate.bababooi_data['info']['class_names']:
            filename = f"{data_path}/{class_name}.ndjson"
            gamestate.bababooi_data["img"][class_name] = []
            with open(filename, "r") as drawings:
                drawings_data = drawings.read()
                for line in drawings_data.split("\n"):
                    if line:
                        gamestate.bababooi_data["img"][class_name].append(json.loads(line))
    
    print("finished local load")

def preload():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('bababooi')

    # Load bababooi data

    # TODO: Remove this cache for prod
    if not os.path.isfile('cached_bababooi.txt'):
        info = bucket.Object('games/adv_draw/info.json')
        gamestate.bababooi_data['info'] = json.loads(info.get()['Body'].read())
        gamestate.bababooi_data['img'] = {}
        for class_name in gamestate.bababooi_data['info']['class_names']:
            filename = 'games/adv_draw/' + class_name + '.ndjson'
            imgs = bucket.Object(filename)
            gamestate.bababooi_data['img'][class_name] = []
            imgFileStr = imgs.get()['Body'].read()
            for line in imgFileStr.splitlines():
                gamestate.bababooi_data['img'][class_name].append(json.loads(line))
        with open('cached_bababooi.txt', 'w') as fp:
            fp.write(json.dumps(gamestate.bababooi_data))
    else:
        with open('cached_bababooi.txt', 'r') as fp:
            gamestate.bababooi_data = json.loads(fp.read())
 
    gamestate.masked_feud_data['prompts'] = []
    gamestate.masked_feud_data['prompts'].append('I love eating [MASK].')
    gamestate.masked_feud_data['prompts'].append('The first thing I do after work is [MASK].')
    gamestate.masked_feud_data['prompts'].append('Who ate my [MASK]?')
    gamestate.masked_feud_data['prompts'].append('I prefer [MASK] over dogs.')
    gamestate.masked_feud_data['prompts'].append('I no longer love [MASK].')
    