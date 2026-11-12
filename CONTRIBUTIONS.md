# Team Contributions and AI-Tool Disclosure 

## 1. Team Contributions

### 1.1 Alvin Murithi — Technical Development and Model Implementation

<!-- NATALIE: check these bullets match the AI-use statement in section 2 for the v2 code. -->

Alvin led the technical development and implementation of the Shona intent classification system.

His contributions included:

* Setting up the development environment and adapting the datathon starter kit for the Shona dataset.

* Preparing and maintaining the dataset's CSV structure, metadata fields, and validation workflow.

* Implementing and training the intent classification model using TF-IDF character n-grams and logistic regression.

* Evaluating model performance, analyzing classification errors, and identifying areas requiring additional training examples.

* Conducting duplicate detection, cross-split similarity checks, and robustness testing.

* Developing the Streamlit demonstration application (`app_shona.py`), including intent predictions and unsupported-request handling.

### 1.2 Mukundi Witness Chingwena — Shona Language Lead and Dataset Development

Mukundi led the dataset's linguistic development, ensuring the examples represented the intended meanings of the ten Shona intent categories.

His contributions included:

* Writing and labeling the initial 250 Shona sentences across the ten intent categories.

* Developing 45 additional training examples to improve coverage of list, calendar, and date/time requests.

* Writing 300 more sentences on 12 Nov 2026 (SN-296 to SN-595): a fresh 100-sentence test set and 200 training sentences, with new wording, informal spelling, code-switching and some Karanga and Ndau words, and revising them after FDK's review.

* Establishing consistent Shona wording, spelling, and sentence structure throughout the dataset.

* Reviewing sentence meanings and their corresponding intent labels to improve linguistic accuracy.

* Generating the separate 360-sentence stress set with ChatGPT and checking its Shona sentences and labels (see section 2).

* Coordinating with the independent Shona reviewer to support language quality assurance.

### 1.3 Natalie Chelagat — Documentation, Provenance, and Quality Assurance

Natalie led the project's documentation and supported quality assurance to ensure that the submission met all datathon requirements.

Her contributions included:

* Preparing the dataset statement, data collection plan, provenance documentation, and ethical considerations.

* Documenting the annotation process, language review procedures, and dataset preparation.

* Preparing the quality assurance and model evaluation write-ups using the team's technical findings.

* Maintaining records of team contributions, AI-tool usage, and project responsibilities.

* Reviewing documentation for accuracy, consistency, completeness, and alignment with submission guidelines.

### 1.4 Independent Shona Reviewer — FDK

FDK supported the project's linguistic quality assurance as an independent reviewer who was not an author of the dataset sentences.

The review responsibilities included:

* Checking Shona sentences for grammatical correctness, spelling, and naturalness.

* Assessing whether sentence meanings were clear and appropriate for their assigned intent categories.

* Independently reviewing all 595 sentences (including both test sets) to ensure 100% review coverage and support fair evaluation.

* Reviewing the 300 sentences added on 12 Nov in three rounds and recording every change (79 sentences changed) in `review_log.csv`, including rewording test sentences that were too close to existing ones.

* Identifying linguistic issues requiring clarification or correction.

The dataset records FDK as the reviewer across all 595 records in `data/contribution.csv`.

## 2. AI-Tool Disclosure

<!-- NATALIE: this section describes v1 only; update for the v2 work (see the notes Alvin has). -->

None of the 295 sentences in `data/contribution.csv` was written by AI or with AI help.

### Claude Code — Anthropic

Alvin led the code and demo work: he set up the repository, ran the validation, training and checks, and made the demo changes. He used Claude Code (Anthropic) to help him understand what the task required and how to set up the starter-kit files, and to explain the parts he was less familiar with, such as how the kit's `train.py` and `evaluate.py` work. The kit's `validate.py`, `train.py`, `evaluate.py` and `core.py` are used as provided, except for one added line in `train.py` (see `README.md`). Claude Code did not write any of the 295 dataset sentences or their labels.

### ChatGPT — OpenAI

Mukundi used ChatGPT to generate a separate stress set of 360 Shona sentences (300 supported requests and 60 that should be refused). Mukundi checked these sentences. The stress set is synthetic data: it was used only as an extra check on the model and demo, never for training or for the test score, and it is not part of the dataset or this repository.
