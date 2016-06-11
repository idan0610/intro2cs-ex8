######################################################################
# FILE: asteroidsMain.py
# WRITER: Idan Refaeli, idan0610, 305681132
# EXERCISE: intro2cs ex8 2014-2015
# DESCRIPTION:
# Functions cares for the running of Asteroids game
#######################################################################

from torpedo import *
from asteroid import *
from spaceship import *
from gameMaster import *
import math
import sys

PI = math.pi
FLAT_ANGLE = 180
NUM_OF_TORPEDOES = 20
SCORE_SIZE_1 = 100
SCORE_SIZE_2 = 50
SCORE_SIZE_3 = 20
SHIP_DOWN_TITLE = "Lost 1 life!"
SHIP_DOWN_MESSAGE = "The spaceship got hit by an asteroid"
STOP_WIN_TITLE = "You Win!"
STOP_WIN_MESSAGE = "You destroyed all the asteroids!"
STOP_LOST_TITLE = "You lost!"
STOP_LOST_MESSAGE = "You have lost all your lives!"
STOP_QUIT_TITLE = "Quit"
STOP_QUIT_MESSAGE = "You chose to quit"
DEFAULT_AMOUNT = 3
NUM_OF_ARGUMENTS = 2

def _convert_to_radians(degrees):
    """
    The function coverts degrees to radians

    :param degrees: float, the angle in degrees
    :return: radians: float, the angle in radians
    """

    # According the formula for converting degrees to radians:
    radians = (degrees * PI) / FLAT_ANGLE
    return radians


