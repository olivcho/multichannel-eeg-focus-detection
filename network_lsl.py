from pylsl import StreamInlet, resolve_byprop
import time
import matplotlib.pyplot as plt
import numpy as np

# CONSTANTS
fs = 200 # Sampling rate in Hz

# HELPER FUNCTIONS

# helper print data function
def round_print(data: list):
    rounded_data = [[round(sample, 2) for sample in row] for row in data]
    print(rounded_data)

def convert_samples_to_time(data: list, sampling_frequency = fs):
    return np.linspace(0, len(data) / sampling_frequency, len(data))

def generate_graph(data: list):
    plt.plot(convert_samples_to_time(data), data)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (µV)')
    plt.show()

def get_lsl_channel(channel_name: str, duration_seconds: int) -> list:
    """
    Get data from the LSL stream.

    Channel count agnostic. Data contains # of channels.
    """
    start = time.time()
    data = []

    stream = resolve_byprop('type', channel_name)[0]
    inlet = StreamInlet(stream)

    while time.time() < start + duration_seconds:
        chunk, timestamps = inlet.pull_chunk(timeout=0.05)
        if timestamps:
            for sample in chunk:
                data.append(sample)
                print(sample)

    return data

if __name__ == "__main__":
    data = get_lsl_channel('EEG', 5)
    generate_graph(data)

    # data = get_lsl_channel('FFT', 5)
    # generate_graph(data)

    # data = get_lsl_channel('FOCUS', 5)
    # generate_graph(data)