# Quality Assurance and Evaluation Report

**Team / language / dataset version:** Team 3 "Ubuntu", Shona, `data/contribution.csv` v4, 295 rows (`source_version` 2026-11-08-draft for 283 rows; 2026-11-10-reword for the 12 reworded rows). Frozen on 10 Nov 2026; final test run once on 11 Nov 2026.

## 1. Dataset Quality and Validation

Team Ubuntu developed a Shona intent classification dataset containing **295 labeled sentences** across ten intent categories.

The dataset was validated with the organizers' `validate.py` script (without `--practice`), which checks:

- Dataset structure, required fields and no empty fields.
- Intent label consistency and category coverage (every label in every split).
- Training, development, and testing split integrity, including row minimums.
- No duplicate ids or duplicate normalised text; one language.
- Review metadata (every test row independently reviewed) and no emails or phone numbers.

**The dataset passed validation on 10 November 2026.**

| Label | Train | Dev | Test | Total |
|---|---:|---:|---:|---:|
| `calendar_query` | 27 | 5 | 5 | 37 |
| `lists_createoradd` | 25 | 5 | 5 | 35 |
| `lists_query` | 25 | 5 | 5 | 35 |
| `datetime_query` | 23 | 5 | 5 | 33 |
| `calendar_set` | 20 | 5 | 5 | 30 |
| `weather_query`, `alarm_set`, `news_query`, `play_music`, `qa_definition` | 15 | 5 | 5 | 25 each |

Rows SN-001 to SN-250 are batch 1. SN-251 to SN-295 are batch 2 (all train): `lists_createoradd` 10, `lists_query` 9, `calendar_query` 8, `calendar_set` 4, `datetime_query` 7. Unchanged external rows: none.

## 2. Language Review and Annotation Quality

All 295 rows are `original_human`, written by `MUK` (Mukundi) with no AI help, and reviewed by `FDK`, a second Shona speaker. The licence text's "two shona speakers" means this writer and this reviewer.

The review focused on:

- Grammatical correctness and natural Shona expressions.
- Clarity of sentence meaning.
- Consistency between sentences and their assigned intent labels.

All records are marked `independently_reviewed`, including the 50 test rows. Mukundi confirmed all texts and labels on 9 Nov. Supporting reviewer evidence is kept privately; whether a reviewer from outside the team is eligible is still to be confirmed with the organisers.

The team followed the decision rules in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md) for closely related categories.

## 3. Data Cleaning and Leakage Prevention

The team ran duplicate detection and cross-split similarity checks (character n-gram cosine similarity).

Findings before the fix:

- **New train rows rewording a dev or test row:** SN-268 vs SN-173 (test), SN-280 vs SN-123 (test), SN-277 vs SN-117 (dev), SN-279 vs SN-118 (dev), SN-282 vs SN-118 and SN-095 (dev), SN-285 vs SN-092 (dev), SN-292 vs SN-041 (dev), SN-269 vs SN-168 (dev, mild).
- **Older rows that already leaked:** SN-046 (test) vs SN-035 (train), SN-050 (test) vs SN-027, SN-047 (test) vs SN-036, SN-200 (test) vs SN-180.
- **Train-to-train template reuse (variety, not leakage):** about 15 pairs, for example SN-283/SN-077, SN-284/SN-079, SN-287/SN-082; twins inside batch 2 such as SN-288/SN-295 and SN-272/SN-278.

**Fix applied on 10 Nov (train rows only; dev and test untouched):** Mukundi reworded 12 train rows (SN-027, 035, 036, 180, 268, 269, 277, 279, 280, 282, 285, 292), reviewed by FDK. Some near-duplicate clusters now share a `group_id` (285 groups for 295 rows), and no `group_id` spans two splits. After the rewording, no reworded row pairs with a dev or test row above 0.6 similarity.

Remaining: 12 cross-split pairs still score 0.60 or more, almost all inside the original 250 rows (for example SN-235 train vs SN-241 dev at 0.71, SN-009 vs SN-024 at 0.69). They are template-similar questions, not copies, and are considered when interpreting the results.

## 4. Model Development and Evaluation

The project uses a lightweight supervised approach: **character-level TF-IDF features (2–5 grams)** with **logistic regression**, trained on the train split only (`random_state=42`). It was chosen because it is fast and suits a small labeled dataset. A majority-class baseline (always predicts the most common label) is trained alongside it for comparison.

