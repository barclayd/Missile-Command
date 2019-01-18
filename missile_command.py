import spgl
import math
import random


# Classes
class MissileCommand(spgl.Game):
    def __init__(self, screen_width, screen_height, background_colour, title, splash_time):
        spgl.Game.__init__(self, screen_width, screen_height, background_colour, title, splash_time)
        self.level = 1
        self.score = 0

    def click(self, x, y):
        closest_missile = None
        closest_missile_distance = 100000
        for player_missile in player_missiles:
            if player_missile.state == 'ready':
                a = player_missile.xcor()-x
                b = player_missile.ycor()-y
                distance = math.sqrt((a**2) + (b**2))
                if distance < closest_missile_distance:
                    closest_missile = player_missile
                    closest_missile_distance = distance
        if closest_missile:
            closest_missile.set_target(x, y)


class City(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.name = 'City'

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None
        cities.remove(self)

    def tick(self):
        pass


class Silo(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.name = 'Silo'

    def destroy(self):
        self.clear()
        self.penup()
        self.setposition(2000, 2000)
        self.state = None
        silos.remove(self)

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
        self.name = 'Player'

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
        player_missiles.remove(self)

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
        self.speed = 4
        self.size = 0.2
        self.shapesize(self.size, self.size, 0)
        self.pendown()
        self.state = 'ready'
        self.target_x = 0
        self.target_y = 0
        self.frame = 2
        self.name = 'Enemy'

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
        enemy_missiles.remove(self)

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


# functions
def check_collision(missile, target):
    # check if missile is exploding
    if missile.state == 'explode':
        radius = (missile.size * 20) / 2
        if missile.distance(target) < radius:
            missile.destroy()
            target.destroy()
            if missile.name == 'Player' and target.name == 'Enemy':
                game.score += 10


# Game set up and scoring
# show hide/splash screen with 0, default is 5
game = MissileCommand(800, 600, "black", "Missile Command", 0)

# Sprites
cities = []
silos = []
# active player missiles used at each level
player_missiles = []
# all player missiles
player_missiles_storage = []
# active enemy missiles used at each level
enemy_missiles = []
# all enemy missiles
enemy_missiles_storage = []

for i in range(6):
    cities.append(City("square", "green", -250 + (i * 100), -250))

for i in range(3):
    silos.append(Silo("square", "blue", -350 + (i * 350), -225))

for i in range(30):
    if i < 10:
        x = -350
    elif i < 20:
        x = 0
    else:
        x = 350

    player_missiles_storage.append(PlayerMissile("circle", "white", x, -225))

for player_missile in player_missiles_storage:
    player_missiles.append(player_missile)

for i in range(30):
    enemy_missiles_storage.append(EnemyMissile("circle", "red", random.randint(-450, 450), random.randint(400, 800)))

for enemy_missile in enemy_missiles_storage:
    if len(enemy_missiles) < game.level:
        enemy_missile.set_target(random.choice(cities))
        enemy_missiles.append(enemy_missile)


# scoring
game_status = spgl.Label("Level: {} \nScore: {} \nCities: {}  \nSilos: {} \nPlayer Missiles: {} \nEnemy Missiles: {}",
                         "white", -390, 210)

while True:
    game.tick()

    # check if player missile collides with enemy missile
    for player_missile in player_missiles:
        for enemy_missile in enemy_missiles:
            check_collision(player_missile, enemy_missile)

    # check if enemy missile collides with city or silos
    for enemy_missile in enemy_missiles:
        for city in cities:
            check_collision(enemy_missile, city)

        for silo in silos:
            check_collision(enemy_missile, silo)

    # no more enemy missiles left
    if len(enemy_missiles) < 1:
        # add up score
        city_bonus = 100 * len(cities)
        silos_bonus = 50 * len(silos)
        missile_bonus = 10 * len(player_missiles)

        game.score += (city_bonus + silos_bonus + missile_bonus)
        print("Level {} Complete".format(game.level))
        print("City bonus: {} Silo bonus: {} Missile bonus: {}".format(city_bonus, silos_bonus, missile_bonus))
        game.level += 1

        # reset enemy missiles
        for enemy_missile in enemy_missiles_storage:
            if len(enemy_missiles) < game.level:
                enemy_missile.set_target(random.choice(cities + silos))
                enemy_missiles.append(enemy_missile)

        # reset player missiles
        for player_missile in player_missiles:
            player_missile.destroy()

        player_missiles = []

        for player_missile in player_missiles_storage:
            player_missiles.append(player_missile)

        for i in range(30):
            if i < 10:
                x = -350
            elif i < 20:
                x = 0
            else:
                x = 350

            player_missiles[i].clear()
            player_missiles[i].state = 'ready'
            player_missiles[i].setposition(x, -225)
            player_missiles[i].shapesize(0.2, 0.2, 0)
            player_missiles[i].clear()

    game_status.update("Level: {} \nScore: {} \nCities: {}  \nSilos: {} \nPlayer Missiles: {} \nEnemy Missiles: {}"
                       .format(game.level, game.score, len(cities),
                               len(silos), len(player_missiles), len(enemy_missiles)))
