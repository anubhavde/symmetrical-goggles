#!/usr/bin/env python
# This file is the entrypoint for your submission.
# You can modify this file to include your code or directly call your functions/modules from here.
import random
from PIL import Image
from evaluator.airborne_detection import AirbornePredictor


class RandomPredictor(AirbornePredictor):
    """
    PARTICIPANT_TODO: You can name your implementation as you like. `RandomPredictor` is just an example.
    Below paths will be preloaded for you, you can read them as you like.
    """
    training_data_path = None
    test_data_path = None
    vocabulary_path = None

    """
    PARTICIPANT_TODO:
    You can do any preprocessing required for your codebase here like loading up models into memory, etc.
    """
    def predict_setup(self):
        random.seed(42)
        pass

    """
    PARTICIPANT_TODO:
    During the evaluation all combinations for flight_id and flight_folder_path will be provided one by one.

    NOTE: In case you want to load your model, please do so in `predict_setup` function.
    """
    def inference(self, flight_id):
        for frame_image in self.get_all_frame_images(flight_id):
            frame_image_path = self.get_frame_image_location(flight_id, frame_image)
            img = Image.open(frame_image_path)
            # Do something...

            for i in range(random.randint(-4, 7)):
                bbox = [random.uniform(1300, 1500), random.uniform(1000, 1200), random.uniform(50, 100),
                        random.uniform(50, 100)]
                confidence = random.uniform(0.5, 1)
                class_name = random.choice(["Airplane1", "Helicopter1"])
                self.register_object_and_location(class_name, random.randint(0, 3), bbox, confidence, frame_image)


if __name__ == "__main__":
    submission = RandomPredictor()
    submission.run()
    print("Successfully generated predictions!")
