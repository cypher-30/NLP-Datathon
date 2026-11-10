

# Data Collection and Preparation Plan


## Data Collection


The dataset was developed by creating Shona sentences corresponding to the ten intent categories defined in the datathon guidelines.


The initial collection contained 250 sentences, prepared on 8 November 2026.


Following model development and error analysis, **45 additional training sentences** were added on 9–10 November to improve coverage of list queries, calendar questions, and date/time expressions.


The final dataset contains **295 sentences**. The contributor is confirming whether any sentence creation or variation involved AI assistance.


## Annotation and Review Workflow


Each sentence was assigned one primary intent label based on its meaning.


The annotation process followed the decision rules documented in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md), particularly for categories with overlapping meanings.


An independent Shona speaker, identified as `FDK`, reviewed the examples for linguistic correctness and label suitability.


Review evidence and outstanding verification requirements are documented in [`QUALITY.md`](QUALITY.md).


## Dataset Splitting


We divided the original 250 examples into 150 training, 50 development, and 50 testing sentences.


We assigned the 45 additional sentences to the training set.


| **Split** | **Sentences** | **Percentage** |
|---|---:|---:|
| Training | 195 | 66.1% |
| Development | 50 | 16.9% |
| Testing | 50 | 16.9% |
| **Total** | **295** | **100%** |


Each intent contains at least 15 training examples and exactly five development and five test examples.


The training set fits the model, the development set supports model improvement, and the test set is reserved for final evaluation.


## Cleaning and Preparation


We checked the dataset for missing fields, unsupported labels, duplicate sentences, and similarities between splits.


We reworded twelve training sentences that closely resembled development or test examples.


Related examples were assigned `group_id` values to prevent the same group from appearing across different splits.


The remaining similarity findings and validation results are recorded in [`QUALITY.md`](QUALITY.md).


## Final Dataset Status


The 295-sentence working dataset passed the organizers' validation script on **10 November 2026**.


The final test evaluation and outstanding provenance confirmations must be completed before submission.




