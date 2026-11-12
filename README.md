# Team 03 | Ubuntu: understanding Shona requests (intent classification)

## Team and task

- Team number and name: Team 03, "Ubuntu"
- Three members and their contributions:
  - Alvin Murithi (GitHub `cypher-30`): code and demo. Set up the repository, adapted the starter kit, ran validation, training and the test runs, built the Streamlit demo.
  - Mukundi Witness Chingwena: Shona data and language review. Wrote and labelled all 595 sentences and coordinated the independent review.
  - Natalie Chelagat (GitHub `natalie400`): documentation. Data card, data plan, annotation guide, quality report and contribution statement.
  - Independent reviewer `FDK`, a Shona speaker who is not an author, reviewed every row.
- Working language/variety: Shona (`sn`), mostly standard written Shona, with some informal spelling, Shona–English code-switching and a few Karanga and Ndau words in the newer rows.
- Track: **A, intent classification** (10 MASSIVE-aligned labels)
- Original team repository URL: https://github.com/cypher-30/NLP-Datathon
- Full source commit SHA for the version submitted: `<<FILL: full SHA of the final commit>>`. Earlier frozen points are tagged: `v1-frozen` (v1 data, model and test), `fresh-test-frozen` (v2 test set, before any model saw it), `v2-selection-frozen` (v2 model choice, before the test run), `v2-final` (v2 test results).

## Idea and approach

Voice and chat assistants rarely understand Shona, which is spoken by more than 10 million people, mostly in Zimbabwe. We built a small classifier that reads a typed Shona request, such as a weather question or a request to set an alarm, and works out which of 10 actions the person wants. It says "not supported" instead of guessing when a request looks unlike anything it knows, and it can show which words led to its answer.

1. **Data:** Shona is not in MASSIVE, so we wrote our own: 595 new sentences (`original_human`, none written by AI), each independently reviewed by a second Shona speaker, with a written annotation guide for confusable labels.
2. **v1 (11 Nov):** the starter kit's model (character TF-IDF + logistic regression) on 295 sentences. Test split scored once: 0.80 accuracy.
3. **Fresh test for a fair v2:** because the v1 test results had been seen, we did not reuse that test. Mukundi wrote 100 new test sentences and 200 new training sentences; FDK reviewed them and changed 79. The test was frozen and committed before any model was trained on it, and the old 50 test sentences were moved into training.
4. **v2 model choice on train and dev only:** three candidates (the kit model, a tuned word + character TF-IDF model, and LaBSE multilingual sentence embeddings) were compared with 5-fold cross-validation on train plus the dev split. The selection rule was fixed in code before training. The tuned TF-IDF model won. The choice was committed, then all models were scored **once** on the fresh test.
5. **Demo:** Streamlit app adapted from the kit: plain-language answer, top-3 alternatives, "not supported" fallback, a "Why did it decide this?" panel (which words mattered, most similar training sentences) and a "How good is it?" tab with the results.

Reused: the starter kit's `validate.py`, `train.py` (one added line), `evaluate.py` and `core.py`, used as provided. New: the dataset, `review_log.csv`, `app_shona.py`, `prepare_working.py`, `models_v2.py`, `train_v2.py`, `compare.py`, `tune_thresholds.py`.

## Data and review

- [`data/contribution.csv`](data/contribution.csv): **595 rows**, 10 labels, data SHA-256 `e347b077f941d9b98fe508eb1e1ac1a9a067bb1d1e36d44236d044562b7850ec`.
- Splits are stored in the CSV: **445 train / 50 dev / 100 test**.

| Label | Train | Dev | Test | Total |
|---|---:|---:|---:|---:|
| `weather_query` | 40 | 5 | 10 | 55 |
| `datetime_query` | 48 | 5 | 10 | 63 |
| `alarm_set` | 40 | 5 | 10 | 55 |
| `calendar_set` | 45 | 5 | 10 | 60 |
| `calendar_query` | 52 | 5 | 10 | 67 |
| `lists_createoradd` | 50 | 5 | 10 | 65 |
| `lists_query` | 50 | 5 | 10 | 65 |
| `play_music` | 40 | 5 | 10 | 55 |
| `news_query` | 40 | 5 | 10 | 55 |
| `qa_definition` | 40 | 5 | 10 | 55 |

