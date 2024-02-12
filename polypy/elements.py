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
        self.delta_speed = 0.02
        self.circle_speed = [
            (self.points[1][0] - self.points[0][0]) * self.delta_speed,
            (self.points[1][1] - self.points[0][1]) * self.delta_speed,
        ]

    def move(self):
        a = np.array(self.points[self.next_point])
        b = np.array(self.circle_pos)

        dist = np.linalg.norm(a - b)
        if dist < 10:
            for sounds in self.note:
                sounds.play(int(quarter / 2))
            self.next_point += 1
            if self.next_point >= len(self.points):
                self.next_point = 0
            self.circle_speed = [
                (self.points[self.next_point][0] - self.points[self.next_point - 1][0])
                * self.delta_speed,
                (self.points[self.next_point][1] - self.points[self.next_point - 1][1])
                * self.delta_speed,
            ]
        self.circle_pos = [
            self.circle_pos[0] + self.circle_speed[0],
            self.circle_pos[1] + self.circle_speed[1],
        ]

    def draw(self, screen):
        pygame.draw.lines(screen, self.color, False, self.points, self.width)
        pygame.draw.circle(screen, ORANGE, self.circle_pos, self.circle_width)
