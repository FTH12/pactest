import hashlib
import os
from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

def runpachong(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_page = soup.find("li", class_="next")
    disabled = soup.find("li", class_ = "next disabled")
    game_list = soup.find('div', class_='ztliswrap')
    games = game_list.find_all('div', class_='lis')
    game_list = []
    game_list.extend(get_games(games))
    if disabled:
        return game_list
    npurl = next_page.find("a").get("href")
    print(npurl)
    game_list.extend(runpachong(npurl))
    return game_list


def solveinfo(info:Tag):
    lis = info.find_all('li')
    inf_dic = {}
    for ls in lis:
        k_v = ls.text.split("：")
        k = k_v[0]
        v = k_v[1].strip(" ")
        if(k=='发售'):
            v = v.replace(" ","")
        inf_dic[k]=v
    return inf_dic

def merge_dic(name,game_md5,img,info,jj):
    game = {'name':name,'name_md5':game_md5, 'img':img}
    game.update(info)
    game['jianjie'] = jj
    return game

def md5tool(str):
    return hashlib.md5(str.encode()).hexdigest()

def get_games(games):
    img_path = os.getcwd() + '\gameimg\\'
    game_list = []
    for game in games:
        # 游戏名
        game_name = game.find("a", class_='bt').text.replace(" ", "").strip()
        # 跳过广告游戏
        if (game_name == '3DM自营《热血封神》'):
            continue
        # 游戏图片
        game_img = game.find("img").attrs['data-original']
        game_name_md5 = md5tool(game_name)
        img_fomat = game_img[-4:]
        game_img_name = game_name_md5 + img_fomat
        # print(game_img_name)
        urlretrieve(game_img, img_path + game_img_name)
        # 游戏信息
        game_info = game.find("ul", class_='info')
        game_info = solveinfo(game_info)
        # 游戏简介
        game_jj = game.find("div", class_="miaoshu").text
        game_jj = game_jj.strip('\n ')
        game_list.append(merge_dic(game_name, game_name_md5, game_img_name, game_info, game_jj))
    return game_list