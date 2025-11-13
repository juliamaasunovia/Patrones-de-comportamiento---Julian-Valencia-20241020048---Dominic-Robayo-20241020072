import pygame

# Dimensiones generales
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 20)
BLUE = (50, 80, 230)
GREEN = (0, 200, 0)
GRAY = (90, 90, 90)

# Inicialización Pygame
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 20)
