# Project status and continuation

Corvid Observatory is an open, early-stage research project, not a translator. The working repository is https://github.com/neuro-cp/corvid-observatory. Sources and conditions for the included audio and annotations are in `data/PROVENANCE.md` and `data/rook/PROVENANCE.md`.

## Completed

- Two American crow recordings with provenance, checksums, and reproducible waveform/spectrogram generation. One includes the recordist's behavioral notes with approximate times, not independently reviewed event intervals.
- A Powdermill soundscape segment matched to expert American crow time-frequency labels and a reproducible overlay. A five-window MP3–WAV comparison found zero-sample peak offset in each window. These labels identify species rather than behavioral context.
- A CC-BY 4.0 archive of captive rook annotations with checksum verification and a descriptive inventory.
- An exploratory per-identified-rook duration summary, including a report of the comparison's sampling and interpretation limitations.
- A CSV joiner for independently observed behavior and calls, which retains missing or ambiguous matches as unknown; example inputs are invented.

## Next work

1. Obtain independently observed, time-aligned recordings or a suitable existing dataset, with clear permission and annotation definitions. Rook TSV files are not labels for either crow recording. Do not fabricate event windows from the recordist's approximate notes.
2. Inspect and annotate audio manually, ideally with independent reviewers blinded to context, then assess annotation agreement and observation effort including no-call sessions.
3. Form a bounded, preregistered prediction, split independent sessions and sites before model development, and evaluate simple baselines with appropriate grouping and uncertainty. Do not claim semantic translation or causal meaning from correlations.
4. Continue documenting data provenance, methods, negative results, limitations, and any conditions for redistribution. Push verified project-only commits to the existing public repository after checking remote state.

## Reproduction

Run `python -m unittest discover -s tests -v`, the rook commands in `README.md`, and the documented spectrogram commands after installing requirements into a virtual environment. No evidence yet supports a validated context classifier; the exploratory duration result is not a hypothesis test.
