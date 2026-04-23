import pygame as pyg
import math
from pygame import key, K_z, K_KP_PLUS, K_KP_MINUS
from collections import deque
from pygame.math import Vector2
from Bodies import Body,G,scale
pyg.init()
screen = pyg.display.set_mode((1080, 740))
pyg.display.set_caption("Gravity Simulation")
clock = pyg.time.Clock()
spaceImg = pyg.image.load("media/space.png").convert()
zoom = 1


# def createSatellites(name, distance_planet, planet: Body, mass, radius, color):
#     pos = Vector2(planet.pos.x + distance_planet, planet.pos.y)
#     v_mag = math.sqrt((G * planet.mass) / distance_planet)
#     relative_vel = Vector2(0, v_mag)
#     full_vel = planet.vel + relative_vel
#
#     return Body(name, pos, mass, radius, full_vel, color)

# Initialization of all the planets and other bodies like dwarf planets in the solar system
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
# moon = createSatellites("Moon", 384_400_000, earth, 7.34e22, 2, (200, 200, 200))

bodies = [sun, mercury, venus, earth, mars, ceres, jupiter, saturn, uranus, neptune,pluto,eris]
running = True
offset = Vector2(0, 0)
dragging = False
last_mouse_pos = Vector2(0, 0)
dt = 20000
step = max(1,10)
launching = False
launch_start_pos = Vector2(0, 0)
# Main Game loop
while running:
    # Events like mouse clicks or keys pressed
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
            if event.button == 4:
                launching = True
                launch_start_pos = Vector2(event.pos)

        if event.type == pyg.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
            if event.button == 4:
                launching = False
                launch_end_pos = Vector2(event.pos)

                world_x = (launch_start_pos.x - screen.get_width() // 2 - offset.x) / (scale * zoom)
                world_y = (launch_start_pos.y - screen.get_height() // 2 - offset.y) / (scale * zoom)
                vel_vec = (launch_start_pos - launch_end_pos) * 100

                new_probe = Body("Probe", (world_x, world_y), 1e10, 4, (vel_vec.x, vel_vec.y), (255, 255, 255))
                bodies.append(new_probe)

        if event.type == pyg.MOUSEMOTION:
            if dragging:
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
                if dt > 10:
                    dt /= 2
                    step = min(50, step * 2)

    to_remove = []
    accelerations = {}

    for b1 in bodies:
        total_accel = pyg.Vector2(0, 0)
        for b2 in bodies:
            if b1 in to_remove: continue
            if b1 is not b2:
                total_accel += b1.acceleration(b2)
                # Έλεγχος σύγκρουσης
                if b1.impact(b2):
                    if b2.mass > b1.mass:
                        b2.mass += b1.mass
                        to_remove.append(b1)
                    else:
                        b1.mass += b2.mass
                        to_remove.append(b2)
        accelerations[b1] = total_accel

    for b in bodies:
        if b not in to_remove:
            b.vel += accelerations[b] * dt
            b.pos += b.vel * dt
            b.update(step)

    for b in to_remove:
        if b in bodies: bodies.remove(b)
    screen.blit(spaceImg, (0, 0))

    for b in bodies:
        b.draw(screen,zoom,offset)
    if launching:
        current_mouse = Vector2(pyg.mouse.get_pos())
        pyg.draw.line(screen, (255, 255, 255), launch_start_pos, current_mouse, 2)

    pyg.display.flip()
    clock.tick(60)

pyg.quit()