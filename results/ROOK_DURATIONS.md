# Exploratory annotation durations

This is a descriptive examination of the [Martin et al. captive rook annotations](../data/rook/PROVENANCE.md), not a test of what birds communicate. The source labels time intervals `Song=TRUE` or `FALSE`. We calculate each interval's end minus start, exclude the special source categories `Inc`, `Pls`, `Comment`, and `Ignore`, then report the median duration for each `(colony, identified source, sex, Song)` group in [rook_individual_durations.csv](rook_individual_durations.csv). Source labels and boundaries are taken as supplied, not independently verified against audio.

The archive has **27,828 retained annotation rows from 22 identified sources**. Fifteen sources have both song labels. For those 15, the median duration for `TRUE` is shorter than the `FALSE` median for 10, and longer for five. The median of the 15 within-source differences (`TRUE` minus `FALSE`) is about **−0.078 seconds**. This was an exploratory calculation chosen after inspecting the data, not a preregistered hypothesis or an independent replication of the authors' paper.

This comparison gives each source one summary, but it does not establish statistical independence: birds share colonies, recording sessions and social conditions. Recording effort, group sizes, annotation completeness, activity and timing differ. The `TRUE` and `FALSE` annotations can represent different units and recording contexts; a difference in interval durations is not necessarily a biological difference in calls. Sources with only one label are excluded from the paired comparison, which may introduce selection bias. No confidence intervals, hypothesis tests, effect on receivers or meaning should be inferred. It is not evidence about American crows in the wild.

Reproduce the CSV and printed summary:

```text
python rook_durations.py data/rook/clean_labels.zip --output results/rook_individual_durations.csv
```

The summary CSV is derived from the source archive and is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); cite the original dataset and article as detailed in the provenance file.
