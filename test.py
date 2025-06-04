import math
import pygame

NE = 45
NW = 135
SW = 225
SE = 315
V = 5
TICK = 60
RADIUS = 10


def convert_degrees_to_radians(angle_degrees):
    return math.radians(angle_degrees)


class Circle:

    def __init__(self, center_pos, direction_angle):
        self.center_pos = center_pos
        self.movement_angle, self.movement_direction = None, None
        self.change_direction(direction_angle)

    def change_direction(self, new_angle):
        self.movement_angle = new_angle
        self.movement_direction = pygame.math.Vector2(math.cos(convert_degrees_to_radians(new_angle)),
                                                      math.sin(convert_degrees_to_radians(new_angle)))

    def change_position(self, new_position):
        self.center_pos = new_position


def draw_circle(position):
    pygame.draw.circle(screen, pygame.Color('white'), (round(position[0]), round(position[1])), RADIUS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Balls')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size, vsync=1)

    running = True
    circles = []
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                draw_circle(event.pos)
                circles.append(Circle(event.pos, NW))
        screen.fill(pygame.Color('black'))
        clock.tick(TICK)
        for circle in circles:
            new_center_pos = [circle.center_pos[0] + V * circle.movement_direction.x,
                  circle.center_pos[1] - V * circle.movement_direction.y]
            circle.change_position(tuple(new_center_pos))
            draw_circle(circle.center_pos)
            if circle.center_pos[0] <= RADIUS:
                if circle.movement_angle == SW:
                    circle.change_direction(SE)
                if circle.movement_angle == NW:
                    circle.change_direction(NE)
            if circle.center_pos[0] >= width - RADIUS:
                if circle.movement_angle == SE:
                    circle.change_direction(SW)
                if circle.movement_angle == NE:
                    circle.change_direction(NW)
            if circle.center_pos[1] <= RADIUS:
                if circle.movement_angle == NW:
                    circle.change_direction(SW)
                if circle.movement_angle == NE:
                    circle.change_direction(SE)
            if circle.center_pos[1] >= height - RADIUS:
                if circle.movement_angle == SW:
                    circle.change_direction(NW)
                if circle.movement_angle == SE:
                    circle.change_direction(NE)
        pygame.display.flip()
    pygame.quit()
