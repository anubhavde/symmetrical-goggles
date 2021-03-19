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
        self.inference_output_path = get_results_directory()
        self.inference_setup_timeout = int(os.getenv("INFERENCE_SETUP_TIMEOUT_SECONDS", "600"))
        self.inference_flight_timeout = int(os.getenv("INFERENCE_PER_FLIGHT_TIMEOUT_SECONDS", "1000"))
        self.results = []
        self.current_flight_results = []
        self.current_img_name = None
        self.track_id_seq = 0


    def register_object_and_location(self, class_name, bbox, confidence, track_id=None, img_name=None):
        """
        Register all your tracking results to this function.
           `track_id` (optional): unique id for your detected airborne object
           `img_name` (optional): this prediction belong to which image? default being the current image passed
        """
        assert 0 < confidence < 1
        assert class_name is not None
        if img_name is None:
            img_name = self.current_img_name
        if track_id is None:
            track_id = self.track_id_seq
            self.track_id_seq += 1
        self.results.append([img_name, class_name, bbox[0], bbox[1], bbox[2], bbox[3], confidence, track_id])
        self.current_flight_results.append([img_name, class_name, bbox[0], bbox[1], bbox[2], bbox[3], confidence, track_id])


    def evaluation(self):
        """
        Admin function: Runs the whole evaluation
        """
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
            save_results(flight_id)

        save_results()
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

    def inference_setup(self):
        """
        You can do any preprocessing required for your codebase here like loading up models into memory, etc.
        """
        raise NotImplementedError


    def inference(self, flight_id, img_name):
        """
        This function will be called for all the flights one by one during the evaluation.
        NOTE: In case you want to load your model, please do so in `inference_setup` function.
        """
        raise NotImplementedError


    def get_results_directory(self, flight_id=None):
        """
        Utility function: results directory path
        """
        root_directory = os.getenv("INFERENCE_OUTPUT_PATH", os.getcwd() + "/data/results/")
        run_id = os.getenv("DATASET_ENV", "run1")
        results_directory = os.path.join(root_directory, run_id)
        if flight_id is not None:
            results_directory = os.path.join(root_directory, flight_id)
        if not os.path.exists(os.path.dirname(self.inference_output_path)):
            os.makedirs(os.path.dirname(self.inference_output_path))
        return results_directory

    def save_results(self, flight_id=None):
        """
        Utility function: save results in nested direcotry based on flight_id
        This helps in giving continuous feedback in terms of approx scores and so on.
        """
        if flight_id is None:
            submission_df = pd.DataFrame(self.results)
        else:
            submission_df = pd.DataFrame(self.current_flight_results)

        submission_df.columns = ["img_name", "n", "x", "y", "w", "h", "s", "track_id"]
        submission_df.to_csv(
            get_results_directory(flight_id),
            index=False,
        )
        self.current_flight_results = []
