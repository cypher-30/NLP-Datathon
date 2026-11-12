# Quality Assurance and Evaluation Report

## 1. Dataset Quality and Validation

Team Ubuntu developed a Shona intent classification dataset containing **595 labelled sentences** across ten intent categories. It grew in three stages: 250 sentences (SN-001 to SN-250), 45 training sentences added on 9–10 Nov (SN-251 to SN-295), and 300 sentences added on 12 Nov (SN-296 to SN-595: a fresh 100-sentence test set and 200 training sentences).

The dataset was checked with the competition's `validate.py` script (non-practice mode), which covers:

* Dataset structure and required CSV fields.
* Intent label consistency and 10-class taxonomy coverage.
* Training (445), development (50) and test (100) split integrity: every label in every split, and no `group_id` across two splits.
* Duplicate detection (record IDs and normalised text) and review metadata (every test row reviewed by someone other than its author).

The current file passes all of these checks. `validate.py` does not check language quality, which is covered by the human review below.

## 2. Language Review and Annotation Quality

* **100% Independent Review:** All 595 records (training, development and test) were reviewed by a Shona speaker who did not write them (reviewer code `FDK`). Mukundi (`MUK`) wrote every sentence.
* **Evaluation Scope:** The review checked natural phrasing, Shona spelling, grammar, and whether the sentence clearly expresses one intent.
<!-- NATALIE: the next bullet is a data AI-use statement. Mukundi must confirm whether the 300 rows added on 12 Nov (SN-296 to SN-595) were written without AI before it is changed from 295 to 595. -->
* **No AI-written rows:** All 295 records are `original_human`. None of the 295 sentences was written by AI or with AI help.
* **Review Provenance:** Every row in `data/contribution.csv` is marked `independently_reviewed` with `FDK` as the reviewer.

### Review log: the 300 sentences added on 12 Nov (SN-296 to SN-595)

FDK reviewed the new sentences in three rounds. Every change is recorded in [`review_log.csv`](review_log.csv) with the record ID, split, label, the text before and after, and the reason.

| Outcome | Test rows (100) | Train rows (200) | Total (300) |
|---|---:|---:|---:|
| Kept unchanged | 71 | 150 | 221 |
| Changed | 29 | 50 | 79 |
| Rejected | 0 | 0 | 0 |

Four rows were changed twice (SN-354, SN-364, SN-549, SN-554; the in-between wording was not recorded) and SN-376 was changed in Round 1 and again in Round 3. No label was changed.

The reasons for the changes:

| Round | What FDK looked for |
|---|---|
| 1 | A sentence too close to an existing row, or to a row in the other split (for example SN-305 was too close to old SN-006, and SN-436 to old SN-052). |
| 2 | The same sentence pattern with only a name or place changed, too many uses of *nyamusi* (today), and adding Karanga and Ndau words (for example SN-390 and SN-590 use Karanga words, SN-455 and SN-466 Ndau words). |
| 3 | A final check for repeated sentence patterns. Most of the sentences changed in this round had started with the same few patterns, such as "Isa alarm…", "Ridza nziyo…" or "Ndiudze nhau…". |

Examples (the "after" text is the sentence now in `data/contribution.csv`):

| Record | Split | Label | Before review | After review |
|---|---|---|---|---|
| SN-392 | test | qa_definition | Shoko rekuti 'mukwerera' rinorevei? | Mukwerera unorevei? |
| SN-309 | test | datetime_query | Nyamusi i date ringani? | date yanhasi ndeyei |
| SN-357 | test | lists_query | Dovi rakaiswa here pa shopping list? | Dovi rakaiswa here mune zvekutenga? |
| SN-455 | train | alarm_set | Ndavata, ndimutse kana yasvika 11 manheru. | Ndoda kuqambaya zvishoma, ndimutse na11 manheru. |
| SN-550 | train | play_music | ridza nziyo dzaSniper Storm | sniper storm plz, chero rwiyo |

### Review log: the first batch

For the 75 first-batch sentences in `alarm_set`, `calendar_query` and `datetime_query` (25 each), FDK's review record shows:

| Outcome | Sentences |
|---|---|
| Kept unchanged | 63 |
| Changed | 12 |
| Rejected | 0 |

Examples of FDK's changes (the "after" text is the sentence now in `data/contribution.csv`):

| Record | Label | Before review | After review |
|---|---|---|---|
| SN-052 | alarm_set | Isa alarm na5:30 mangwanani. | Isa alarm ya5:30 mangwanani. |
| SN-058 | alarm_set | Ndikaisire alarm na8 manheru ano. | Ndikaisire alarm ye8 manheru ano. |
| SN-069 | alarm_set | Ndimutse na7 mangwanani eSvondo yega yega. | Ndimutse na7 mangwanani eSvondo ega ega. |
| SN-106 | calendar_query | Tarisa kana ndine chidzidzo masikati ano. | Tarisa kana ndine clasi masikati ano. |
| SN-039 | datetime_query | Inguvai muBulawayo pari zvino? | Inguvai muBulawayo izvezvi? |

