import pygame

def component_Gravity(GameObject, GameState):
    GameObject.velocity[1] += 0.1

def component_Movement(GameObject, GameState):
    GameObject.pos[0] += GameObject.velocity[0]
    GameObject.pos[1] += GameObject.velocity[1]

    # added max speed
    if GameObject.velocity[0] < -3:
        GameObject.velocity[0] = -3
        
    if GameObject.velocity[0] > 3:
        GameObject.velocity[0] = 3

def component_AI(GameObject, GameState):
    GameObject.velocity[0] -= 0.1

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
            if 'event_collide' in dir(target):
                target.event_collide(GameObject)

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

        # You can move the jumping code to a component, to make the code cleaner
        self.isJumping = False
        self.maxJumpPower = 5
        self.jumpPower = self.maxJumpPower
        
    def update(self, GameState):
        GameObject.update(self, GameState)
        
        keystate = pygame.key.get_pressed()
        #if GameState.joystick.get_axis(0) < -0.2:
        if keystate[pygame.K_LEFT]:
            self.velocity[0] -= 1 / 4
        #if GameState.joystick.get_axis(0) > 0.2:
        if keystate[pygame.K_RIGHT]:
            self.velocity[0] += 1 / 4
        if keystate[pygame.K_SPACE]:
            if self.jumpPower > 0:
                self.velocity[1] -= 0.1
                
                if self.jumpPower == self.maxJumpPower:
                    self.isJumping = True
                    self.velocity[1] = -7
                elif self.jumpPower > 0:
                    self.velocity[1] -= 0.2
                    
            self.jumpPower -= 1
            
    def draw(self, surface):
        GameObject.draw(self, surface)

        # debug so we can see the collision boxes
        Debug = False
        if Debug:
            box1 = self.image.get_rect()
            box1 = box1.move(self.pos)
            
            pygame.draw.rect(surface, [255, 0, 0], box1, 1)
            
    def event_collide(self, target):
        self.jumpPower = self.maxJumpPower
    
class Enemy(GameObject):
    def __init__(self):
        GameObject.__init__(self, 'moongoose.png')
        self.pos[0] = 500
        self.velocity = [0, 0]
        self.components.append(component_Gravity)        
        self.components.append(component_Movement)        
        self.components.append(component_Collidable)        
        self.components.append(component_AI)        

class Platform(GameObject):
    def __init__(self, pos):
        GameObject.__init__(self, 'RTS_Crate.png')
        self.pos = pos

    def draw(self, surface):
        GameObject.draw(self, surface)
        
        # debug so we can see the collision boxes
        Debug = False
        if Debug:
            box2 = self.image.get_rect()
            box2 = box2.move(self.pos)
                        
            padding = 10
            box2 = box2.inflate(-padding, -padding)
                
            pygame.draw.rect(surface, [255, 0, 0], box2, 10)

    def event_collide(self, target):
        if 'isJumping' in dir(target):
            # ignore collisions with the platform on the first frame of jumping
            if target.isJumping:
                target.isJumping = False
                return
    
        box1 = target.image.get_rect()
        box1 = box1.move(target.pos)
        box2 = self.image.get_rect()
        box2 = box2.move(self.pos)
                        
        padding = 10
        box2 = box2.inflate(-padding, -padding)
                
        # another fix to the character passing through the platform is by checking
        # against the bottom. notice the bug that this fix causes. There are ways
        # to get perfect collision, but I'll leave that as your homework        
        
        if box1.bottom <= box2.bottom:
            target.pos[1] = box2.top - box1.height
            target.velocity[1] = 0
        elif box1.right > box2.left and box1.right < box2.right:
            target.pos[0] = box2.left - box1.width
            target.velocity[0] = 0
        elif box1.left < box2.right and box1.left > box2.left:
            target.pos[0] = box2.right
            target.velocity[0] = 0
