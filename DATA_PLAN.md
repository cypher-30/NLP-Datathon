# Data Collection and Preparation Plan 

## 1. Data Collection & Evolution

To solve the lack of training data for Shona intent classification, we built our own dataset from scratch. We first collected a baseline set of native Shona sentences covering all ten required datathon intent categories. 

After testing our initial model and reviewing errors, we added 45 more training sentences to improve how well the model handles list queries, calendar questions, and date/time expressions. This brought the dataset to **295 sentences** (v4), which was used for our first model (v1). None of these sentences was written by AI or with AI help.

After v1's single test run on 11 Nov, we could no longer use its 50 test sentences to judge a new model fairly, because we had seen its results. On 12 Nov Mukundi wrote **300 more sentences** (SN-296 to SN-595), which FDK reviewed:

- **100 fresh test sentences**, 10 per intent, with new wording, names and places, some informal spelling and code-switching. They were checked for near-copies of every older sentence and committed before any model was trained on them.
- **200 training sentences**, 20 per intent, with list words other than *runyorwa* (for example *rondedzero*, *zvekuita*, *zvandichatenga*), calendar questions in different forms, and a few Karanga and Ndau words.

The final dataset (v5) has **595 sentences**. None of the 300 new sentences was written by AI or with AI help either.

A separate 360-sentence stress set was generated with ChatGPT and checked by Mukundi. It was used only to find weaknesses in the model and demo. It was not copied into the dataset, and it was not used for training or for the test score.

---

## 2. Annotation & Review Workflow

To keep the meanings clear and consistent, every sentence was given one main intent label following the rules in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md). 

To meet the datathon's quality and provenance rules, every sentence was independently reviewed by a second Shona speaker (`FDK`) to check for natural wording and correct labels. All review notes and checks are saved in [`QUALITY.md`](QUALITY.md).

---

## 3. Dataset Splitting

For v1, the 295 sentences were split 195 train / 50 dev / 50 test (5 dev and 5 test per intent, stratified 60/20/20 with seed 42).

For v2, the split is:

| **Split** | **Sentences** | **Percentage** | **What it holds** |
|---|---:|---:|---|
| Training | 445 | 74.8% | v1 train (195) + v1 test retired after its run (50) + new train (200) |
| Development | 50 | 8.4% | unchanged from v1 |
| Testing | 100 | 16.8% | the fresh test sentences, 10 per intent |
| **Total** | **595** | **100%** | |

Every intent has at least 40 training examples, five development and ten test examples. We use the training set to train, the training set (cross-validation) and the dev set to choose settings and models, and the test set only once, for the final evaluation.

---

## 4. Cleaning & Preventing Data Leakage

Before running the model, we checked the data for missing fields, duplicate rows, and accidental overlaps between splits. 

To prevent data leakage where the model memorizes test answers because similar sentences appear in training we reworded 12 training sentences that were too close to the dev or test sets. We also grouped related sentences using `group_id` so that similar variations always stay in the same split. Full details are in [`QUALITY.md`](QUALITY.md).

---

## 5. Final Status

Both versions pass the organisers' validation script.

- **v1:** the 295-sentence dataset was frozen and its test run **once**, on **11 November 2026**: accuracy **0.800**, macro-F1 **0.799**, against a majority baseline macro-F1 of 0.018.
- **v2:** the 595-sentence dataset was frozen (git tag `fresh-test-frozen`) before any model was trained on it, the model was chosen on train and dev only, and the fresh test was run **once**, on **12 November 2026**: accuracy **0.920**, macro-F1 **0.919**, against 0.681 for the v1 model on the same sentences and 0.018 for the majority baseline.

Full results are in [`QUALITY.md`](QUALITY.md).