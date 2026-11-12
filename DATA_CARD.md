# Dataset Card — Shona Intent Classification

## Dataset Overview

Team Ubuntu (Team 3) developed a Shona-language dataset for **Track A — Intent Classification** at the Strathmore NLP Hub Datathon 2026.

The dataset contains **595 Shona sentences** labeled across ten predefined intent categories. It supports developing a supervised machine learning model that identifies the intended action behind a user's written request.

- **Dataset file:** `data/contribution.csv`
- **Language:** Shona (`sn`)
- **Licence:** CC BY 4.0

## Dataset Composition

| Intent | Description | Records |
|---|---|---:|
| `weather_query` | Weather requests | 55 |
| `datetime_query` | Date and time questions | 63 |
| `alarm_set` | Alarm requests | 55 |
| `calendar_set` | Scheduling events | 60 |
| `calendar_query` | Retrieving calendar events | 67 |
| `lists_createoradd` | Creating or updating lists | 65 |
| `lists_query` | Retrieving list information | 65 |
| `play_music` | Music playback | 55 |
| `news_query` | News requests | 55 |
| `qa_definition` | Definitions and explanations | 55 |
| **Total** | | **595** |

Splits: 445 train / 50 dev / 100 test. Dev has 5 and test 10 sentences per intent. The 100 test sentences (SN-296 to SN-395) were written on 12 Nov 2026 as a fresh test set; the 50 sentences that were the test set for the first model are now in train (see [`DATA_PLAN.md`](DATA_PLAN.md)).

Each record contains a sentence, its intent label, and metadata describing its origin, contributor, reviewer, and dataset split.

## Data Origin and Provenance

The Shona examples were prepared by Mukundi Witness Chingwena (contributor code `MUK`). The dataset records an independent language reviewer identified by code `FDK`, who reviewed every sentence. FDK's changes to the 300 newest sentences are listed in [`review_log.csv`](review_log.csv).

All 595 records have the source method `original_human`. **None of the 595 sentences was written by AI or with AI help.**

No external datasets are included in the counted contribution.

**Separate stress set (not part of this dataset).** Mukundi used ChatGPT to generate a separate set of 360 Shona sentences (300 supported requests and 60 that the demo should refuse), and then checked it himself. Because it is AI-generated, it is synthetic data. It was used only as an extra check on the trained model and the demo. It was never used for training or for the test score, and it is not included in `data/contribution.csv` or in this repository.

The collection, expansion, and splitting procedures are described in [`DATA_PLAN.md`](DATA_PLAN.md). Annotation rules are documented in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md).

## Data Rights and Ethics

The dataset is released under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** licence. Anyone may reuse it with credit to Team Ubuntu, Strathmore NLP Hub Datathon 2026.

The dataset records contributor authorization for Team Ubuntu's datathon use. Supporting permission and review evidence should be retained privately.

The team aims to ensure that examples are appropriate for educational research and do not unnecessarily contain personal or sensitive information.

## Limitations

The dataset is relatively small and represents a limited range of Shona expressions.

Most sentences use standard, fully punctuated Shona. The 300 sentences added on 12 Nov include some informal spelling, English–Shona code-switching and a few Karanga and Ndau words, but these remain a small share.

All 595 sentences were written by one contributor and reviewed by one reviewer, including the test set, so the data reflects one writer's Shona. Some template similarity remains between examples in the older splits (see [`QUALITY.md`](QUALITY.md)).

These factors may limit the model's ability to generalize to unfamiliar real-world requests.

## Intended Use

The dataset is intended for educational NLP research, supervised intent classification, model evaluation, and demonstration purposes.
