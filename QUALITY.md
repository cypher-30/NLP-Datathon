# Quality Assurance and Evaluation Report 

## 1. Dataset Quality and Validation

Team Ubuntu developed a Shona intent classification dataset containing **295 labeled sentences** across ten intent categories.

The dataset underwent automated validation using the competition's `validate.py` script to assess:

* Dataset structure and required CSV fields.
* Intent label consistency and 10-class taxonomy coverage.
* Training (195), development (50), and testing (50) split integrity.
* Duplicate detection, paraphrase grouping (`group_id`), and review metadata.

The dataset successfully passed all automated schema and integrity checks. This provided a consistent, error-free foundation for model training and evaluation.

## 2. Language Review and Annotation Quality

Language quality and orthographic correctness were prioritized throughout dataset development:

* **100% Independent Review:** All 295 records (including training, development, and frozen test splits) were independently evaluated and verified by a native Shona reviewer (reviewer code `FDK`).
* **Evaluation Scope:** The language review verified natural phrasing, correct Shona orthography, proper grammar, and unambiguous intent assignment.
* **No AI-written rows:** All 295 records are `original_human`. None of the 295 sentences was written by AI or with AI help.
* **Review Provenance:** Every row in `data/contribution.csv` is explicitly marked as `independently_reviewed` with `FDK` recorded as the verifying reviewer.

The annotation process adhered strictly to the guidelines defined in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md) to maintain clear label boundaries across overlapping categories.

## 3. Data Cleaning and Leakage Prevention

To prevent data leakage and ensure reliable evaluation results, the team conducted rigorous quality audits:

* **Lexical Overlap Reduction:** An initial cross-split similarity scan identified 12 training sentences with close lexical overlap to development or test sentences. These training sentences were reworded to introduce distinct syntactic phrasing and vocabulary.
* **Paraphrase Grouping Integrity:** Semantically equivalent variants and template variations were assigned matching `group_id` tags. Automated checks confirmed that no `group_id` spans across multiple splits. Some template-similar sentences remain across splits (12 pairs at 0.60 similarity or more); they are not copies, but they are considered when reading the results.

These measures reduce the chance that the development and test splits reward memorized paraphrases.

## 4. Model Development and Evaluation

The team implemented a lightweight, reproducible machine learning pipeline combining **character-level TF-IDF vectorization (2–5 n-grams)** with a **Logistic Regression** classifier. This approach was selected for its strong performance on low-resource, morphologically rich languages and fast CPU inference.

### Development Set Results

The model was evaluated on the 50-sentence development set (5 examples per intent class):

| Metric | Result | 
| ----- | ----- | 
| **Development Accuracy** | **92%** | 
| **Macro-F1 Score** | **0.919** | 
| **Correct Predictions** | **46 / 50** | 
| **Incorrect Predictions** | **4 / 50** | 

### Error Analysis

A detailed examination of the 4 misclassified development examples revealed two primary error patterns:

1. **`weather_query` vs. `datetime_query` Confusion:** Sentences containing the polysemous word *zuva* were occasionally misclassified when contextual cues were minimal (e.g., asking about "today's sun" vs. "today's date").
2. **`calendar_query` vs. `calendar_set` Boundary:** Complex phrasing involving retrieve-and-display requests (e.g., "Show me my appointment") occasionally triggered scheduling intent features.

These diagnostic insights directly informed targeted dataset refinements and rule clarifications in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md).

## 5. Defense Engineering and Fallback Logic

To test real-world robustness beyond static benchmarks, the team evaluated the pipeline against out-of-scope requests and a separate stress set of reworded requests (see below):

* **Confidence Thresholding:** The application (`app_shona.py`) enforces a probability threshold. Inputs with low classification confidence are flagged rather than assigned an arbitrary label.
* **Graceful Fallbacks:** Unrecognized or low-confidence requests output clear, plain-language guidance stating that the intent is unsupported, preventing deceptive system behavior.

### Stress Set (synthetic, not part of the dataset)

**Separate stress set (not part of this dataset).** Mukundi used ChatGPT to generate a separate set of 360 Shona sentences (300 supported requests and 60 that the demo should refuse), and then checked it himself. Because it is AI-generated, it is synthetic data. It was used only as an extra check on the trained model and the demo. It was never used for training or for the test score, and it is not included in `data/contribution.csv` or in this repository. On the first (250-row) model it gave about 74% top-label accuracy on supported requests, and 42 of the 60 should-be-refused requests were refused. Its main finding was that list and calendar questions with unfamiliar wording were often misread; Mukundi then wrote the 45 new training rows himself to cover these gaps.

## 6. Final Test Evaluation

The final test was run **once**, on **11 November 2026**, on the 50 frozen test sentences: accuracy **0.800**, macro-F1 **0.799**, against a majority baseline macro-F1 of 0.018.

| Metric | Model | Majority baseline |
| ----- | ----- | ----- |
| **Test Accuracy** | **0.800 (40 / 50)** | 0.10 |
| **Test Macro-F1** | **0.799** | 0.018 |

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

Test errors (10 of 50): SN-023 (`weather_query` read as `calendar_query`), SN-100 (`calendar_set` read as `calendar_query`), SN-121 (`calendar_query` read as `datetime_query`), SN-123 and SN-125 (`calendar_query` read as `calendar_set`), SN-149 (`lists_createoradd` read as `lists_query`), SN-172 (`lists_query` read as `lists_createoradd`), SN-200 (`play_music` read as `lists_query`), SN-248 (`qa_definition` read as `lists_createoradd`), SN-249 (`qa_definition` read as `datetime_query`). Five of the ten are between closely related labels (calendar set/query, list add/query). With five test sentences per label, one mistake moves a label's score by about 20 points.

## 7. Summary

Team Ubuntu has established a validated Shona intent classification dataset and implemented a working machine learning pipeline.

The project has achieved several key milestones:

- **295 labeled Shona sentences** across ten intent categories.
- **Successful dataset validation** using the organizers' script.
- **Documented language review** covering the full dataset.
- **Duplicate and cross-split similarity checks** to support data quality.
- **92% development accuracy and 0.919 macro-F1**, supported by error analysis.
- **Final test (run once): 0.800 accuracy and 0.799 macro-F1**, against a majority baseline of 0.018.
- **A ChatGPT-generated, Mukundi-checked stress set** used only as an extra check, kept out of training and testing.
- **Targeted dataset improvements** informed by model performance.

These results demonstrate meaningful progress toward developing a practical Shona-language intent classification system.