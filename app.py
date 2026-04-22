import pygame as pyg
import math
from pygame.math import Vector2

pyg.init()
screen = pyg.display.set_mode((1080, 740))
clock = pyg.time.Clock()

spaceImg = pyg.image.load("media/space.png").convert()

scale = 1 / 500000000

G = 6.67430 * math.pow(10,-11)

class Body:
    def __init__(self, pos, mass, radius, vel, color):
        self.pos = pyg.Vector2(pos)
        self.vel = pyg.Vector2(vel)
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(self, surface):
        screen_x = self.pos.x * scale + (surface.get_width() // 2)
        screen_y = self.pos.y * scale + (surface.get_height() // 2)

        pyg.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), self.radius)

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

sun = Body((0, 0), 1.98e30, 20, (0, 0), (255, 255, 0))  # Κίτρινος Ήλιος
earth = Body((150_000_000_000, 0), 1.5e11, 8, (0, 30_000), (100, 150, 255))  # Γαλάζια Γη

bodies = [sun, earth]
running = True
while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False

    screen.blit(spaceImg, (0, 0))

    dt = 20000  # Το χρονικό βήμα (100 δευτερόλεπτα ανά frame)

    for b1 in bodies:
        total_accel = pyg.Vector2(0, 0)

        for b2 in bodies:
            if b1 is not b2:
                total_accel += b1.acceleration(b2)
        b1.vel += total_accel * dt
        b1.update(dt)

    screen.blit(spaceImg, (0, 0))

    for b in bodies:
        b.draw(screen)

    pyg.display.flip()  # Ενημέρωση της οθόνης
    clock.tick(60)  # Κλείδωμα στα 60 FPS για σταθερή φυσική

pyg.quit()