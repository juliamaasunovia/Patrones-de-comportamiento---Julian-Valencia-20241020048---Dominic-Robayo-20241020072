import pygame
from settings import WIDTH, HEIGHT, GREEN, GRAY
from enemy import Enemy, PatrolState, SineState, FastState

# Grosor de muros (coincide con la versión escalada)
WALL_THICK = 18

def r(x, y, w, h):
    return pygame.Rect(x, y, w, h)

class Level:
    def __init__(self, walls, enemies, start, goal):
        self.walls = walls
        self.enemies = enemies
        self.start = start
        self.goal = goal

levels = []

# ---------------- Level 1: Callejón con mini salida y patrulla mejorada ----------------
walls1 = [
    # Bordes exteriores
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),

    # Pared izquierda (más abajo desde arriba, cierra hasta abajo)
    r(180, WALL_THICK + 80, WALL_THICK, HEIGHT - (WALL_THICK + 80) - WALL_THICK),

    # Pared derecha (PEGADA al techo y dejando hueco abajo)
    r(620, 0, WALL_THICK, HEIGHT - 140),

    # Pared transversal que deja una mini salida en el medio (hueco x=380..420)
    r(200, 300, 180, WALL_THICK),
    r(420, 300, 200, WALL_THICK),
]

e1 = Enemy(260, 240, radius=21, speed=140, state=PatrolState())
e1.targets = [
    (220, 240),
    (580, 240),
    (580, 320),
    (220, 320),
]

levels.append(
    Level(
        walls1,
        [e1],
        (WALL_THICK + 40, HEIGHT // 2),
        pygame.Rect(WIDTH - 100, HEIGHT // 2 - 24, 48, 48),
    )
)

# ---------------- Level 2: Columnas con huecos + enemigos verticales (más rápidos) ----------------
walls2 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

# Columnas verticales con huecos (dos fragmentos por columna)
col_xs = [120, 300, 480, 660]
top_height = 180
bottom_y = 360
for x in col_xs:
    walls2.append(r(x, WALL_THICK + 20, WALL_THICK, top_height - 20))
    walls2.append(r(x, bottom_y, WALL_THICK, HEIGHT - bottom_y - WALL_THICK))

# pared horizontal baja
walls2.append(r(150, HEIGHT - WALL_THICK - 140, 500, WALL_THICK))

# Enemigos no bloqueantes
e2a = Enemy(220, 150, radius=21, speed=110, state=SineState()); e2a.bounds = (180, 620)
e2b = Enemy(600, 450, radius=21, speed=120, state=FastState()); e2b.targets = [(600, 450), (220, 450)]
e2c = Enemy(420, 250, radius=18, speed=85, state=SineState()); e2c.bounds = (360, 520)

# NUEVOS: 4 enemigos verticales con velocidad aumentada
vertical_enemies = []
vertical_positions_x = [180, 340, 520, 700]
for x in vertical_positions_x:
    ev = Enemy(x, 200, radius=18, speed=130, state=PatrolState())  # velocidad aumentada
    ev.targets = [(x, WALL_THICK + 40), (x, HEIGHT - WALL_THICK - 60)]
    vertical_enemies.append(ev)

levels.append(
    Level(
        walls2,
        [e2a, e2b, e2c] + vertical_enemies,
        (WALL_THICK + 40, HEIGHT // 2),
        pygame.Rect(WIDTH - 120, HEIGHT // 2 - 24, 48, 48),
    )
)

# ---------------- Level 3: Paredes intercaladas ----------------
walls3 = [
    r(0, 0, WIDTH, WALL_THICK),
    r(0, 0, WALL_THICK, HEIGHT),
    r(WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT),
    r(0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK),
]

# Intercalado con gaps grandes suficientes
GAP = 160
for i in range(1, 6):
    x = 100 * i
    if i % 2 == 1:
        # pegada arriba (hueco abajo)
        h = HEIGHT - WALL_THICK - GAP
        walls3.append(r(x, WALL_THICK, WALL_THICK, h))
    else:
        # pegada abajo (hueco arriba)
        walls3.append(r(x, GAP, WALL_THICK, HEIGHT - GAP - WALL_THICK))

e3a = Enemy(150, 150, radius=18, speed=95, state=PatrolState()); e3a.targets = [(150, 150), (650, 150)]
e3b = Enemy(650, 500, radius=24, speed=130, state=FastState()); e3b.targets = [(650, 500), (120, 500)]
e3c = Enemy(350, 300, radius=21, speed=80, state=SineState()); e3c.bounds = (200, 500)

levels.append(
    Level(
        walls3,
        [e3a, e3b, e3c],
        (WALL_THICK + 40, WALL_THICK + 40),
        pygame.Rect(WIDTH - 110, HEIGHT - 110, 48, 48),
    )
)

# Final empty level (se usa para detectar victory)
final_level = Level([], [], (0, 0), None)
levels.append(final_level)
