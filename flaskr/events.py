import eventlet
from flask import request
from flask_socketio import emit, join_room, leave_room
from . import socketio
 
from enums import Team, TowerType, UnitType
from game import GameObject
from models.game_map import MapObject
from models.base import BaseObject
from models.player import AttackerPlayer, DefenderPlayer
from models.map_def import DEFAULT_WAYPOINTS, SPAWN_POS, BASE_POS
 

# { room_id: { "players": { sid: {...} }, "game": GameObject | None } }
rooms = {}
 
# Tick rate : 20 fois par seconde
TICK_RATE = 1 / 20
 
 
def _make_game(room_id: str, players_data: dict) -> GameObject:
    """Fabrique un GameObject complet à partir des données de la room."""
    base = BaseObject(_id=1, _hp=100, _max_hp=100, _x=BASE_POS[0], _y=BASE_POS[1])
    game_map = MapObject(_base=base, _units=[], _towers=[])
 
    # Identifier les SIDs par team
    defender_sid = next(
        sid for sid, p in players_data.items() if p["team"] == "defender"
    )
    attacker_sid = next(
        sid for sid, p in players_data.items() if p["team"] == "attacker"
    )
 
    defender = DefenderPlayer(
        _id=1,
        _username=players_data[defender_sid]["username"],
        _gold=150,
        _team=Team.DEFENDER,
        _map=game_map,
        _towers=[],
        _base=base,
    )
    attacker = AttackerPlayer(
        _id=2,
        _username=players_data[attacker_sid]["username"],
        _gold=100,
        _team=Team.ATTACKER,
        _map=game_map,
        _units_sent=[],
        _income_rate=5,          # 5 or/seconde
    )
 
    game = GameObject(
        _round=1,
        _max_round=10,
        _attacker=attacker,
        _defender=defender,
        _map=game_map,
        _base=base,
        _tick_rate=TICK_RATE,
        _room_id=room_id,
        _socketio=socketio,
    )
    return game
 
 
def _game_loop(room_id: str) -> None:
    """Boucle de jeu tournant dans un greenlet eventlet."""
    game = rooms[room_id]["game"]
    game.start()
 
    while room_id in rooms and rooms[room_id]["game"] is not None:
        game = rooms[room_id]["game"]
 
        if game.state.value == "game_over":
            break
 
        # Tick principal (mouvement, tirs, broadcast)
        game.game_loop(TICK_RATE)
 
        eventlet.sleep(TICK_RATE)
 
    print(f"[LOOP] Game loop terminée pour la room '{room_id}'")
 
 
def _find_room_of(sid: str):
    """Retourne (room_id, room_data) pour un SID donné, ou (None, None)."""
    for room_id, room_data in rooms.items():
        if sid in room_data["players"]:
            return room_id, room_data
    return None, None


@socketio.on('connect')
def on_connect():
    print(f"[WS] Client connecté : {request.sid}")
    emit('connection_success', {'sid': request.sid})


@socketio.on('disconnect')
def on_disconnect():
    print(f"[WS] Client déconnecté : {request.sid}")
    # Nettoyer le joueur de sa room
    for room_id, room_data in list(rooms.items()):
        if request.sid in room_data['players']:
            del room_data['players'][request.sid]
            emit('player_left', {'sid': request.sid}, room=room_id)
            # Si la room est vide, la supprimer
            if not room_data['players']:
                del rooms[room_id]
            break


@socketio.on('create_room')
def on_create_room(data):
    """Créer une nouvelle room. Le créateur devient le défenseur."""
    room_id = data.get('room_id')
    username = data.get('username', 'Joueur')

    if room_id in rooms:
        emit('error', {'message': 'Cette room existe déjà'})
        return

    rooms[room_id] = {
        'players': {
            request.sid: {'username': username, 'team': 'defender', 'ready': False}
        },
        'game': None  # Sera initialisé quand les 2 joueurs seront prêts
    }

    join_room(room_id)
    emit('room_created', {'room_id': room_id, 'team': 'defender'})
    print(f"[WS] Room '{room_id}' créée par {username}")