The changes were mainly word choice, phrasing and grammatical agreement; no label changed. The review records for the other seven labels of the first batch and for the 45 rows added on 9–10 Nov are not included here, so for those rows the evidence is the `reviewer_code` and `review_status` columns only.

The annotation followed the rules in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md) for overlapping categories.

## 3. Data Cleaning and Leakage Prevention

* **Lexical overlap reduction (v1):** a cross-split similarity scan found 12 training sentences very close to development or test sentences. Their author reworded them and they were reviewed again. Some template-similar sentences remained across splits (12 pairs at 0.60 similarity or more); they are not copies, but they are considered when reading the v1 results.
* **Fresh test set (v2):** because the v1 test results had already been seen, the 50 v1 test sentences were not reused as a test. They were moved into training, and a new 100-sentence test set was written. Before any model was trained on the new data, each fresh test sentence was compared with every older sentence and every new training sentence (character 2–5-gram TF-IDF cosine similarity). The highest match was 0.76 (SN-356 vs SN-261, both `lists_query`); none reached our 0.8 threshold, and no two test sentences were near-copies of each other. FDK's Round 1 had already reworded test sentences that were too close to existing ones. The data was then committed (tag `fresh-test-frozen`) before any v2 model was trained.
* **Dev check:** no dev sentence is within 0.8 similarity of any training sentence (highest 0.70, between two older rows).
* **Paraphrase grouping:** related variants share a `group_id`, and `validate.py` confirms that no `group_id` spans two splits.
* **Not checked:** the 360-sentence ChatGPT stress set was not part of the v2 near-duplicate check, because those files are no longer available.

## 4. Model Development and Evaluation

### v1 model

The kit's pipeline: **character-level TF-IDF (2–5 grams)** with **logistic regression**, trained on the training split only. It was chosen because it is the kit's baseline, works on small data and runs quickly on a CPU.

Development results (v4 data, 50 sentences, 5 per intent):

| Metric | Result |
|---|---|
| Development accuracy | 92% (46 / 50) |
| Macro-F1 | 0.919 |

The 4 development errors:

| Record | Sentence | True | Predicted |
|---|---|---|---|
| SN-020 | Kuchange kune madhigirii mangani muBulawayo nhasi? | weather_query | datetime_query |
| SN-094 | Ronga kufonerana nevhidhiyo nehanzvadzi yangu mangwana na7 manheru. | calendar_set | calendar_query |
| SN-116 | Chiitiko chekutanga pakarenda yangu mangwana ndechipi? | calendar_query | calendar_set |
| SN-117 | Tarisa nguva yemharidzo yangu neChina chinouya. | calendar_query | calendar_set |

Two patterns: SN-020 asks about temperature (*madhigirii*) together with a time word (*nhasi*), and the model follows the time word; three of the four are calendar set vs query, the same weak pair as on the test.

### v2 model choice (train and dev only)

Three candidates were trained on the v5 training split (445 sentences). Settings were chosen by stratified 5-fold cross-validation on train, and each was then scored on dev. The selection rule was written into `train_v2.py` before training: highest mean of CV macro-F1 and dev macro-F1, and LaBSE must lead by at least 0.02 because it is much heavier to run.

| Candidate | CV macro-F1 | Dev macro-F1 |
|---|---:|---:|
| A: kit model (char TF-IDF 2–5 + logistic regression) | 0.847 | 0.918 |
| **B: tuned TF-IDF** (word 1-grams + char_wb 2–5-grams, logistic regression C=3) | 0.884 | 1.000 |
| C: LaBSE sentence embeddings + logistic regression (C=30) | 0.916 | 0.917 |

B was chosen. Its perfect dev score is on only 50 sentences and is optimistic. All candidates and settings tried are in `artifacts/v2/selection.json`. The same candidates were also trained on the v4 data (`artifacts/v2_ablation_v4data/`) to separate the effect of the new data from the effect of the model.

## 5. Handling Unsupported Input

* **Thresholds:** `app_shona.py` refuses a request when the model's top confidence is below 0.25, or when the request's similarity to every training sentence is below 0.22. These values were chosen with `tune_thresholds.py` on the 50 dev sentences and 16 English off-topic requests: every dev sentence scored at least 0.316 confidence and every off-topic request at most 0.231, so no dev sentence and all 16 off-topic requests are refused. The test split was not used.
* **Plain-language fallback:** refused requests get "Sorry, I don't think I can help with that" instead of a forced label.
* **Known gap:** there is no "not supported" class, so Shona requests for unsupported actions on supported topics (for example cancelling an alarm) can still be accepted.

### Stress Set (synthetic, not part of the dataset)

