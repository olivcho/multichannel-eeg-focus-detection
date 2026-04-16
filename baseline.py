"""
Baseline calibration: records a short resting-state EEG session and saves
the mean and standard deviation of the focus score. This lets run.py
normalize scores relative to YOUR resting brain, not an arbitrary threshold.
"""

import json
import numpy as np
from network_lsl import get_lsl_channel
from focus import compute_focus_score

BASELINE_FILE = "baseline.json"
BASELINE_DURATION_SECONDS = 10
WINDOW_SIZE = 400
STEP_SIZE   = 100


def record_baseline() -> dict:
    """
    Record resting EEG, compute focus scores across all windows, return focus scores statistics for each channel.
    """
    print("Relax and look straight ahead.")
    print("Starting baseline recording.")

    data = get_lsl_channel('EEG', BASELINE_DURATION_SECONDS)
    focus_scores = {}

    num_channels = len(data[0])
    for channel in range(num_channels):
        channel_samples = [sample[channel] for sample in data]

        channel_scores = []
        for i in range(0, len(channel_samples) - WINDOW_SIZE, STEP_SIZE):
            window = channel_samples[i:i+WINDOW_SIZE]
            focus_score = compute_focus_score(window)
            channel_scores.append(focus_score)

        focus_scores[channel] = {
            "mean": np.mean(channel_scores),
            "std": np.std(channel_scores)
        }

    return focus_scores

def save_baseline(focus_scores: dict):
    """
    Save baseline focus scores to BASELINE_FILE as JSON.
    """
    try:
        with open(BASELINE_FILE, 'w') as f:
            json.dump(focus_scores, f)
        print(f"Baseline saved to {BASELINE_FILE}")
    except Exception as e:
        print(f"Error saving baseline: {e}")


def load_baseline() -> dict:
    """
    Load baseline stats from BASELINE_FILE.
    """
    try:
        with open(BASELINE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading baseline: {e}")
        return None


if __name__ == "__main__":
    focus_scores = record_baseline()
    save_baseline(focus_scores)
