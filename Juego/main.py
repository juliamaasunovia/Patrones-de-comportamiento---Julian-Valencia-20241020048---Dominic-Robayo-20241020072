import pygame
import sys
from settings import CLOCK, FPS, SCREEN, WIDTH, HEIGHT, FONT, WHITE
from game import Game
from level import levels
from movement_strategy import NormalMovement, SlowMovement, InvertedMovement


def show_victory(screen, seconds=3.0):
    t0 = pygame.time.get_ticks()
    ms = int(seconds * 1000)
    showing = True
    while showing:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                showing = False

        screen.fill((8, 8, 8))
        big = pygame.font.Font(None, 96)
        text = big.render("¡HAS GANADO!", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, rect)

        small = pygame.font.Font(None, 28)
        sub = small.render("Gracias por jugar", True, (200, 200, 200))
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 + 60))

        pygame.display.flip()
        CLOCK.tick(FPS)
        if pygame.time.get_ticks() - t0 >= ms:
            showing = False


def draw_strategy_info(screen, current_strategy_name):
    """Dibuja en pantalla las instrucciones y la estrategia actual"""
    info_font = pygame.font.Font(None, 26)
    text1 = info_font.render(
        "Presiona [1] Normal | [2] Lento | [3] Invertido", True, WHITE
    )
    text2 = info_font.render(
        f"Modo de movimiento actual: {current_strategy_name}", True, WHITE
    )

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT - 60))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT - 35))


def main():
    pygame.display.set_caption("The Hardest Game - Recreated (con Strategy)")
    game = Game()
    game.load_level(0)
    running = True
    current_strategy_name = "Normal"

    while running:
        dt = CLOCK.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    game.paused = not game.paused
                elif event.key == pygame.K_u:
                    game.undo()
                elif event.key == pygame.K_r:
                    game.restart()

                # Cambiar estrategia de movimiento (Strategy Pattern)
                elif event.key == pygame.K_1:
                    game.player.set_strategy(NormalMovement())
                    current_strategy_name = "Normal"
                    print("Movimiento normal activado")
                elif event.key == pygame.K_2:
                    game.player.set_strategy(SlowMovement())
                    current_strategy_name = "Lento"
                    print("Movimiento lento activado")
                elif event.key == pygame.K_3:
                    game.player.set_strategy(InvertedMovement())
                    current_strategy_name = "Invertido"
                    print("Movimiento invertido activado")

 
        game.update(dt)
        game.draw()

      
        draw_strategy_info(SCREEN, current_strategy_name)

        pygame.display.flip()

        # Si llegaste al nivel final, muestra victoria
        if game.player.level >= len(levels) - 1:
            show_victory(SCREEN, seconds=3.0)
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
