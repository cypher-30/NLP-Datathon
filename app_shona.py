"""Team Ubuntu demo (Shona intent). Adapted from the starter kit's app.py (credit: Strathmore NLP Hub starter kit).

Changes from the kit app: intent track only; says "not supported" instead of forcing a label when the input
looks unlike anything we trained on; shows plain-language results and top-3 guesses instead of raw numbers/JSON.
Run:  python -m streamlit run app_shona.py
"""
from pathlib import Path
import joblib
import streamlit as st
from core import FRIENDLY

# Thresholds were chosen by looking at DEV rows and a few off-topic probes, never the test split.
MIN_SIMILARITY = 0.22   # below this the text looks unlike any training sentence -> unsupported
MIN_CONFIDENCE = 0.145  # below this the model is basically guessing -> unsupported
SURE_CONFIDENCE = 0.20  # below this (but above MIN) we show the answer as "not sure"

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
st.title('Shona assistant demo')
st.caption('Type a request in Shona and see what the assistant thinks you want. Nothing is actually done: no alarm, calendar, music or search is run.')

path = Path('artifacts') / 'intent' / 'model.joblib'
if not path.exists():
    st.info('Train the model first: python train.py --track intent --data data/contribution_working.csv --practice')
    st.stop()
pack = joblib.load(path)  # Only load model files you created and trust.
if pack['practice']:
    st.warning('Working draft: this model was trained on a draft dataset that is still being reviewed. Results are not final.')

with st.sidebar:
    st.subheader('What it can understand')
    for k in WHAT_HAPPENS:
        st.write('•', FRIENDLY.get(k, k))
    st.caption('Anything else is reported as not supported.')

text = st.text_area('Your request (Shona)', placeholder='Type here...')
if st.button('Understand'):
    if not text.strip():
        st.info('Please type something first.')
        st.stop()
    model = pack['model']
    vec = model.steps[0][1]
    proba = model.predict_proba([text])[0]
    order = proba.argsort()[::-1]
    top, conf = model.classes_[order[0]], proba[order[0]]
    # similarity to the closest training sentence (computed from the kit's own vectoriser)
    sim = pack.get('train_matrix')
    similarity = None
    if sim is not None:
        similarity = float((vec.transform([text]) @ sim.T).max())

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
    st.caption('This is a small model trained on a few hundred sentences, so it can be wrong. Treat it as a demonstration.')
