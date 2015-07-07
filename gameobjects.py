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
            if 'event_collide' in dir(GameObject):
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
        box1 = self.image.get_rect()
        box1 = box1.move(self.pos)
        box2 = target.image.get_rect()
        box2 = box2.move(target.pos)
                
        # In games, the collision between objects inside the engine is different from the sprite on screen.
        # This is to lower frustration on 'pixel-perfect' collision. Example:
        #   1. The fireball on-screen hits the player. With pixel-perfect collision, the fireball will collide
        #      with the player as soon as it touches the collision box. If we lower the fireball's collision
        #      box, the player will have a feeling of "I almost got hit. I'm so lucky it didn't"
        #   2. For platforms, it is possible for a player to fall through the platforms or to walk through
        #      walls if their velocity is high enough. Ways to prevent this is to:
        #           a. add a velocity limit
        #           b. move the platform's collision box by the object's velocity
        #           c. make the platform's collision box smaller or larger 
        #              (depending on how the designer wants the game object to interact)
        # For this game, we choose 2.c., but the other methods can also be used. It depends entirely on the 
        # game and testing.
        
        padding = 10        # try playing with the numbers
        box2 = box2.inflate(-padding, -padding)
                
        if box1.bottom <= box2.top:
            self.pos[1] = box2.top - box1.height
            self.velocity[1] = 0
            
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
