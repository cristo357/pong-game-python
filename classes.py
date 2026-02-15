from turtle import Turtle, Screen
import math

'''
GAME CONFIG CONSTANT VARIABLES.
'''
# Map config.
MAP_DIMENSIONS = {
    "width": 800,
    "height": 500
}
MAP_DELIMETERS = {
    "x": 30,
    "y": 15
}
MAP_DIVIDER_LINES = 30
MAP_LIMITS = {
    "x": (MAP_DIMENSIONS["width"] / 2) - MAP_DELIMETERS["x"],
    "y": (MAP_DIMENSIONS["height"] / 2) - MAP_DELIMETERS["y"],
    "-x": (-MAP_DIMENSIONS["width"] / 2) + abs(MAP_DELIMETERS["x"]),
    "-y": (-MAP_DIMENSIONS["height"] / 2) + abs(MAP_DELIMETERS["x"])
}
# Speed config
PLAYER_SPEED = {
    "human": MAP_DIMENSIONS["width"] * 0.60,
    # Easy = 0.03, Medium = 0.31, Hard = 0.32, God = 0.4
    "ia": MAP_DIMENSIONS["width"] * 0.04
}
# Writing
FONTS ={
    "scoreboard": ('Courier', 40, 'bold'),
    "angle_draw": ('Courier', 10, 'normal')
}


class Vector:
    """
    Used for generating vector speed components on both (X,Y) and positioning cords as well.

    Speed vector: a component that used to determinate ball angle and speed, reducing the actual position the speed vector multiplied by a fixed time. Ex.: y = 50 + (45.77 * 0.05)
    """
    def __init__(self, x: float, y: float):
        """
        Init the speed vector or the position cord.

        :param x: (FLOAT) X cord of the speed vector / position
        :param y: (FLOAT) Y cord of the speed vector / position
        """
        self.x = x
        self.y = y

    def longitude(self) -> float:
        """
        Calculate the actual longitud of the speed vector from its origin.

        :return: (FLOAT) Longitude.
        """
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    def escale(self, speed_adjust: float) -> object:
        """
        Adjust the speed vector component to an adding/reducing (X,Y) position component.
        Ex.: ball.pos.y = 50, then speed vector is (11.234 * 0.05) = 0.5617, 50 +/- 0.5617

        :param speed_adjust: (FLOAT) Time to adjust the speed (generally 0.05)
        :return: (OBJECT) Vector
        """
        return Vector((self.x * speed_adjust), (self.y * speed_adjust))

    def sum(self, vector: object) -> object:
        """
        Sum actual .escale() speed vector to the (X,Y) positions.

        :param vector: (OBJECT) Actual position on (X,Y).
        :return: (OBJECT) Vector
        """
        return Vector((self.x + vector.x), (self.y + vector.y))

    def normalize(self) -> object:
        """
        Adjust vector speed depending on its longitude.

        :return: (OBJECT) Vector
        """
        longitude = self.longitude()

        if longitude != 0:
            vector = self.escale(1 / longitude)
        else:
            vector = Vector(x=0, y=0)

        return vector

    def rotate(self, angle: float) -> object:
        """
        Generate a new inclination angle when collision with a paddle depending on its actual angle.

        :param angle: (FLOAT) Current angle between ball and paddle.
        :return: (OBJECT) Vector
        """
        radians = math.radians(angle)

        # Calculate the new speed components in (X, Y)
        x = self.x * math.cos(radians) - self.y * math.sin(radians)
        y = self.x * math.sin(radians) + self.y * math.cos(radians)

        return Vector(x, y)

    def is_over_angle_limit(self, max_angle: int) -> bool:
        """
        Check if actual ball angle is over max angle in order to prevent being too horizontal.

        :param max_angle: (INT) Max angle.
        :return: (BOOL) True if over max angle / False if not.
        """
        current_angle = self.getAngle()
        current_angle += 360 if current_angle < 0 else 0 # Convert to 360 grades due to math.atan2 only returns degrees in -180 and +180

        LIMITS = {
            "top_right": max_angle,
            "top_left": 90 + max_angle,
            "bottom_left": 270 - max_angle,
            "bottom_right": 270 + max_angle
        }

        # Top cuadrant
        if current_angle > LIMITS["top_right"] and current_angle < LIMITS["top_left"]:
            return True
        # Bottom cuadrant.
        elif current_angle > LIMITS["bottom_left"] and current_angle < LIMITS["bottom_right"]:
            return True
        else:
            return False

    def getAngle(self) -> float:
        """
        Get current angle in ANGLE, not radians.

        :return: (FLOAT) Current angle.
        """
        return math.atan2(self.y, self.x) * 180 / math.pi

    def getRelativeAngle(self) -> float:
        """
        Get the relative angle to the paddle.

        :return: (FLOAT) Current relative angle.
        """
        angle = self.getAngle()

        if angle >= 180: angle -= 180
        if angle > 90: angle = 180 - angle
        if angle <= -180: angle += 180
        if angle < -90: angle = -180 - angle

        return angle

    def clone(self) -> object:
        """
        Clone the actual speed vector config.

        :return: (OBJECT) Vector
        """
        return Vector(self.x, self.y)


