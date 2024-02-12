# pygame window and main loop
import pygame
from elements import Note, SampleNote, PolyLine


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

    wave = Note(440, 25)
    snare = SampleNote("snare.wav", 25)
    hi_hat = SampleNote("hi_hat.wav", 25)
    tom = SampleNote("tom.wav", 25)
    """
        
        PolyLine(
            [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 150],
            3,
            400,
            [Note(587, 5)],
            (200, 255, 100),
            5,
        ),
    """
    figures = [
        PolyLine(
            [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2],
            2,
            400,
            [tom],
            (255, 255, 255),
            5,
        ),
        PolyLine(
            [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 200],
            4,
            400,
            [snare],
            (150, 150, 255),
            5,
        ),
        PolyLine(
            [SCREEN_RESOLUTION[0] / 2 + 200, SCREEN_RESOLUTION[1] / 2 + 300],
            5,
            400,
            [hi_hat],
            (255, 100, 100),
            5,
        ),
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
