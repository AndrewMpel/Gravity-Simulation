import math
from collections import deque

import pygame as pyg
scale = 1 / 600000000
pyg.font.init()
my_font = pyg.font.SysFont("Arial", 16)
# The gravitational constant
G = 6.67430 * math.pow(10,-11)

# Body Class that creates a celestial body and gives access to physics methods
class Body:
    def __init__(self,name, pos, mass, radius, vel, color):
        self.pos = pyg.Vector2(pos)
        self.name = name
        self.vel = pyg.Vector2(vel)
        self.mass = mass
        self.radius = radius
        self.color = color
        self.path = deque(maxlen=1000)
        self.step_counter = 0
        self.current_screen_pos = (0, 0)
        self.current_hitbox_radius = radius

    # A method that draws the celestial body,its orbit line, and creates hitbox for the collision event
    def draw(self, surface,zoom,offset):
        if len(self.path) > 2:
            points = []
            for p in self.path:
                x = (p.x * scale * zoom) + (surface.get_width() // 2) + offset.x
                y = (p.y * scale * zoom) + (surface.get_height() // 2) + offset.y
                points.append((x, y))
            pyg.draw.aalines(surface, self.color, False, points)
        screen_x = self.pos.x * scale *zoom+ (surface.get_width() // 2) + offset.x
        screen_y = self.pos.y * scale * zoom+ (surface.get_height() // 2) + offset.y
        display_radius = max(1, int(self.radius * zoom))
        if 0.05 < zoom:
            if zoom > 2:
                text_surface = my_font.render(self.name, True, (255, 255, 255))
                surface.blit(text_surface, (int(screen_x) - 40, int(screen_y) + 40))
            else:
                text_surface = my_font.render(self.name, True, (255, 255, 255))
                surface.blit(text_surface, (int(screen_x)-12, int(screen_y)+12))
        pyg.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), display_radius)

        self.current_hitbox_radius = max(8, int(self.radius * zoom))
        self.current_screen_pos = (int(screen_x), int(screen_y))

    def update(self,step):
        self.step_counter += 1
        if self.step_counter >= step:
            self.path.append(pyg.Vector2(self.pos))
            self.step_counter = 0
    # Method that calculates the distance of 2 bodies
    def distance(self , body: Body):
        diff = self.pos - body.pos
        return diff.magnitude()
    # Method that calculates the Gravitational Force
    def force(self, body: Body):
        r_vec = body.pos - self.pos
        dist = r_vec.magnitude()
        if dist < 1:
            return pyg.Vector2(0, 0)

        r_unit = r_vec.normalize()
        F_mag = G * ((self.mass * body.mass) / math.pow(dist, 2))
        return F_mag * r_unit
    # Method that calculates the acceleration of a celestial body
    def acceleration(self , body: Body):
        return self.force(body)/ self.mass
    # A method that decides whether a body hits another
    def impact(self,body: Body):
        dist = (math.sqrt(pow((body.pos.x - self.pos.x),2)+pow((body.pos.y - self.pos.y),2))-self.radius-body.radius ) * scale
        return dist <= self.current_hitbox_radius