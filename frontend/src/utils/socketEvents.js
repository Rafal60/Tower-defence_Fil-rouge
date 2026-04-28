/**
 * Constantes des événements WebSocket.
 * Utilisées côté client et correspondant aux handlers dans flaskr/events.py.
 */

// Client → Serveur
export const EMIT = {
  CREATE_ROOM: 'create_room',
  JOIN_ROOM: 'join_room',
  PLAYER_READY: 'player_ready',
  PLACE_TOWER: 'place_tower',
  SEND_UNIT: 'send_unit',
  SELL_TOWER: 'sell_tower',
};

// Serveur → Client
export const ON = {
  CONNECTION_SUCCESS: 'connection_success',
  ROOM_CREATED: 'room_created',
  ROOM_JOINED: 'room_joined',
  PLAYER_JOINED: 'player_joined',
  PLAYER_LEFT: 'player_left',
  GAME_START: 'game_start',
  GAME_STATE_UPDATE: 'game_state_update',
  GAME_OVER: 'game_over',
  TOWER_PLACED: 'tower_placed',
  UNIT_SENT: 'unit_sent',
  TOWER_SOLD: 'tower_sold',
  ERROR: 'error',
};
