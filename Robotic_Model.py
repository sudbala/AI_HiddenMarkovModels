# CS 76: Artificial Intelligence - PA6: Hidden Markov Models
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming

from model import model
import random
from Maze import Maze
import numpy as np


class Robotic_Model(model):

    # Constructor for the Robot model class
    def __init__(self, maze_file_name, move_limit, initial_position):

        # Maze Work
        self.maze = Maze(maze_file_name)
        self.initial_location = initial_position
        self.location = initial_position
        self.locations = []

        # Colors
        self.color_matrix = np.zeros((self.maze.height, self.maze.width))
        self.color_dict = {1: 'r', 2: 'g', 3: 'y', 4: 'b'}
        self.colors = list(self.color_dict.keys())
        self.color_sequence = []

        # Moves
        self.move_dict = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}
        self.move_robot_dict = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
        self.move_limit = move_limit
        self.moves = []

        # Maze initialization, makes a color matrix, color sequence, everything needed for the works
        self.init_maze()

        # Get the things needed for the actual model that will be filtered
        update_matrices = self.get_update_matrices()
        transition_model = self.get_transition_model()
        prior_matrix = self.get_prior_matrix()

        # Now put it all into the model
        super().__init__(update_matrices, transition_model, prior_matrix)

    def get_update_matrices(self):
        # What the update matrices are, are just a dictionary of all the matrices that update could be depending on the
        # color that we read. We build this dictionary based on the color matrix.
        update_matrices = {'r': None, 'g': None, 'y': None, 'b': None}

        # First loop through all colors we could have
        for color in self.colors:
            # Start with an empty zeroes column vector
            color_vector = np.zeros((self.maze.height*self.maze.width, 1))
            # Now loop through x and y
            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    # find out if the color is the color we want. If so, 0.88, if not, 0.04
                    if self.color_matrix[self.maze.height - 1 - y][x] == color:
                        color_vector[x*self.maze.height + y] = 0.88
                    else:
                        color_vector[x*self.maze.height + y] = 0.04
            # Add this to dictionary
            update_matrices[self.color_dict[color]] = color_vector * np.identity(len(color_vector))
        # Return dictionary
        return update_matrices

    def get_transition_model(self):
        # Rows are the previous position, columns are the new position. What is the probability I go from position A to
        # position B? That is what will be in this matrix. Now we have to ask ourselves, how many positions could you be
        # at in a 4x4 maze. Yes, the answer is 16.
        transition_model = np.zeros((self.maze.height*self.maze.width, self.maze.height*self.maze.width))

        # Now we need to loop through all positions in the maze, fill out the matrix
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # We know that we can go in any cardinal direction with a probability of 0.25. We also know that if we
                # have the ability to move, we will move. That is, if we can move in any cardinal direction at a given
                # space, then the probability of staying at that space is 0. Now we make sure we are a floor and loop
                # through all the positions we can get to from here. We want matrix to have rows be (0,0), (0, 1), ...
                if self.maze.is_floor(x, y):
                    # Now loop through neighbors, keep track of how many walls to determine the prob of staying
                    # If we want (3,3), the last pos to map to 15th or last row, we use following equation
                    row = x * self.maze.height + y
                    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

                    for neighbor in neighbors:
                        # Find new x and new y
                        new_x = x + neighbor[0]
                        new_y = y + neighbor[1]
                        # Check if floor, add stay prob if so
                        if not self.maze.is_floor(new_x, new_y):
                            transition_model[row][row] += 0.25
                        # Otherwise, just find corresponding matrix row and column, set .25
                        else:
                            if neighbor[0] == 0:
                                # This means, we moved in the y direction
                                col = self.maze.height*x + new_y
                                transition_model[row][col] = 0.25
                            else:
                                # This means, that we moved in the x direction
                                col = self.maze.height*new_x + y
                                transition_model[row][col] = 0.25
        # Now we just return the model
        return transition_model

    def get_prior_matrix(self):
        # For the prior matrix, we need to find out the number of possible locations fro the robot and then we just
        # assign a uniform probability based on the number floors. Best way to do this is by marking if floor or not,
        # then multiplying by number of walls
        prior_matrix = np.zeros((self.maze.height*self.maze.width, 1))
        num_floors = 0
        # Loop through all positions
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                row = x * self.maze.height + y
                # If a floor, increment floor count and set matrix to 1
                if self.maze.is_floor(x, y):
                    prior_matrix[row] = 1
                    num_floors += 1
        # Now simply just multiply by 1/num_floors. All pos with 1 will get number
        prior_matrix *= 1/num_floors
        # Return the prior
        return prior_matrix




        pass

    # Initializes the maze, returns a color matrix, sequence of colors, the actual moves, all that jazz
    def init_maze(self):
        # Creation of a color matrix. We have to realize that the maze works on the coordinate plane whereas a matrix
        # works on x being the row and y being the column. So it is slightly different, but we can use corresponding
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # Loop through, assign a random color (number) to every single cell
                if self.maze.is_floor(x, y):
                    self.color_matrix[self.maze.height - y - 1][x] = random.randint(1, 4)

        # Now we want to generate a list of moves that the robot would actually take
        for i in range(self.move_limit):
            # For the given move limit, come up with a sequence of moves
            move = self.move_dict[random.randint(1, 4)]
            self.moves.append(move)
            # Now perform that move for the robot and then obtain and add the color to the color sequence
            robot_move = self.move_robot_dict[move]

            if self.maze.is_floor(self.location[0] + robot_move[0], self.location[1] + robot_move[1]):
                self.location = (self.location[0] + robot_move[0], self.location[1] + robot_move[1])
            self.locations.append(self.location)
            # Obtain actual color at the spot. First we grab all colors, remove the one we know, use numpy
            actual_color = self.color_matrix[self.maze.height - 1 - self.location[1]][self.location[0]]
            color_array = self.colors.copy()
            color_array.remove(actual_color)
            color_array.append(actual_color)
            probabilities = (4, 4, 4, 88)
            self.color_sequence.append(
                self.color_dict[random.choices(color_array, cum_weights=probabilities, k=1)[0]])


if __name__ == "__main__":
    # Some Testing
    model = Robotic_Model("no_wall_maze.maz", 10, (0, 0))
    # Testing the transition model
    # print(model.transition_model)

    # Testing update matrices
    # print(model.update_matrices)

    # Testing prior matrix
    # print(model.prior_matrix)

    # Testing color matrix
    # print(model.color_matrix)

    # Testing moves and color sequence
    # print(model.color_matrix)
    # print(model.moves)
    # print(model.color_sequence)


