import pygame

class Camera:
    def __init__(self, width, height, screen_width, screen_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def apply(self, target):
        # Updates where to draw the object each frame
        if isinstance(target, pygame.Rect):
            return target.move(self.camera.topleft)
        elif isinstance(target, pygame.sprite.Sprite):
            return target.rect.move(self.camera.topleft)
        elif isinstance(target, tuple) and len(target) == 2:
            return (target[0] + self.camera.x, target[1] + self.camera.y)
        else:
            raise ValueError("Invalid target type")
        
    # Updating the camera's location based on a target
    def update(self, target):
        x = -target.rect.center[0] + self.screen_width // 2
        y = -target.rect.center[1] + self.screen_height // 2

        # Limit to map bounds
        x = min(0, max(-(self.width - self.screen_width), x))
        y = min(0, max(-(self.height - self.screen_height), y))

        self.camera = pygame.Rect(x, y, self.width, self.height)