import pygame as pyg
import math
from pygame import key, K_z
from collections import deque
from pygame.math import Vector2

pyg.init()
screen = pyg.display.set_mode((1080, 740))
clock = pyg.time.Clock()

spaceImg = pyg.image.load("media/space.png").convert()

scale = 1 / 600000000

G = 6.67430 * math.pow(10,-11)

zoom = 1

class Body:
    def __init__(self, pos, mass, radius, vel, color):
        self.pos = pyg.Vector2(pos)
        self.vel = pyg.Vector2(vel)
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(self, surface,zoom,offset):
        screen_x = self.pos.x * scale *zoom+ (surface.get_width() // 2) + offset.x
        screen_y = self.pos.y * scale * zoom+ (surface.get_height() // 2) + offset.y

        display_radius = max(1, int(self.radius * zoom))
        pyg.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), display_radius)

    def update(self, dt):
        self.pos += self.vel * dt

    def distance(self , body: Body):
        diff = self.pos - body.pos
        return diff.magnitude()

    def force(self , body: Body):
        r = body.pos - self.pos
        r = r.normalize()
        F = G*((self.mass*body.mass)/math.pow(self.distance(body),2))
        return F * r
    def acceleration(self , body: Body):
        return self.force(body)/ self.mass

sun = Body((0, 0), 1.98e30, 30, (0, 0), (255, 255, 0))  # Κίτρινος Ήλιος
earth = Body((150_000_000_000, 0), 5.97e24, 8, (0, 30_000), (100, 150, 255))
mercury = Body((57_900_000_000,0),3.30e23,3,(0,47_400),(169, 169, 169))
venus = Body((108_000_000_000,0),4.87e24,8,(0,35_000),(255, 198, 73))
mars = Body((228_000_000_000,0),6.39e23,6,(0,24_070),(226, 123, 88))
jupiter = Body((778_000_000_000,0),6.39e23,18,(0,13_070),(196, 156, 126))

bodies = [sun, mercury,venus,earth,mars,jupiter]
running = True
offset = Vector2(0, 0)
dragging = False
last_mouse_pos = Vector2(0, 0)
while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

        if event.type == pyg.MOUSEWHEEL:
            if event.y > 0:
                zoom *= 1.1
            elif event.y < 0:
                zoom /= 1.1
        if event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 3:
                dragging = True
                last_mouse_pos = Vector2(event.pos)

        if event.type == pyg.MOUSEBUTTONUP:
            if event.button == 3: dragging = False

        if event.type == pyg.MOUSEMOTION and dragging:
            new_mouse_pos = Vector2(event.pos)
            offset += new_mouse_pos - last_mouse_pos
            last_mouse_pos = new_mouse_pos
        if event.type == pyg.KEYDOWN:
            if event.key == K_z:
                offset = Vector2(0, 0)
                zoom = 1

    dt = 20000

    for b1 in bodies:
        total_accel = pyg.Vector2(0, 0)

        for b2 in bodies:
            if b1 is not b2:
                total_accel += b1.acceleration(b2)
        b1.vel += total_accel * dt
        b1.update(dt)

    screen.blit(spaceImg, (0, 0))

    for b in bodies:
        b.draw(screen,zoom,offset)

    pyg.display.flip()  # Ενημέρωση της οθόνης
    clock.tick(60)  # Κλείδωμα στα 60 FPS για σταθερή φυσική

pyg.quit()