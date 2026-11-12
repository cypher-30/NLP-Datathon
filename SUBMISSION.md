# Submission manifest — Team 3 "Ubuntu"

Strathmore NLP Hub Datathon 2026.

| Item | Value |
|---|---|
| Team | Team 3, "Ubuntu" |
| Members | Alvin Murithi (code and demo), Mukundi Witness Chingwena (Shona data and language review), Natalie Chelagat (documentation) |
| Primary language | Shona (`sn`) |
| Track | Track A, intent classification (10 MASSIVE-aligned labels) |
| GitHub | https://github.com/cypher-30/NLP-Datathon |
| v1 frozen (data, model, test run 11 Nov) | `f5933d8c94809ad7c87e4cdc60be57688d97fc47` (tag `v1-frozen`) |
| v2 fresh test frozen, before any model saw it | `05f2be9df160e16b170fcce0951dbefb5eb51f0e` (tag `fresh-test-frozen`) |
| v2 model choice frozen (train CV + dev only) | `c8a335d9b3fde87dbd936d69450fc96a15e8790b` (tag `v2-selection-frozen`) |
| v2 fresh-test results (run once, 12 Nov) | `0817e071895f6cd08c16bfebf9dc0b72dfc702be` (tag `v2-final`); the run itself was at `19f6401` |
| Final submission commit | `<<FILL: full SHA of the final commit>>` |
| v2 model (demo default) | `artifacts/v2/B_tuned_tfidf.joblib` in the repository, SHA-256 `9b9ccc9fb74e365827a32673a4dc9e0ffb6a67d1208fb09389e17d9c1d901152` |
| v1 model | GitHub release `v1.0-final`: https://github.com/cypher-30/NLP-Datathon/releases/tag/v1.0-final (`model.joblib`, SHA-256 `29f4510b2cef49556960f558d9a3f38ef44d83f897943275c71f2c45d853995d`) |
| Demo recording | *link to be added* |

## Data v5 (current file; fresh test frozen 12 Nov 2026, before any model saw it)
- File: `data/contribution.csv`, v5, 595 rows, SHA-256 `e347b077f941d9b98fe508eb1e1ac1a9a067bb1d1e36d44236d044562b7850ec`.
- Added SN-296 to SN-595 (300 rows, `source_version` `2026-11-12`): 100 **fresh test** rows (SN-296 to SN-395, 10 per label) and 200 new train rows (20 per label). All written by `MUK`, independently reviewed by `FDK`, `original_human`; none written by AI or with AI help (confirmed by Mukundi).
- The 50 v1 test rows were **retired into train**, because their v1 results had already been seen. Dev is the same 50 rows as before. Split: 445 train / 50 dev / 100 test.
- FDK's review changed 79 of the 300 new rows (29 test, 50 train) over three rounds (no rejections or label changes were recorded). Every change, with before and after text and the reason, is in `review_log.csv`. The reasons: a sentence too close to an existing row, the same pattern with only a name changed, too many uses of *nyamusi*, and adding Karanga and Ndau words.
- Near-duplicate check, done before any model was trained on v5: each fresh test row was compared with every older row and every new train row (character 2–5-gram TF-IDF cosine). The highest match is SN-356 vs SN-261 (both `lists_query`) at 0.76, below the 0.8 threshold, so it was kept unchanged. There are no near-pairs within the test set. The 360-row ChatGPT stress set could not be included in this check because those files are no longer available.
- The source file Mukundi sent carried `source_version` `2026-11-08-draft` on all 300 rows, copied from older rows; it was set to `2026-11-12`, the date they were written, before this freeze. No other field was changed.

