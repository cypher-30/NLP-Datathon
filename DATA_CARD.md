# Dataset Card — Shona Intent Classification

## Dataset Overview

Team Ubuntu (Team 3) developed a Shona-language dataset for **Track A — Intent Classification** at the Strathmore NLP Hub Datathon 2026.

The dataset contains **295 Shona sentences** labeled across ten predefined intent categories. It supports developing a supervised machine learning model that identifies the intended action behind a user's written request.

- **Dataset file:** `data/contribution.csv`
- **Language:** Shona (`sn`)
- **Version:** v4, 10 November 2026 (frozen; final test run on 11 November 2026)
- **Licence:** CC BY 4.0

## Dataset Composition

| Intent | Description | Train | Dev | Test | Records |
|---|---|---:|---:|---:|---:|
| `weather_query` | Weather requests | 15 | 5 | 5 | 25 |
| `datetime_query` | Date and time questions | 23 | 5 | 5 | 33 |
| `alarm_set` | Setting an alarm to ring | 15 | 5 | 5 | 25 |
| `calendar_set` | Scheduling events | 20 | 5 | 5 | 30 |
| `calendar_query` | Retrieving calendar events | 27 | 5 | 5 | 37 |
| `lists_createoradd` | Creating or updating lists | 25 | 5 | 5 | 35 |
| `lists_query` | Retrieving list information | 25 | 5 | 5 | 35 |
| `play_music` | Music playback | 15 | 5 | 5 | 25 |
| `news_query` | News requests | 15 | 5 | 5 | 25 |
| `qa_definition` | Definitions and explanations | 15 | 5 | 5 | 25 |
| **Total** | | **195** | **50** | **50** | **295** |

Each record contains a sentence, its intent label, and metadata describing its origin, contributor, reviewer, and dataset split.

## Data Origin and Provenance

The Shona examples were written by Mukundi Witness Chingwena (contributor code `MUK`). Every record was reviewed by a second Shona speaker, an independent reviewer identified by code `FDK`. The licence field's "two shona speakers" refers to these two people: the writer and the reviewer.

All 295 records have the source method `original_human`. **None of the 295 sentences was written by AI or with AI help.**

No external datasets are included in the counted contribution.

**Separate stress set (not part of this dataset).** Mukundi used ChatGPT to generate a separate set of 360 Shona sentences (300 supported requests and 60 that the demo should refuse), and then checked it himself. Because it is AI-generated, it is synthetic data. It was used only as an extra check on the trained model and the demo. It was never used for training or for the test score, and it is not included in `data/contribution.csv` or in this repository.

The collection, expansion, and splitting procedures are described in [`DATA_PLAN.md`](DATA_PLAN.md). Annotation rules are documented in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md).

## Data Rights and Ethics

The dataset is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence. Anyone may reuse it with credit to Team Ubuntu, Strathmore NLP Hub Datathon 2026.

The contributor authorized the use of the sentences for Team Ubuntu's datathon work. Supporting permission and review evidence is kept privately and is not part of this repository.

The examples are everyday assistant requests written for this project. They contain no names of real private individuals, emails or phone numbers; `validate.py` checks for emails and phone numbers.

## Limitations

The dataset is relatively small and represents a limited range of Shona expressions.

Most sentences use formal, fully punctuated language, with limited informal spelling, dialect variation, and English–Shona code-switching.

The dataset also relies primarily on one sentence contributor and one reviewer. Some template similarity remains between examples across the training and evaluation splits (see [`QUALITY.md`](QUALITY.md)).

These factors may limit the model's ability to generalize to unfamiliar real-world requests.

## Intended Use

The dataset is intended for educational NLP research, supervised intent classification, model evaluation, and demonstration purposes.

It is not intended for high-stakes decisions or unrestricted production deployment without further evaluation.
