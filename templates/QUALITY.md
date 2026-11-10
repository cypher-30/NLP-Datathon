
# Quality Assurance and Evaluation Report

## 1. Dataset Quality and Validation

Team Ubuntu developed a Shona intent classification dataset containing **295 labeled sentences** across ten intent categories.

The dataset underwent validation using the organizers' `validate.py` script to assess:

- Dataset structure and required fields.
- Intent label consistency and category coverage.
- Training, development, and testing split integrity.
- Duplicate detection and review metadata.

**The dataset successfully passed validation on 10 November 2026.**

This provided a consistent foundation for model training and evaluation.

## 2. Language Review and Annotation Quality

Language quality was an important consideration throughout dataset development.

The dataset records an independent Shona reviewer (`FDK`) for all 295 sentences, including the 50 test examples.

The review focused on:

- Grammatical correctness and natural Shona expressions.
- Clarity of sentence meaning.
- Consistency between sentences and their assigned intent labels.

All records are marked `independently_reviewed`. Supporting reviewer evidence and external-reviewer eligibility are being finalized.

The team also followed documented annotation guidelines to maintain consistency across similar intent categories.

## 3. Data Cleaning and Leakage Prevention

To improve dataset quality, the team performed duplicate detection and cross-split similarity checks.

The analysis identified 12 training sentences with strong similarities to development or test examples. These were reworded to introduce greater linguistic variation and reduce potential overlap.

The final dataset also passed group-level separation checks, with no `group_id` appearing across multiple splits.

Some sentence-template similarities remain and are considered when interpreting evaluation results.

These checks helped strengthen the reliability of the dataset preparation process.

## 4. Model Development and Evaluation

The project uses a lightweight supervised machine learning approach combining **character-level TF-IDF features (2–5 n-grams)** with **logistic regression**.

This approach was selected because it is computationally efficient and suitable for a relatively small labeled dataset.

### Development Set Results

The model was evaluated on 50 development examples.

| Metric | Result |
|---|---:|
| Development accuracy | **92%** |
| Macro-F1 score | **0.919** |
| Correct predictions | **46/50** |
| Incorrect predictions | 4 |

The results demonstrate that the model can distinguish between the ten supported Shona intent categories on the development set.

### Error Analysis

The team examined incorrect predictions to identify areas requiring improvement.

The main challenges involved distinguishing:

- Weather-related requests from date and time questions.
- Calendar information queries from calendar event creation.

These findings informed targeted dataset improvements, including the addition of 45 training examples to strengthen selected categories.

This iterative process helped the team make improvements based on observed model behavior rather than relying solely on overall accuracy.

## 5. Robustness and Generalization

Beyond the standard development evaluation, the team conducted supplementary tests using alternative sentence formulations and unsupported requests.

These checks helped identify weaknesses in handling unfamiliar expressions and guided improvements to the training data and demonstration application.

The supplementary examples were kept separate from the official dataset and evaluation splits.

Although the development results are encouraging, further testing is necessary to assess performance on a wider range of Shona expressions.

## 6. Final Test Evaluation

The project includes a reserved test set of **50 independently reviewed examples**, covering all ten intent categories.

As of 10 November 2026, the final test evaluation was pending. It will be conducted using the finalized model and frozen test set.

| Metric | Result |
|---|---|
| Test accuracy | Pending final evaluation |
| Test macro-F1 | Pending final evaluation |
| Per-intent performance | Pending final evaluation |

The final results will provide an additional assessment of the model's ability to classify previously unseen Shona requests.

## 7. Summary

Team Ubuntu has established a validated Shona intent classification dataset and implemented a working machine learning pipeline.

The project has achieved several key milestones:

- **295 labeled Shona sentences** across ten intent categories.
- **Successful dataset validation** using the organizers' script.
- **Documented language review** covering the full dataset.
- **Duplicate and cross-split similarity checks** to support data quality.
- **92% development accuracy and 0.919 macro-F1**, supported by error analysis.
- **Targeted dataset improvements** informed by model performance.

These results demonstrate meaningful progress toward developing a practical Shona-language intent classification system.

The next step is to complete the frozen test evaluation and finalize the supporting review and provenance evidence.