## Data v4 (used for the v1 model and the 11 Nov test run)
- SHA-256 `974c50c5808129539867611aa8b511fcaae8ce4eee9ebe78bac5c0de1629e49e` after the metadata correction below.
- Metadata correction after the final test (12 Nov 2026): the 37 rows added on 9–10 Nov that still carried `source_version` `2026-11-08-draft` (SN-251 to SN-295, except the 8 marked `2026-11-10-reword`) now carry `2026-11-10-added`, the date they were committed. Only that column changed: text, labels, splits and group IDs are identical, so the model and all results are unchanged. The file as trained and tested at `f5933d8` had SHA-256 `5eb442f7ba66e330b47cb6bc7db406b22eb543107d93adb80bf659a09cd30160`.
- 295 Shona sentences, 10 labels. Split: 195 train / 50 dev / 50 test (5 dev and 5 test per label; 15 to 27 train per label).
- All rows `original_human`, written by `MUK`, independently reviewed by `FDK`. No AI-written rows. No external datasets.
- A separate 360-sentence stress set (generated with ChatGPT, checked by Mukundi) was used only as an extra check. It is not in the dataset or the repository.

## Licences
- Data: CC BY 4.0 (team-written; no third-party sources).
- Code: the Strathmore starter kit's licence, `LICENSE_CODE.txt`. Our changes are listed in `README.md`.

## Results and metric files
| Model and test | Accuracy | Macro-F1 | Majority baseline macro-F1 |
|---|---|---|---|
| v2 (tuned TF-IDF, v5 data), fresh test of 100, run once 12 Nov 2026 | 0.920 | 0.919 | 0.018 |
| v1 (kit model, v4 data), same fresh test | 0.680 | 0.681 | 0.018 |
| v1, its own test of 50, run once 11 Nov 2026 | 0.800 | 0.799 | 0.018 |
| v1 dev (50) | 0.920 | 0.919 | 0.018 |

- `artifacts/v2/selection.json` (all v2 candidates, CV and dev scores, model hashes), `artifacts/v2_ablation_v4data/selection.json`, `artifacts/train_v2_log.txt`
- `artifacts/v2/test_metrics.json`, `artifacts/v2/test_predictions.csv`, `artifacts/v2/test_run.lock`, `artifacts/v2/compare_log.txt`
- `artifacts/intent/dev_metrics.json`
- `artifacts/intent/test_metrics.json`
- `artifacts/intent/per_label_report.csv`
- `artifacts/intent/test_predictions.csv`

## Documents
`README.md` (overview, reproduction, results, error analysis), `review_log.csv` (FDK review changes), `DATA_CARD.md`, `DATA_PLAN.md`, `ANNOTATION_GUIDE.md`, `QUALITY.md`, `CONTRIBUTIONS.md` (team roles and AI-use statement).

## Run the demo
From the repository folder, with Python 3.10 or later:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app_shona.py    # uses artifacts/v2/B_tuned_tfidf.joblib, included in the repository
```

Open the local address Streamlit prints, type a Shona request and press **Understand**. Full commands, including validation and evaluation, are in `README.md`.

## Known unresolved issues
- Whether a reviewer from outside the team (`FDK`) is eligible is still to be confirmed with the organisers.
- v2's weakest label is `lists_createoradd` (fresh-test F1 0.78): list add requests phrased as statements are read as list queries. Mostly-English requests and words never seen in training are also weak. v1's weakest label was `calendar_query` (F1 0.444 on its test).
- The demo can accept unsupported "cancel / remove / change" requests on supported topics, because there is no "not supported" class.
- The freeze commits and tags were pushed to GitHub after the fresh-test run, so the order (test frozen, then model chosen, then test scored) rests on the local commit history, not on GitHub's timestamps.
- Each row's `licence_or_permission` field holds the original authorization text; the dataset licence (CC BY 4.0) is stated in `DATA_CARD.md`. Edits to the CSV after the v1 test run: the `source_version` correction and the v5 additions, both described under Data.
- One writer (`MUK`) and one reviewer (`FDK`) for all 595 rows, including the fresh test, so the test does not measure how the model copes with other writers.
