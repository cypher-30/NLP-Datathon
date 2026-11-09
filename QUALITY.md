# Quality report (draft, test results not yet run)

**Team / language / dataset version:** Team 3 "Ubuntu", Shona, `data/contribution.csv` v4, 295 rows (`source_version` 2026-11-08-draft; 2 rows 2026-11-10-reword).

## Accepted contributions
All 295 rows are `original_human`, author `MUK`, reviewer `FDK`, `independently_reviewed`. Rows SN-001 to SN-250 are batch 1. SN-251 to SN-295 are batch 2 (all train): lists_createoradd 10, lists_query 9, calendar_query 8, calendar_set 4, datetime_query 7.
MUK wrote and corrected every row and FDK reviewed every row (one reviewer; the licence text says "two shona speakers", meaning author plus reviewer).

| label | train | dev | test | total |
|---|---|---|---|---|
| calendar_query | 27 | 5 | 5 | 37 |
| lists_createoradd | 25 | 5 | 5 | 35 |
| lists_query | 25 | 5 | 5 | 35 |
| datetime_query | 23 | 5 | 5 | 33 |
| calendar_set | 20 | 5 | 5 | 30 |
| weather, alarm, news, music, qa | 15 | 5 | 5 | 25 each |

**Unchanged external training rows:** none.

## Review
Every row, including all 50 test rows, was reviewed by someone other than the author. Mukundi confirmed all texts and labels on 9 Nov. The team reviewed the near-duplicate analysis below.

## Automated checks
`validate.py` passes without `--practice`: schema, no empty fields, no duplicate ids or normalised text, one language, every label in every split, no emails or phone numbers.

## Duplicates and leakage (honest findings)
`group_id` equals `record_id` on every row, so group-aware splitting does nothing and reworded rows can land in different splits.

- **Tier A, a new train row rewords a dev or test row:** SN-268 vs SN-173 (test), SN-280 vs SN-123 (test), SN-277 vs SN-117 (dev), SN-279 vs SN-118 (dev), SN-282 vs SN-118 and SN-095 (dev), SN-285 vs SN-092 (dev), SN-292 vs SN-041 (dev), SN-269 vs SN-168 (dev, mild).
- **Tier B, train-to-train template reuse (variety, not leakage):** about 15 pairs, for example SN-283/SN-077, SN-284/SN-079, SN-287/SN-082, SN-261/SN-151, SN-274/SN-108.
- **Tier C, twins inside batch 2:** SN-288/SN-295, SN-272/SN-278, SN-264/SN-269, SN-251/SN-256.
- **Older rows that already leak:** SN-046 (test) vs SN-035 (train), SN-050 (test) vs SN-027, SN-047 (test) vs SN-036, SN-200 (test) vs SN-180.

**Fix applied on 10 Nov (train rows only; dev and test untouched):** Mukundi reworded 12 train rows that closely matched dev or test rows (SN-027, 035, 036, 180, 268, 269, 277, 279, 280, 282, 285, 292), reviewed by FDK; shared `group_id` for some near-duplicate clusters; no `group_id` spans two splits. After the rewording no reworded row pairs with a dev or test row above 0.6 similarity.

Remaining: 12 cross-split pairs still score 0.60 or more (character n-gram cosine), almost all inside the original 250 rows (for example SN-235 train vs SN-241 dev at 0.71, SN-009 vs SN-024 at 0.69). They are template-similar questions, not copies; list them in the write-up.

## Baseline and model
Majority baseline: dev accuracy 0.10, macro-F1 0.018. Character TF-IDF (2 to 5 grams) + logistic regression, trained on train only (`random_state=42`): dev accuracy 0.92, macro-F1 0.919 (after the rewording). Frozen-test metrics: **to be filled in after the single `evaluate.py` run.**

## Errors
Dev errors (4 of 50): SN-020 (weather read as datetime), SN-094 (calendar_set read as calendar_query), SN-116 and SN-117 (calendar_query read as calendar_set). Cause for the weather one: time words ("nguva", "zuva", "pari zvino") without a clear weather noun, and datetime has more training rows. Test errors: to be filled in from `test_predictions.csv`.

## Limits and unresolved
One writer, one reviewer, one dialect, mostly formal spelling. Dev and test hold only 5 rows per label, so one sentence moves a label's score by 20 points. A separate AI-generated stress set (360 rows, never used for training) gave about 74% top-label accuracy on the v1 model; it is unreviewed and not part of the dataset.