Mukundi used ChatGPT to generate a separate set of 360 Shona sentences (300 supported requests and 60 that the demo should refuse), and then checked it himself. Because it is AI-generated, it is synthetic data. It was used only as an extra check on the trained model and the demo. It was never used for training or for the test score, and it is not included in `data/contribution.csv` or in this repository. On the first (250-row) model it gave about 74% top-label accuracy on supported requests, and 42 of the 60 should-be-refused requests were refused. Its main finding was that list and calendar questions with unfamiliar wording were often misread; Mukundi then wrote the 45 new training rows himself to cover these gaps.

## 6. Test Results

### v1: original test, run once on 11 November 2026

50 frozen test sentences: accuracy **0.800**, macro-F1 **0.799**, against a majority baseline macro-F1 of 0.018.

| Intent | Test F1 |
| ----- | ----- |
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

Confusion matrix (rows = true label, columns = predicted):

| True \ Predicted | weather | datetime | alarm | cal_set | cal_query | list_add | list_query | music | news | definition |
|---|---|---|---|---|---|---|---|---|---|---|
| **weather** | **4** | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| **datetime** | 0 | **5** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **alarm** | 0 | 0 | **5** | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **cal_set** | 0 | 0 | 0 | **4** | 1 | 0 | 0 | 0 | 0 | 0 |
| **cal_query** | 0 | 1 | 0 | 2 | **2** | 0 | 0 | 0 | 0 | 0 |
| **list_add** | 0 | 0 | 0 | 0 | 0 | **4** | 1 | 0 | 0 | 0 |
| **list_query** | 0 | 0 | 0 | 0 | 0 | 1 | **4** | 0 | 0 | 0 |
| **music** | 0 | 0 | 0 | 0 | 0 | 0 | 1 | **4** | 0 | 0 |
| **news** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **5** | 0 |
| **definition** | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | **3** |

Test errors (10 of 50): SN-023 (`weather_query` read as `calendar_query`), SN-100 (`calendar_set` read as `calendar_query`), SN-121 (`calendar_query` read as `datetime_query`), SN-123 and SN-125 (`calendar_query` read as `calendar_set`), SN-149 (`lists_createoradd` read as `lists_query`), SN-172 (`lists_query` read as `lists_createoradd`), SN-200 (`play_music` read as `lists_query`), SN-248 (`qa_definition` read as `lists_createoradd`), SN-249 (`qa_definition` read as `datetime_query`). With five test sentences per label, one mistake moves a label's score by about 20 points.

### v2: fresh test, run once on 12 November 2026

`compare.py` scored every model once on the 100 fresh test sentences (10 per label). It refuses to run twice (`artifacts/v2/test_run.lock`), and it checks that each model file matches the hash recorded when the model was chosen.

| Model | Trained on | Accuracy | Macro-F1 | 95% CI |
|---|---|---:|---:|---|
| **B tuned TF-IDF (v2)** | v5 | **0.920** | **0.919** | 0.853–0.967 |
| A kit model | v5 | 0.890 | 0.890 | 0.820–0.943 |
| C LaBSE | v5 | 0.860 | 0.857 | 0.772–0.919 |
| v1 model (unchanged) | v4 | 0.680 | 0.681 | 0.574–0.759 |
| B tuned TF-IDF | v4 | 0.760 | 0.772 | 0.675–0.844 |
| C LaBSE | v4 | 0.820 | 0.818 | 0.728–0.888 |
| Majority baseline | v5 | 0.100 | 0.018 | |

* Most of the improvement comes from the new data: the same kit model rises from 0.681 to 0.890 macro-F1 when trained on v5. The tuned model adds about 0.03 more, within the uncertainty.
* v1 scores 0.68 here against 0.80 on its own test, because the fresh sentences use new wording, names and some code-switching.
* v2's 8 errors: SN-305, SN-307, SN-313, SN-331, SN-346, SN-350, SN-355, SN-369. Three are list add read as list query (its weakest label, F1 0.78), two are mostly-English or English-mixed requests. The README explains five of them.
* All test sentences were written by one person (`MUK`), so the result does not show how the model handles other writers.

## 7. Summary

- **595 labelled Shona sentences** across ten intents, all reviewed by an independent Shona speaker, with a per-row change log for the newest 300.
- **Passes the organisers' validation script.**
- **Leakage checks:** cross-split similarity scans for v1, and for v2 a fresh test checked for near-copies and frozen before any model saw it.
- **v1 (kit model, 295 sentences):** 0.800 accuracy and 0.799 macro-F1 on its test, run once.
- **v2 (tuned TF-IDF, 595 sentences):** 0.920 accuracy and 0.919 macro-F1 on 100 unseen sentences, run once, against 0.681 for v1 on the same sentences and 0.018 for the majority baseline.
- **A ChatGPT-generated, Mukundi-checked stress set** used only as an extra check on v1, kept out of training and testing.
- **Main remaining weaknesses:** list add vs list query, mostly-English requests, unseen words, and a single writer.
