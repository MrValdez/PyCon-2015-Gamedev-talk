import pygame

import gameobjects

pygame.init()
clock = pygame.time.Clock()

resolution = [640, 480]
surface = pygame.display.set_mode(resolution)
#pygame.joystick.init()     # disable joystick if you have no joystick connected

class GameState:
    def __init__(self):
        #self.joystick = pygame.joystick.Joystick(0)
        #self.joystick.init()
        pass
        
GameObjects = []

player1 = gameobjects.Hero()
GameObjects.append(player1)
GameObjects.append(gameobjects.Enemy())
GameObjects.append(gameobjects.Platform([0, 400]))

stage1 = GameState()

while True:
    surface.fill([255, 255, 255])
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        pygame.quit()

    for GO in GameObjects:
        GO.update(stage1)
        
    for GO in GameObjects:
        GO.draw(surface)    
        
    pygame.display.update()
    clock.tick(60)