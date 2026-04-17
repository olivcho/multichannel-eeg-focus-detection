# neuro2 — EEG focus pipeline

[OpenBCI Networking Data Formats](https://docs.google.com/document/u/1/d/e/2PACX-1vR_4DXPTh1nuiOwWKwIZN3NkGP3kRwpP4Hu6fQmy3jRAOaydOuEI1jket6V4V6PG4yIG15H1N7oFfdV/pub#h.fs64qwm9zn45)

Small Python project that reads OpenBCI / Ganglion–style EEG over **Lab Streaming Layer (LSL)**, estimates a simple **focus** score from band powers, calibrates it per person, then labels **FOCUSED / NEUTRAL / DISTRACTED** in real time.

## How it fits together

1. **`calibration.py`** — Shared constants: sampling rate `fs`, EEG frequency band ranges (delta through gamma), and hardware scaling notes for Ganglion exports.
2. **`signal_processing.py`** — Turns a 1D chunk of samples into **band power** (bandpass filter + mean squared amplitude). Used by the focus metric and by `test.py` for plots.
3. **`focus.py`** — **Focus score** ≈ beta power divided by (theta + alpha), then **smoothed** with an exponential moving average per channel.
4. **`network_lsl.py`** — LSL helpers: resolve a stream by type, pull chunks for a fixed duration (`get_lsl_channel`), optional plotting for quick checks.
5. **`baseline.py`** — Records ~10s of resting EEG via LSL, slides a window over each channel, computes raw focus scores, saves **mean and std** per channel to **`baseline.json`** so later scores can be z-scored to *you*.
6. **`run.py`** — Main loop: load `baseline.json`, subscribe to the `EEG` LSL stream, maintain a sliding buffer, compute per-channel focus → z-score vs baseline → print **FOCUSED | NEUTRAL | …** labels.

**Typical order:** run **`baseline.py`** once (relaxed, eyes open) → run **`run.py`** while streaming EEG.

## Other files

| File | Role |
|------|------|
| **`test.py`** | Offline check: load a BrainFlow CSV tab export, scale voltages, plot time domain, filtered signal, and band-power traces (uses `signal_processing` + `calibration`). |
| **`udp_send_marker.py`** | Standalone UDP sender that emits random double markers for ~10s (for syncing or testing another app that listens on UDP). |
| **`baseline.json`** | Generated baseline stats (not hand-edited). Gitignored in this repo. |
| **`instructions.md`** | Short Ganglion electrode wiring table (also listed in `.gitignore` for this workspace). |

## Dependencies

`numpy`, `scipy`, `pylsl`, and for scripts that plot: `matplotlib` (and `pandas` for `test.py`).
