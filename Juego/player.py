from dataclasses import dataclass
import pygame
from settings import RED
from movement_strategy import NormalMovement

@dataclass
class PlayerMemento:
    x: float
    y: float
    level_index: int

class PlayerCaretaker:
    def __init__(self, player):
        self.player = player
        self._memento = None
    def create_memento(self):
        self._memento = PlayerMemento(self.player.x, self.player.y, self.player.level)
    def get_memento(self):
        return self._memento
    def restore(self, memento=None):
        if memento is None:
            memento = self._memento
        if memento:
            self.player.x = memento.x
            self.player.y = memento.y
            self.player.level = memento.level_index

class Player:
    SPEED = 200
    SIZE = 32

    def __init__(self, x, y, level=0):
        self.x = float(x)
        self.y = float(y)
        self.level = level
        self.rect = pygame.Rect(int(self.x), int(self.y), self.SIZE, self.SIZE)
        self.movement_strategy = NormalMovement()  # 👈 Estrategia por defecto

    def set_strategy(self, strategy):
        """Permite cambiar la estrategia en tiempo de ejecución"""
        self.movement_strategy = strategy

    def move(self, dx, dy):
        """Usa la estrategia actual para moverse"""
        self.movement_strategy.move(self, dx, dy)

    def update_rect(self):
        self.rect.topleft = (int(self.x), int(self.y))
        self.rect.width = self.SIZE
        self.rect.height = self.SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
