from enums import State
from models import MapObject, BaseObject
from models.player import AttackerPlayer, DefenderPlayer
import math
 
WAVE_BREAK    = 10.0   # secondes de préparation entre les vagues
WAVE_DURATION = 40.0   # secondes max de la phase de combat
class GameObject:
    def __init__(
        self,
        _round: int,
        _max_round: int,
        _attacker: AttackerPlayer,
        _defender: DefenderPlayer,
        _map: MapObject,
        _base: BaseObject,
        _tick_rate: float,
        _room_id: str,
        _socketio,
                    
    ):
        self.state = State.WAITING
        self.round = _round
        self.max_round = _max_round
        self.attacker = _attacker
        self.defender = _defender
        self.map = _map
        self.base = _base
        self.tick_rate = _tick_rate
        self.room_id = _room_id
        self.socketio = _socketio
        self.wave_phase   = "prep"       # "prep" | "fighting"
        self.wave_timer   = WAVE_BREAK   # compte à rebours affiché
        self.fight_timer  = WAVE_DURATION

 
    def start(self) -> None:
        self.state = State.PLAYING
 
    def game_loop(self, dt):
        if self.state != State.PLAYING:
            return

        if self.wave_phase == "prep":
            self.wave_timer -= dt
            if self.wave_timer <= 0:
                # Démarrer la phase de combat
                self.wave_phase  = "fighting"
                self.fight_timer = WAVE_DURATION
                print(f"[GAME] Vague {self.round} — combat !")

        else:  # fighting
            self.update_units(dt)
            self.update_towers(dt)
            self.attacker.collect_income(dt)
            self.fight_timer -= dt

            # Fin de vague : plus d'unités ET timer écoulé (ou juste timer)
            no_units   = len(self.map.units) == 0
            time_up    = self.fight_timer <= 0

            if time_up or (no_units and self.fight_timer < WAVE_DURATION - 5):
                self.next_round()

        self.check_game_over()
        self.broadcast_state()
 
 
    def update_units(self, dt: float) -> None:
        """Déplace chaque unité le long du chemin (waypoints)."""
        waypoints = self.map.waypoints
 
        for unit in list(self.map.units):
            wp_idx = unit.waypoint_index
            if not isinstance(wp_idx, int):
                # Compatibilité si stocké en tuple (x, y) — on reset
                unit.waypoint_index = 1
                wp_idx = 1
 
            if wp_idx >= len(waypoints):
                # L'unité a atteint la base
                self.base.get_attacked(unit.damage)
                self.map.remove_unit(unit)
                continue
 
            target_x, target_y = waypoints[wp_idx]
            dx = target_x - unit.x
            dy = target_y - unit.y
            dist = math.hypot(dx, dy)
            step = unit.speed * dt  # distance à parcourir ce tick
 
            if dist <= step:
                # Arrivé sur ce waypoint
                unit.x, unit.y = target_x, target_y
                unit.waypoint_index = wp_idx + 1
            else:
                # Avancer vers le waypoint
                unit.x += (dx / dist) * step
                unit.y += (dy / dist) * step
 
    def update_towers(self, dt: float) -> None:
        """Chaque tour cherche la cible la plus proche dans sa portée et attaque."""
        for tower in self.map.towers:
            tower.cooldown_remaining -= dt
            if tower.cooldown_remaining <= 0:
                units_in_range = [
                    u for u in self.map.units
                    if math.hypot(u.x - tower.x, u.y - tower.y) <= tower.attack_range
                ]
                if units_in_range:
                    tower.attack(units_in_range)   # attaque l'unité la plus proche
                    tower.cooldown_remaining = tower.attack_speed

 
    def check_game_over(self) -> None:
        if self.base.hp <= 0:
            self.end_game("attacker")
            return
        if self.round > self.max_round and len(self.map.units) == 0:
            self.end_game("defender")
 
    def next_round(self) -> None:
        self.round      += 1
        self.wave_phase  = "prep"
        self.wave_timer  = WAVE_BREAK
        self.attacker.earn(50 + 25 * (self.round - 1))
        self.defender.earn(50)
        print(f"[GAME] Vague terminée — repos {WAVE_BREAK}s")
 
    def end_game(self, winner: str) -> None:
        self.state = State.GAME_OVER
        self.socketio.emit("game_over", {"winner": winner}, room=self.room_id)
 
 
    def broadcast_state(self) -> None:
        self.socketio.emit("game_state_update", self.to_dict(), room=self.room_id)
 
    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "round": self.round,
            "max_round": self.max_round,
            "base_hp": self.base.hp,
            "base_max_hp": self.base.max_hp,
            "attacker_gold": self.attacker.gold,
            "defender_gold": self.defender.gold,
            "units": [u.to_dict() for u in self.map.units],
            "towers": [t.to_dict() for t in self.map.towers],
            "grid": self.map.to_grid(),
            "wave_phase":  self.wave_phase,
            "wave_timer":  round(self.wave_timer if self.wave_phase == "prep" else self.fight_timer, 1),
        }