- How the dataset grew: SN-001 to SN-250 (first set), SN-251 to SN-295 (45 train rows for list, calendar and date/time wording, 9–10 Nov), SN-296 to SN-595 (100 fresh test rows and 200 train rows, 12 Nov). The 50 v1 test rows were moved to train after v1's single test run (`SUBMISSION.md` records the v4 file and its hash).
- All rows `original_human`, written by `MUK`, reviewed by `FDK` (`independently_reviewed`; the reviewer never wrote the rows they reviewed). No external datasets.
- Review evidence: [`review_log.csv`](review_log.csv) lists every change FDK made to the 300 newest rows: 79 rows changed (29 test, 50 train) over three rounds, each with the text before and after and the reason. For the first 75 rows of three labels, [`QUALITY.md`](QUALITY.md) records 63 kept and 12 changed.
- Quality checks: the organisers' `validate.py` passes (non-practice). Each fresh test row was compared with every older row and every new training row (character 2–5-gram TF-IDF cosine); the highest match is 0.76 and none reach 0.8. No dev row is within 0.8 of any training row. No `group_id` spans two splits.
- Data licence: CC BY 4.0. Permission evidence is kept privately, outside this repository.

## Code and how to run

Python 3.13.5 (3.10+ should work); scikit-learn 1.7.2, pandas 2.3.3, streamlit 1.67.0, joblib 1.6.0 ([`requirements.txt`](requirements.txt)). LaBSE (candidate C only) also needs `requirements-labse.txt`, which installs torch and downloads about 1.8 GB on first use. Run everything from this folder.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1            # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python validate.py --track intent --data data/contribution.csv

