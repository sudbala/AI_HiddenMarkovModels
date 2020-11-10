# CS 76: Artificial Intelligence - PA6: Hidden Markov Models
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming

# Import statements
from Robotic_Model import Robotic_Model
from filter import filter
from RobotUI import RobotUI


class RobotTest:

    # Just a test class to test everything, modelling and filtering
    model = Robotic_Model("no_wall_maze.maz", 20, (0, 0))

    # Now filter
    robotic_filter = filter(model)

    # filtered distributions
    filtered_distributions = robotic_filter.filtering(model.color_sequence)
    # print(filtered_distributions)

    # Looks like we are working. Now to just UI
    robot_ui = RobotUI(model, filtered_distributions)
    robot_ui.display()

