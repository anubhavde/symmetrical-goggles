######################################################################################
### This is read-only file so participants can run their codes locally.            ###
### It will be over-writter during the evaluation, don't make any changes to this. ###
######################################################################################

import traceback
import pandas as pd
import os
import signal
from contextlib import contextmanager
from os import listdir
from os.path import isfile, join

from evaluator import aicrowd_helpers

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Prediction timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class AirbornePredictor:
    def __init__(self):
        self.test_data_path = os.getenv("TEST_DATASET_PATH", os.getcwd() + "/data/val/")
        self.inference_output_path = os.getenv("INFERENCE_OUTPUT_PATH", os.getcwd() + "/data/results/result.csv")
        self.inference_setup_timeout = int(os.getenv("INFERENCE_SETUP_TIMEOUT_SECONDS", "600"))
        self.inference_flight_timeout = int(os.getenv("INFERENCE_PER_FLIGHT_TIMEOUT_SECONDS", "1000"))
        self.results = []
        self.current_img_name = None
        self.track_id_seq = 0


    """Register all your tracking results to this function.
       `track_id` (optional): unique id for your detected airborne object
       `img_name` (optional): this prediction belong to which image? default being the current image passed
    """
    def register_object_and_location(self, class_name, bbox, confidence, track_id=None, img_name=None):
        assert 0 < confidence < 1
        assert class_name is not None
        if img_name is None:
            img_name = self.current_img_name
        if track_id is None:
            track_id = self.track_id_seq
            self.track_id_seq += 1
        self.results.append([img_name, class_name, bbox[0], bbox[1], bbox[2], bbox[3], confidence, track_id])


    """Admin function: Runs the whole evaluation
    """
    def evaluation(self):
        aicrowd_helpers.execution_start()
        try:
            with time_limit(self.inference_setup_timeout):
                self.inference_setup()
        except NotImplementedError:
            print("inference_setup doesn't exist for this run, skipping...")

        aicrowd_helpers.execution_running()

        flights = [f for f in listdir(self.test_data_path) if not isfile(join(self.test_data_path, f))]

        for flight_id in flights:
            img_names = [f for f in listdir(self.test_data_path + flight_id) if isfile(join(self.test_data_path + flight_id, f))]
            with time_limit(self.inference_flight_timeout):
                for img_name in img_names:
                    self.track_id_seq = 0
                    self.current_img_name = img_name
                    self.inference(flight_id, img_name)

        submission_df = pd.DataFrame(self.results)
        submission_df.columns = ["img_name", "n", "x", "y", "w", "h", "s", "track_id"]
        submission_df.to_csv(
            self.inference_output_path,
            index=False,
        )

        aicrowd_helpers.execution_success()

    def run(self):
        try:
            self.evaluation()
        except Exception as e:
            error = traceback.format_exc()
            print(error)
            aicrowd_helpers.execution_error(error)
            if not aicrowd_helpers.is_grading():
                raise e

    """
    You can do any preprocessing required for your codebase here like loading up models into memory, etc.
    """
    def inference_setup(self):
        raise NotImplementedError

    """
    This function will be called for all the flights one by one during the evaluation.
    NOTE: In case you want to load your model, please do so in `inference_setup` function.
    """
    def inference(self, flight_id, img_name):
        raise NotImplementedError

