"""
Real-time focus detection loop.
Reads EEG from LSL in sliding windows, scores focus, and prints feedback.

Run baseline.py first to generate baseline.json before running this.
"""

from focus import get_focus
from baseline import load_baseline
from pylsl import StreamInlet, resolve_byprop

WINDOW_SIZE = 400
STEP_SIZE   = 100
FOCUS_THRESHOLD_Z = 5


def get_z_score(raw: float, mean: float, std: float) -> float:
    return (raw - mean) / std


def get_label(z: float) -> str:
    if z >= FOCUS_THRESHOLD_Z:
        return "FOCUSED"
    elif z <= -FOCUS_THRESHOLD_Z:
        return "DISTRACTED"
    else:
        return "NEUTRAL"

def run():
    baseline = load_baseline()
    stream = resolve_byprop('type', 'EEG')[0]
    inlet = StreamInlet(stream)

    buffer = []
    num_channels = len(baseline.keys())

    while True:
        chunk, timestamps = inlet.pull_chunk(timeout=0.05)
        if timestamps:
            buffer.extend(chunk)
            if len(buffer) > WINDOW_SIZE:
                buffer = buffer[-WINDOW_SIZE:]

                labels = []
                for channel in range(num_channels):
                    channel_samples = [sample[channel] for sample in buffer]
                    raw_score = get_focus(channel_samples, channel)
                    z_score = get_z_score(raw_score, baseline[str(channel)]['mean'], baseline[str(channel)]['std'])
                    label = get_label(z_score)
                    labels.append(label)
                print(" | ".join(labels))

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
