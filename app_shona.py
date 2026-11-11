"""Team Ubuntu demo (Shona intent). Adapted from the starter kit's app.py (credit: Strathmore NLP Hub starter kit).

Changes from the kit app: intent track only; says "not supported" instead of forcing a label when the input
looks unlike anything we trained on; shows plain-language results, the top-3 guesses, which words drove the
answer and the most similar sentences it learned from; a second tab shows how good the model is on held-out data.
Loads the v2 winner (artifacts/v2/selection.json) if present, otherwise the frozen v1 model.
Run:  python -m streamlit run app_shona.py
"""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from core import FRIENDLY, INTENTS
from models_v2 import explain_words  # also makes v2 packs unpicklable-safe (their classes live there)

# Thresholds were chosen by looking at DEV rows and off-topic probes, never the test split.
MIN_SIMILARITY = 0.28   # below this the text looks unlike any training sentence -> unsupported
MIN_CONFIDENCE = 0.16   # below this the model is basically guessing -> unsupported
SURE_CONFIDENCE = 0.22  # below this (but above MIN) we show the answer as "not sure"

WHAT_HAPPENS = {
    'weather_query': 'would look up the weather forecast for you.',
    'datetime_query': 'would tell you the date or the time.',
    'alarm_set': 'would set an alarm.',
    'calendar_set': 'would add an event to your calendar.',
    'calendar_query': 'would read out what is on your calendar.',
    'lists_createoradd': 'would create a list or add something to one.',
    'lists_query': 'would read out what is on one of your lists.',
    'play_music': 'would play music.',
    'news_query': 'would read you the latest news.',
    'qa_definition': 'would explain what a word or idea means.',
}

st.set_page_config(page_title='Team Ubuntu - Shona assistant demo', page_icon='💬')


@st.cache_resource
def load_pack():
    sel = Path('artifacts/v2/selection.json')
    if sel.exists():
        winner = json.loads(sel.read_text(encoding='utf-8'))['winner']
        path = Path('artifacts/v2') / f'{winner}.joblib'
        if path.exists():
            return joblib.load(path), f'v2 ({winner})'  # only load model files you created and trust
    path = Path('artifacts/intent/model.joblib')
    if path.exists():
        return joblib.load(path), 'v1 (kit baseline)'
    return None, None


pack, model_name = load_pack()
if pack is None:
    st.info('Train a model first: python train_v2.py --data data/contribution.csv')
    st.stop()
model = pack['model']
sim_vec = pack.get('sim_vectorizer') or model.steps[0][1]  # v1 packs reuse the classifier's own vectoriser
train_matrix = pack.get('train_matrix')

st.title('Shona assistant demo')
st.caption('Type a request in Shona and see what the assistant thinks you want. Nothing is actually done: no alarm, calendar, music or search is run.')

with st.sidebar:
    st.subheader('What it can understand')
    for k in WHAT_HAPPENS:
        st.write('•', FRIENDLY.get(k, k))
    st.caption('Anything else is reported as not supported.')
    st.caption(f'Model in use: {model_name}')

try_tab, quality_tab = st.tabs(['Try it', 'How good is it?'])

# Example requests: real TRAINING sentences from our dataset (never test rows), plus one off-topic request.
EXAMPLES = [
    ('Weather', 'Mamiriro ekunze achange akaita sei nhasi?'),
    ('Alarm', 'Isa alarm ya5:30 mangwanani.'),
    ('Add to a list', 'Wedzera chingwa parunyorwa rwangu rwezvekutenga.'),
    ('Calendar', 'Ndiratidze zviitiko zviri pakarenda yangu nhasi.'),
    ('Meaning of a word', 'Inflation chii?'),
    ('Not supported', 'Please book me a flight to Nairobi'),
]
if 'request_text' not in st.session_state:
    st.session_state['request_text'] = ''


def use_example(example):
    st.session_state['request_text'] = example


