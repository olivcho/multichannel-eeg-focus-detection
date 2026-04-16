from signal_processing import bandpass_filter, band_power, fs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from calibration import SCALE_FACTOR, FREQUENCY_BANDS

FILE_PATH = "data/BrainFlow-RAW_2026-04-16_00-24-04_0.csv"

# BrainFlow raw export is tab-delimited and has no header row.
def load_data(file_path: str, start_index: int = 90000, end_index: int = 95000):
    samples = pd.read_csv(file_path, sep="\t", header=None).iloc[start_index:end_index, 1:5].to_numpy(dtype=float)
    samples = samples * SCALE_FACTOR
    t = np.arange(len(samples)) / fs
    return samples, t

def generate_plot(samples: np.ndarray, t: np.ndarray, plot_title: str):
    plt.figure()
    for i, channel in enumerate(samples.T):
        plt.plot(t, channel, label=f"Channel {i}")
    plt.title(plot_title)
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (µV)")
    plt.legend()

def generate_frequency(samples, t, plot_title: str):
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
    fig.suptitle(plot_title)

    for i, channel in enumerate(samples.T):
        ax = axes.flat[i]
        for band_name, band_range in FREQUENCY_BANDS.items():
            power = band_power(channel, band_range[0], band_range[1])
            ax.plot(t, power, label=f"{band_name}")
        ax.set_title(f"Channel {i}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (µV^2)")
        ax.set_yscale("log")
        ax.legend(fontsize="small")
    fig.tight_layout()

# -----------------------------------------------------

if __name__ == "__main__":
    samples, t = load_data(FILE_PATH)
    generate_plot(samples, t, "All Channels (time domain)")
    generate_plot(bandpass_filter(samples, 1, 10), t, "Bandpass Filtered (1-10 Hz)")
    generate_frequency(samples, t, "All Channels (frequency domain)")
    plt.show()