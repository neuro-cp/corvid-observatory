# Rook annotations: initial inventory

The public [Martin et al. dataset](https://doi.org/10.2306/rook.comp) contains annotated recordings of captive rooks, not American crows. We checked the original archive against the publisher's MD5 and inventoried the included TSV files without editing them.

The script found **107 TSV files**, **31,148 annotation rows**, and **41 distinct date prefixes**. There are **24,999** rows labeled Strasbourg and **6,149** labeled Cambridge. It flagged **3,320** rows with a special `Source` value (`Inc`, `Pls`, `Ignore`, or `Comment`); **7,918** rows have blank event fields. All rows have finite, non-negative, increasing timestamps. These are integrity checks, not verification against audio.

`Song` is `TRUE` for 15,521 rows and `FALSE` for 15,627 rows; these are the source annotations and include special entries. The row counts are not counts of independent birds, trials, or vocalizations: for example, overlapping birds and ignored intervals are represented in the data. A date prefix is not necessarily a separate independent session, and multiple files may split a recording. These figures do not estimate behavior rates, prevalence, meaning, or differences between colonies.

Reproduce with `python rook_inventory.py data/rook/clean_labels.zip --output results/rook_inventory.json`. The audio has not been checked in this inventory; its original archive is 26.2 GB. Future analysis must investigate the labeling codebook, recording effort, and non-independent repeated recordings before comparing groups.
