import pygame

pygame.init()
clock = pygame.time.Clock()

resolution = [640, 480]
surface = pygame.display.set_mode(resolution)

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
        
    def update(self):
        self.pos[0] += 1

player1 = Hero()

while True:
    surface.fill([255, 255, 255])
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        pygame.quit()

    player1.draw(surface)
    pygame.display.update()
    clock.tick(60)