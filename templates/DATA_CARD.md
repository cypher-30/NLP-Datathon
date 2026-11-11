# Dataset Card — Shona Intent Classification

## Dataset Overview

Team Ubuntu (Team 3) developed a Shona-language dataset for **Track A — Intent Classification** at the Strathmore NLP Hub Datathon 2026.

The dataset contains **295 Shona sentences** labeled across ten predefined intent categories. It supports developing a supervised machine learning model that identifies the intended action behind a user's written request.

- **Dataset file:** `data/contribution.csv`
- **Language:** Shona (`sn`)

## Dataset Composition

| Intent | Description | Records |
|---|---|---:|
| `weather_query` | Weather requests | 25 |
| `datetime_query` | Date and time questions | 33 |
| `alarm_set` | Alarm requests | 25 |
| `calendar_set` | Scheduling events | 30 |
| `calendar_query` | Retrieving calendar events | 37 |
| `lists_createoradd` | Creating or updating lists | 35 |
| `lists_query` | Retrieving list information | 35 |
| `play_music` | Music playback | 25 |
| `news_query` | News requests | 25 |
| `qa_definition` | Definitions and explanations | 25 |
| **Total** | | **295** |

Each record contains a sentence, its intent label, and metadata describing its origin, contributor, reviewer, and dataset split.

## Data Origin and Provenance

The Shona examples were prepared by Mukundi Witness Chingwena (contributor code `MUK`). The dataset records an independent language reviewer identified by code `FDK`.

All 295 records currently have the source method `original_human`.

No external datasets are included in the counted contribution.

The collection, expansion, and splitting procedures are described in [`DATA_PLAN.md`](DATA_PLAN.md). Annotation rules are documented in [`ANNOTATION_GUIDE.md`](ANNOTATION_GUIDE.md).

## Data Rights and Ethics

The dataset records contributor authorization for Team Ubuntu's datathon use. Supporting permission and review evidence should be retained privately.

The team aims to ensure that examples are appropriate for educational research and do not unnecessarily contain personal or sensitive information.

## Limitations

The dataset is relatively small and represents a limited range of Shona expressions.

Most sentences use formal, fully punctuated language, with limited informal spelling, dialect variation, and English–Shona code-switching.

The dataset also relies primarily on one sentence contributor and one reviewer. Some template similarity remains between examples across the training and evaluation splits.

These factors may limit the model's ability to generalize to unfamiliar real-world requests.

## Intended Use

The dataset is intended for educational NLP research, supervised intent classification, model evaluation, and demonstration purposes.
