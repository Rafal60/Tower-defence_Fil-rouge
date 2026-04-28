from flask import request
from flask_socketio import emit, join_room, leave_room
from . import socketio

# Stocke les parties en cours : { room_id: { "players": {...}, "game": GameObject } }
rooms = {}


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
        # TODO: Initialiser le GameObject ici
        # room_data['game'] = GameObject(...)
        emit('game_start', {
            'room_id': room_id,
            'players': {
                sid: {'username': p['username'], 'team': p['team']}
                for sid, p in room_data['players'].items()
            }
        }, room=room_id)
        print(f"[WS] Partie démarrée dans la room '{room_id}'")


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

    # TODO: Appeler game.defender.place_tower(tower_type, x, y)
    # Puis broadcast le nouvel état
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

    # TODO: Appeler game.attacker.send_unit(unit_type)
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

    # TODO: Appeler game.defender.sell_tower(tower)
    emit('tower_sold', {'tower_id': tower_id}, room=room_id)
