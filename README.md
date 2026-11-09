# Team Ubuntu: Shona intent classification

Strathmore NLP Hub Datathon 2026, Team 3 "Ubuntu". Track A (intent), language Shona (`sn`).

A small text classifier that reads a Shona request (for example a question about the weather, or a request to set an alarm) and says which of 10 actions the person wants. A Streamlit demo shows the result in plain language and says "not supported" for requests it does not recognise.

Team: Alvin Murithi (code and demo), Mukundi Witness Chingwena (Shona data and language review), Natalie Chelagat (documentation).

## Credit and what we changed
This repository is built on the **Strathmore NLP Hub datathon starter kit v2**. The validation, training and evaluation scripts and `core.py` are the kit's, used as provided. The kit's own README is kept as `STARTER_KIT_README.md`. Our changes are:

| File | Change |
|---|---|
| `data/contribution.csv` | Our Shona dataset (see "Data"). |
| `train.py` | One addition: the pack also saves `train_matrix` (the training sentences as TF-IDF vectors), so the demo can tell when input looks unlike the training data. Training itself is unchanged. |
| `app_shona.py` | New demo, adapted from the kit's `app.py`. Intent track only. Reports "not supported" instead of forcing a label, shows plain-language results and the top 3 guesses instead of raw probabilities. |
| `prepare_working.py` | Helper that can regenerate the `split` column (stratified 60/20/20 per label, seed 42). The current `data/contribution.csv` already contains its split. |

AI tools: Claude (Anthropic) was used through Claude Code to help with explanations, the demo app and this README. Any AI involvement in the dataset is declared by the team in the documentation, not here. See `source_method` and the data statement.

## Reproduce the results
Python 3.13.5 was used (3.10 or later should work). Tested library versions: scikit-learn 1.7.2, pandas 2.3.3, streamlit 1.67.0, joblib 1.6.0. Run everything from this folder.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt

python validate.py --track intent --data data/contribution.csv
python train.py    --track intent --data data/contribution.csv
python evaluate.py --track intent --data data/contribution.csv
python -m streamlit run app_shona.py
```

What each step does:
1. `validate.py` checks the CSV against the datathon rules (schema, no duplicates, one language, every label in every split, no personal data, row minimums, valid `source_method`, independent review of every test row).
2. `train.py` fits a character TF-IDF (2 to 5 grams) plus logistic regression model on the **train** rows only (`random_state=42`), and a majority-class baseline. It scores on the **dev** rows and saves `artifacts/intent/model.joblib` and `dev_metrics.json`.
3. `evaluate.py` scores the **test** rows once and writes `test_metrics.json`, `per_label_report.csv` and `test_predictions.csv`. It refuses to run if the dataset changed since training (SHA-256 fingerprint), so any CSV edit needs a retrain first.
4. `streamlit run` starts the demo from the saved model.

The split is stored in the CSV, and the model has a fixed seed, so the same data gives the same model and scores.

Practice run (English teaching data, not our result): add `--practice` and use `data/practice_intent.csv`. It saves to the same `artifacts/intent/` folder, so retrain on `data/contribution.csv` afterwards.

## Data
`data/contribution.csv`: 295 Shona sentences, 10 intent labels, split 195 train / 50 dev / 50 test (dev and test are 5 per label; train is 15 to 27 per label; 45 train-only rows were added for list, calendar and date/time phrasing, and 12 train rows that closely matched dev or test rows were reworded by the author and re-reviewed). Labels are defined in `taxonomy.csv`.

- Sentences were written by the contributor (`contributor_code` MUK, `source_method` `original_human`).
- Every row was reviewed by a second Shona speaker (`reviewer_code` FDK, `review_status` `independently_reviewed`). The reviewer differs from the author on every row.
- No external datasets are included in these 295 rows. Optional outside Shona resources, if we use any, would be kept in a separate file and would not count towards the row minimum.
- Permission evidence and contributor details are kept out of this repository.

## Demo behaviour
- Confident match: "It looks like you want: <action>", plus what the assistant would do and two other possibilities.
- Weak match: "I am not sure, but it looks like you want: <action>".
- Unrecognised input: "Sorry, I don't think I can help with that". This happens when the model's top confidence is below 0.16 or the text's similarity to every training sentence is below 0.28. The thresholds were chosen on dev rows and off-topic probes, never on the test split.
- The demo never performs real actions.

## Results
Final test results are added here only after the single `evaluate.py` run on the frozen dataset.

- Dev (working figure, may change while the data is being fixed): accuracy 0.92, macro-F1 0.919 against a majority baseline of 0.018.
- Test: *to be filled in after the final evaluation.*
- Error analysis (up to five real errors from `test_predictions.csv`): *to be filled in by the documentation lead.*

## Limitations
- Small data: 295 sentences, 5 test sentences per label, so scores move a lot with one sentence.
- Closely related labels, especially `calendar_set` and `calendar_query`, are confused because they share vocabulary.
- One writer and one reviewer, so the data reflects one variety of Shona and one spelling style.
- The model matches letter patterns, not meaning. It cannot understand words it has never seen.
- Probabilities are uncalibrated and should not be read as percentages of certainty.

## Model file
`*.joblib` is gitignored. Anyone who clones the repo rebuilds the model with the commands above. How the trained model is handed to the judges is to be confirmed with the organisers. Only load `.joblib` files you created yourself.

## Licence
Kit code: see `LICENSE_CODE.txt`. Data licence: to be stated by the team before publishing.
