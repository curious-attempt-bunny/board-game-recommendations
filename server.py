from flask import Flask
from flask import render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def hello():
    games = [68448, # 7 Wonders
             5, #Acquire
             15987, # Arkham Horror
             822,   # Carcassonne
             50381, # Cards Against Humanity
             104162, # Descent: Journeys in the Dark (Second Edition)
             #36218, # Dominion
             161936] # Pandemic Legacy: Season 1

    return render_template('home.html', games = games, metadata=metadata)

similarity = pd.read_csv('similarity.csv', encoding='utf-8', index_col=0)
metadata = pd.read_csv('metadata.csv', encoding='utf-8', index_col=0)
@app.route('/boardgame/<game_id>')
def boardgame(game_id):
    game_id = int(game_id)
    similar_games = similarity.loc[game_id].sort_values(ascending=False)[1:8]
    return render_template('boardgame.html', game_id=game_id, similar_games = zip(similar_games.index.values.astype(int), similar_games.values), metadata=metadata)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

