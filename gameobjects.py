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
                        
        padding = 10
        box2 = box2.inflate(-padding, -padding)
                
        if box1.bottom <= box2.top:
            self.pos[1] = box2.top - box1.height
            self.velocity[1] = 0
        elif box1.right > box2.left and box1.right < box2.right:
            self.pos[0] = box2.left - box1.width
            self.velocity[0] = 0
        elif box1.left < box2.right and box1.left > box2.left:
            self.pos[0] = box2.right
            self.velocity[0] = 0

    def draw(self, surface):
        GameObject.draw(self, surface)
        
        # debug so we can see the collision boxes
        Debug = True
        if Debug:
            box1 = self.image.get_rect()
            box1 = box1.move(self.pos)
            
            pygame.draw.rect(surface, [255, 0, 0], box1, 1)
            
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
        self.velocity = [0, 0]
        self.components.append(component_Gravity)        
        self.components.append(component_Movement)        
        self.components.append(component_Collidable)        

    def event_collide(self, target):
        box1 = self.image.get_rect()
        box1 = box1.move(self.pos)
        box2 = target.image.get_rect()
        box2 = box2.move(target.pos)
                        
        padding = 10
        box2 = box2.inflate(-padding, -padding)
                
        if box1.bottom <= box2.top:
            self.pos[1] = box2.top - box1.height
            self.velocity[1] = 0
        elif box1.right > box2.left and box1.right < box2.right:
            self.pos[0] = box2.left - box1.width
            self.velocity[0] = 0
        elif box1.left < box2.right and box1.left > box2.left:
            self.pos[0] = box2.right
            self.velocity[0] = 0

class Platform(GameObject):
    def __init__(self, pos):
        GameObject.__init__(self, 'RTS_Crate.png')
        self.pos = pos

    def draw(self, surface):
        GameObject.draw(self, surface)
        
        # debug so we can see the collision boxes
        Debug = True
        if Debug:
            box2 = self.image.get_rect()
            box2 = box2.move(self.pos)
                        
            padding = 10
            box2 = box2.inflate(-padding, -padding)
                
            pygame.draw.rect(surface, [255, 0, 0], box2, 10)
