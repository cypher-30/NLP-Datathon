# Submission manifest — Team 3 "Ubuntu"

Strathmore NLP Hub Datathon 2026.

| Item | Value |
|---|---|
| Team | Team 3, "Ubuntu" |
| Members | Alvin Murithi (code and demo), Mukundi Witness Chingwena (Shona data and language review), Natalie Chelagat (documentation) |
| Primary language | Shona (`sn`) |
| Track | Track A, intent classification (10 MASSIVE-aligned labels) |
| GitHub | https://github.com/cypher-30/NLP-Datathon |
| Frozen commit (data, model, final test) | `f5933d8c94809ad7c87e4cdc60be57688d97fc47` |
| Final submission commit | the latest commit on `main` that contains this file (documentation only after `f5933d8`) |
| Trained model | GitHub release `v1.0-final`: https://github.com/cypher-30/NLP-Datathon/releases/tag/v1.0-final (`model.joblib`, SHA-256 `29f4510b2cef49556960f558d9a3f38ef44d83f897943275c71f2c45d853995d`) |
| Demo recording | *link to be added* |

## Data v5 (current file; fresh test frozen 12 Nov 2026, before any model saw it)
- File: `data/contribution.csv`, v5, 595 rows, SHA-256 `e347b077f941d9b98fe508eb1e1ac1a9a067bb1d1e36d44236d044562b7850ec`.
- Added SN-296 to SN-595 (300 rows, `source_version` `2026-11-12`): 100 **fresh test** rows (SN-296 to SN-395, 10 per label) and 200 new train rows (20 per label). All written by `MUK`, independently reviewed by `FDK`, `original_human`, no AI.
- The 50 v1 test rows were **retired into train**, because their v1 results had already been seen. Dev is the same 50 rows as before. Split: 445 train / 50 dev / 100 test.
- FDK's review changed 79 of the 300 new rows (29 test, 50 train) over three rounds; nothing was rejected. Every change, with before and after text and the reason, is in `review_log.csv`. The reasons: a sentence too close to an existing row, the same pattern with only a name changed, too many uses of *nyamusi*, and adding Karanga and Ndau words.
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
| Split | Accuracy | Macro-F1 | Majority baseline macro-F1 |
|---|---|---|---|
| Dev | 0.920 | 0.919 | 0.018 |
| Test (run once, 11 Nov 2026) | 0.800 | 0.799 | 0.018 |

- `artifacts/intent/dev_metrics.json`
- `artifacts/intent/test_metrics.json`
- `artifacts/intent/per_label_report.csv`
- `artifacts/intent/test_predictions.csv`

## Documents
`README.md` (overview, reproduction, results, error analysis), `DATA_CARD.md`, `DATA_PLAN.md`, `ANNOTATION_GUIDE.md`, `QUALITY.md`, `CONTRIBUTIONS.md` (team roles and AI-use statement).

## Run the demo
From the repository folder, with Python 3.10 or later:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python train.py --track intent --data data/contribution.csv   # or place the release's model.joblib in artifacts/intent/
python -m streamlit run app_shona.py
```

Open the local address Streamlit prints, type a Shona request and press **Understand**. Full commands, including validation and evaluation, are in `README.md`.

## Known unresolved issues
- Whether a reviewer from outside the team (`FDK`) is eligible is still to be confirmed with the organisers.
- `calendar_query` is the weakest label (test F1 0.444); calendar and list "set" vs "query" requests are often confused.
- The demo refuses some valid requests (for example SN-100, SN-248 on test) and accepts some unsupported "cancel / remove / change" requests, because the model mostly ignores verbs. There is no "not supported" class.
- Each row's `licence_or_permission` field holds the original authorization text; the dataset licence (CC BY 4.0) is stated in `DATA_CARD.md`. Edits to the CSV after the v1 test run: the `source_version` correction and the v5 additions, both described under Data.
- One writer (`MUK`) and one reviewer (`FDK`) for all 595 rows, including the fresh test, so the test does not measure how the model copes with other writers.
