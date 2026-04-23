import pygame as pyg
import math
from pygame import key, K_z, K_KP_PLUS, K_KP_MINUS
from collections import deque
from pygame.math import Vector2

pyg.init()
pyg.font.init()
my_font = pyg.font.SysFont("Arial", 16)
screen = pyg.display.set_mode((1080, 740))
pyg.display.set_caption("Gravity Simulation")
clock = pyg.time.Clock()

spaceImg = pyg.image.load("media/space.png").convert()

scale = 1 / 600000000

G = 6.67430 * math.pow(10,-11)

zoom = 1

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
                screen.blit(text_surface, (int(screen_x) - 40, int(screen_y) + 40))
            else:
                text_surface = my_font.render(self.name, True, (255, 255, 255))
                screen.blit(text_surface, (int(screen_x)-12, int(screen_y)+12))
        pyg.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), display_radius)

        self.current_hitbox_radius = max(8, int(self.radius * zoom))
        self.current_screen_pos = (int(screen_x), int(screen_y))


    def update(self, dt ,step):
        self.pos += self.vel * dt

        self.step_counter += 1
        if self.step_counter >= step:
            self.path.append(pyg.Vector2(self.pos))
            self.step_counter = 0

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
    def impact(self,body: Body):
        dist = self.pos.distance_to(body.pos)
        return dist < (self.radius + body.radius) * 500000000

sun = Body("",(0, 0), 1.98e30, 30, (0, 0), (255, 255, 0))  # Κίτρινος Ήλιος
earth = Body("Earth",(150_000_000_000, 0), 5.97e24, 8, (0, 30_000), (100, 150, 255))
mercury = Body("Mercury",(57_900_000_000,0),3.30e23,3,(0,47_400),(169, 169, 169))
venus = Body("Venus",(108_000_000_000,0),4.87e24,8,(0,35_000),(255, 198, 73))
mars = Body("Mars",(228_000_000_000,0),6.39e23,6,(0,24_070),(226, 123, 88))
ceres = Body("Ceres",(414_000_000_000, 0), 9.39e20, 3, (0, 17_900), (150, 150, 150))
jupiter = Body("Jupiter",(778_000_000_000,0),1.898e27,18,(0,13_070),(196, 156, 126))
saturn = Body("Saturn", (1_430_000_000_000, 0), 5.68e26, 15, (0, 9_680), (234, 214, 184))
uranus = Body("Uranus", (2_870_000_000_000, 0), 8.68e25, 12, (0, 6_810), (209, 231, 231))
neptune = Body("Neptune", (4_500_000_000_000, 0), 1.02e26, 12, (0, 5_430), (63, 84, 186))
pluto = Body("Pluto", (5_906_000_000_000, 0), 1.31e22, 6, (0, 4_740), (198, 156, 109))
eris = Body("Eris", (10_125_000_000_000, 0), 1.66e22, 6, (0, 3_430), (220, 220, 220))

bodies = [sun, mercury, venus, earth, mars, ceres, jupiter, saturn, uranus, neptune,pluto,eris]
running = True
offset = Vector2(0, 0)
dragging = False
last_mouse_pos = Vector2(0, 0)
dt = 20000
step = max(1,10)
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
            if event.button == 1:
                dragging = True
                last_mouse_pos = Vector2(event.pos)

        if event.type == pyg.MOUSEBUTTONUP:
            if event.button == 1: dragging = False

        if event.type == pyg.MOUSEMOTION and dragging:
            new_mouse_pos = Vector2(event.pos)
            offset += new_mouse_pos - last_mouse_pos
            last_mouse_pos = new_mouse_pos
        if event.type == pyg.KEYDOWN:
            if event.key == K_z:
                offset = Vector2(0, 0)
                zoom = 1
                dt = 20000
                step = 10
                for b in bodies:
                    b.path.clear()
            if event.key == K_KP_PLUS:
                if dt < 320000:
                    dt *= 2
                    step = max(1, step // 2)

            if event.key == K_KP_MINUS:
                if dt > 625:
                    dt /= 2
                    step = min(50, step * 2)

    to_remove = []
    for b1 in bodies:
        total_accel = pyg.Vector2(0, 0)

        for b2 in bodies:
            if b1 is not b2:
                total_accel += b1.acceleration(b2)
                if b1.impact(b2):
                    if b2.mass > b1.mass:
                        b2.mass += b1.mass
                        to_remove.append(b1)
                    else:
                        b1.mass += b2.mass
                        to_remove.append(b2)
        b1.vel += total_accel * dt
        b1.update(dt , step)
    for b in to_remove:
        if b in bodies: bodies.remove(b)
    screen.blit(spaceImg, (0, 0))

    for b in bodies:
        b.draw(screen,zoom,offset)


    pyg.display.flip()
    clock.tick(60)

pyg.quit()