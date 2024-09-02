import numpy as np
from pathlib import Path
import pygame
from constants import ORANGE, WHITE, PURPLE, quarter, SCREEN_RESOLUTION
from decimal import getcontext, Decimal, ROUND_HALF_UP


getcontext().rounding = ROUND_HALF_UP
GLOBAL_SPEED = 0.01
ROOT_DIR = Path(__file__).parent
SOUNDS_DIR = ROOT_DIR / "sounds"

import math

# Constants
A4_FREQUENCY = 440.0  # Frequency of A4
SEMITONE_RATIO = 2 ** (1 / 12)  # Ratio of one semitone in the equal temperament scale

# Note frequencies for the chromatic scale (C4 to B4)
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
SEMITONES_FROM_A4 = {
    "C": -9,
    "C#": -8,
    "D": -7,
    "D#": -6,
    "E": -5,
    "F": -4,
    "F#": -3,
    "G": -2,
    "G#": -1,
    "A": 0,
    "A#": 1,
    "B": 2,
}

# Major and minor scale intervals (in semitones)
MAJOR_SCALE_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
MINOR_SCALE_INTERVALS = [2, 1, 2, 2, 1, 2, 2]


def get_note_frequency(note, octave):
    """Get the frequency of a note in a given octave."""
    semitone_distance_from_A4 = SEMITONES_FROM_A4[note] + (octave - 4) * 12
    frequency = A4_FREQUENCY * (SEMITONE_RATIO**semitone_distance_from_A4)
    return frequency


def generate_scale(root_note, octave, scale_type="major"):
    """Generate the frequencies for a scale starting from the root note."""
    scale_intervals = (
        MAJOR_SCALE_INTERVALS if scale_type == "major" else MINOR_SCALE_INTERVALS
    )
    scale_notes = []
    note_index = NOTE_NAMES.index(root_note)

    for interval in scale_intervals:
        scale_notes.append(
            (NOTE_NAMES[note_index], get_note_frequency(NOTE_NAMES[note_index], octave))
        )
        note_index = (note_index + interval) % len(NOTE_NAMES)

    return scale_notes


root_note = "C"
octave = 4
scale_type = "major"  # minor

scale_frequencies = generate_scale(root_note, octave, scale_type)


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
        self.color = ORANGE
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
        pygame.draw.circle(screen, self.color, self.pos, self.circle_width, 0)


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


MAX_ANGLE = 2 * np.pi

START_TIME = pygame.time.get_ticks()


def delta_time():
    return pygame.time.get_ticks() - START_TIME


class AngularCircle(Circle):
    def __init__(self, pos, fig_size, direction, speed, angle, radius, note) -> None:
        self.angle = angle
        self.radius = radius
        self.center = pos
        self.note = note

        super().__init__(pos, fig_size, direction, speed)

        self.circle_width = 20
        self.velocity = 2 * np.pi * speed / 200000

    def move(self):
        angle = np.pi + delta_time() * self.velocity

        distance = angle % MAX_ANGLE
        if distance <= np.pi:
            distance = MAX_ANGLE - distance

        if angle % np.pi <= 0.05:  # TODO Find a better collision detection
            self.note.play(int(quarter / 2))
            self.color = PURPLE if self.color == ORANGE else ORANGE

        self.pos = (
            self.center[0] + np.cos(distance) * self.radius,
            self.center[1] + np.sin(distance) * self.radius,
        )

    def draw(self, screen):
        # draw a semi circle
        rect = pygame.Rect(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.radius * 2,
            self.radius * 2,
        )  # (x, y, width, height)
        pygame.draw.arc(screen, WHITE, rect, 0, 2 * np.pi, 1)  # 0 to pi (half-circle)

        super().draw(screen)


class CircularMove:
    def __init__(self, pos, number, radius):
        self.size = radius
        self.pos = (pos[0] - self.size / 2, pos[1] / 2)

        self.circles = []
        for i in range(number):
            self.circles.append(
                AngularCircle(
                    pos=(self.pos[0] + self.size / 2, self.pos[1] + self.size / 2),
                    fig_size=50,
                    direction=[1, 1],
                    speed=50 - i,
                    angle=np.pi,
                    radius=(self.size / 2) - i * 75,
                    note=Note(scale_frequencies[i][1], 5),
                )
            )

    def move(self):
        for circle in self.circles:
            circle.angle += 0.1
            circle.speed = (
                np.cos(circle.angle) + 10,
                np.sin(circle.angle) + 10,
            )
            circle.move()

    def draw(self, screen):
        # draw a line
        pygame.draw.line(
            screen,
            WHITE,
            (100, self.pos[1] + self.size / 2),
            (SCREEN_RESOLUTION[0] - 100, self.pos[1] + self.size / 2),
            3,
        )

        for circle in self.circles:
            circle.draw(screen)
