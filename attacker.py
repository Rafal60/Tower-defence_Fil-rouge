import pygame
import socketio

sio = socketio.Client()
sio.connect('http://localhost:5000')

# Pygame Init
pygame.init()
screen = pygame.display.set_mode((800, 600))


def send_monster(m_type):
    sio.emit('spawn_enemy', {'type': m_type})


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Appuie sur 1 pour envoyer un monstre
                send_monster("goblin")

    screen.fill((50, 0, 0))  # Fond rouge pour l'attaquant
    pygame.display.flip()