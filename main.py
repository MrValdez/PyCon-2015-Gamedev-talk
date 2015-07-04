import pygame

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

class GameObject:
    def __init__(self, image):
        image = pygame.image.load(image).convert()
        pos = [0, 0]
        image.set_colorkey([255, 128, 255])

        self.image = image
        self.pos = pos

    def update(self, GameState):
        pass
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'snake.png')
        self.velocity = [0, 0]
        
    def update(self, GameState):
        keystate = pygame.key.get_pressed()
        #if GameState.joystick.get_axis(0) < -0.2:
        if keystate[pygame.K_LEFT]:
            self.velocity[0] -= 1 / 4
        #if GameState.joystick.get_axis(0) > 0.2:
        if keystate[pygame.K_RIGHT]:
            self.velocity[0] += 1 / 4
            
        self.pos[0] += self.velocity[0]
            
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
        
GameObjects = []

player1 = Hero()
GameObjects.append(player1)
GameObjects.append(Enemy())

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