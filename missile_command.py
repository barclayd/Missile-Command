import spgl


# Classes
class MissileCommand(spgl.Game):
    def __init__(self, screen_width, screen_height, background_colour, title, splash_time):
        spgl.Game.__init__(self, screen_width, screen_height, background_colour, title, splash_time)

    def click(self, x, y):
        player_missile.set_target(x, y)


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
        self.speed = 7
        self.state = 'ready'
        self.target_x = 0
        self.target_y = 0

    def set_target(self, target_x, target_y):
        if self.state == 'ready':
            self.target_x = target_x
            self.target_y = target_y

            self.dx = self.xcor() - target_x
            self.dy = self.ycor() - target_y
            self.m = self.dy / self.dx

            self.state = 'launched'

    def tick(self):
        if self.state == 'launched':
            self.setx(self.xcor() + (1 / self.m) * self.speed)
            self.sety(self.ycor() + self.speed)


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
# show hide/splash screen with 0, default is 5
game = MissileCommand(800, 600, "black", "Missile Command", 0)

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
