# Team Contributions and AI-Tool Disclosure 

## 1. Team Contributions

### 1.1 Alvin Murithi — Technical Development and Model Implementation

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

* Independently reviewing all 295 sentences (including the 50 test examples) to ensure 100% review coverage and support fair evaluation.

* Identifying linguistic issues requiring clarification or correction.

The dataset records FDK as the reviewer across all 295 records in `data/contribution.csv`.

## 2. AI-Tool Disclosure

None of the 295 sentences in `data/contribution.csv` was written by AI or with AI help.

### Claude Code — Anthropic

Claude Code was utilized to assist technical development and troubleshooting during project execution:

* **Code & Pipeline Assistance:** Assisting with refactoring Python scripts (`train.py`, `evaluate.py`), setting up Streamlit UI layout logic (`app_shona.py`), and generating utility scripts for `validate.py` compliance.

* **Human-in-the-Loop Oversight:** The team remained fully responsible for reviewing all generated outputs, directing architectural choices, verifying linguistic correctness, and validating all model results.

### ChatGPT — OpenAI

Mukundi used ChatGPT to generate a separate stress set of 360 Shona sentences (300 supported requests and 60 that should be refused). Mukundi checked these sentences. The stress set is synthetic data: it was used only as an extra check on the model and demo, never for training or for the test score, and it is not part of the dataset or this repository.
