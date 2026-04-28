# Walkthrough — Frontend React + Backend Flask-SocketIO

## Ce qui a été créé

### Backend Flask-SocketIO

| Fichier | Description |
|---|---|
| [__init__.py](file:///flaskr/__init__.py) | Factory app Flask + SocketIO + CORS |
| [routes.py](file:///flaskr/routes.py) | Routes HTTP (`/`, `/health`) |
| [events.py](file:///flaskr/events.py) | Handlers WebSocket : `create_room`, `join_room`, `player_ready`, `place_tower`, `send_unit`, `sell_tower`, `disconnect` |
| [run.py](file:///run.py) | Point d'entrée `socketio.run(app)` |

### Frontend React (Vite)

| Fichier | Description |
|---|---|
| [App.jsx](file:///frontend/src/App.jsx) | Router : Lobby → GameBoard |
| [useSocket.js](file:///frontend/src/hooks/useSocket.js) | Hook custom Socket.IO (connect, emit, on) |
| [socketEvents.js](file:///frontend/src/utils/socketEvents.js) | Constantes des noms d'événements |
| [Lobby.jsx](file:///frontend/src/components/Lobby.jsx) | Créer/rejoindre une room, bouton "Prêt" |
| [GameBoard.jsx](file:///frontend/src/components/GameBoard.jsx) | Conteneur principal (HUD + Grid + Shop) |
| [GameGrid.jsx](file:///frontend/src/components/GameGrid.jsx) | Grille 2D prête à recevoir les données backend |
| [HUD.jsx](file:///frontend/src/components/HUD.jsx) | Or, vies, vague |
| [TowerShop.jsx](file:///frontend/src/components/TowerShop.jsx) | Sélection des tours (défenseur) ou envoi d'unités (attaquant) |

---

## Comment lancer

**Terminal 1 — Backend Flask :**
```bash
cd Tower-defence_Fil-rouge
.\.venv\Scripts\activate
python run.py
```
→ Tourne sur `http://localhost:5000`

**Terminal 2 — Frontend React :**
```bash
cd Tower-defence_Fil-rouge/frontend
npm run dev
```
→ Tourne sur `http://localhost:5173`

---

## Flux WebSocket

```
Lobby → create_room / join_room → player_ready → game_start
                                                      ↓
                                                 GameBoard
                                                      ↓
                              ← game_state_update ← (backend game loop)
                              → place_tower / send_unit / sell_tower →
                                                      ↓
                              ← game_over ←
```

---

## Ce qu'il reste à faire

1. **Grille 2D côté backend** : `MapObject` doit exposer un `to_grid()` qui retourne un tableau 2D de `{"type": "grass|path|water|spawn|base"}`
2. **Intégrer le `GameObject`** dans `events.py` : créer une vraie partie dans `on_player_ready`
3. **Lancer la game loop** avec `eventlet.spawn` pour envoyer `game_state_update` à chaque tick

## Validation

- ✅ `npm run build` → build OK (57 modules, 0 erreurs)
- ✅ `from flaskr import create_app` → Flask app créée sans erreur
