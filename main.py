import math
import time
from classes import Game, Player, IA, Ball

def startup():
    """
    Game startup and loop.

    :return:
    """
    # Init entities.
    players = [IA(1), IA(2)] # Could be Player class or IA class.
    ball = Ball()

    # Main game variables
    passed_time = time.time()

    while not game.stop:
        delta = (time.time() - passed_time) * 5
        passed_time = time.time()

        # Prevent screen being shown when moving entities.
        game.screen.tracer(0)

        # Update user cords.
        game.screen.listen()
        if players[0].is_ia == False:
            game.screen.onkeypress(lambda: players[0].move(time=delta, direction="up"), key="w")
            game.screen.onkeypress(lambda: players[0].move(time=delta, direction="down"), key="s")
        if players[1].is_ia == False:
            game.screen.onkeypress(lambda: players[1].move(time=delta, direction="up"), key="Up")
            game.screen.onkeypress(lambda: players[1].move(time=delta, direction="down"), key="Down")

        # Update IA cords.
        if players[0].is_ia:
            direction1 = players[0].direction(ball=ball)
            players[0].move(time=delta, direction=direction1)
        if players[1].is_ia:
            direction2 = players[1].direction(ball=ball)
            players[1].move(time=delta, direction=direction2)

        # Update Ball movement cords.
        quantum = math.floor(delta/0.005)
        for i in range(quantum):
            ball.move(players=players, time=0.005)

        # Update entities position on the game (Player or IA and Ball)
        for player in players:
            player.place_position()
        ball.place_position()

        # Update main screen with all the changes.
        game.screen.update()


# Game Startup
game = Game()

# Main Startup Entrance
startup()

game.screen.mainloop()