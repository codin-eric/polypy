import numpy as np
import math
import pygame
from constants import ORANGE, quarter


class Note:
    def __init__(self, freq, volume=1, size=44100):
        buffer = np.sin(2 * np.pi * np.arange(size) * freq / size) * volume
        buffer = np.repeat(buffer.reshape(size, 1), 2, axis=1).astype(np.int8)

        self.sound = pygame.sndarray.make_sound(buffer)
        self.sound.fadeout(300)

    def play(self, duration):
        self.sound.play(maxtime=duration, fade_ms=100)


class Circle:
    def __init__(self, pos, direction, speed) -> None:
        self.circle_width = 25
        self.pos = pos
        self.delta_speed = speed
        self.circle_shadow = []
        self.change_dir(direction)

    def change_dir(self, new_dir):
        self.speed = [
            new_dir[0] * self.delta_speed,
            new_dir[1] * self.delta_speed,
        ]

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
        pygame.draw.circle(screen, ORANGE, self.pos, self.circle_width, 5)


class CircleGrow(Circle):
    def __init__(self, pos, direction, speed) -> None:
        self.circle_width = 25
        self.pos = pos
        self.delta_speed = speed
        self.change_dir(direction)

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

        angle = np.pi - (np.pi * (vertex - 2)) / vertex
        next_pos = pos

        for i in range(1, vertex + 1):
            x = next_pos[0] + size * np.cos(i * angle)
            y = next_pos[1] + size * np.sin(i * angle)

            next_pos = [math.ceil(x), math.ceil(y)]
            self.points.append(next_pos)

        self.note = note
        self.color = color
        self.width = width

        circle_speed = [
            (self.points[1][0] - self.points[0][0]),
            (self.points[1][1] - self.points[0][1]),
        ]
        self.circle = Circle(self.points[0], circle_speed, 0.02)

    def move(self):
        a = np.array(self.points[self.next_point])
        b = np.array(self.circle.pos)

        dist = np.linalg.norm(a - b)
        if dist < 10:
            for sounds in self.note:
                sounds.play(int(quarter / 2))
                self.circle.grow()
            self.next_point += 1
            if self.next_point >= len(self.points):
                self.next_point = 0
            new_dir = [
                self.points[self.next_point][0] - self.points[self.next_point - 1][0],
                self.points[self.next_point][1] - self.points[self.next_point - 1][1],
            ]
            self.circle.change_dir(new_dir)

        self.circle.move()

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, self.points, self.width)
        self.circle.draw(screen)
