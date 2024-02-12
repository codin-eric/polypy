# pygame window and main loop
import pygame
from elements import Note, PolyLine


BPM = 120
note = 20000


SCREEN_RESOLUTION = (1080, 1080)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("PolyPy")
    clock = pygame.time.Clock()
    running = True

    pygame.mixer.init(size=-8, channels=2)

    line = PolyLine(
        [SCREEN_RESOLUTION[0] / 2, SCREEN_RESOLUTION[1] / 2 - 200],
        3,
        200,
        Note(440),
        (255, 255, 255),
        5,
    )

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("space")

        screen.fill((0, 0, 0))
        # line.move()
        line.draw(screen)

        pygame.display.flip()

    pygame.quit()
