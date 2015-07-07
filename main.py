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

        GameObjects = []

        player1 = gameobjects.Hero()
        GameObjects.append(gameobjects.Platform([0, 400]))
        GameObjects.append(gameobjects.Platform([100, 400]))
        GameObjects.append(gameobjects.Platform([200, 400]))
        GameObjects.append(gameobjects.Platform([300, 300]))
        GameObjects.append(gameobjects.Enemy())
        GameObjects.append(player1)
        
        self.GameObjects = GameObjects
        
    def update(self):
        for GO in self.GameObjects:
            GO.update(stage1)
    
    def draw(self, surface):
        for GO in self.GameObjects:
            GO.draw(surface)    

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
        
    stage1.update()
    stage1.draw(surface)
        
    pygame.display.update()
    clock.tick(60)