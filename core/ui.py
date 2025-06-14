import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, WHITE

# Drawing the 'pasue/resume' button
def draw_button(screen, font, paused):
    btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 45, 120, 35)
    color = RED if paused else GREEN
    label = "Resume" if paused else "Pause"
    pygame.draw.rect(screen, color, btn_rect)
    text = font.render(label, True, WHITE)
    text_rect = text.get_rect(center=btn_rect.center)
    screen.blit(text, text_rect)
    return btn_rect
