"""Compare MP3 and WAV timing in five windows using normalized cross-correlation."""
import hashlib
import json
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import correlate, correlation_lags

ROOT = Path("data/powdermill")
WAV = ROOT / "Recording_1_Segment_22.wav"
MP3 = ROOT / "Recording_1_Segment_22.mp3"
OUTPUT = Path("results/powdermill_alignment.json")
STARTS = (30, 100, 145, 200, 270)
DURATION = 5


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    wi, mi = sf.info(WAV), sf.info(MP3)
    if wi.samplerate != mi.samplerate or wi.channels != 1 or mi.channels != 1:
        raise ValueError("Expected matching sample rates and mono audio")
    rate = wi.samplerate
    results = []
    for start in STARTS:
        wav, _ = sf.read(WAV, start=start * rate, frames=DURATION * rate, dtype="float64")
        mp3, _ = sf.read(MP3, start=start * rate, frames=DURATION * rate, dtype="float64")
        if len(wav) != DURATION * rate or len(mp3) != DURATION * rate:
            raise ValueError(f"Incomplete sample at {start} seconds")
        wav -= wav.mean()
        mp3 -= mp3.mean()
        denom = np.linalg.norm(wav) * np.linalg.norm(mp3)
        if denom == 0:
            raise ValueError(f"Silent window at {start} seconds")
        corr = correlate(mp3, wav, mode="full", method="fft") / denom
        lags = correlation_lags(len(mp3), len(wav), mode="full")
        keep = np.abs(lags) <= rate // 2
        selected_lags, selected_corr = lags[keep], corr[keep]
        index = int(np.argmax(selected_corr))
        results.append({"start_s": start, "duration_s": DURATION,
                        "lag_samples_mp3_relative_to_wav": int(selected_lags[index]),
                        "lag_seconds": float(selected_lags[index] / rate),
                        "normalized_peak": float(selected_corr[index])})
    out = {"wav_sha256": digest(WAV), "mp3_sha256": digest(MP3), "sample_rate_hz": rate,
           "search_lag_seconds": 0.5, "windows": results}
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
