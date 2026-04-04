from flask import Flask
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

# --- Logique de synchronisation ---
game_state = {
    "enemies_queued": [],
    "towers_placed": [],
    "defender_hp": 100,
    "wave_active": False
}

@socketio.on('spawn_enemy')
def handle_spawn(data):
    enemy_type = data['type']
    game_state["enemies_queued"].append(enemy_type)
    emit('new_enemy_in_queue', {'type': enemy_type}, broadcast=True)

@socketio.on('tower_placed')
def handle_tower(data):
    game_state["towers_placed"].append(data)
    emit('update_towers', data, broadcast=True)

@socketio.on('start_wave')
def start_wave():
    game_state["wave_active"] = True
    emit('wave_started', game_state["enemies_queued"], broadcast=True)
    game_state["enemies_queued"] = []

if __name__ == '__main__':
    socketio.run(app, port=5000)