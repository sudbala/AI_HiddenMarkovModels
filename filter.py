# Import statements
import numpy as np
import model as model

# Filtering Algorithm


class filter:

    def __init__(self, model):
        self.model = model

    # Normalize to get the alpha value
    def normalize(self, new_state_estimate):
        current_state_estimate = new_state_estimate
        # Normalize a matrix of probabilities. We take marginal distribution, they are all conditional probabilities.
        # We multiply every term by to get the probability which is our state estimate.
        return current_state_estimate

    def filtering(self, color_sequence, prior_matrix):
        # Go through each color in a sequence and a prior matrix
        current_state_estimate = prior_matrix
        for color in color_sequence:
            new_state_estimate = self.model.update_matrix().dot(self.model.transition_model()
                                                                .dot(current_state_estimate))
            current_state_estimate = self.normalize(new_state_estimate)




