# Real crow audio with expert annotations

The [Powdermill dataset](../data/powdermill/PROVENANCE.md) supplies audio and corresponding time-frequency labels. This repository contains one five-minute MP3 and the original annotation archive. In the selected 145–205 second window of recording 1, segment 22, **seven annotation boxes** are labeled `AMCR` (American crow). The [figure](powdermill_crow_boxes.png) overlays those source boxes on a spectrogram of the corresponding MP3.

The image shows where the original annotators labeled sounds; it does not independently verify species or call boundaries, and sounds from other species and background noise remain. The label is species identity, not an observed behavior or translation. The source selection intentionally omits short chips; the count is not a complete count of all crow sounds or individuals. This one window was selected after checking the annotations, and is not a held-out evaluation.

Generate from the repository root after installing requirements: `python powdermill_figure.py`. The plot uses a Hann window, 1024 samples, 75% overlap, and shows 0–4 kHz; cyan boxes correspond to source annotations fully contained in the window. See provenance for citation, the 44.1 kHz MP3 versus 32 kHz README discrepancy, and alignment limitations.
