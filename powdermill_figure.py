"""Plot a recording window with the original American crow annotation boxes."""
import csv
import io
import zipfile
from pathlib import Path
import numpy as np
import soundfile as sf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import spectrogram

AUDIO = Path("data/powdermill/Recording_1_Segment_22.mp3")
ANNOTATIONS = Path("data/powdermill/annotation_Files.zip")
MEMBER = "Recording_1/Recording_1_Segment_22.Table.1.selections.txt"
OUTPUT = Path("results/powdermill_crow_boxes.png")
START, END = 145, 205

rate = sf.info(AUDIO).samplerate
signal, decoded_rate = sf.read(AUDIO, start=START * rate, stop=END * rate, always_2d=True)
if decoded_rate != rate or len(signal) != (END - START) * rate:
    raise ValueError("Unexpected sample rate or incomplete decoded window")
signal = signal.mean(axis=1)
freq, times, power = spectrogram(signal, fs=rate, window="hann", nperseg=1024, noverlap=768, mode="psd")
db = 10 * np.log10(np.maximum(power, 1e-12))
with zipfile.ZipFile(ANNOTATIONS) as archive, archive.open(MEMBER) as raw:
    rows = list(csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""), delimiter="\t"))
boxes = []
for row in rows:
    if row["Species"].strip() != "AMCR":
        continue
    begin, end = float(row["Begin Time (s)"]), float(row["End Time (s)"])
    if begin >= START and end <= END:
        boxes.append((begin, end, float(row["Low Freq (Hz)"]), float(row["High Freq (Hz)"])))
if not boxes:
    raise ValueError("No completely contained AMCR labels found")
fig, ax = plt.subplots(figsize=(14, 5), constrained_layout=True)
plot = ax.pcolormesh(START + times, freq / 1000, db, shading="auto", cmap="magma", vmin=-110, vmax=-35)
for begin, end, low, high in boxes:
    ax.add_patch(Rectangle((begin, low / 1000), end - begin, (high - low) / 1000,
                           fill=False, edgecolor="cyan", linewidth=1.2))
ax.set(xlabel="Seconds in source recording", ylabel="Frequency (kHz)", ylim=(0, 4),
       title=f"Powdermill recording 1, segment 22: {len(boxes)} source AMCR annotations")
fig.colorbar(plot, ax=ax, label="dB/Hz relative to full scale")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT, dpi=160)
print(f"Wrote {OUTPUT}; {len(boxes)} source boxes; duration {len(signal)/rate:.1f}s")
