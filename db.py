import json
from settings import DATABASE_PATH as path

def write_highscore(score):
    if float(score) > float(read_highscore()):
        file = open(path, "w")
        json.dump({"highscore": score}, file)
        file.close()

def read_highscore():
    file = open(path, "r")
    file_data = json.load(file)
    file.close()
    return file_data['highscore']