# Demo with the v2 model (artifacts/v2/B_tuned_tfidf.joblib is included in the repository)
python -m streamlit run app_shona.py
```

Rebuild v2 (model choice on train cross-validation + dev only):

```powershell
python -m pip install -r requirements-labse.txt                       # only if you want candidate C
python train_v2.py --data data/contribution.csv --out artifacts/v2   # writes the packs + artifacts/v2/selection.json
python train_v2.py --data data/ablation/contribution_v4.csv --out artifacts/v2_ablation_v4data   # same models on the v1 data
python compare.py --final --data data/contribution.csv --packs artifacts/v2 artifacts/v2_ablation_v4data
```

`compare.py` scores every model on the fresh test once. It refuses to run if the working tree has uncommitted changes, if `selection.json` is not committed, if any model file differs from the hash recorded at selection, or if `artifacts/v2/test_run.lock` exists (it has: our run is recorded there). To repeat it, delete the lock in your own copy. Results go to `artifacts/v2/test_metrics.json` and `test_predictions.csv`.

The kit pipeline also runs on the v5 data: `python train.py --track intent --data data/contribution.csv` then `python evaluate.py ...` (writes to `artifacts/intent/`, and replaces the v1 model there).

Model files:
- v2 winner: [`artifacts/v2/B_tuned_tfidf.joblib`](artifacts/v2/B_tuned_tfidf.joblib), SHA-256 `9b9ccc9fb74e365827a32673a4dc9e0ffb6a67d1208fb09389e17d9c1d901152` (also recorded in `artifacts/v2/selection.json`).
- v1: [`artifacts/intent/model.joblib`](artifacts/intent/model.joblib) (in the repository; also GitHub release `v1.0-final`, https://github.com/cypher-30/NLP-Datathon/releases/tag/v1.0-final), SHA-256 `29f4510b2cef49556960f558d9a3f38ef44d83f897943275c71f2c45d853995d`. `compare.py` checks this hash.
- Only load `.joblib` files from a source you trust.

## Results and limitations

### v2: fresh test (100 sentences no model had seen, run once on 12 Nov 2026)

Files: [`artifacts/v2/test_metrics.json`](artifacts/v2/test_metrics.json), [`artifacts/v2/test_predictions.csv`](artifacts/v2/test_predictions.csv), model choice in [`artifacts/v2/selection.json`](artifacts/v2/selection.json).

| Model | Trained on | Accuracy | Macro-F1 | Macro-F1 95% CI (bootstrap) |
|---|---|---:|---:|---|
| **B tuned TF-IDF (v2, chosen before the test)** | v5 | **0.920** | **0.919** | 0.853–0.967 |
| A kit model | v5 | 0.890 | 0.890 | 0.820–0.943 |
| C LaBSE | v5 | 0.860 | 0.857 | 0.772–0.919 |
| v1 (frozen release model) | v4 | 0.680 | 0.681 | 0.574–0.759 |
| B tuned TF-IDF | v4 | 0.760 | 0.772 | 0.675–0.844 |
| C LaBSE | v4 | 0.820 | 0.818 | 0.728–0.888 |
| Majority baseline | v5 | 0.100 | 0.018 | |

How the winner was chosen (no test data used): highest mean of train cross-validation macro-F1 and dev macro-F1, with LaBSE needing a 0.02 lead to win because it is much heavier to run.

| Candidate (v5 data) | CV macro-F1 | Dev macro-F1 (50 rows) |
|---|---:|---:|
| A kit model | 0.847 | 0.918 |
| **B tuned TF-IDF** (word 1-grams + character 2–5-grams, logistic regression C=3) | 0.884 | **1.000** |
| C LaBSE + logistic regression | **0.916** | 0.917 |

What this shows:
- **The new data did most of the work.** The unchanged kit model goes from 0.681 to 0.890 macro-F1 when trained on v5 instead of v4. The tuned model adds a further 0.03, but the confidence intervals overlap, so that extra gain is uncertain.
- **v1 scores lower on the fresh test (0.68) than on its own test (0.80).** The fresh test uses new wording, names and some code-switching, so it is a harder and more realistic check.
- LaBSE had the best cross-validation score and did best of the three on the v4 data, but not on the fresh test with v5 data.
- B's perfect dev score is on only 50 sentences and is optimistic; the fresh-test score is the one to rely on.

Per-label F1 on the fresh test:

| Label | v1 | v2 (B) |
|---|---:|---:|
| `weather_query` | 0.33 | 0.95 |
| `datetime_query` | 0.72 | 0.89 |
| `alarm_set` | 0.75 | 0.95 |
| `calendar_set` | 0.67 | 0.95 |
| `calendar_query` | 0.51 | 0.91 |
| `lists_createoradd` | 0.78 | 0.78 |
| `lists_query` | 0.67 | 0.87 |
| `play_music` | 0.89 | 0.95 |
| `news_query` | 0.82 | 0.95 |
| `qa_definition` | 0.67 | 1.00 |

v2 (B) confusion matrix on the fresh test (rows = true label, columns = predicted):

| True \ Predicted | weather | datetime | alarm | cal_set | cal_query | list_add | list_query | music | news | definition |
|---|---|---|---|---|---|---|---|---|---|---|
| **weather** | **9** | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **datetime** | 0 | **8** | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| **alarm** | 0 | 0 | **10** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **cal_set** | 0 | 0 | 1 | **9** | 0 | 0 | 0 | 0 | 0 | 0 |
| **cal_query** | 0 | 0 | 0 | 0 | **10** | 0 | 0 | 0 | 0 | 0 |
| **list_add** | 0 | 0 | 0 | 0 | 0 | **7** | 3 | 0 | 0 | 0 |
| **list_query** | 0 | 0 | 0 | 0 | 0 | 0 | **10** | 0 | 0 | 0 |
| **music** | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **9** | 0 | 0 |
| **news** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **10** | 0 |
| **definition** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **10** |

Five of v2's 8 errors (from `test_predictions.csv`):

| Record | True | Predicted | Likely cause |
|---|---|---|---|
| SN-346 | lists_createoradd | lists_query | "zvandichatenga" (shopping list) appears equally in add and query training rows, and the request is phrased as a statement ("Dovi rapera…") rather than with an "add" verb. SN-350 and SN-355 fail the same way: list add vs query is the weakest pair. |
| SN-313 | datetime_query | news_query | Mostly English ("What's the time ikozvino…"); the training data has very little English, so the model has few clues. |
| SN-331 | calendar_set | alarm_set | "na4 pm" (at 4 pm) is a time pattern seen mostly in alarm rows, and "book call" is English. |
| SN-369 | play_music | lists_createoradd | "jiti" (a music genre) never appears in training, so the model follows "isa" (put/add), which is common in list rows. |
| SN-305 | weather_query | calendar_query | Asks whether a jacket is needed when going out at night; no weather word, so the model cannot see it is about the weather. |

All 8: SN-305, SN-307, SN-313, SN-331, SN-346, SN-350, SN-355, SN-369.

### v1: original test (50 sentences, run once on 11 Nov 2026)

Files: [`artifacts/intent/test_metrics.json`](artifacts/intent/test_metrics.json), [`per_label_report.csv`](artifacts/intent/per_label_report.csv), [`test_predictions.csv`](artifacts/intent/test_predictions.csv). Dev 0.920 accuracy / 0.919 macro-F1; **test 0.800 accuracy / 0.799 macro-F1**; majority baseline 0.018. Weakest label `calendar_query` (F1 0.44). Errors: SN-023, SN-100, SN-121, SN-123, SN-125, SN-149, SN-172, SN-200, SN-248, SN-249; five of them are between calendar set/query or list add/query. Details and the confusion matrix are in [`QUALITY.md`](QUALITY.md). These 50 sentences are now training data for v2.

### Limitations
- **One writer and one reviewer** for all 595 sentences, including the fresh test, so the scores do not show how the model copes with other people's Shona.
- Small test sets (10 per label for v2, 5 for v1): one sentence moves a label's F1 by 5 to 20 points. The confidence intervals above are wide.
- Mostly standard written Shona. Code-switched and dialect sentences are a small share, and mostly-English requests are weak (SN-313).
- The model matches word and letter patterns, not meaning, and misses words it has never seen (SN-369).
- The demo refuses unsupported requests by thresholds tuned on dev rows and 16 English off-topic probes; Shona requests for unsupported actions ("cancel", "remove") can still be accepted, because there is no "not supported" class.
- Probabilities are uncalibrated and are not percentages of certainty.
- An extra stress check on v1 with 360 ChatGPT-generated sentences (checked by Mukundi, never used for training or scoring, not in this repository) found weak handling of unfamiliar list and calendar wording, which shaped the new training rows. Those files were not available for the v2 near-duplicate check.
- Evidence of order: the freeze points are local git commits and tags (`fresh-test-frozen` before `v2-selection-frozen` before `v2-final`); they were pushed to GitHub after the test run, so GitHub's own timestamps do not prove the order.

## Demo behaviour
- Confident match: "It looks like you want: <action>", plus what the assistant would do and two other possibilities.
- Weak match: "I am not sure, but it looks like you want: <action>".
- Unrecognised input: "Sorry, I don't think I can help with that". This happens when the model's top confidence is below 0.25 or the text's similarity to every training sentence is below 0.22 (values for the v2 model; `tune_thresholds.py`). The thresholds were chosen on dev rows and 16 English off-topic probes, never on the test split. With them, no dev row and all 16 probes are refused. If only the v1 model is present, the demo uses v1's own thresholds (0.16 and 0.28).
- "Why did it decide this?": the words whose removal lowers the model's confidence most, and the three most similar training sentences.
- "How good is it?" tab: v1 and v2 results read from the committed metric files.
- The demo never performs real actions.

## Presentation and demo video

- Presentation/demo video URL (REQUIRED): `<<FILL: unlisted YouTube or Drive "anyone with the link" URL>>`
- Optional hosted app URL: `<<FILL or delete>>`

## Required materials

- Contribution dataset and splits: [`data/contribution.csv`](data/contribution.csv)
- Annotation guide: [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md)
- Source log and source terms: the source columns of [`data/contribution.csv`](data/contribution.csv) (`source_dataset`, `source_version`, `source_method`, `contributor_code`, `reviewer_code`), [`DATA_PLAN.md`](DATA_PLAN.md) and [`SUBMISSION.md`](SUBMISSION.md)
- Dataset card: [`DATA_CARD.md`](DATA_CARD.md)
- Quality/review report: [`QUALITY.md`](QUALITY.md) and [`review_log.csv`](review_log.csv)
- Contribution and AI-use statement: [`CONTRIBUTIONS.md`](CONTRIBUTIONS.md)
- Evaluation outputs and baseline comparison: [`artifacts/v2/`](artifacts/v2/) (v2 and v1 on the fresh test) and [`artifacts/intent/`](artifacts/intent/) (v1 original test)
- Runnable code and dependency file: `validate.py`, `train.py`, `evaluate.py`, `core.py`, `models_v2.py`, `train_v2.py`, `compare.py`, `tune_thresholds.py`, `app_shona.py`, [`requirements.txt`](requirements.txt), [`requirements-labse.txt`](requirements-labse.txt)
- Trained artefacts or reproduction instructions: `artifacts/v2/B_tuned_tfidf.joblib` (in the repository), release `v1.0-final` (link above), or the commands above
- Video link: see above
- Submission manifest: [`SUBMISSION.md`](SUBMISSION.md)

## Attribution and permissions

Built on the **Strathmore NLP Hub datathon starter kit v2** (code licence in `LICENSE_CODE.txt`; the kit's README is kept as `STARTER_KIT_README.md`). Candidate C uses the pretrained `sentence-transformers/LaBSE` model through the `sentence-transformers` library; it is not part of the chosen v2 model. Our data is CC BY 4.0. No upstream datasets are used.

<!-- NATALIE: AI-use statement below still describes v1 only. Update it for the v2 work (see the notes Alvin has). -->
AI tools:
- Alvin led the code and demo work: he set up the repository, ran the validation, training and checks, made the demo changes and drafted the documentation. He used Claude Code (Anthropic) to help him understand what the task required and how to set up the starter-kit files, and to explain the parts he was less familiar with. Claude Code did not write the team's documentation; it was used to merge Natalie's drafts into the final repository files and add the final test results.
- The 595 rows in `data/contribution.csv` are written by the team (`source_method` `original_human`); none was written by AI or with AI help.
- A separate 360-row stress set was generated by Mukundi with ChatGPT (OpenAI) and then checked by him. It is synthetic data, so it was used only as an extra check on the trained model and the demo. It was never used for training or for the test score, and it is not part of `data/contribution.csv` or this repository.

Unresolved: whether an independent reviewer from outside the team (`FDK`) is acceptable has not been confirmed by the organisers.
