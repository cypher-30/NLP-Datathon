# Data Collection and Preparation Plan 

## 1. Data Collection & Evolution

To solve the lack of training data for Shona intent classification, we built our own dataset from scratch. We first collected a baseline set of native Shona sentences covering all ten required datathon intent categories. 

After testing our initial model and reviewing errors, we added 45 more training sentences to improve how well the model handles list queries, calendar questions, and date/time expressions. This brought our final dataset to **295 sentences**. None of the 295 sentences was written by AI or with AI help.

A separate 360-sentence stress set was generated with ChatGPT and checked by Mukundi. It was used only to find weaknesses in the model and demo. It was not copied into the dataset, and it was not used for training or for the test score.

---

## 2. Annotation & Review Workflow

To keep the meanings clear and consistent, every sentence was given one main intent label following the rules in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md). 

To meet the datathon's quality and provenance rules, every sentence was independently reviewed by a second Shona speaker (`FDK`) to check for natural wording and correct labels. All review notes and checks are saved in [`QUALITY.md`](QUALITY.md).

---

## 3. Dataset Splitting

We split our 295 sentences into training, development, and test sets to keep a balanced mix across all categories:

| **Split** | **Sentences** | **Percentage** |
|---|---:|---:|
| Training | 195 | 66.1% |
| Development | 50 | 16.9% |
| Testing | 50 | 16.9% |
| **Total** | **295** | **100%** |

Every intent class has at least 15 training examples, plus exactly five development and five test examples. We use the training set to train the model, the dev set to test different settings, and the test set only for the final evaluation.

---

## 4. Cleaning & Preventing Data Leakage

Before running the model, we checked the data for missing fields, duplicate rows, and accidental overlaps between splits. 

To prevent data leakage where the model memorizes test answers because similar sentences appear in training we reworded 12 training sentences that were too close to the dev or test sets. We also grouped related sentences using `group_id` so that similar variations always stay in the same split. Full details are in [`QUALITY.md`](QUALITY.md).

---

## 5. Final Status

Our 295-sentence dataset successfully passed the organizers' validation script and was then frozen. The final test was run **once**, on **11 November 2026**, on the 50 frozen test sentences: accuracy **0.800**, macro-F1 **0.799**, against a majority baseline macro-F1 of 0.018. Full results are in [`QUALITY.md`](QUALITY.md).