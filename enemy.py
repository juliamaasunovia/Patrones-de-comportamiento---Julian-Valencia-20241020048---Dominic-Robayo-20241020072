import pygame, math
from settings import BLUE, WIDTH

class EnemyState:
    def update(self, enemy, dt):
        raise NotImplementedError

class PatrolState(EnemyState):
    def update(self, enemy, dt):
        tx, ty = enemy.targets[enemy.target_index]
        dx, dy = tx - enemy.x, ty - enemy.y
        dist = (dx**2 + dy**2)**0.5
        if dist < enemy.speed * dt:
            enemy.x, enemy.y = tx, ty
            enemy.target_index = (enemy.target_index + 1) % len(enemy.targets)
        else:
            enemy.x += (dx / dist) * enemy.speed * dt
            enemy.y += (dy / dist) * enemy.speed * dt

class SineState(EnemyState):
    def __init__(self):
        self.t = 0
    def update(self, enemy, dt):
        self.t += dt
        enemy.x += enemy.direction * enemy.speed * dt
        enemy.y = enemy.base_y + enemy.amplitude * math.sin(self.t * enemy.frequency)
        if enemy.x < enemy.bounds[0] or enemy.x > enemy.bounds[1]:
            enemy.direction *= -1

class FastState(EnemyState):
    def update(self, enemy, dt):
        tx, ty = enemy.targets[enemy.target_index]
        dx, dy = tx - enemy.x, ty - enemy.y
        dist = (dx**2 + dy**2)**0.5
        if dist < enemy.speed * dt * 2:
            enemy.x, enemy.y = tx, ty
            enemy.target_index = (enemy.target_index + 1) % len(enemy.targets)
        else:
            enemy.x += (dx / dist) * enemy.speed * 2 * dt
            enemy.y += (dy / dist) * enemy.speed * 2 * dt

class Enemy:
    def __init__(self, x, y, radius=10, speed=100, state=None):
        self.x = x
        self.y = y
        self.base_y = y
        self.radius = radius
        self.speed = speed
        self.state = state or PatrolState()
        self.targets = []
        self.target_index = 0
        self.amplitude = 30
        self.frequency = 2
        self.bounds = (0, WIDTH)
        self.direction = 1

    def update(self, dt):
        self.state.update(self, dt)

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, rect):
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top, min(self.y, rect.bottom))
        dx, dy = cx - self.x, cy - self.y
        return dx**2 + dy**2 < self.radius**2
