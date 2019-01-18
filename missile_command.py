import spgl
import math


# Classes
class MissileCommand(spgl.Game):
    def __init__(self, screen_width, screen_height, background_colour, title, splash_time):
        spgl.Game.__init__(self, screen_width, screen_height, background_colour, title, splash_time)

    def click(self, x, y):
        player_missile.set_target(x, y)


class City(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None

    def tick(self):
        pass


class Silo(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None

    def tick(self):
        pass


class PlayerMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.speed = 7
        self.state = 'ready'
        self.target_x = 0
        self.target_y = 0
        self.shapesize(0.2, 0.2, 0)
        self.size = 0.2
        self.frame = 0.0

    def set_target(self, target_x, target_y):
        if self.state == 'ready':
            self.target_x = target_x
            self.target_y = target_y

            self.dx = self.xcor() - target_x
            # avoid dive by 0 logic error
            if self.dx == 0:
                self.dx = 0.01
            self.dy = self.ycor() - target_y
            self.m = self.dy / self.dx

            self.state = 'launched'

    def explode(self):
        self.frame += 1.0
        if self.frame < 30.0:
            self.size = self.frame / 10
            self.shapesize(self.size, self.size, 0)
        elif self.frame < 55:
            self.size = (60 - self.frame) / 10
            self.shapesize(self.size, self.size, 0)
        else:
            self.destroy()

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None

    def tick(self):
        if self.state == 'launched':
            self.pendown()
            self.setx(self.xcor() + (1 / self.m) * self.speed)
            self.sety(self.ycor() + self.speed)

            # check if missile reached target
            a = self.xcor()-self.target_x
            b = self.ycor()-self.target_y
            distance = math.sqrt((a**2) + (b**2))

            if distance < 5:
                self.state = 'explode'

        if self.state == 'explode':
            self.explode()


class EnemyMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.dx = 0
        self.dy = 0
        self.speed = 2
        self.size = 0.2
        self.shapesize(self.size, self.size, 0)
        self.pendown()
        self.state = 'ready'
        self.target_x = 0
        self.target_y = 0
        self.frame = 2

    def set_target(self, target):
        self.target_x = target.xcor()
        self.target_y = target.ycor()
        # avoid dive by 0 logic error
        self.dx = self.xcor() - target.xcor()
        if self.dx == 0:
            self.dx = 0.01
        self.dy = self.ycor() - target.ycor()
        self.m = self.dy / self.dx
        self.state = 'launched'

    def explode(self):
        self.frame += 1.0
        if self.frame < 30.0:
            self.size = self.frame / 10
            self.shapesize(self.size, self.size, 0)
        elif self.frame < 55:
            self.size = (60 - self.frame) / 10
            self.shapesize(self.size, self.size, 0)
        else:
            self.destroy()

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None

    def tick(self):
        if self.state == 'launched':
            self.setx(self.xcor() - (1/self.m) * self.speed)
            self.sety(self.ycor() - self.speed)

            # check if missile reached target
            a = self.xcor() - self.target_x
            b = self.ycor() - self.target_y
            distance = math.sqrt((a ** 2) + (b ** 2))

            if distance < 10:
                self.state = 'explode'

        if self.state == 'explode':
            self.explode()


# Functions
def check_collision(missile, target, targets):
    # check if missile is exploding
    if missile.state == 'explode':
        radius = (missile.size * 20) / 2
        if missile.distance(target) < radius:
            target.destroy()
            targets.remove(target)


# Initial Game setup
# show hide/splash screen with 0, default is 5
game = MissileCommand(800, 600, "black", "Missile Command", 0)
game.score = 0
# Sprites

city1 = City("square", "green", -300, -250)

silo1 = Silo("square", "blue", 0, -200)

player_missile1 = PlayerMissile("circle", "white", 0, -250)

enemy_missile1 = EnemyMissile("circle", "red", 0, 250)
enemy_missile1.set_target(city1)

cities = [city1]
silos = [silo1]
player_missiles = [player_missile1]
enemy_missiles = [enemy_missile1]

# scoring
game_status = spgl.Label("Score: {}  Cities: {}  Silos: {}", "white", -300, 280)
# Buttons

# Keyboard Bindings

while True:
    game.tick()

    # check if player missile collides with enemy missile
    for player_missile in player_missiles:
        for enemy_missile in enemy_missiles:
            check_collision(player_missile, enemy_missile, enemy_missiles)

    # check if enemy missile collides with city or silos
    for enemy_missile in enemy_missiles:
        for city in cities:
            check_collision(enemy_missile, city, cities)

        for silo in silos:
            check_collision(enemy_missile, silo, silos)

    game_status.update("Score: {}  Cities: {}  Silos: {}".format(game.score, len(cities), len(silos)))
