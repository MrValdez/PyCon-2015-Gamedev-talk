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

        self.player1 = gameobjects.Hero()
        self.player1.pos = [110, 0]
        GameObjects.append(gameobjects.Platform([100, 400]))
        GameObjects.append(gameobjects.Platform([200, 400]))
        GameObjects.append(gameobjects.Platform([300, 400]))
        GameObjects.append(gameobjects.Platform([400, 300]))
        GameObjects.append(gameobjects.Platform([500, 300]))
        GameObjects.append(gameobjects.Platform([600, 300]))
        GameObjects.append(gameobjects.Platform([0, 300]))
        GameObjects.append(gameobjects.Enemy())
        GameObjects.append(self.player1)
        
        self.GameObjects = GameObjects
        
        self.background = pygame.image.load('background.png')
        self.background = self.background.convert()         # we need to convert the image to something that is native to pygame
                                                             # try commenting this to see the effect on the FPS
        
        # to allow scrolling, we have to separate the game world from the camera
        self.gameWorld = pygame.Surface([1280, 960])       
        self.gameWorld = self.gameWorld.convert()       
        self.camera_pos = [0, 0]
        
    def update(self):
        # starting from the top, uncomment each line to see the effect of each camera_pos style
        #self.camera_pos = [self.player1.pos[0], self.player1.pos[1]]
        #self.camera_pos = [self.player1.pos[0], 0]
        #self.camera_pos = [-self.player1.pos[0], 0]
        #self.camera_pos = [-self.player1.pos[0] + 100, 0]
        
        for GO in self.GameObjects:
            GO.update(stage1)
    
    def draw(self, surface):
        self.gameWorld.blit(self.background, [0, 0])
        
        for GO in self.GameObjects:
            GO.draw(self.gameWorld)    
            
        surface.blit(self.gameWorld, self.camera_pos)

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