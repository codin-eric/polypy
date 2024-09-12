# pygame window and main loop
import pygame
from circle_elements import CircularMove


BPM = 120
note = 20000


SCREEN_RESOLUTION = (1920, 1920)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("PolyPy")
    clock = pygame.time.Clock()
    running = True

    circles = CircularMove(
        pos=(SCREEN_RESOLUTION[0] / 2, SCREEN_RESOLUTION[1] / 10),
        number=7,
        radius=SCREEN_RESOLUTION[1] / 1.5,
    )

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("space")

        circles.move()

        screen.fill((0, 0, 0))
        circles.draw(screen)
        pygame.display.flip()

    pygame.quit()
