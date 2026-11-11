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
* **Review Provenance:** Every row in `data/contribution.csv` is explicitly marked as `independently_reviewed` with `FDK` recorded as the verifying reviewer.

The annotation process adhered strictly to the guidelines defined in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md) to maintain clear label boundaries across overlapping categories.

## 3. Data Cleaning and Leakage Prevention

To prevent data leakage and ensure reliable evaluation results, the team conducted rigorous quality audits:

* **Lexical Overlap Reduction:** An initial cross-split similarity scan identified 12 training sentences with close lexical overlap to development or test sentences. These training sentences were reworded to introduce distinct syntactic phrasing and vocabulary.
* **Paraphrase Grouping Integrity:** Semantically equivalent variants and template variations were assigned matching `group_id` tags. Automated checks confirmed that no `group_id` spans across multiple splits, completely eliminating split contamination.

These measures guarantee that the development and test splits evaluate true generalization rather than memorized paraphrases.

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

To test real-world robustness beyond static benchmarks, the team evaluated the pipeline against out-of-scope inputs, non-Shona sentences, and noisy user text:

* **Confidence Thresholding:** The application (`app_shona.py`) enforces a probability threshold. Inputs with low classification confidence are flagged rather than assigned an arbitrary label.
* **Graceful Fallbacks:** Unrecognized or low-confidence requests output clear, plain-language guidance stating that the intent is unsupported, preventing deceptive system behavior.

## 6. Summary

Team Ubuntu has established a validated Shona intent classification dataset and implemented a working machine learning pipeline.

The project has achieved several key milestones:

- **295 labeled Shona sentences** across ten intent categories.
- **Successful dataset validation** using the organizers' script.
- **Documented language review** covering the full dataset.
- **Duplicate and cross-split similarity checks** to support data quality.
- **92% development accuracy and 0.919 macro-F1**, supported by error analysis.
- **Targeted dataset improvements** informed by model performance.

These results demonstrate meaningful progress toward developing a practical Shona-language intent classification system.