class Paddle:
    """
    Paddle main config.
    """
    def __init__(self, num_player: int):
        """
        Init the paddle.

        :param num_player: (INT) Number of player (1 or 2).
        """
        self.block_length = 3
        self.diameter = 20
        self.body_blocks = []
        self.num_player = num_player
        self.width = self.diameter
        self.height = self.diameter * self.block_length

        self.__init_paddle()

    def __init_paddle(self) -> None:
        """
        Init the paddle position on the left or right side of the screen.

        :return:
        """
        for block in range(self.block_length):
            self.body_blocks.append(Turtle(shape="square"))
            self.body_blocks[block].color("white")
            self.body_blocks[block].shapesize(stretch_len=(self.diameter / 20), stretch_wid=(self.diameter / 20))

            if block == 0:
                self.body_blocks[block].pos = Vector((MAP_LIMITS["-x"] if self.num_player == 1 else MAP_LIMITS["x"]), 0)
            elif block % 2 == 0:
                self.body_blocks[block].pos = Vector((MAP_LIMITS["-x"] if self.num_player == 1 else MAP_LIMITS["x"]), self.body_blocks[block - 2].ycor() - 20)
            else:
                if block == 1:
                    self.body_blocks[block].pos = Vector((MAP_LIMITS["-x"] if self.num_player == 1 else MAP_LIMITS["x"]), self.body_blocks[block - 1].ycor() + 20)
                else:
                    self.body_blocks[block].pos = Vector((MAP_LIMITS["-x"] if self.num_player == 1 else MAP_LIMITS["x"]), self.body_blocks[block - 2].ycor() + 20)

    def __map_collission(self, direction: str) -> bool:
        """
        Check if paddle is in collission with the top and bottom screen.

        :param direction: (STR) "up" or "down"
        :return: (BOOL) True if in collision / False if not.
        """
        half = self.height / 2

        if direction == "up":
            if (self.body_blocks[0].pos.y + half) < MAP_LIMITS["y"]:
                return False
        elif direction == "down":
            if (self.body_blocks[0].pos.y - half) > MAP_LIMITS["-y"]:
                return False

        return True

    def move(self, time: float, direction: str) -> None:
        """
        Moving the paddles.

        :param time: (FLOAT) Given time to adjust the speed (generally 0.05)
        :param direction: (STR) "up", "down" or "hold"
        :return:
        """
        # y = y * Vy * t
        distance = round(self.speed * time)

        if not self.__map_collission(direction=direction):
                for block in self.body_blocks:
                    if direction == "hold":
                        continue
                    elif direction == "up":
                        block.pos.y = (block.pos.y + distance)
                    elif direction == "down":
                        block.pos.y = (block.pos.y - distance)

    def place_position(self) -> None:
        """
        Place the actual paddle position into the screen.

        :return:
        """
        for block in self.body_blocks:
            block.teleport(block.pos.x, block.pos.y)


class Player(Paddle):
    """
    Human controlled paddle.
    """
    def __init__(self, num_player):
        """
        Init the paddle as well as the human paddle config.

        :param num_player: (INT) Number of player (1 or 2)
        """
        super().__init__(num_player=num_player)
        self.is_ia = False
        self.score = Scoreboard(player=num_player)
        self.speed = PLAYER_SPEED["human"]


