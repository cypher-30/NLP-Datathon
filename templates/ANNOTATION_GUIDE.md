
# Annotation Guide — Shona Intent Classification

## 1. Purpose

This guide outlines the annotation framework Team Ubuntu uses to classify Shona-language sentences into ten predefined intent categories.

The objective was to ensure consistent, accurate, and meaningful labeling by assigning each sentence an intent that reflects the user's intended action.

## 2. Intent Categories

The dataset uses the following ten intent labels:

| Intent Label | Description |
|---|---|
| `weather_query` | Requests for weather information or conditions |
| `datetime_query` | Questions about dates, times, or days |
| `alarm_set` | Requests to set alarms or reminders |
| `calendar_set` | Requests to schedule events or appointments |
| `calendar_query` | Requests to retrieve scheduled events |
| `lists_createoradd` | Requests to create lists or add items |
| `lists_query` | Requests to retrieve information from lists |
| `play_music` | Requests to play songs or music |
| `news_query` | Requests for news or current events |
| `qa_definition` | Requests for definitions or explanations |

## 3. Annotation Methodology

Each Shona sentence received a single intent label based on its primary meaning and the action the user requested.

The annotation process followed three key principles:

1. **Intent over keywords:** Labels were determined by the overall meaning of a sentence rather than individual words.
2. **Consistency:** Sentences expressing the same intention were assigned the same category, even when phrased differently.
3. **Clarity:** Ambiguous expressions were examined carefully to identify the most appropriate intent.

This approach helped keep labeling consistent across the dataset.

## 4. Annotation Decision Rules

To distinguish categories with overlapping meanings, the team established the following rules.

### Rule 1: Creating vs. Retrieving Information

Requests involving creating or adding information were distinguished from requests asking to retrieve existing information.

- `lists_createoradd`: Creating a list or adding an item.
- `lists_query`: Asking about items already in a list.
- `calendar_set`: Scheduling an event.
- `calendar_query`: Asking about an existing calendar event.

### Rule 2: Calendar vs. List Requests

We classified requests by the information container referenced in the sentence.

An explicit reference to a calendar or list took priority over general action words such as "add" or "show."

### Rule 3: Calendar Queries vs. Date/Time Queries

- `calendar_query`: Requests concerning scheduled events or appointments.
- `datetime_query`: Requests concerning dates or times without referring to scheduled events.

### Rule 4: Alarm vs. Calendar

Requests to set alarms were classified as `alarm_set`, while requests to schedule events or appointments were classified as `calendar_set`.

The presence of a time expression alone did not determine the category.

### Rule 5: Weather vs. Date/Time

The Shona word *zuva* can refer to the sun, a day, or a date depending on context.

Sentences were classified according to their intended meaning:

- `weather_query`: Questions about weather conditions.
- `datetime_query`: Questions about dates or times.

### Rule 6: Music and Playlists

Requests to play songs or music were assigned `play_music`.

When playlists were mentioned, the intended action determined whether the sentence belonged to music playback or list management.

### Rule 7: Definition Questions

Requests asking for the meaning or explanation of a word or concept were assigned `qa_definition`.

Questions requesting weather, news, or calendar information retained their respective intent categories.

### Rule 8: Ambiguous Sentences

When a sentence could reasonably fit multiple categories, the team considered the full meaning and intended action.

The team reviewed sentences requiring clarification to determine the most appropriate label. Unresolved cases were revised or excluded to maintain annotation consistency.

## 5. Annotation Quality Assurance

The annotation process incorporated language review and consistency checks to strengthen dataset quality.

The review focused on:

- Correct interpretation of Shona expressions.
- Consistency between sentence meaning and intent labels.
- Grammatical correctness and natural sentence structure.
- Clear distinctions between closely related categories.

An independent Shona-language reviewer supported the assessment of sentence quality and label suitability.

The detailed review and validation findings are documented in [`QUALITY.md`](QUALITY.md).

## 6. Annotation Consistency

We applied the same annotation rules across the training, development, and test sets.

We checked sentence wording and intent labels for consistency, particularly in categories where similar expressions could lead to different interpretations.

This framework provided a structured basis for preparing the dataset and evaluating the Shona intent classification model.



