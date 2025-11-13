# movement_strategy.py
# Implementación del patrón Strategy para movimiento del jugador

class MovementStrategy:
    """Interfaz base para estrategias de movimiento"""
    def move(self, player, dx, dy):
        raise NotImplementedError("Debes implementar este método en la subclase")


class NormalMovement(MovementStrategy):
    """Movimiento normal"""
    def move(self, player, dx, dy):
        player.x += dx
        player.y += dy
        player.update_rect()


class SlowMovement(MovementStrategy):
    """Movimiento más lento (por ejemplo en zonas con hielo o ralentización)"""
    def move(self, player, dx, dy):
        player.x += dx * 0.5
        player.y += dy * 0.5
        player.update_rect()


class InvertedMovement(MovementStrategy):
    """Movimiento invertido (por ejemplo en una zona de confusión)"""
    def move(self, player, dx, dy):
        player.x -= dx
        player.y -= dy
        player.update_rect()