class IA(Paddle):
    """
    Computer controlled paddle.
    """
    def __init__(self, num_player):
        """
        Init the paddle as well as the computer paddle config.

        :param num_player: (INT) Number of player (1 or 2)
        """
        super().__init__(num_player=num_player)
        self.is_ia = True
        self.score = Scoreboard(player=num_player)
        self.speed = PLAYER_SPEED["ia"]
        self.prediction = None

    def calculate_bounces(self, ball: object) -> None:
        """
        Calculate the bounces of the ball in order to position whe computer controlled paddle in the correct direction.

        :param ball: (OBJECT) Actual ball instance (with all its attributes).
        :return:
        """
        if self.prediction != None:
            return

        # Actual time bewteen ball and paddle.
        time = (abs(self.body_blocks[0].pos.x) + abs(ball.pos.x)) / abs(ball.vector.x)

        # Init calc of the y cord position
        y = ball.vector.y * time + ball.pos.y

        # Adjust Y cord depending on num of bounces on the walls.
        # Because Y could go over map limits, adjust the calculation to detect ball collission on the y cord sides.
        low = MAP_LIMITS["-y"]
        high = MAP_LIMITS["y"]

        while y < low or y > high:
            if y < low:
                y = low + (abs(y) - abs(low))
            elif y > high:
                y = high - (y - high)

        self.prediction = y

    def direction(self, ball: object) -> str:
        """
        Control when to start moving the paddle and when to go to the center position.

        :param ball: (OBJECT) Actual ball instance (with all its attributes).
        :return: (STR) "up", "down" or "hold"
        """
        ideal = None

        if (self.num_player == 1 and ball.vector.x > 0) or (self.num_player == 2 and ball.vector.x < 0):
            ideal = 0 # Center of the screen (MAP_LIMITS["x" or "-x"], 0)
            self.prediction = None
        else:
            self.calculate_bounces(ball=ball)
            ideal = self.prediction

        ball_side = ball.diameter / 2
        if ideal - ball_side < self.body_blocks[0].pos.y - self.height / self.block_length:
            return "down"
        elif ideal + ball_side > self.body_blocks[0].pos.y + self.height / self.block_length:
            return "up"

        return "hold"


class Ball(Turtle):
    """
    Creates and controls the ball.
    """
    def __init__(self):
        """
        Init the ball and all its variables, as well as place to its init pos.
        """
        # Speed
        self.init_speed = MAP_DIMENSIONS["height"] * 0.1
        self.speed = self.init_speed
        self.speed_increment = 5

        # Vector speed movement
        self.vector: object

        # Ball position
        self.init_pos = Vector(x=0, y=0)
        self.pos: object

        # Angle movement
        self.max_angle = 40

        # Ball size
        self.diameter = 20

        # Ball init
        super().__init__(shape="square")
        self.color("white")
        self.shapesize(stretch_len=(self.diameter / 20), stretch_wid=(self.diameter / 20))

        # Angle drawer
        self._drawer = Turtle(visible=False)

        # Put ball into center and set X vector to -1.
        self.relocate(-1)

    def increment_speed(self) -> None:
        """
        Increment the speed vector when collission with a paddle.

        :return:
        """
        self.speed += self.speed_increment
        self.vector = self.vector.normalize().escale(self.speed)

    def relocate(self, direction: int) -> None:
        """
        Re-position the ball to the center of the screen.
        Depending on the actual vector direction config, the ball will start moving to the left or right side.

        :param direction: (INT) -1 to start moving on left side or 1 to the right side.
        :return:
        """
        self.speed = self.init_speed
        self.pos = self.init_pos.clone()
        # Set a no-zero value in Y in order to not gettin' a 0 grade angle.
        self.vector = Vector(x=direction, y=0.2).normalize().escale(self.init_speed)

    def move(self, players: list, time: float) -> None:
        """
        Start moving the ball.
        Adding or reducing the actual speed vector components on (X,Y) to the actual (X,Y) ball position.

        :param players: (LIST) all players instances with all its attributes.
        :param time: (FLOAT) Actual time to adjust the speed vector (generally 0.05).
        :return:
        """
        # Sum the speed vector adjustment to the actual (X,Y) POSITION.
        self.pos = self.pos.sum(self.vector.escale(time))

        # Goal on each player side.
        if self.pos.x < MAP_LIMITS["-x"]:
            players[1].score.update()
            self.relocate(1)
        elif self.pos.x > MAP_LIMITS["x"]:
            players[0].score.update()
            self.relocate(-1)

        # Map sides
        if self.pos.y > MAP_LIMITS["y"]:
            self.vector.y *= -1
            self.draw_angle()
        elif self.pos.y < MAP_LIMITS["-y"]:
            self.vector.y *= -1
            self.draw_angle()

        # Ball collision on paddle.
        vector: object
        if self.vector.x < 0 and self.collision(players[0]):
            self.vector.x *= -1
            self.increment_speed()
            vector = self.vector.clone() # Clone vector. Used in case .rotate() gives a high horizontal angle.
            self.vector = self.vector.rotate(self.pos.y - players[0].body_blocks[0].pos.y)

            # Checking current angle in order to prevent ball being too vertical.
            # Fix the angle if neccesary in order to maintain the diagonal movement.
            if self.vector.is_over_angle_limit(self.max_angle):
                self.vector = vector

            self.draw_angle()
        elif self.vector.x > 0 and self.collision(players[1]):
            self.vector.x *= -1
            self.increment_speed()
            vector = self.vector.clone()
            self.vector = self.vector.rotate(players[1].body_blocks[0].pos.y - self.pos.y)

            if self.vector.is_over_angle_limit(self.max_angle):
                self.vector = vector

            self.draw_angle()

    def collision(self, paddle: object) -> bool:
        """
        Detect ball collission on the paddles.

        :param paddle: (OBJECT) Paddle instance with all its attributes.
        :return: (BOOL) True if in collission / False if not.
        """
        ball_side = (self.diameter / 2)

        if self.pos.x + ball_side < paddle.body_blocks[0].pos.x - (paddle.width / 2): return False
        if self.pos.y + ball_side < paddle.body_blocks[0].pos.y - (paddle.height / 2): return False
        if self.pos.x - ball_side > paddle.body_blocks[0].pos.x + (paddle.width / 2): return False
        if self.pos.y - ball_side > paddle.body_blocks[0].pos.y + (paddle.height / 2): return False

        return True

    def draw_angle(self) -> None:
        """
        Draw the actual ball relative angle on the bottom left of the screen.

        :return:
        """
        self._drawer.clear()
        self._drawer.teleport(x=MAP_LIMITS["-x"] + 45, y=MAP_LIMITS["-y"])
        self._drawer.color("white")

        self._drawer.write(arg=f"Angle: {round(self.vector.getRelativeAngle(), 2)}", move=False, align="center", font=FONTS["angle_draw"])


    def place_position(self):
        """
        Update on the screen the actual ball position.

        :return:
        """
        self.teleport(self.pos.x, self.pos.y)


