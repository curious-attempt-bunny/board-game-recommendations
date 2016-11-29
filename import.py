import pandas as pd
import numpy as np
import requests
import time
from xml.etree import ElementTree
import sys
import threading

game_ratings = pd.DataFrame([])
game_ratings = pd.read_csv('game_ratings.csv', encoding='utf-8', index_col=0)
user_games = pd.DataFrame([])

games_done = set(game_ratings.index.values)
users_done = set()

lock = threading.Lock()

def addgame(df, game_id):
    lock.acquire()
    is_done = game_id in games_done
        
    if is_done:
        print('Skipping %d, already loaded.' % game_id)
        lock.release()
        return
    
    games_done.add(game_id)
    lock.release()    
    
    url = "http://www.boardgamegeek.com/xmlapi/boardgame/%d?comments=1&pagesize=100" % game_id
    page = 1
    
    total = 0
    votes = 0

    
    try:
        while(True):
            sys.stdout.write('.')
            sys.stdout.flush()
    #         print('Getting page %d...' % page)
            r = False
            for i in np.arange(5):
                try:
                    r = requests.get('%s&page=%d' % (url,page))
                    if r.status_code != 200:
                        print("Sleeping. Status code %d." % r.status_code)
                        time.sleep(30)
                    else:
                        break
                except Exception as detail:
                    print('Failed to get: ', detail)
                    time.sleep(1)
                    pass
            if r == False:
                print('Aborted after max retries')
                break

            tree = ElementTree.fromstring(r.content)
            assert tree.tag == 'boardgames', 'tree.tag : "%s" %s' % (tree.tag, r.content)

            if page == 1:
    #             print(r.content)
                print('%d is %s' % (game_id, tree.findall(".//name[@primary='true']")[0].text))

            comments = tree.findall(".//comment")
    #         print("comments ", len(comments))
    #         print()

            for comment in comments:
                if comment.get('rating') != 'N/A':
#                     print(comment.get('username'),comment.get('rating'))
                    username = comment.get('username')
                    rating = float(comment.get('rating'))
                    lock.acquire()
                    df.loc[game_id,username] = rating
                    lock.release()
                    votes = votes + 1
                    total = total + float(comment.get('rating'))
            
            if len(comments) != 100:
                break

            page = page + 1

        # print('%d votes added.' % votes)
    except Exception as detail:
        print('Caught an error... :(', detail)
        pass
    
    return df

def get_user(user_games, user):
    print('Getting user %s' % user)
    url = "http://www.boardgamegeek.com/xmlapi/collection/" + user
    r = requests.get(url)
    while(r.status_code == 202):
        time.sleep(1)
        print("Slept 1")
        r = requests.get(url)
        
#     print(r.content)
    tree = ElementTree.fromstring(r.content)
    
    lock.acquire()    
    for game in tree.findall(".//item[@subtype='boardgame']"):
        user_games.loc[user, game.get('objectid')] = 1
    lock.release()
    
#     print(r.content)
    
    return user_games

def find_a_user(game_ratings, user_games):
    lock.acquire()    
    users = list(set(game_ratings.columns.values).difference(users_done))
    if len(users) == 0:
        return
    user = users[0]
    users_done.add(user)
    lock.release()    
    return get_user(user_games, user)

def find_game(game_ratings, user_games):
    lock.acquire()    
    games = user_games.sum().sort_values(ascending=False).index.values
    lock.release()    
    print("#games: %d" % len(games))
    for game_id in games:
        game_id = int(game_id)
        lock.acquire()
        is_done = not(game_id in games_done)
        lock.release()
        if is_done:
            # print('Found %d' % game_id)
        
            return addgame(game_ratings, game_id)

    print('Getting more users')
    find_a_user(game_ratings, user_games)
    return find_game(game_ratings, user_games)
        
# find_a_user(game_ratings, user_games)

class MyThread ( threading.Thread ):
    def run(self):
        while(True):
            find_game(game_ratings, user_games)
            lock.acquire()
            print("[%d]" % game_ratings.index.values.shape[0])
            if game_ratings.index.values.shape[0] % 50 == 0:
                print("%d. Persisting." % game_ratings.index.values.shape[0])
                game_ratings.to_csv('game_ratings.csv', encoding='utf-8')            
            lock.release()

# get_user(user_games, 'hitechbunny')
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()    
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()    
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()    
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()
MyThread().start()    