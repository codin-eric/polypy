import numpy as np
import math
import pygame
from constants import ORANGE, quarter


class Note:
    def __init__(self, freq, size=44100):
        buffer = np.sin(2 * np.pi * np.arange(size) * freq / size) * 50
        buffer = np.repeat(buffer.reshape(size, 1), 2, axis=1).astype(np.int8)

        self.sound = pygame.sndarray.make_sound(buffer)

    def play(self, duration):
        self.sound.play(maxtime=duration)


class PolyLine:
    def __init__(self, pos, vertex, size, note, color=(255, 255, 255), width=5):
        self.pos = pos
        self.points = [pos]
        self.vertex = vertex
        self.size = size

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

        self.circle_width = 25
        self.circle_pos = self.points[0]
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
