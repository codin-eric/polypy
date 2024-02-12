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
        [SCREEN_RESOLUTION[0] / 2 + 100, SCREEN_RESOLUTION[1] / 2 - 100],
        3,
        200,
        [Note(440, 50), Note(523, 25), Note(659, 17)],
        (255, 255, 255),
        5,
    )
    line2 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 50, SCREEN_RESOLUTION[1] / 2 - 50],
        4,
        100,
        [Note(329, 50), Note(493, 25), Note(587, 17)],
        (255, 255, 255),
        5,
    )
    line3 = PolyLine(
        [SCREEN_RESOLUTION[0] / 2 + 150, SCREEN_RESOLUTION[1] / 2 - 200 - 150],
        5,
        300,
        [Note(392, 50), Note(466, 25), Note(587, 17)],
        (255, 255, 255),
        5,
    )

    figures = [
        line,
        line2,
        line3,
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