@socketio.on('join_room')
def on_join_room(data):
    """Rejoindre une room existante. Le 2ème joueur devient l'attaquant."""
    room_id = data.get('room_id')
    username = data.get('username', 'Joueur')

    if room_id not in rooms:
        emit('error', {'message': 'Room introuvable'})
        return

    room_data = rooms[room_id]

    if len(room_data['players']) >= 2:
        emit('error', {'message': 'Room pleine'})
        return

    room_data['players'][request.sid] = {
        'username': username,
        'team': 'attacker',
        'ready': False
    }

    join_room(room_id)
    emit('room_joined', {'room_id': room_id, 'team': 'attacker'})
    emit('player_joined', {
        'username': username,
        'team': 'attacker',
        'player_count': len(room_data['players'])
    }, room=room_id)

    print(f"[WS] {username} a rejoint la room '{room_id}'")


@socketio.on('player_ready')
def on_player_ready(data):
    """Le joueur signale qu'il est prêt. Quand les 2 sont prêts, la partie démarre."""
    room_id = data.get('room_id')

    if room_id not in rooms:
        return

    room_data = rooms[room_id]
    if request.sid in room_data['players']:
        room_data['players'][request.sid]['ready'] = True

    # Vérifier si tous les joueurs sont prêts
    all_ready = (
        len(room_data['players']) == 2
        and all(p['ready'] for p in room_data['players'].values())
    )

    if all_ready:
        # Créer la partie
        game = _make_game(room_id, room_data["players"])
        room_data["game"] = game

        emit('game_start', {
            'room_id': room_id,
            'players': {
                sid: {'username': p['username'], 'team': p['team']}
                for sid, p in room_data['players'].items()
            }
        }, room=room_id)
        
        socketio.emit('game_state_update', game.to_dict(), room=room_id)
        eventlet.spawn(_game_loop, room_id)


@socketio.on('place_tower')
def on_place_tower(data):
    """Le défenseur place une tour."""
    room_id = data.get('room_id')
    tower_type = data.get('type')
    x = data.get('x')
    y = data.get('y')

    if room_id not in rooms:
        return

    # Vérifier que c'est bien le défenseur
    player = rooms[room_id]['players'].get(request.sid)
    if not player or player['team'] != 'defender':
        emit('error', {'message': 'Seul le défenseur peut placer des tours'})
        return

    game = rooms[room_id].get("game")
    if game is None:
        return
 
    try:
        tower = TowerType[tower_type]
    except KeyError:
        emit("error", {"message": f"Type de tour inconnu : {tower_type}"})
        return
 
    game.defender.place_tower(tower, x, y)
    emit('tower_placed', {'type': tower_type, 'x': x, 'y': y}, room=room_id)


@socketio.on('send_unit')
def on_send_unit(data):
    """L'attaquant envoie une unité."""
    room_id = data.get('room_id')
    unit_type = data.get('type')

    if room_id not in rooms:
        return

    # Vérifier que c'est bien l'attaquant
    player = rooms[room_id]['players'].get(request.sid)
    if not player or player['team'] != 'attacker':
        emit('error', {'message': "Seul l'attaquant peut envoyer des unités"})
        return

    game = rooms[room_id].get("game")
    if game is None:
        return
 
    try:
        unit_type = UnitType[unit_type]
    except KeyError:
        emit("error", {"message": f"Type d'unité inconnu : {unit_type}"})
        return
 
    game.attacker.send_unit(unit_type)
    emit('unit_sent', {'type': unit_type}, room=room_id)


@socketio.on('sell_tower')
def on_sell_tower(data):
    """Le défenseur vend une tour."""
    room_id = data.get('room_id')
    tower_id = data.get('tower_id')

    if room_id not in rooms:
        return

    player = rooms[room_id]['players'].get(request.sid)
    if not player or player['team'] != 'defender':
        emit('error', {'message': 'Seul le défenseur peut vendre des tours'})
        return

    game = rooms[room_id].get("game")
    if game is None:
        return
 
    # Chercher la tour par ID
    tower = next((t for t in game.map.towers if t.id == tower_id), None)
    if tower is None:
        emit("error", {"message": "Tour introuvable"})
        return
 
    game.defender.sell_tower(tower)
    emit('tower_sold', {'tower_id': tower_id}, room=room_id)