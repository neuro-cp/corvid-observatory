# A recording with observed behavior

Jonathon Jongsma's [XC112598](https://commons.wikimedia.org/wiki/File:Corvus_brachyrhynchos_-_American_Crow_XC112598.mp3) contains American crow audio and an observer's description of one bird's posture and soft sounds at approximately 112, 117, and 123 seconds. The unmodified audio and attribution are in [provenance](../data/PROVENANCE.md).

The included [waveform and spectrogram](xc112598_108-126.png) covers 108–126 seconds. It is a view of the sound, not an independent identification of individual calls: multiple events and background sound are present, the sound is faint, and the recordist's timestamps are approximate. We have not verified the notes against video, assigned boundaries, or determined what the sounds communicate. This recording provides a concrete hypothesis for independent annotation, not a validated behavior classifier.

Reproduce after installing `requirements.txt`:

```text
python inspect_audio.py data/american_crow_xc112598.mp3 --start 108 --end 126 --output results/xc112598_108-126.png
```

The visualization is derived from the CC BY-SA 3.0 recording and is shared under the same license; see the provenance file for credit. Window: Hann, 1024 samples, 75% overlap, power spectral density, displayed 0–10 kHz. The fixed color range may obscure quiet sounds; a plot cannot replace listening or independent event annotation.
