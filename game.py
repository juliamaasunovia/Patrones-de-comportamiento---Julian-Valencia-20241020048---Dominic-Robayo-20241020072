import pygame
from settings import SCREEN, CLOCK, FONT, WIDTH, HEIGHT, FPS, BLACK, WHITE, GRAY, GREEN
from command import MoveCommand, RestartCommand
from player import Player, PlayerCaretaker
from level import levels

class Game:
    def __init__(self):
        self.player = Player(*levels[0].start)
        self.caretaker = PlayerCaretaker(self.player)
        self.caretaker.create_memento()
        self.command_history = []
        self.paused = False
        self.flash_time = 0
        self.flash_msg = ''

    def push(self, cmd):
        cmd.execute()
        self.command_history.append(cmd)

    def undo(self):
        if self.command_history:
            cmd = self.command_history.pop()
            cmd.undo()

    def restart(self):
        cmd = RestartCommand(self.caretaker)
        self.push(cmd)
        self.load_level(self.player.level)

    def load_level(self, idx):
        # set current level and player start
        idx = max(0, min(idx, len(levels)-1))
        level = levels[idx]
        self.player.level = idx
        # if level has start defined, move player there; otherwise keep current
        if getattr(level, 'start', None):
            self.player.x, self.player.y = level.start
        self.caretaker.create_memento()
        # recreate enemy instances (to reset their internal state) if needed
        # (we assume level.enemies are already Enemy instances; if you want to clone, do it here)

    def next_level(self):
        if self.player.level + 1 < len(levels):
            self.load_level(self.player.level + 1)
        else:
            self.flash('¡Has completado todos los niveles!')

    def flash(self, msg, t=2.0):
        self.flash_time = t
        self.flash_msg = msg

    def update(self, dt):
        if self.paused:
            return

        level = levels[self.player.level]

        # movimiento fluido continuo
        keys = pygame.key.get_pressed()
        dx = dy = 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.player.SPEED * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.player.SPEED * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.player.SPEED * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.player.SPEED * dt

        # solo push si hay movimiento (evita crear comandos nulos)
        if dx != 0.0 or dy != 0.0:
            self.push(MoveCommand(self.player, dx, dy))

        # actualizar rect del jugador
        self.player.update_rect()

        # colisiones con paredes
        for w in getattr(level, 'walls', []):
            if self.player.rect.colliderect(w):
                self.caretaker.restore()
                self.load_level(self.player.level)
                self.flash('¡Pared!')
                return

        # enemigos
        for e in getattr(level, 'enemies', []):
            e.update(dt)
            if e.collides_with(self.player.rect):
                self.caretaker.restore()
                self.load_level(self.player.level)
                self.flash('¡Te golpearon!')
                return

        # meta (sólo si existe)
        if getattr(level, 'goal', None) is not None:
            if self.player.rect.colliderect(level.goal):
                self.flash('¡Nivel completado!')
                # avanzar al siguiente
                self.next_level()

        # tick flash
        if self.flash_time > 0:
            self.flash_time -= dt
            if self.flash_time <= 0:
                self.flash_msg = ''

    def draw(self):
        level = levels[self.player.level]

        SCREEN.fill(BLACK)

        # dibujar paredes si las hay
        for w in getattr(level, 'walls', []):
            pygame.draw.rect(SCREEN, GRAY, w)

        # dibujar meta solo si existe (evitar None)
        if getattr(level, 'goal', None) is not None:
            pygame.draw.rect(SCREEN, GREEN, level.goal)

        # dibujar enemigos
        for e in getattr(level, 'enemies', []):
            e.draw(SCREEN)

        # dibujar jugador (si tiene)
        if hasattr(self.player, 'draw'):
            self.player.draw(SCREEN)

        # HUD
        hud = FONT.render(f'Nivel: {self.player.level+1} / {len(levels)}   Comandos: {len(self.command_history)}   P: pausa  U: deshacer  R: reiniciar', True, WHITE)
        SCREEN.blit(hud, (10, 10))

        if self.flash_msg:
            txt = FONT.render(self.flash_msg, True, WHITE)
            SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, 40))

        pygame.display.flip()

