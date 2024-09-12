import numpy as np
import pygame
from constants import LIGHT_BLUE, WHITE, PURPLE, quarter, SCREEN_RESOLUTION
from elements import Circle, CircleGrow, SawtoothNote, Note


MAX_ANGLE = 2 * np.pi

START_TIME = pygame.time.get_ticks()


def get_delta_time():
    return pygame.time.get_ticks() - START_TIME


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
AEOLIAN_SCALE_INTERVALS = [2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2]

scale_intervales = {
    "major": MAJOR_SCALE_INTERVALS,
    "minor": MINOR_SCALE_INTERVALS,
    "aeolian": AEOLIAN_SCALE_INTERVALS,
}


def get_note_frequency(note, octave):
    """Get the frequency of a note in a given octave."""
    semitone_distance_from_A4 = SEMITONES_FROM_A4[note] + (octave - 4) * 12
    frequency = A4_FREQUENCY * (SEMITONE_RATIO**semitone_distance_from_A4)
    return frequency


def generate_scale(root_note, octave, scale_type="major"):
    """Generate the frequencies for a scale starting from the root note."""
    intervals = scale_intervales[scale_type]
    scale_notes = []
    note_index = NOTE_NAMES.index(root_note)

    for interval in intervals:
        scale_notes.append(
            (NOTE_NAMES[note_index], get_note_frequency(NOTE_NAMES[note_index], octave))
        )
        note_index = (note_index + interval) % len(NOTE_NAMES)

    return scale_notes


root_note = "G"
octave = 4
scale_type = "aeolian"  # major minor aeolian

scale_frequencies = generate_scale(root_note, octave, scale_type)


class AngularCircle(Circle):
    def __init__(
        self, pos, fig_size, direction, speed, angle, radius, note, color
    ) -> None:
        self.angle = angle
        self.radius = radius
        self.center = pos
        self.note = note
        self.last_collision_time = get_delta_time()
        self.shadow = None
        self.trail = None

        super().__init__(pos, fig_size, direction, speed, color)

        self.circle_width = 15
        self.velocity = 2 * np.pi * speed / 200000

    def move(self):
        delta_time = get_delta_time()
        angle = np.pi + delta_time * self.velocity

        distance = angle % MAX_ANGLE

        self.pos = (
            self.center[0] + np.cos(distance) * self.radius,
            self.center[1] + np.sin(distance) * self.radius,
        )

        if self.shadow:
            self.shadow.move()
        if self.trail:
            self.trail.move()

    def collision(self, other):
        self.note.play(int(quarter / 2))
        self.color = PURPLE if self.color == LIGHT_BLUE else LIGHT_BLUE
        self.shadow = CircleGrow([self.pos[0], other.pos[1]], self.speed, 1)
        self.trail = CircularTrail(self.center, self.radius)

    def draw(self, screen):
        if self.trail:
            self.trail.draw(screen)
        if self.shadow:
            self.shadow.draw(screen)
        super().draw(screen)


class CircularTrail:
    def __init__(self, center, radius) -> None:
        self.center = center
        self.radius = radius
        self.delta_speed = 25
        self.alpha = 255

    def move(self):
        self.alpha -= self.delta_speed * 0.5

    def draw(self, screen):
        arc_img = pygame.Surface([5 + self.radius * 2, 5 + self.radius * 2])

        rect = pygame.Rect(
            0,
            0,
            self.radius * 2,
            self.radius * 2,
        )  # (x, y, width, height)

        pygame.draw.arc(arc_img, WHITE, rect, 0, 2 * np.pi, 1)  # 0 to pi (half-circle)
        arc_img.set_colorkey(0)
        arc_img.set_alpha(self.alpha)

        screen.blit(
            arc_img,
            [5 + self.center[0] - self.radius, self.center[1] - self.radius],
        )


class ColideLine:
    def __init__(self, p0, p1, size):
        self.pos = p0
        self.p0 = p0
        self.p1 = p1
        self.size = size

    def draw(self, screen):
        pygame.draw.line(screen, WHITE, self.p0, self.p1, self.size)

    def collision(self):
        pass


class CircularMove:
    def __init__(self, pos, number, radius):
        self.size = radius
        self.pos = (pos[0] - self.size / 2, pos[1] / 2)

        p0 = (100, self.pos[1] + self.size / 2)
        p1 = (SCREEN_RESOLUTION[0] - 100, self.pos[1] + self.size / 2)
        size = 3
        self.colide_line = ColideLine(p0, p1, size)

        self.circles = []
        for i in range(number):
            self.circles.append(
                AngularCircle(
                    pos=(self.pos[0] + self.size / 2, self.pos[1] + self.size / 2),
                    fig_size=50,
                    direction=[1, 1],
                    speed=75 + i * 0.5,
                    angle=np.pi,
                    radius=(self.size / 16) + i * 50,
                    note=Note(scale_frequencies[i][1], 5),
                    color=LIGHT_BLUE,
                )
            )

    def move(self):
        for circle in self.circles:
            circle.move()
            distance = np.sqrt((circle.pos[1] - self.colide_line.p0[1]) ** 2)
            if distance < circle.circle_width + 5:
                if circle.note.sound.get_num_channels() == 0:
                    circle.collision(self.colide_line)

    def draw(self, screen):
        # draw a line
        self.colide_line.draw(screen)

        for circle in self.circles:
            circle.draw(screen)
