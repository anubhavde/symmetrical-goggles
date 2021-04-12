#!/usr/bin/env python3
import os
import json
from loguru import logger
from core.flight import Flight
from core.file_handler import FileHandler


class Dataset:
    metadata = None
    flights = {}

    def __init__(self, local_path, s3_path, download_if_required=True):
        self.file_handler = None
        self.add(local_path, s3_path, download_if_required)

    def load_gt(self):
        logger.info("Loading ground truth...")
        gt_content = self.file_handler.get_file_content(self.gt_loc)
        gt = json.loads(gt_content)
        self.metadata = gt["metadata"]
        for flight_id in gt["samples"].keys():
            self.flights[flight_id] = Flight(flight_id, gt["samples"][flight_id], self.file_handler)

    def add(self, local_path, s3_path, download_if_required=True):
        self.file_handler = FileHandler(local_path, s3_path, download_if_required)
        self.load_gt()

    def get_flight_ids(self):
        return list(self.flights.keys())

    @property
    def gt_loc(self):
        return 'ImageSets/groundtruth.json'

    def get_flight_by_id(self, flight_id):
        return self.flights[flight_id]

    def get_flight(self, flight_id):
        return self.get_flight_by_id(flight_id)

    def __str__(self):
        return "Dataset(num_flights=%s)" % (len(self.flights))


if __name__ == "__main__":
    local_path = '/Users/skbly7/Terminal/aicrowd/repos/airborne-detection-starter-kit/data'
    s3_path = 's3://airborne-obj-detection-challenge-training/part1/'
    dataset = Dataset(local_path, s3_path)
    print(dataset.flights)
