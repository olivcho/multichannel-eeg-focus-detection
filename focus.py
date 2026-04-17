"""
Focus metric computation from raw EEG samples.
Depends on signal_processing.py for band power extraction.
"""

from signal_processing import band_power
from calibration import FREQUENCY_BANDS

EMA_ALPHA = 0.8

_smoothed_scores = {}


def compute_focus_score(samples: list) -> float:
    """
    Compute a raw (unsmoothed) focus score from a window of EEG samples.
    """
    beta_power = band_power(samples, FREQUENCY_BANDS["BETA"][0], FREQUENCY_BANDS["BETA"][1])
    theta_power = band_power(samples, FREQUENCY_BANDS["THETA"][0], FREQUENCY_BANDS["THETA"][1])
    alpha_power = band_power(samples, FREQUENCY_BANDS["ALPHA"][0], FREQUENCY_BANDS["ALPHA"][1])

    if (theta_power + alpha_power) == 0:
        return 0.0

    return beta_power / (theta_power + alpha_power)


def smooth_focus_score(raw_score: float, channel: int = 0) -> float:
    """
    Apply a per-channel exponential moving average to the raw focus score.
    """
    if channel not in _smoothed_scores:
        _smoothed_scores[channel] = raw_score
    else:
        _smoothed_scores[channel] = EMA_ALPHA * _smoothed_scores[channel] + (1 - EMA_ALPHA) * raw_score

    return _smoothed_scores[channel]


def get_focus(samples: list, channel: int = 0) -> float:
    """
    Full pipeline: raw EEG samples → smoothed focus score.
    """
    raw_score = compute_focus_score(samples)
    return smooth_focus_score(raw_score, channel)
