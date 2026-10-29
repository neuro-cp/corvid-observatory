"""Create a waveform and spectrogram for a recording; no call detection."""
import argparse
from pathlib import Path
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("audio", type=Path)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
signal, rate = sf.read(args.audio, always_2d=True)
signal = signal.mean(axis=1)
if not len(signal):
    raise SystemExit("Empty audio file")
freq, times, power = spectrogram(signal, fs=rate, window="hann", nperseg=1024, noverlap=768, mode="psd")
db = 10 * np.log10(np.maximum(power, 1e-12))
fig, (wave, spec) = plt.subplots(2, 1, figsize=(12, 7), constrained_layout=True)
wave.plot(np.arange(len(signal)) / rate, signal, linewidth=.4)
wave.set(xlabel="Time (s)", ylabel="Amplitude", title=f"{args.audio.name}: waveform")
plot = spec.pcolormesh(times, freq / 1000, db, shading="auto", cmap="magma", vmin=-100, vmax=-20)
spec.set(xlabel="Time (s)", ylabel="Frequency (kHz)", ylim=(0, min(10, rate / 2000)), title="Spectrogram (dB power spectral density)")
fig.colorbar(plot, ax=spec, label="dB/Hz (relative to full scale)")
args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, dpi=160)
print(f"{len(signal)/rate:.2f} seconds; {rate} Hz; {signal.size} samples; wrote {args.output}")
