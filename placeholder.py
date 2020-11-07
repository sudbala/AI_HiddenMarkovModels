from Maze import Maze
import numpy as np
import random

class placeholder:

    # Takes in a maze file name, a move limit and a tuple initial position that has the x coord and y coordinate
    def __init__(self, maze_file_name, move_limit, initial_position):
        self.maze_file_name = maze_file_name
        self.maze = Maze(maze_file_name)
        self.location = initial_position

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

        self.init_maze()
        pass

    # The prior matrix for the model
    def prior(self):
        # TODO: rewrite
        # prior should be a 16x1 matrix, n^2 in general
        # where each row is a different position in the maze and the number in the column is the probability of being in
        # that position.
        pass

    # The transition model for the model
    def transition_model(self):
        # A 16 x 16 matrix, where rows are previous position of the robot
        # The columns are the current positions of the robots.. That is the value at (1,1) would be the probability that
        # robot was at position 1 and is now at position 1, where position 1 is a tuple.
        # Told that the robot will move that the robot will move with a .25 percent prob in any direction, we need to
        # that there are walls, so if wall, probability that it doesnt move is nonzero. Probability it doesnt move
        # becomes sum of all walls around that position.
        pass

    # Update of the current state
    def update_matrix(self):
        # The update matrix is based on the sensor model. Given a color, what is the probability we got that color from
        # a specific position. There are 16, or n^2 positions we could be at. Prob of reading color c at those given is
        # in an identity matrix that corresponds to the rows that we have in the transition matrix. 16x1 matrix (rows
        # correspond to locations in the matrix. We multiply by identity matrix where the diagonal. All other entries
        # are 0. We need info from maze to tell us the update
        pass

    # Initializes the maze, returns a color matrix, sequence of colors, the actual moves, all that jazz
    def init_maze(self):
        # Creation of a color matrix. We have to realize that the maze works on the coordinate plane whereas a matrix
        # works on x being the row and y being the column. So it is slightly different, but we can use corresponding
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # Loop through, assign a random color (number) to every single cell
                if self.maze.is_floor(x, y):
                    self.color_matrix[self.maze.height-y-1][x] = random.randint(1, 4)

        # Now we want to generate a list of moves that the robot would actually take
        for i in range(self.move_limit):
            # For the given move limit, come up with a sequence of moves
            move = self.move_dict[random.randint(1, 4)]
            self.moves.append(move)
            # Now perform that move for the robot and then obtain and add the color to the color sequence
            robot_move = self.move_robot_dict[move]
            if self.maze.is_floor((self.location + robot_move)[0], (self.location + robot_move)[1]):
                self.location += robot_move
            # Obtain actual color at the spot. First we grab all colors, remove the one we know, use numpy
            actual_color = self.color_matrix[self.maze.height - 1 - self.location[1]][self.location[0]]
            color_array = self.colors.copy()
            color_array.remove(actual_color)
            color_array.append(actual_color)
            probabilities = (.04, .04, .04, .88)
            self.color_sequence.append(self.color_dict[random.choices(color_array, cum_weights=probabilities, k=1)[0]])







model = model("maze1.maz", 5, (1, 0))
print(model.color_matrix)
print(model.moves)
print(model.color_sequence)

