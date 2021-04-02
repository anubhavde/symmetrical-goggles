#!/usr/bin/env python
# This file is the entrypoint for your submission.
# You can modify this file to include your code or directly call your functions/modules from here.
import random

from evaluator import aicrowd_helpers
from evaluator.airborne_detection import AirbornePredictor

# TODO: You can name your implementation as you like.
class RandomPredictor(AirbornePredictor):

    """
    Below paths will be preloaded for you, you can read them as you like.
    """
    training_data_path = None
    test_data_path = None
    vocabulary_path = None

    """
    TODO:
    You can do any preprocessing required for your codebase here like loading up models into memory, etc.
    """
    def predict_setup(self):
        random.seed(42)
        pass

    """
    TODO:
    This function will be called for all the flights & img combination one by one during the evaluation.
    NOTE: In case you want to load your model, please do so in `predict_setup` function.
    """
    def inference(self, flight_id, img_name):
        """
          Your code needs to go here.
          You can add predictions using the interface like this.
        """

        """
          You can add predictions using the interface like this:
          register_object_and_location(class, bbox, confidence, track_id=None, img_name=None)

          class      => Name of the class
          bbox       => Boundry of bbox
          confidence => Range (0-1)
          track_id   => You can pass track_id manually for tracking same objects in multiple images properly,
                        Otherwise the interface automatically add track_id.
        """

        for i in range(random.randint(-4, 7)):
            bbox = [random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 100)]
            confidence = random.uniform(0.5, 1)
            class_name = random.choice(["intruder", "Airplane1", "Helicopter1"])
            self.register_object_and_location(class_name, bbox, confidence)


if __name__ == "__main__":
    submission = RandomPredictor()
    submission.run()
    print("Successfully generated predictions!")
