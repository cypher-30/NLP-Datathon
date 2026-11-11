# Annotation Guide — Shona Intent Classification

Version: final, 11 Nov 2026. Covers `data/contribution.csv` v4 (295 rows). Rows are referenced by id (SN-xxx).

## 1. Purpose

This guide outlines the annotation framework Team Ubuntu used to classify Shona-language sentences into ten predefined intent categories.

The objective was to ensure consistent, accurate, and meaningful labeling by assigning each sentence an intent that reflects the user's intended action.

## 2. Intent Categories

Each sentence is a spoken-style request to an assistant. The dataset uses the following ten intent labels (from `taxonomy.csv`):

| Intent Label | Description |
|---|---|
| `weather_query` | Requests for weather information or conditions |
| `datetime_query` | Questions about dates, times, or days |
| `alarm_set` | Requests to set an alarm to ring |
| `calendar_set` | Requests to schedule events or appointments |
| `calendar_query` | Requests to retrieve scheduled events |
| `lists_createoradd` | Requests to create lists or add items |
| `lists_query` | Requests to retrieve information from lists |
| `play_music` | Requests to play songs or music |
| `news_query` | Requests for news or current events |
| `qa_definition` | Requests for definitions or explanations |

## 3. Language and Spelling

Shona, written mostly in standard (Zezuru-like) formal spelling with punctuation. Real-world variation (informal spelling, English mixed in, other dialects) is thin and is listed under section 8.

## 4. Annotation Methodology

Each Shona sentence received a single intent label based on its primary meaning and the action the user requested.

The annotation process followed three key principles:

1. **Intent over keywords:** Labels were determined by the overall meaning of a sentence rather than individual words.
2. **Consistency:** Sentences expressing the same intention were assigned the same category, even when phrased differently.
3. **Clarity:** Ambiguous expressions were examined carefully to identify the most appropriate intent.

## 5. Annotation Decision Rules

### Rule 1: Creating vs. Retrieving Information
An imperative that adds or schedules something (Ronga, Wedzera, Isa, Gadzira, Tanga, Nyora) is `calendar_set` or `lists_createoradd`. A question, or Ndiratidze / Tarisa / Ndiudze / "...here?", is a `*_query`. Watch tense: "Ronga..." (do it) is set; "Ndakaronga here...?" (did I schedule it?) is query.

### Rule 2: Calendar vs. List Requests
- Calendar: an event tied to a time slot (musangano, chiitiko, nguva yekuonana, bvunzo, mhemberero, mharidzo).
- List: a collection of items or tasks with no time slot (runyorwa, rondedzero, list, zvekutenga, zvekuita, mabasa).
- An explicit container word takes priority: "pakarenda / calendar" means calendar; "parunyorwa / rondedzero / list / pane zvekuita" means list.
- The verb never decides, because Nyora, Isa and Wedzera appear on both sides (SN-285 is calendar, SN-257 is list).
- A to-do named by a day ("zvekuita zvangu zveMugovera", SN-254) is a list. An event with a clock time or date ("na3 masikati", "musi wa12") is calendar.
- No container word, plus an event noun or appointment, plus a date: calendar (SN-275).
- Things to buy, pack, invite or do are a list even when a date is mentioned.

### Rule 3: Calendar Queries vs. Date/Time Queries
If the answer needs the user's own calendar data, it is `calendar_query` (SN-277 "Mharidzo yedu inotanga nguvai"). If it is about the clock or the calendar itself, it is `datetime_query` (SN-033, SN-028).

### Rule 4: Alarm vs. Calendar
"alarm", "ndimutse" or "irire" means `alarm_set`. A named event to put on the schedule means `calendar_set`. The presence of a time expression alone does not determine the category.

### Rule 5: Weather vs. Date/Time
The Shona word *zuva* can refer to the sun, a day, or a date depending on context. Sunny weather ("kuchava nezuva") is `weather_query`. The time of sunrise or sunset is `datetime_query` (SN-043, SN-044). "nguva/nguvai" about rain lasting or stopping is `weather_query` (SN-013, SN-018).

### Rule 6: Music and Playlists
Requests to play songs or music are `play_music`. "runyorwa rwenziyo" (playlist) in a request to play music is `play_music`, not a list.

### Rule 7: Definition Questions
"X chii / zvinorevei / nditsanangurire" (what is X, what does X mean, explain X) is `qa_definition`, even when X is a weather or news topic (SN-230).

### Rule 8: Disagreement
If the rules do not settle a row, it is marked adjudicated and a one-line note is kept.

## 6. Borderline Rows Noted During Review
These rows sit close to two labels. Their labels follow the rules above.
- Calendar vs list: SN-275, SN-254, SN-285, SN-253, SN-257, SN-112, SN-110 vs SN-160.
- `calendar_query` vs `datetime_query`: SN-277 vs SN-033; SN-281 (bare "next event", no owner or container word).
- `play_music` vs lists: SN-180, SN-200 ("runyorwa rwenziyo").
- weather vs news vs qa: SN-230, SN-212, SN-223 vs SN-023.
- Spelling points for a Shona speaker, not label questions: SN-293 and SN-295 (noun-class concord), SN-013 ("kucha mira" vs "kuchamira", no "?"), SN-026 (all lowercase, no "?").

## 7. Annotation Quality Assurance

Every row was written by `MUK` and reviewed by `FDK`, a different Shona speaker. The review focused on:

- Correct interpretation of Shona expressions.
- Consistency between sentence meaning and intent labels.
- Grammatical correctness and natural sentence structure.
- Clear distinctions between closely related categories.

We applied the same rules across the training, development, and test sets. The detailed review and validation findings are documented in [`QUALITY.md`](QUALITY.md).

## 8. Limits of the Data

- Mostly formal, standard, fully punctuated Shona, one writer and one reviewer.
- Code-switching is rare (alarm, fog, seminar, data, charger, application; "list" once in SN-258; "network" once in SN-243).
- Weather has 25 rows and gained none in the latest batch, while datetime gained 8.
- Future work: about 20% code-switched, 15% informal spelling, 15% honorific vs casual register and 20% non-Zezuru dialect per label, with dialects (Zezuru, Karanga, Manyika, Korekore) written by speakers from each area. Informal spelling should be collected from real WhatsApp-style text, not invented. More weather rows that pair time words with clear weather words (mvura, mhepo, kupisa, kutonhora, madhigirii) would help with the weather vs date/time confusion.

## 9. Changes
- v1 (8 Nov): 250 rows.
- v2 (10 Nov): added SN-251 to SN-295, all `train`.
- v3/v4 (10 Nov): Mukundi reworded 12 train rows that closely matched dev or test rows; related rows given shared `group_id`. Frozen on 10 Nov; final test run on 11 Nov.
