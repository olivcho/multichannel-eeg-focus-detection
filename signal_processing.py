"""
Signal processing utilities for EEG data.
Transforms raw EEG samples into frequency-band features.
"""

import numpy as np
from scipy.signal import butter, sosfiltfilt, welch
from calibration import fs

def bandpass_filter(samples: list, low_hz: float, high_hz: float, fs: int = fs) -> np.ndarray:
    """
    Apply a bandpass filter to raw EEG samples.

    Butterworth bandpass filter:
      - Order 4
      - Cutoff frequencies at Nyquist rate
      - Implemented with second-order sections for numerical stability

    Returns the filtered signal as a NumPy array.
    """
    sos = butter(4, [low_hz / (fs / 2), high_hz / (fs / 2)], btype="band", output="sos")
    samples_arr = np.asarray(samples, dtype=float)
    filtered = sosfiltfilt(sos, samples_arr, axis=0)
    return filtered


def band_power(samples: list, low_hz: float, high_hz: float, fs: int = fs, window: int = 100) -> float:
    """
    Compute the average power of a signal within a frequency band.

    Steps:
    1. Bandpass filter `samples` to isolate the band (use bandpass_filter above)
    2. Compute power as the mean of the squared filtered signal
       - power = mean(filtered ** 2)
    3. Return the scalar power value

    Note: This is simpler than Welch's method but good enough for a first pass.
    You could swap in scipy.signal.welch later for better noise handling.
    """
    filtered = bandpass_filter(samples, low_hz, high_hz, fs=fs)
    return float(np.mean(filtered ** 2))