import pygame as pyg

pyg.init()
screen = pyg.display.set_mode((1080, 740))
clock = pyg.time.Clock()

spaceImg = pyg.image.load("media/space.png").convert()

class Body:
    def __init__(self , pos, mass , radius , vel):
        self.pos = pyg.Vector2(pos)
        self.mass = mass
        self.radius = radius
        self.vel = vel

    def draw(self):
        pass
        # pyg.draw.circle(radius=self.radius,center=self.pos)

running = True
while running:
    # 1. Inputs (Events)
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
    # 2. Physics Update (Εδώ θα μπει ο Runge-Kutta σου!)

    # 3. Drawing
    screen.blit(spaceImg, (0, 0))

    # Εδώ θα σχεδιάζεις τα σώματα (π.χ. pyg.draw.circle...)

    pyg.display.flip()  # Ενημέρωση της οθόνης
    clock.tick(60)  # Κλείδωμα στα 60 FPS για σταθερή φυσική

pyg.quit()