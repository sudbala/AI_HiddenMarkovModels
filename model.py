# CS 76: Artificial Intelligence - PA6: Hidden Markov Models
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming

# Import statements
import numpy as np


# Class that handles the general model building. Other models will be specialized.
class model:
    # Generalized model construction class, other models will extend this model class
    def __init__(self, update_matrices, transition_model, prior_matrix):
        self.update_matrices = update_matrices
        self.transition_model = transition_model
        self.prior_matrix = prior_matrix


if __name__ == "__main__":
    # We are going to do the umbrella model from class
    # First the prior matrix, what we know
    prior_matrix = np.array([[0.5], [0.5]])
    # Then the transition model
    transition_model = np.array([[0.7, 0.3], [0.3, 0.7]])

    # Now we create the update_matrices
    update_matrices = {'Y': np.array([[0.9, 0], [0, 0.2]])}

    # Observations. Y is for yes we saw an umbrella, and N is for no we didn't
    observations = ['Y', 'Y']

    # Create the model and the filter
    umbrella_test_model = model(update_matrices, transition_model, prior_matrix)