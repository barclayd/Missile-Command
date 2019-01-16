# Import SPGL
import spgl


# Classes
class City(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def tick(self):
        pass


class Silo(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def tick(self):
        pass


class PlayerMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)

    def tick(self):
        pass


class EnemyMissile(spgl.Sprite):
    def __init__(self, shape, color, x, y):
        spgl.Sprite.__init__(self, shape, color, x, y)
        self.dx = 0
        self.dy = 0
        self.speed = 2

    def set_target(self, target):
        self.dx = self.xcor() - target.xcor()
        self.dy = self.ycor() - target.ycor()
        self.m = self.dy / self.dx
        print(self.dx, self.dy, self.m)

    def tick(self):
        self.setx(self.xcor() - (1/self.m) * self.speed)
        self.sety(self.ycor() - self.speed)

# Functions


# Initial Game setup
# show hide/splash screen with 0
game = spgl.Game(800, 600, "black", "Missile Command", 0)

# Sprites

city = City("square", "green", -300, -250)

silo = Silo("square", "blue", 0, -200)

player_missile = PlayerMissile("circle", "white", 0, -250)

enemy_missile = EnemyMissile("circle", "red", 0, 250)
enemy_missile.set_target(city)



# Labels

# Buttons

# Keyboard Bindings

while True:
    # Call the game tick method
    game.tick()