class Scoreboard(Turtle):
    """
    Hits record of all involved players (1 and 2).
    """
    def __init__(self, player: int):
        """
        Init the player scoreboard.

        :param player: (INT) Number of player (1 or 2).
        """
        super().__init__(visible=False)
        self.color("white")
        self.num_player = player
        self.current_score = -1 # On 1st init, need to be 0.
        self.update()

    def update(self) -> None:
        """
        Update the player score if hit a goal.

        :return:
        """
        self.current_score += 1
        self.clear()

        if self.num_player == 1:
            self.teleport(x=-40, y=(MAP_LIMITS["y"] - 55))
        else:
            self.teleport(x=40, y=(MAP_LIMITS["y"] - 55))

        self.write(arg=f"{self.current_score}", move=False, align="center", font=FONTS["scoreboard"])


class Game:
    """
    Game screen config.
    """
    def __init__(self):
        """
        Init the screen and game variables.
        """
        self.screen = Screen()
        self.screen.title("Arcade Pong (by MasterCoria)")
        self.screen.setup(MAP_DIMENSIONS["width"], MAP_DIMENSIONS["height"])
        self.screen.bgcolor("black")

        # Game variables
        self.stop = False

        # Map dividers
        self.screen.tracer(0)
        self.__draw_map_divider()
        self.screen.update()


    def __draw_map_divider(self):
        """
        Draw map divider between player 1 and 2.

        :return:
        """
        self.dividers = []
        # StrokeLine height + init delimeter length
        self.num_dividers = (MAP_LIMITS["y"] * 2) / (20 + 10)
        self.delimeter = 10 if self.num_dividers % 2 == 0 else 10 + \
            ((((MAP_LIMITS["y"] * 2) * float("0." + str(self.num_dividers).split('.')[1])) \
              / math.floor(self.num_dividers)) / math.floor(self.num_dividers))
        self.num_dividers = math.floor(self.num_dividers)

        for block in range(self.num_dividers):
            self.dividers.append(Turtle(shape="square"))
            self.dividers[block].shapesize(stretch_len=0.3, stretch_wid=1)
            self.dividers[block].color("white")

            if block == 0:
                # Remeber that .ycor() is in center of the block. Each block is 20 points height so we ensure not standing 10 points out of the Y Cord MAP LIMIT.
                self.dividers[block].teleport(0, (MAP_LIMITS["y"] - 10))
            else:
                self.dividers[block].teleport(0, (self.dividers[block - 1].ycor() - 20 - self.delimeter))

