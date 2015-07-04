import pygame

pygame.init()
clock = pygame.time.Clock()


resolution = [640, 480]
surface = pygame.display.set_mode(resolution)
pygame.joystick.init()

class GameState:
    def __init__(self):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

class GameObject:
    def __init__(self, image):
        image = pygame.image.load(image).convert()
        pos = [0, 0]
        image.set_colorkey([255, 128, 255])

        self.image = image
        self.pos = pos

    def update(self):
        pass
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'snake.png')
        self.velocity = [0, 0]
        
    def update(self, GameState):
        keystate = pygame.key.get_pressed()
        if GameState.joystick.get_axis(0) < -0.2:
            self.velocity[0] -= 1 / 4
        if GameState.joystick.get_axis(0) > 0.2:
            self.velocity[0] += 1 / 4
            
        self.pos[0] += self.velocity[0]
            
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
        

player1 = Hero()
enemy = Enemy()

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

    player1.update(stage1)
    enemy.update()
    
    player1.draw(surface)
    #enemy.draw(surface)
    
    pygame.display.update()
    clock.tick(60)