# CS 76: Artificial Intelligence - PA6: Hidden Markov Models
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming

from Maze import Maze
import numpy as np

# A class that handles the UI building of the robot works.
class RobotUI:

    # Constructor, takes in a model, the filtering distributions. That's all we need!
    def __init__(self, robotic_model, filtered_distributions):
        self.robotic_model = robotic_model
        self.filtered_distributions = filtered_distributions

    def display(self):
        # First we want to show the initial position and the first distribution for the robot when no moves
        print("Move 0:")
        print("--------------------------")
        # We show the actual move first
        print("Actual Location in Maze:")
        self.robotic_model.maze.robotloc = self.robotic_model.initial_location
        print(str(self.robotic_model.maze))

        # Now the Initial Prior Distribution
        print("What the Robot Thinks:")
        self.get_position_distribution(self.robotic_model.prior_matrix)

        # Awesome, now we have the first move. Lets do this for the rest
        move = 1
        for distribution in self.filtered_distributions:
            print('\n')
            print("Move " + str(move) + ":")
            print("--------------------------")

            # We show the actual move first
            print("Actual Location in Maze: Moved " + str(self.robotic_model.moves[move - 1]))
            location = self.robotic_model.locations[move - 1]
            self.robotic_model.maze.robotloc = location
            print(str(self.robotic_model.maze))

            # Now we show the distribution
            print("What the Robot Thinks after observing: " + str(self.robotic_model.color_sequence[move - 1]))
            pos_dist = self.get_position_distribution(distribution)

            # For fun, lets get the most likely location
            max_index = np.where(pos_dist == np.amax(pos_dist))
            list_of_coords = list(zip(max_index[0], max_index[1]))
            # Create a tuple
            state = ()
            for coords in list_of_coords:
                coord = (coords[1], self.robotic_model.maze.height - 1 - coords[0])
                state += coord

            # Now update maze, print it
            print("\n Most Likely Locations:")
            self.robotic_model.maze.robotloc = state
            print(str(self.robotic_model.maze))

            self.print_color_matrix()

            # Increment move
            move += 1

    # A stochastic matrix of positions based on a distribution
    def get_position_distribution(self, distribution):
        # A matrix to hold probabilities
        pos_matrix = np.zeros((self.robotic_model.maze.height, self.robotic_model.maze.width))

        # Now, begin the transfer
        for pos in range(len(distribution)):
            row = self.robotic_model.maze.height - 1 - pos//self.robotic_model.maze.width
            col = pos % self.robotic_model.maze.width

            # Now just store
            pos_matrix[row][col] = float(distribution[pos] * 100)
        string_representation = ""
        for x in range(self.robotic_model.maze.height):
            for y in range(self.robotic_model.maze.width):
                string_representation += ('%.02f\t' % (pos_matrix[x][y]))
            string_representation += '\n'
        print(string_representation)
        return pos_matrix

    # Prints color representation matrix
    def print_color_matrix(self):
        string_representation = ""
        for x in range(self.robotic_model.maze.height):
            for y in range(self.robotic_model.maze.width):
                string_representation += ('%s\t' % self.robotic_model.color_dict[self.robotic_model.color_matrix[x][y]])
            string_representation += '\n'
        print(string_representation)


