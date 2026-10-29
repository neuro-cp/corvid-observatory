# MP3–WAV timing check

We compared the selected Powdermill MP3 with its corresponding WAV extracted from the source archive. Both decode as mono 44,100 Hz audio, despite the source README's 32 kHz statement. This observation describes these files and does not explain the discrepancy.

In five 5-second windows beginning at 30, 100, 145, 200, and 270 seconds, the highest normalized cross-correlation within ±0.5 seconds occurs at **zero samples** in each case. Peaks range from 0.964 to 0.972. Details and file hashes are in [powdermill_alignment.json](powdermill_alignment.json). The 145- and 200-second windows cover the beginning and end of the plotted annotation view; the other samples check points across the recording.

This supports timing alignment in the sampled windows; it does not prove all labels are accurate or validate the entire file sample by sample. The audio formats differ and the MP3 is lossy. This comparison does not independently verify the human annotations or species identification.

To reproduce (downloads approximately 19 MB in ranges; the 26 MB extracted WAV is ignored by Git):

```text
python fetch_powdermill_sample.py --format wav
python check_powdermill_alignment.py
```

Use the project's dependency environment for the second command. The source data and citation are documented in [provenance](../data/powdermill/PROVENANCE.md).