### Development Set Results

| Metric | Model | Majority baseline |
|---|---:|---:|
| Development accuracy | **0.920** (46/50) | 0.10 |
| Macro-F1 score | **0.919** | 0.018 |

Dev errors (4 of 50): SN-020 (`weather_query` read as `datetime_query`), SN-094 (`calendar_set` read as `calendar_query`), SN-116 and SN-117 (`calendar_query` read as `calendar_set`). The weather error comes from time words ("nguva", "zuva", "pari zvino") without a clear weather noun, while date/time has more training rows.

These findings informed the 45 added training examples. Settings were chosen on dev; the test split was not used to change the data, model or demo thresholds.

## 5. Robustness and Generalization (Stress Set)

Beyond the development set, the team built a separate **stress set of 360 Shona sentences**: 300 supported requests (30 per label) and 60 requests the demo should refuse. Mukundi generated it with **ChatGPT** and then checked the sentences and labels himself. It is synthetic data, so it was used only as an extra check on the model and demo. It was never used for training or for the test score, and it is not part of `data/contribution.csv`.

On the v1 model (250 rows), the stress set gave about **74% top-label accuracy** on supported requests, and 42 of the 60 should-be-refused requests were refused. Weakest labels: `lists_query`, `calendar_query` and `lists_createoradd`. The main causes were that almost all training list rows used the single word "runyorwa" (the stress set also uses rondedzero, zvekuita, mabasa, list), and that calendar questions had few training rows. Mukundi then wrote the 45 new training rows himself to cover these gaps; no stress-set sentence was copied into the dataset.

The model also mostly ignores verbs, so "remove / stop / cancel / change" requests about supported things are routed to a supported label instead of being refused. This is a known limitation.

## 6. Final Test Evaluation

The final test was run **once**, on **11 November 2026**, on the 50 frozen, independently reviewed test rows.

| Metric | Model | Majority baseline |
|---|---:|---:|
| Test accuracy | **0.800** (40/50) | 0.10 |
| Test macro-F1 | **0.799** | 0.018 |

| Label | Test F1 |
|---|---:|
| `alarm_set` | 1.000 |
| `news_query` | 1.000 |
| `weather_query` | 0.889 |
| `play_music` | 0.889 |
| `datetime_query` | 0.833 |
| `qa_definition` | 0.750 |
| `calendar_set` | 0.727 |
| `lists_createoradd` | 0.727 |
| `lists_query` | 0.727 |
| `calendar_query` | 0.444 |

Test errors (10 of 50): SN-023 (`weather_query` read as `calendar_query`), SN-100 (`calendar_set` read as `calendar_query`), SN-121 (`calendar_query` read as `datetime_query`), SN-123 and SN-125 (`calendar_query` read as `calendar_set`), SN-149 (`lists_createoradd` read as `lists_query`), SN-172 (`lists_query` read as `lists_createoradd`), SN-200 (`play_music` read as `lists_query`; "runyorwa rwenziyo" means playlist), SN-248 (`qa_definition` read as `lists_createoradd`), SN-249 (`qa_definition` read as `datetime_query`).

Five of the ten are between closely related labels (calendar set/query, list add/query), the same weakness seen on dev and the stress set. The drop from dev (0.92) to test (0.80) is six more wrong sentences; with five test rows per label, one sentence moves a label's score by about 20 points.

## 7. Limits and Unresolved

- One writer, one reviewer, one dialect, mostly formal spelling; little code-switching.
- Dev and test hold only 5 rows per label, so scores are rough.
- `calendar_query` remains the weakest label.
- The model matches letter patterns, not meaning, and cannot understand words it has never seen.
- Reviewer eligibility (outside the team) is still to be confirmed with the organisers.

## 8. Summary

- **295 labeled Shona sentences**, all human-written, across ten intent categories.
- **Passed the organizers' validation script** on 10 Nov 2026.
- **Every row independently reviewed** by a second Shona speaker.
- **Duplicate and cross-split similarity checks**, with 12 rows reworded.
- **Dev: 0.920 accuracy, 0.919 macro-F1. Test (run once): 0.800 accuracy, 0.799 macro-F1**, against a majority baseline of 0.018.
- **A ChatGPT-generated, Mukundi-checked stress set** used only to find weaknesses, kept out of training and testing.
