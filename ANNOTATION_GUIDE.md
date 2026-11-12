# Annotation Guide — Shona Intent Classification 

## 1. Purpose

This guide outlines the annotation framework Team Ubuntu uses to classify Shona-language sentences into ten predefined intent categories.

The objective was to ensure consistent, accurate, and meaningful labeling by assigning each sentence an intent that reflects the user's intended action.

## 2. Intent Categories

The dataset strictly adheres to the ten predefined intent labels required by the competition schema (`validate.py`):

| Intent Label | Description | 
| ----- | ----- | 
| `weather_query` | Requests for weather information or atmospheric conditions | 
| `datetime_query` | Questions about dates, time of day, or calendar days | 
| `alarm_set` | Requests to set an alarm to ring | 
| `calendar_set` | Requests to schedule events, meetings, or appointments | 
| `calendar_query` | Requests to retrieve or check scheduled events | 
| `lists_createoradd` | Requests to create lists or add items to an existing list | 
| `lists_query` | Requests to retrieve or check information from lists | 
| `play_music` | Requests to play songs, audio tracks, or music playlists | 
| `news_query` | Requests for news updates, current events, or headlines | 
| `qa_definition` | Requests for definitions, word meanings, or factual explanations | 

## 3. Annotation Methodology

Each Shona sentence received a single intent label based on its primary meaning and the action the user requested.

The annotation process followed four key principles:

1. **Intent over keywords:** Labels were determined by the overall pragmatic intent of a sentence rather than isolated individual words.

2. **Consistency:** Sentences expressing the same core request were assigned the same category, even when phrased with different syntactic patterns.

3. **Clarity:** Ambiguous expressions were evaluated against boundary guidelines to identify the single most appropriate intent.

4. **Loanword & Code-Switching Handling:** Common English loanwords integrated into Shona grammar (e.g., *“alarm”*, *“calendar”*, *“play-a”*) were annotated based on the root action intended in Shona context.

## 4. Annotation Decision Rules & Concrete Examples

To distinguish categories with overlapping meanings, the team established the following rules supported by real dataset examples (record IDs in brackets, from `data/contribution.csv`).

### Rule 1: Creating vs. Retrieving Information

Requests involving creating or adding information were distinguished from requests asking to retrieve existing information.

* `lists_createoradd`: Creating a list or appending an item.
  * *Example:* `"Wedzera chingwa parunyorwa rwangu rwezvekutenga."` $\rightarrow$ `lists_createoradd` (SN-127)

* `lists_query`: Checking items already in a list.
  * *Example:* `"Chii chiri parunyorwa rwangu rwezvekutenga?"` $\rightarrow$ `lists_query` (SN-151)

* `calendar_set`: Scheduling an event or meeting.
  * *Example:* `"Ronga musangano wemangwana na9 mangwanani."` $\rightarrow$ `calendar_set` (SN-076)

* `calendar_query`: Checking scheduled events.
  * *Example:* `"Ndine misangano ipi mangwana?"` $\rightarrow$ `calendar_query` (SN-101)

### Rule 2: Calendar vs. List Requests

We classified requests by the explicit information container referenced in the sentence. An explicit reference to a calendar or list took priority over general action verbs such as "add" or "show."

* *Example (List):* `"Nyora kuchenesa imba mumabasa angu emwedzi uno."` $\rightarrow$ `lists_createoradd` (SN-257)
* *Example (Calendar):* `"Nyora pakarenda kuti mwana wangu ane mutambo wechikoro musi wa12."` $\rightarrow$ `calendar_set` (SN-285)

### Rule 3: Calendar Queries vs. Date/Time Queries

* `calendar_query`: Requests concerning scheduled personal/work events or appointments.
  * *Example:* `"Kurovedza kwechikwata kunotanga nguvai neChitatu?"` $\rightarrow$ `calendar_query` (SN-277)

* `datetime_query`: Requests concerning general date or current time without referring to personal schedules.
  * *Example:* `"Mangwana izuva ripi revhiki?"` $\rightarrow$ `datetime_query` (SN-028)

### Rule 4: Alarm vs. Calendar

Requests to set an alarm to ring were classified as `alarm_set`, while requests to schedule future events or appointments were classified as `calendar_set`.

* *Example (Alarm):* `"Ndimutse na6 mangwana mangwanani."` $\rightarrow$ `alarm_set` (SN-051)
* *Example (Calendar):* `"Wedzera nguva yangu yekuonana nachiremba musi weChishanu pakarenda."` $\rightarrow$ `calendar_set` (SN-077)

### Rule 5: Disambiguating Polysemous Shona Words (e.g., *Zuva*)

The Shona word *zuva* can refer to the sun/weather, a day, or a date depending on syntactic context. Sentences were classified according to their semantic target:

* `weather_query`: Weather conditions or sun intensity.
  * *Example:* `"Kuchava nezuva here mangwana masikati?"` $\rightarrow$ `weather_query` (SN-019)

* `datetime_query`: Questions about a date, a day of the week, or a time of day, including sunrise and sunset times.
  * *Example:* `"Zuva richabuda nenguvai mangwana?"` $\rightarrow$ `datetime_query` (SN-043)

### Rule 6: Music and Playlists

Requests to play music or audio streams were assigned `play_music`. Mentioning a "playlist" in the context of playback remains `play_music`, whereas creating/editing a named playlist as a generic list falls under list operations.

* *Example:* `"Tanga kuridza playlist yangu yandinofarira."` $\rightarrow$ `play_music` (SN-180)

### Rule 7: Definition Questions

Requests asking for the meaning, definition, or translation of a word or concept were assigned `qa_definition`.

* *Example:* `"Shoko rekuti 'ubuntu' rinorevei?"` $\rightarrow$ `qa_definition` (SN-229)

### Rule 8: Ambiguous Sentences

When a sentence could reasonably fit multiple categories, the team evaluated the dominant user action. Sentences that the rules did not settle were given the label of the dominant action.

## 5. Quality Assurance & Validation Compliance

The annotation process incorporated independent verification and computational validation:

* **Language Review:** Every sentence was reviewed by an independent Shona speaker (`FDK`) to check for natural phrasing, correct orthography, and accurate intent mapping.
* **Schema Validation:** All target intent labels strictly match the allowed values in `taxonomy.csv` and pass automated checks via `validate.py`.
* **Detailed Findings:** Error analysis and verification logs are maintained in [`QUALITY.md`](QUALITY.md).

## 6. Annotation Consistency

We applied the same annotation rules across the training, development, and test sets.

We checked sentence wording and intent labels for consistency, particularly in categories where similar expressions could lead to different interpretations.

This framework provided a structured basis for preparing the dataset and evaluating the Shona intent classification model.