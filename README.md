# Corvid Observatory

A small starting point for studying whether crow or raven calls are associated with observable events. This is a research notebook and descriptive analysis tool, not a translator. It contains no real observations yet.

## First question

Are manually classified call types distributed differently during independently observed aerial threats versus ordinary activity? An association would be a lead for further study, not proof that a call means “hawk.” Species, site, individual, recording conditions, and observer expectations can all confound results.

## Try it

Requires Python 3. Run from this folder:

```text
python analyze.py example.csv
```

For audio inspection, install the dependencies in an isolated environment and run:

```text
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python inspect_audio.py data/american_crow_mcgrane_2004.ogg --output results/american_crow.png
```

On macOS or Linux use `.venv/bin/python` in place of `.venv\Scripts\python`. The output is a waveform and spectrogram, not an automated identification or context classifier. See [recording provenance](data/PROVENANCE.md), [research notes](RESEARCH.md), and the [roadmap](ROADMAP.md).

The example is invented solely to demonstrate the output. Replace it with observations recorded under the protocol below; do not combine example rows with real data.

## Field protocol

1. Select sites and observation windows in advance. Record uninterrupted audio where lawful; do not approach nests, bait birds, or play distress calls. Record weather and site separately.
2. Log events with start and end times, including ordinary activity and periods with no visible trigger. Label uncertainty explicitly. Record a session even when no calls occur; otherwise rates are biased.
3. Separately review audio and mark call intervals and acoustic call types without seeing event labels where feasible. Record the reviewer and confidence; use an unknown category when unsure.
4. Link calls to overlapping events only after both annotations are complete. The input file uses one row per observed call and its overlapping event; `none` means no observed event, not that nothing happened. Use `unknown` when the view is obstructed.
5. Keep recordings, original annotations, recording permissions, and species identification evidence. Avoid exact nest locations or personal information in public releases. Do not expose precise coordinates by default.
6. Split discovery and validation by independent sessions and sites. Agree on a prediction before examining validation sessions; report counts, observation effort, and alternative explanations. Calls within the same session are not independent replicates.

## Data format

UTF-8 CSV columns: `session_id`, `species`, `call_type`, `event`, `confidence`. Each row describes one call. Use consistent labels and retain timestamps and recording references in your source annotation files. This minimal tool counts calls and sessions only; it does not compute event-specific rates, statistical significance, or account for unequal observation time. Sessions with zero calls are not represented and must be tracked separately.

## Recording sources

Use your own recordings or obtain permission and check each recording's license and intended use. Cornell's [media request guidance](https://support.ebird.org/en/support/solutions/articles/48001064551) explains access to Macaulay Library material. Publicly accessible recordings are not necessarily freely redistributable. Existing recordings without independent contextual observations are useful for acoustic exploration, but cannot establish what triggered a call.
