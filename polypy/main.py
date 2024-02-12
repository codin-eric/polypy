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

    line2 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2],
        2,
        400,
        [Note(440, 25)],
        (255, 255, 255),
        5,
    )
    line3 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 150],
        3,
        400,
        [Note(523, 10)],
        (200, 255, 100),
        5,
    )

    line4 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 200],
        4,
        400,
        [Note(587, 17)],
        (150, 150, 255),
        5,
    )

    line5 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 300],
        5,
        400,
        [Note(587, 17)],
        (255, 100, 100),
        5,
    )

    figures = [
        line2,
        line3,
        line4,
        line5,
    ]

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
        for figure in figures:
            figure.move()
            figure.draw(screen)

        pygame.display.flip()

    pygame.quit()
