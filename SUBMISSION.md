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

## Data
- File: `data/contribution.csv`, v4, SHA-256 `5eb442f7ba66e330b47cb6bc7db406b22eb543107d93adb80bf659a09cd30160`.
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
- Each row's `licence_or_permission` field holds the original authorization text; the dataset licence (CC BY 4.0) is stated in `DATA_CARD.md`. The CSV was not edited after the final test run so that the model fingerprint stays valid.
- One writer, one reviewer, mostly formal spelling, little dialect variation or code-switching.
