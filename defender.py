import pygame
import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')

current_enemies = []

@sio.on('new_enemy_in_queue')
def on_enemy_added(data):
    print(f"L'attaquant prépare un : {data['type']}")
    current_enemies.append(data['type'])

pygame.init()
screen = pygame.display.set_mode((800, 600))

running = True
while running:
    screen.fill((0, 50, 0))
    pygame.display.flip()