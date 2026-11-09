# Annotation guide (Team 3 "Ubuntu", Shona, intent track)

Version: draft 2, 10 Nov 2026. Covers `data/contribution.csv` (295 rows). Reviewed by the team; rows referenced by id (SN-xxx).

## Task and label set
Each sentence is a spoken-style request to an assistant, labelled with what the person wants. Ten labels (from `taxonomy.csv`): `weather_query`, `datetime_query`, `alarm_set`, `calendar_set`, `calendar_query`, `lists_createoradd`, `lists_query`, `play_music`, `news_query`, `qa_definition`.

## Language and spelling
Shona, written mostly in standard (Zezuru-like) formal spelling with punctuation. Real-world variation (informal spelling, English mixed in, other dialects) is thin and listed under "Limits" below.

## Decision rules
1. **Create or change vs retrieve.** An imperative that adds or schedules something (Ronga, Wedzera, Isa, Gadzira, Tanga, Nyora) is `calendar_set` or `lists_createoradd`. A question, or Ndiratidze / Tarisa / Ndiudze / "...here?", is a `*_query`. Watch tense: "Ronga..." (do it) is set; "Ndakaronga here...?" (did I schedule it?) is query.
2. **Calendar vs list.**
   - Calendar: an event tied to a time slot (musangano, chiitiko, nguva yekuonana, bvunzo, mhemberero, mharidzo).
   - List: a collection of items or tasks with no time slot (runyorwa, rondedzero, list, zvekutenga, zvekuita, mabasa).
   - If a container word is explicit it wins: "pakarenda / calendar" means calendar; "parunyorwa / rondedzero / list / pane zvekuita" means list.
   - The verb never decides, because Nyora, Isa and Wedzera appear on both sides (SN-285 is calendar, SN-257 is list).
   - A to-do named by a day ("zvekuita zvangu zveMugovera", SN-254) is a list. An event with a clock time or date ("na3 masikati", "musi wa12") is calendar.
   - No container word, plus an event noun or appointment, plus a date: calendar (SN-275).
   - Things to buy, pack, invite or do are a list even when a date is mentioned.
3. **`calendar_query` vs `datetime_query`.** If the answer needs the user's own calendar data, it is `calendar_query` (SN-277 "Mharidzo yedu inotanga nguvai"). If it is about the clock or the calendar itself, it is `datetime_query` (SN-033, SN-028).
4. **`alarm_set` vs `calendar_set`.** "alarm", "ndimutse" or "irire" means `alarm_set`. A named event to put on the schedule means `calendar_set`.
5. **`weather_query` vs `datetime_query`.** "zuva" means both sun and day. Sunny weather ("kuchava nezuva") is weather. The time of sunrise or sunset is datetime (SN-043, SN-044). "nguva/nguvai" about rain lasting or stopping is weather (SN-013, SN-018).
6. **Playlist.** "runyorwa rwenziyo" is `play_music`, not a list.
7. **`qa_definition`.** "X chii / zvinorevei / nditsanangurire" is qa even when X is a weather or news topic (SN-230).
8. **Disagreement.** If the rules do not settle a row, mark it adjudicated and keep a one-line note.

## Ambiguous rows (to adjudicate or exclude)
- Calendar vs list: SN-275, SN-254, SN-285, SN-253, SN-257, SN-112, SN-110 vs SN-160.
- `calendar_query` vs datetime: SN-277 vs SN-033; SN-281 (bare "next event", no owner or container word).
- `play_music` vs lists: SN-180, SN-200 ("runyorwa rwenziyo").
- weather vs news vs qa: SN-230, SN-212, SN-223 vs SN-023.
- For a Shona speaker to check, not corrections: SN-293 and SN-295 (noun-class concord), SN-013 ("kucha mira" vs "kuchamira", no "?"), SN-026 (all lowercase, no "?").

## Independent review
Every row was written by `MUK` and reviewed by `FDK`, a different person. The team reviewed this guide and the row analysis. Disagreements are settled by the rules above, and anything unresolved is marked adjudicated.

## Limits of the data (be honest in the write-up)
- Mostly formal, standard, fully punctuated Shona, one writer and one reviewer.
- Code-switching is rare (alarm, fog, seminar, data, charger, application; "list" once in SN-258; "network" once in SN-243).
- Planned, not yet done: about 20% code-switched, 15% informal spelling, 15% honorific vs casual register and 20% non-Zezuru dialect per label, with dialects (Zezuru, Karanga, Manyika, Korekore) translated by speakers from each area from a fixed prompt set. Dialect, register and code-switch go in a separate annotation sheet. Informal spelling should be collected from real WhatsApp-style text, not invented.
- Weather has 25 rows and gained none in the latest batch, while datetime gained 8. Planned fix is about 10 to 15 weather train rows that pair time words with clear weather words (mvura, mhepo, kupisa, kutonhora, madhigirii, forecast), plus contrastive datetime rows.

## Changes
- v1 (8 Nov): 250 rows.
- v2 (10 Nov): added SN-251 to SN-295, all `train`.
- v3 (10 Nov): Mukundi reworded 12 train rows that closely matched dev or test rows.
