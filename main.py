import json

from utils import runpachong


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = 'http://www.3dmgame.com/games/zq/'
    urltest = 'https://www.3dmgame.com/games/zq_84/'
    game_list = runpachong(url)
    # print(game_list)
    with open ("games.json",'a+',encoding='utf-8') as f:
        json.dump(game_list,fp=f,ensure_ascii=False,indent=2)