# CS 76: Artificial Intelligence - PA6: Hidden Markov Models
# Fall 2020
# Authors: Sudharsan Balasubramani & Alberto
# Collaboration: Discussed ideas with James Fleming

# Import statements
import numpy as np
from model import model


# Class that handles the filtering algorithm in Hidden Markov Models
class filter:

    # Constructor, that just asks for a given model to filter.
    def __init__(self, HMM):
        self.model = HMM

    # Normalize to get the alpha value
    def normalize(self, new_state_estimate):
        # Normalize a matrix of probabilities. We take marginal distribution, they are all conditional probabilities.
        # We multiply every term by to get the probability which is our state estimate.
        current_state_estimate = (1/(new_state_estimate.sum())) * new_state_estimate
        return current_state_estimate

    def filtering(self, observations):
        # Go through each color in a sequence and a prior matrix
        model_distributions = []
        current_state_estimate = self.model.prior_matrix
        # Now loop through all observations for the evidence
        for obs in observations:
            # The observation is what determines the update matrix. We store it in a dictionary
            update_matrix = self.model.update_matrices[obs]
            # Now we calc a new state estimate
            new_state_estimate = np.dot(update_matrix, np.dot(self.model.transition_model, current_state_estimate))
            current_state_estimate = self.normalize(new_state_estimate)
            # Now add the current state estimate into the list of all the probability distributions
            model_distributions.append(current_state_estimate)

        return model_distributions


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
    umbrella_filtering = filter(umbrella_test_model)
    probability_distributions = umbrella_filtering.filtering(observations)

    # Checks out
    print(probability_distributions)



