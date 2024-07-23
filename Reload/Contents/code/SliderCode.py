import pygame

# Define colors
Background_color = (200, 200, 200)
Handle_color = (255, 255, 255)
Active_color = (76, 78, 255)
Inactive_color = (255, 255, 255)
set_cursor = False

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):
        self.w = w
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_radius = h * 1.5
        self.handle_rect = pygame.Rect(x, y - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)
        self.handle_color = Handle_color
        self.rect_color = Background_color
        self.val_rect_color = Inactive_color
        self.dragging = False
        self.handle_visible = False

    def update_val_rect(self):
        if self.value >= self.max_val / 15 or self.value == self.min_val:
            self.val_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_rect.centerx - self.rect.x, self.rect.height)
            self.handle_rect.centerx = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            self.handle_rect.centery = self.rect.centery
        else:
            self.val_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width / (self.w / 4), self.rect.height)
            self.handle_rect.centerx = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
            self.handle_rect.centery = self.rect.centery

    def handle_event(self, event):
        global set_cursor
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos) or self.handle_rect.collidepoint(event.pos):
                self.handle_visible = True
                self.val_rect_color = Active_color
                if self.handle_rect.collidepoint(event.pos):
                    set_cursor = True
            elif not self.dragging:
                self.val_rect_color = Inactive_color
                self.handle_visible = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos) and self.handle_visible:
                self.dragging = True
            elif self.rect.collidepoint(event.pos):
                self.dragging = True
                self.handle_rect.centerx = max(self.rect.x, min(event.pos[0], self.rect.right))
                self.value = self.min_val + (self.handle_rect.centerx - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
                self.update_val_rect()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            if not self.rect.collidepoint(event.pos):
                self.handle_visible = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.handle_rect.centerx = max(self.rect.x, min(event.pos[0], self.rect.right))
            self.value = self.min_val + (self.handle_rect.centerx - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
            self.update_val_rect()

    def draw(self, screen):
        self.update_val_rect()
        pygame.draw.rect(screen, self.rect_color, self.rect, border_radius=20)
        pygame.draw.rect(screen, self.val_rect_color, self.val_rect, border_radius=20)
        if self.handle_visible:
            pygame.draw.circle(screen, self.handle_color, self.handle_rect.center, self.handle_radius)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
