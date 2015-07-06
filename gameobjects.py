import pygame

# functions are used for simplicity and demo purposes. 
# It has problems such as making assumptions that the game object has the
# appropriate variables.
# Assignment: use your favorite design pattern
def component_Gravity(GameObject):
    GameObject.velocity[1] -= 1

class GameObject:
    def __init__(self, image):
        image = pygame.image.load(image).convert()
        pos = [0, 0]
        image.set_colorkey([255, 128, 255])

        self.image = image
        self.pos = pos
        
        self.components = []

    def update(self, GameState):
        for component in self.components:
            component(self)
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'snake.png')
        self.velocity = [0, 0]
        self.components.append(component_Gravity)
        
        
    def update(self, GameState):
        keystate = pygame.key.get_pressed()
        #if GameState.joystick.get_axis(0) < -0.2:
        if keystate[pygame.K_LEFT]:
            self.velocity[0] -= 1 / 4
        #if GameState.joystick.get_axis(0) > 0.2:
        if keystate[pygame.K_RIGHT]:
            self.velocity[0] += 1 / 4
            
        GameObject.update(self, GameState)
        
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        
            
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
