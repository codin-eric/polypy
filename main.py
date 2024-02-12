# pygame window and main loop
import pygame
import numpy as np

BPM = 120

quarter = 500
note = 20000
ORANGE = (255, 165, 0)

SCREEN_RESOLUTION = (1080, 1080)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("PolyPy")
    clock = pygame.time.Clock()
    running = True

    pygame.mixer.init(size=-8, channels=2)

    class Note:
        def __init__(self, freq, size=44100):
            buffer = np.sin(2 * np.pi * np.arange(size) * freq / size) * 50
            buffer = np.repeat(buffer.reshape(size, 1), 2, axis=1).astype(np.int8)

            self.sound = pygame.sndarray.make_sound(buffer)

        def play(self, duration):
            self.sound.play(maxtime=duration)

    class PolyLine:
        def __init__(self, points, note, color=(255, 255, 255), width=5):
            self.points = points
            self.note = note
            self.color = color
            self.width = width

            self.circle_width = 25
            self.circle_pos = points[0]
            self.next_point = 1
            self.circle_speed = 10

        def move(self):
            a = np.array(self.points[self.next_point])
            b = np.array(self.circle_pos)

            dist = np.linalg.norm(a - b)
            if dist < 10:
                self.note.play(int(quarter / 2))
                self.next_point += 1
                if self.next_point >= len(self.points):
                    self.next_point = 0
                self.circle_speed *= -1

            self.circle_pos = [
                self.circle_pos[0],
                self.circle_pos[1] + self.circle_speed,
            ]

        def draw(self, screen):
            pygame.draw.lines(screen, self.color, False, self.points, self.width)
            pygame.draw.circle(screen, ORANGE, self.circle_pos, self.circle_width)

    line = PolyLine(
        [
            [SCREEN_RESOLUTION[0] / 2, SCREEN_RESOLUTION[1] / 2 - 200],
            [SCREEN_RESOLUTION[0] / 2, SCREEN_RESOLUTION[1] / 2 + 200],
        ],
        Note(440),
        (255, 255, 255),
        5,
    )
    line2 = PolyLine(
        [
            [SCREEN_RESOLUTION[0] / 1.5, SCREEN_RESOLUTION[1] / 2 - 100],
            [SCREEN_RESOLUTION[0] / 1.5, SCREEN_RESOLUTION[1] / 2 + 100],
        ],
        Note(293),
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
        line.move()
        line2.move()
        line.draw(screen)
        line2.draw(screen)

        pygame.display.flip()

    pygame.quit()
