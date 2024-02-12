import numpy as np
from pathlib import Path
import pygame
from constants import ORANGE, quarter
from decimal import getcontext, Decimal, ROUND_HALF_UP


getcontext().rounding = ROUND_HALF_UP
GLOBAL_SPEED = 0.01
ROOT_DIR = Path(__file__).parent
SOUNDS_DIR = ROOT_DIR / "sounds"


class Note:
    def __init__(self, freq, volume=1, size=44100):
        buffer = np.sin(2 * np.pi * np.arange(size) * freq / size) * volume
        buffer = np.repeat(buffer.reshape(size, 1), 2, axis=1).astype(np.int8)

        self.sound = pygame.sndarray.make_sound(buffer)
        self.sound.fadeout(300)

    def play(self, duration):
        self.sound.play(maxtime=duration, fade_ms=100)


class SampleNote(Note):
    def __init__(self, file, volume=1):
        self.sound = pygame.mixer.Sound(SOUNDS_DIR / file)
        self.sound.set_volume(volume)


class Circle:
    def __init__(self, pos, fig_size, direction, speed) -> None:
        self.circle_width = 25
        self.pos = pos
        self.fig_size = fig_size
        self.delta_speed = speed
        self.circle_shadow = []
        self.change_dir(direction)

    def change_dir(self, new_dir):
        self.speed = [new_dir[0] * self.delta_speed, new_dir[1] * self.delta_speed]

    def grow(self):
        self.circle_shadow.append(CircleGrow(self.pos, self.speed, 1))

    def move(self):
        self.pos = [
            self.pos[0] + self.speed[0],
            self.pos[1] + self.speed[1],
        ]
        for circle in self.circle_shadow:
            circle.move()
            if circle.circle_width > 50:
                self.circle_shadow.remove(circle)

    def draw(self, screen):
        for circle in self.circle_shadow:
            circle.draw(screen)
        # TODO: Speed should be calculated by the total distance
        pygame.draw.circle(screen, ORANGE, self.pos, self.circle_width, 5)


class CircleGrow(Circle):
    def __init__(self, pos, direction, speed) -> None:
        self.circle_width = 25
        self.pos = pos
        self.delta_speed = speed

    def move(self):
        # grow the circle

        self.circle_width += self.delta_speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.circle_width, 0)


class PolyLine:
    def __init__(self, pos, vertex, size, note, color=(255, 255, 255), width=5):
        self.pos = pos
        self.points = [pos]
        self.vertex = vertex
        self.size = size
        self.next_point = 1
        self.move_count = 0

        angle = np.pi - (np.pi * (vertex - 2)) / vertex
        # Calculate the position of the next vertex
        for i in range(0, vertex):
            x = pos[0] + size * np.cos(i * angle + np.pi)
            y = pos[1] + size * np.sin(i * angle + np.pi)
            pos = [x, y]
            self.points.append(pos)
        self.note = note
        self.color = color
        self.width = width

        circle_direction = [
            (self.points[1][0] - self.points[0][0]),
            (self.points[1][1] - self.points[0][1]),
        ]

        circle_speed = GLOBAL_SPEED * self.vertex
        self.circle = Circle(self.points[0], self.size, circle_direction, circle_speed)

    # TODO: I think this move logic should be inside the circle
    def move(self):
        self.circle.move()
        self.move_count += 1

        dest = np.array(self.points[self.next_point]) - np.array(
            self.points[self.next_point - 1]
        )
        pos_vec = np.array(self.points[self.next_point - 1]) - np.array(self.circle.pos)
        dist = round(
            Decimal(np.hypot(dest[0], dest[1]) - np.hypot(pos_vec[0], pos_vec[1]))
        )
        hyp_speed = round(Decimal(np.hypot(self.circle.speed[0], self.circle.speed[1])))
        # print(f"dists: {dist} - {np.hypot(self.circle.speed[0], self.circle.speed[1])} - {self.vertex}")

        if dist < hyp_speed:
            self.move_count = 0
            for sounds in self.note:
                sounds.play(int(quarter / 2))
            self.circle.grow()
            self.next_point += 1
            # check if the list of points is over
            if self.next_point >= len(self.points):
                self.next_point = 1
            # calculate the new direction vector
            new_dir = [
                self.points[self.next_point][0] - self.points[self.next_point - 1][0],
                self.points[self.next_point][1] - self.points[self.next_point - 1][1],
            ]
            # set the circle position to the next point
            self.circle.pos = self.points[self.next_point - 1]
            # if the dist is not 0 calculate a vector with the oposite direction and rest that to the new pos
            if dist != 0:
                vector = np.array(new_dir)
                v_hat = vector / np.linalg.norm(vector)
                dist_rest = v_hat * -dist
                self.circle.pos = [
                    self.circle.pos[0] + dist_rest[0],
                    self.circle.pos[1] + dist_rest[1],
                ]
            self.circle.change_dir(new_dir)

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, self.points, self.width)
        self.circle.draw(screen)
