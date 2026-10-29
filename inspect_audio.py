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
parser.add_argument("--start", type=float, default=0.0, help="Start time in seconds")
parser.add_argument("--end", type=float, help="End time in seconds; defaults to end of recording")
args = parser.parse_args()
info = sf.info(args.audio)
duration = info.frames / info.samplerate
end = duration if args.end is None else args.end
if not np.isfinite(args.start) or not np.isfinite(end) or not 0 <= args.start < end <= duration:
    parser.error(f"Require 0 <= start < end <= {duration:.3f} seconds")
start_frame = int(args.start * info.samplerate)
end_frame = int(end * info.samplerate)
signal, rate = sf.read(args.audio, start=start_frame, stop=end_frame, always_2d=True)
if args.end is not None and len(signal) != end_frame - start_frame:
    parser.error("The requested end exceeds decoded audio; file duration metadata may be inaccurate")
signal = signal.mean(axis=1)
if len(signal) < 1024:
    raise SystemExit("Selected audio must contain at least 1024 samples")
freq, times, power = spectrogram(signal, fs=rate, window="hann", nperseg=1024, noverlap=768, mode="psd")
db = 10 * np.log10(np.maximum(power, 1e-12))
fig, (wave, spec) = plt.subplots(2, 1, figsize=(12, 7), constrained_layout=True)
wave.plot(args.start + np.arange(len(signal)) / rate, signal, linewidth=.4)
wave.set(xlabel="Time (s)", ylabel="Amplitude", title=f"{args.audio.name}: waveform")
plot = spec.pcolormesh(args.start + times, freq / 1000, db, shading="auto", cmap="magma", vmin=-100, vmax=-20)
spec.set(xlabel="Time (s)", ylabel="Frequency (kHz)", ylim=(0, min(10, rate / 2000)), title="Spectrogram (dB power spectral density)")
fig.colorbar(plot, ax=spec, label="dB/Hz (relative to full scale)")
args.output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(args.output, dpi=160)
print(f"{len(signal)/rate:.2f} seconds starting at {args.start:.2f}; {rate} Hz; {signal.size} samples; wrote {args.output}")