with try_tab:
    st.caption('Try an example:')
    cols = st.columns(3)
    for i, (label, example) in enumerate(EXAMPLES):
        cols[i % 3].button(label, key=f'ex_{i}', on_click=use_example, args=(example,), use_container_width=True)

    text = st.text_area('Your request (Shona)', key='request_text', placeholder='Type here, or pick an example above...')
    if st.button('Understand', type='primary'):
        if not text.strip():
            st.info('Please type something first.')
            st.stop()
        proba = model.predict_proba([text])[0]
        order = proba.argsort()[::-1]
        top, conf = model.classes_[order[0]], proba[order[0]]
        sims = None
        similarity = None
        if train_matrix is not None:
            sims = (sim_vec.transform([text]) @ train_matrix.T).toarray()[0]
            similarity = float(sims.max())

        unsupported = conf < MIN_CONFIDENCE or (similarity is not None and similarity < MIN_SIMILARITY)
        if unsupported:
            st.warning("Sorry, I don't think I can help with that. I only understand the kinds of requests listed on the left.")
        else:
            name = FRIENDLY.get(top, top)
            if conf >= SURE_CONFIDENCE:
                st.success(f'It looks like you want: **{name}**')
            else:
                st.info(f'I am not sure, but it looks like you want: **{name}**')
            st.write('The assistant ' + WHAT_HAPPENS.get(top, 'would handle this request.'))
            st.caption('Other possibilities:')
            for i in order[1:3]:
                st.write('•', FRIENDLY.get(model.classes_[i], model.classes_[i]))

            with st.expander('Why did it decide this?'):
                words = [(w, d) for w, d in explain_words(model, text, order[0]) if d > 0.01][:3]
                if words:
                    st.write('These words pushed it most towards **' + name + '** (how much less sure it gets without each word):')
                    for w, d in words:
                        st.write(f'• **{w}**  (−{d * 100:.0f} points)')
                else:
                    st.write('No single word decides it; the answer comes from the sentence as a whole.')
                if sims is not None and 'train_texts' in pack:
                    st.write('Most similar sentences it learned from:')
                    for j in np.argsort(sims)[::-1][:3]:
                        st.write(f"• _{pack['train_texts'][j]}_ → {FRIENDLY.get(pack['train_labels'][j])}")
        st.caption('This is a small model trained on a few hundred sentences, so it can be wrong. The "points" are '
                   'uncalibrated model scores, not real percentages of certainty.')


def per_label_table(metrics_by_model):
    rows = {name: {FRIENDLY[l]: m['report'][l]['f1-score'] for l in INTENTS} for name, m in metrics_by_model.items()}
    return pd.DataFrame(rows).round(2)


with quality_tab:
    st.write('Scores come from sentences the model **never saw while learning**. Each test was run only once. '
             'Macro-F1 is the average score over the 10 request types (1.0 is perfect). The "always guess the same '
             'answer" baseline shows what you get with no learning at all.')
    v1 = Path('artifacts/intent/test_metrics.json')
    v2 = Path('artifacts/v2/test_metrics.json')
    if v1.exists():
        m = json.loads(v1.read_text(encoding='utf-8'))
        st.subheader('v1: original test (50 sentences, run 11 Nov 2026)')
        c1, c2, c3 = st.columns(3)
        c1.metric('Correct', f"{m['model']['accuracy'] * 100:.0f}%")
        c2.metric('Macro-F1', f"{m['model']['macro_f1']:.2f}")
        c3.metric('Baseline macro-F1', f"{m['majority_baseline']['macro_f1']:.2f}")
    if v2.exists():
        m2 = json.loads(v2.read_text(encoding='utf-8'))
        st.subheader(f"v2: fresh test ({m2['test_rows']} new sentences, run once)")
        summary = pd.DataFrame({name: {'Correct': r['accuracy'], 'Macro-F1': r['macro_f1'],
                                       '95% range low': r['macro_f1_95ci'][0], '95% range high': r['macro_f1_95ci'][1]}
                                for name, r in m2['models'].items()}).T.round(2)
        st.dataframe(summary, use_container_width=True)
        st.write('Score per request type (F1):')
        st.dataframe(per_label_table({k: v for k, v in m2['models'].items() if k != 'majority_baseline'}), use_container_width=True)
        chosen = next((k for k in m2['models'] if k.endswith(model_name.split('(')[-1].rstrip(')'))), None)
        if chosen:
            st.write(f'Where the demo model ({chosen}) gets confused (rows: true type, columns: its answer):')
            cm = m2['models'][chosen]['confusion_matrix']
            short = [FRIENDLY[l] for l in INTENTS]
            st.dataframe(pd.DataFrame(cm, index=short, columns=short), use_container_width=True)
    else:
        st.info('The fresh-test comparison of v1 and v2 has not been run yet.')
    st.caption('With only 5 to 10 test sentences per type, one mistake moves a type\'s score a lot, so treat these as rough.')