class GameRunner:

    def __init__(self, amnt = 3):
        self.game = GameMaster()
        self.screenMaxX = self.game.get_screen_max_x()
        self.screenMaxY = self.game.get_screen_max_y()
        self.screenMinX = self.game.get_screen_min_x()
        self.screenMinY = self.game.get_screen_min_y()
        shipStartX = (self.screenMaxX-self.screenMinX)/2 + self.screenMinX
        shipStartY = (self.screenMaxY-self.screenMinY)/2 + self.screenMinY
        self.game.set_initial_ship_cords(shipStartX, shipStartY)
        self.game.add_initial_astroids(amnt)
        self.num_of_torpedoes = 0
        self.deadtorpedoes = []
        self.deadasteroids = []

    def run(self):
        self._do_loop()
        self.game.start_game()


    def _do_loop(self):
        self.game.update_screen()
        self.game_loop()
        # Set the timer to go off again
        self.game.ontimer(self._do_loop,5)

    def move_object(self, obj):
        """
        The function get an object from the game and move it according to its
        current speed, coordinates and the size of the screen

        :param obj: torpedo, asteroid, or spaceship
        :return:
        """

        # Get the current speed of the object on both axis
        speed_x = obj.get_speed_x()
        speed_y = obj.get_speed_y()

        # Get the current coordinates of the object
        old_cord_x = obj.get_x_cor()
        old_cord_y = obj.get_y_cor()

        # Get the size of the screen
        x_min_cord, x_max_cord = self.screenMinX, self.screenMaxX
        y_min_cord, y_max_cord = self.screenMinY, self.screenMaxY

        delta_x = x_max_cord - x_min_cord
        delta_y = y_max_cord - y_min_cord

        # Calculate the new coordinates according the guidance on Targil
        new_cord_x = (speed_x + old_cord_x - x_min_cord) % delta_x + x_min_cord
        new_cord_y = (speed_y + old_cord_y - y_min_cord) % delta_y + y_min_cord

        # Move the object to the new coordinates
        obj.move(new_cord_x, new_cord_y)

    def move_asteroids(self):
        """
        The function moves all the asteroids exist currently

        :return: None
        """

        asteroids = self.game.get_asteroids()  # List of asteroids currently
        num_of_asteroids = len(asteroids)  # Number of asteroids currently

        for i in range(num_of_asteroids):
            # Move each asteroid using move_object
            current_asteroid = asteroids[i]
            self.move_object(current_asteroid)

    def move_spaceship(self):
        """
        The function move the spaceship according its angle and speed

        :return: None
        """

        ship = self.game.get_ship()  # The spaceship (the player)

        if self.game.is_right_pressed():
            # If the right button pressed, increase the angle of ship
            ship.increase_angle()
        elif self.game.is_left_pressed():
            # If the right button pressed, decrease the angle of ship
            ship.decrease_angle()
        elif self.game.is_up_pressed():
            # If the up button pressed, accelerate the spaceship

            # Get the current speed of ship on both axis
            current_speed_x = ship.get_speed_x()
            current_speed_y = ship.get_speed_y()

            # Get the angles of ship in degrees and convert it to radians
            ship_angle_degrees = ship.get_angle()
            ship_angle_radians = _convert_to_radians(ship_angle_degrees)

            # Calculate the new speed on both axis, according the guidance
            # on Targil
            new_speed_x = current_speed_x + math.cos(ship_angle_radians)
            new_speed_y = current_speed_y + math.sin(ship_angle_radians)

            # Set the new speed of ship on both axis
            ship.set_speed_x(new_speed_x)
            ship.set_speed_y(new_speed_y)

        # Move the ship using move_object
        self.move_object(ship)

    def fire_torpedoes(self):
        """
        The function fire torpedoes according to user request. The spaceship
        may fire no more then 20 torpedoes.

        :return: None
        """

        ship = self.game.get_ship()  # The spaceship

        while self.game.is_fire_pressed() and self.num_of_torpedoes <= \
                NUM_OF_TORPEDOES:
            # The loop will continue until the player stop to press the fire
            # button or the spaceship fired 20 torpedoes

            # Get the current speed of ship on both axis
            ship_speed_x = ship.get_speed_x()
            ship_speed_y = ship.get_speed_y()

            # Get the angles of ship in degrees and convert it to radians
            ship_angle_degrees = ship.get_angle()
            ship_angle_radians = _convert_to_radians(ship_angle_degrees)

            # Calculate the speed of torpedo according the guidance in Targil
            torpedo_speed_x = ship_speed_x + 2 * math.cos(ship_angle_radians)
            torpedo_speed_y = ship_speed_y + 2 * math.sin(ship_angle_radians)

            # Put the torpedo on the same location of the ship and with the
            # same angel of the ship (degrees)
            torpedo_cord_x = ship.get_x_cor()
            torpedo_cord_y = ship.get_y_cor()
            torpedo_angle = ship_angle_degrees

            # Add the torpedo using add_torpedo
            self.game.add_torpedo(torpedo_cord_x, torpedo_cord_y, \
                                  torpedo_speed_x, torpedo_speed_y, \
                                  torpedo_angle)

            self.num_of_torpedoes += 1

    def move_torpedoes(self):
        """
        The function move all the torpedoes exist currently
        and add torpedoes with life_span <= 0 to the deadtorpedoes list

        :return: None
        """

        torpedoes = self.game.get_torpedos()  # List of live torpedoes
        num_of_torpedoes = len(torpedoes)  # Number of live torpedoes

        for i in range(num_of_torpedoes):
            # Move each torpedo using move_object and check if the torpedo is
            # dead
            current_torpedo = torpedoes[i]
            self.move_object(current_torpedo)
            life_span_torpedo = current_torpedo.get_life_span()
            if life_span_torpedo <= 0:
                # If the life of current torpedo <= 0, add it to the lise
                # of torpedoes to remove
                self.deadtorpedoes.append(current_torpedo)
                self.num_of_torpedoes -= 1

    def asteroids_explode(self):
        """
        The function check if a torpedo hit an asteroid, removes both and
        create 2 new asteroids if necessary

        :return: None
        """

        asteroids = self.game.get_asteroids()  # List of live asteroids
        torpedoes = self.game.get_torpedos()  # List of live torpedoes
        num_of_asteroids = len(asteroids)  # Number of live asteroids
        num_of_torpedoes = len(torpedoes)  # Number of live torpedoes

        for i in range(num_of_torpedoes):
            for j in range(num_of_asteroids):
                # Check if there is an intersect between each couple of
                # torpedoes and asteroids
                current_asteroid = asteroids[j]
                current_torpedo = torpedoes[i]
                size_of_asteroid = current_asteroid.get_size()
                if self.game.intersect(torpedoes[i], asteroids[j]):
                    # If the current torpedo and asteroid checked are intersect
                    if size_of_asteroid > 1:
                        # If the asteroid got hit is bigger then size 1
                        # add 2 new asteroids
                        if size_of_asteroid == 2:
                            # If the asteroid got his is size 2, add 50 points
                            # to score
                            self.game.add_to_score(SCORE_SIZE_2)
                        else:
                            # If the asteroid got his is size 3, add 100 points
                            # to score
                            self.game.add_to_score(SCORE_SIZE_3)

                        # Get the coordinates of the asteroid
                        cord_x = current_asteroid.get_x_cor()
                        cord_y = current_asteroid.get_y_cor()

                        # Get the current speed of the asteroid
                        current_speed_x = current_asteroid.get_speed_x()
                        current_speed_y = current_asteroid.get_speed_y()

                        # Calculate the overall speed, for calculating the
                        # new speed of the new asteroids
                        speed = (current_speed_x**2 + current_speed_y**2)**0.5

                        # Get the speed of the torpedo
                        torpedo_speed_x = current_torpedo.get_speed_x()
                        torpedo_speed_y = current_torpedo.get_speed_y()

                        # Calculate the speed for the new asteroids according
                        # the guidance in Targil
                        new_speed_x = (torpedo_speed_x + current_speed_x)/speed
                        new_speed_y = (torpedo_speed_y + current_speed_y)/speed

                        # The second new speed is the speed for the second
                        # asteroid created from the intersection and is
                        # the additive inverse of the new speed
                        second_new_speed_x = -1 * new_speed_x
                        second_new_speed_y = -1 * new_speed_y

                        # Add the 2 new asteroids using add_asteroid
                        self.game.add_asteroid(cord_x, cord_y, new_speed_x, \
                                    new_speed_y, size_of_asteroid - 1)
                        self.game.add_asteroid(cord_x, cord_y, \
                                    second_new_speed_x, second_new_speed_y, \
                                    size_of_asteroid - 1)
                    else:
                        # If the asteroid got his is size 1, add 20 points
                        # to score
                        self.game.add_to_score(SCORE_SIZE_1)

                    # Add The original torpedo and asteroid to the lists of
                    # torpedoes and asteroids to remove
                    if self.deadasteroids.count(current_asteroid) == 0:
                        self.deadasteroids.append(current_asteroid)
                    if self.deadtorpedoes.count(current_torpedo) == 0:
                        self.deadtorpedoes.append(current_torpedo)
                    self.num_of_torpedoes -= 1

    def remove_dead_torpedoes_and_asteroids(self):
        """
        The function remove the current asteroids and torpedoes that are
        on the lists of dead asteroids and torpedoes, and reset the lists
        to an empty list

        :return: None
        """

        # Use remove_torpedoes to remove the torpedoes from the list of dead
        # torpedoes and reset the list to empty
        self.game.remove_torpedos(self.deadtorpedoes)
        self.deadtorpedoes = []

        num_of_asteroids_to_remove = len(self.deadasteroids)

        for i in range(num_of_asteroids_to_remove):
            # Remove each asteroid from the list of asteroids to remove
            # using remove_asteroid
            self.game.remove_asteroid(self.deadasteroids[i])

        # Reset the list of dead asteroids to empty
        self.deadasteroids = []

    def spaceship_hit(self):
        """
        The function check if the spaceship got hit by an asteroid, and lower
        1 life if that happened

        :return: None
        """

        ship = self.game.get_ship()  # The spaceship

        asteroids = self.game.get_asteroids()  # List of live asteroids
        num_of_asteroids = len(asteroids)  # Number of live asteroids
        was_hit = False  # If the ship got hit by at least 1 asteroid,
                              # show_message = True

        for i in range(num_of_asteroids):
            # Check the ship got hit by each asteroid
            current_asteroid = asteroids[i]
            if self.game.intersect(ship, current_asteroid):
                # If there is an intersection between the ship and the
                # current asteroid
                was_hit = True  # The message will be shown
                if self.deadasteroids.count(current_asteroid) == 0:
                    self.deadasteroids.append(current_asteroid)  # Add the
                                # asteroid to the list of dead asteroids

        if was_hit:
            # If the ship got hit by at least 1 asteroid, a message informing
            # the player he lost 1 life will show
            self.game.ship_down()  # Low 1 life
            self.game.show_message(SHIP_DOWN_TITLE, SHIP_DOWN_MESSAGE)

    def stop_game(self):
        """
        The function check if game ended because the player won or lost,
        or if he chose to quit

        :return: None
        """

        asteroids = self.game.get_asteroids()  # List of live asteroids
        num_of_asteroids = len(asteroids)  # Number of live asteroids
        num_lives = self.game.get_num_lives()  # Number of lives left
        end_game = False  # If the game needs to end, end_game = True

        if num_lives == 0:
            # If the player lost all his lives, show a message he lost
            # and set end_game = True
            self.game.show_message(STOP_LOST_TITLE, STOP_LOST_MESSAGE)
            end_game = True
        elif num_of_asteroids == 0:
            # If the player destroyed all the asteroids and won, show a
            # message he won and set end_game = True
            self.game.show_message(STOP_WIN_TITLE, STOP_WIN_MESSAGE)
            end_game = True
        elif self.game.should_end():
            # If the player chose to quit, show a message indicating that
            # and set end_game = True
            self.game.show_message(STOP_QUIT_TITLE, STOP_QUIT_MESSAGE)
            end_game = True

        if end_game:
            # If 1 of the 3 situations for ending the game happened,
            # the game has ended
            self.game.end_game()


    def game_loop(self):
        """
        The function takes care for the running of the game correctly
        (on the right order). The function starts again over and over until
        the game has ended

        :return: None
        """

        self.move_asteroids()  # Move all live asteroids
        self.move_spaceship()  # Move the spaceship
        self.fire_torpedoes()  # Fire new torpedoes
        self.move_torpedoes()  # Move the live torpedoes
        self.asteroids_explode()  # If the player hit an asteroid, remove it
                                  # and add 2 new asteroids if necessary
        self.spaceship_hit()  # If the spaceship got hit by an asteroid, remove
                              # the asteroid and reduce 1 life
        self.remove_dead_torpedoes_and_asteroids()  # Remove dead torpedoes
                                                    # and asteroids
        self.stop_game()  # If the game has ended, quit the game


def main():
    # Set amount_of_asteroids as 3 for default in case the user didn't entered
    # an amount of asteroids, or entered invalid amount ( <= 0)
    amount_of_asteroids = DEFAULT_AMOUNT
    if len(sys.argv) == NUM_OF_ARGUMENTS:
        # If the player entered an amount of asteroids
        if int(sys.argv[1]) > 0:
            # if the amount entered is valid
            amount_of_asteroids = int(sys.argv[1])
    runner = GameRunner(amount_of_asteroids)
    runner.run()

if __name__ == "__main__":
    main()
