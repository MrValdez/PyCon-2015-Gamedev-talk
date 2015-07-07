import pygame

def component_Gravity(GameObject, GameState):
    GameObject.velocity[1] += 0.1

def component_Movement(GameObject, GameState):
    GameObject.pos[0] += GameObject.velocity[0]
    GameObject.pos[1] += GameObject.velocity[1]

def component_Collidable(GameObject, GameState):
    for target in GameState.GameObjects:
        if target == GameObject:
            # do not perform collision detection against the same object
            continue
            
        box1 = GameObject.image.get_rect()
        box1 = box1.move(GameObject.pos)
        box2 = target.image.get_rect()
        box2 = box2.move(target.pos)

        if box1.colliderect(box2):
            GameObject.event_collide(target)

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
            component(self, GameState)
        
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Hero(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'snake.png')
        self.velocity = [0, 0]
        self.components.append(component_Gravity)        
        self.components.append(component_Movement)        
        self.components.append(component_Collidable)        
        
    def update(self, GameState):
        keystate = pygame.key.get_pressed()
        #if GameState.joystick.get_axis(0) < -0.2:
        if keystate[pygame.K_LEFT]:
            self.velocity[0] -= 1 / 4
        #if GameState.joystick.get_axis(0) > 0.2:
        if keystate[pygame.K_RIGHT]:
            self.velocity[0] += 1 / 4
            
        GameObject.update(self, GameState)
        
    def event_collide(self, target):
        print("Hero has collided")
            
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
        self.velocity = [0, 0]
        self.components.append(component_Gravity)        
        self.components.append(component_Movement)        

class Platform(GameObject):
    def __init__(self, pos):
        GameObject.__init__(self, 'RTS_Crate.png')
        self.pos = pos
