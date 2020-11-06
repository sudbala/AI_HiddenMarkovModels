from Maze import Maze
import numpy as np
import random

class model:

    def __init__(self, maze_file_name, move_limit):
        self.maze_file_name = maze_file_name
        self.maze = Maze(maze_file_name)

        # Colors
        self.color_matrix = np.zeros((self.maze.height, self.maze.width))
        self.color_dict = {1: 'r', 2: 'g', 3: 'y', 4: 'b'}

        # Moves
        self.move_dict = {1: 'N', 2: 'E', 3: 'S', 4: 'W'}
        self.move_limit = move_limit



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
        for x in range(self.maze.height):
            for y in range(self.maze.width):
                # Loop through, assign a random color (number) to every single cell
                print(self.maze.is_floor(1, 0))
                if self.maze.is_floor(y, x):
                    self.color_matrix[x][y] = random.randint(1, 4)

        # Now we want to generate a list of moves that the robot would actually take
        for i in range(self.move_limit):




model = model("maze1.maz")
print(model.color_matrix)

