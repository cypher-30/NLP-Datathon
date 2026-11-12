"""Team Ubuntu v2 model candidates (intent track). Used by train_v2.py, compare.py and app_shona.py.

A  kit baseline:  char TF-IDF (2-5) + logistic regression, identical to the kit's train.py
B  tuned TF-IDF:  word (1-2) + char_wb (2-5) TF-IDF + logistic regression, settings chosen by cross-validation
C  LaBSE:         multilingual sentence embeddings (sentence-transformers/LaBSE, covers Shona 'sn') + logistic regression
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline, make_union
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

LABSE_NAME = 'sentence-transformers/LaBSE'
_ENCODER = None


def _encoder():
    global _ENCODER
    if _ENCODER is None:
        from sentence_transformers import SentenceTransformer  # imported lazily: only candidate C needs torch
        _ENCODER = SentenceTransformer(LABSE_NAME, device='cpu')
    return _ENCODER


class LabseEmbedder(BaseEstimator, TransformerMixin):
    """Turns sentences into normalised LaBSE vectors. The encoder itself is not pickled; it is loaded from the
    Hugging Face cache (downloaded on first use), so saved packs stay small."""
    _cache = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        texts = list(X)
        missing = [t for t in dict.fromkeys(texts) if t not in self._cache]
        if missing:
            vecs = _encoder().encode(missing, batch_size=32, normalize_embeddings=True, show_progress_bar=False)
            self._cache.update(zip(missing, vecs))
        return np.vstack([self._cache[t] for t in texts])


def kit_baseline():
    return make_pipeline(TfidfVectorizer(analyzer='char', ngram_range=(2, 5)),
                         LogisticRegression(max_iter=1000, random_state=42))


def tuned_tfidf(C=10.0, class_weight=None, sublinear_tf=True, word_ngrams=(1, 2)):
    feats = make_union(
        TfidfVectorizer(analyzer='word', ngram_range=word_ngrams, sublinear_tf=sublinear_tf, lowercase=True),
        TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5), sublinear_tf=sublinear_tf, lowercase=True),
    )
    return make_pipeline(feats, LogisticRegression(C=C, class_weight=class_weight, max_iter=3000, random_state=42))


def labse(C=10.0, class_weight=None):
    return make_pipeline(LabseEmbedder(), LogisticRegression(C=C, class_weight=class_weight, max_iter=3000, random_state=42))


# Search spaces, explored with cross-validation on the TRAIN split only.
GRIDS = {
    'A_kit_baseline': [dict()],
    'B_tuned_tfidf': [dict(C=c, class_weight=w, sublinear_tf=s, word_ngrams=n)
                      for c in (1.0, 3.0, 10.0, 30.0) for w in (None, 'balanced') for s in (True, False)
                      for n in ((1, 1), (1, 2))],
    'C_labse': [dict(C=c, class_weight=w) for c in (0.3, 1.0, 3.0, 10.0, 30.0) for w in (None, 'balanced')],
}
BUILDERS = {'A_kit_baseline': kit_baseline, 'B_tuned_tfidf': tuned_tfidf, 'C_labse': labse}


def similarity_index(train_texts):
    """Char TF-IDF index over training sentences: used by the demo to refuse input unlike anything it learned,
    and to show the most similar training sentences. Independent of which classifier wins."""
    vec = TfidfVectorizer(analyzer='char', ngram_range=(2, 5)).fit(train_texts)
    return vec, vec.transform(train_texts)


def explain_words(model, text, label_index):
    """Leave-one-word-out: how much the chosen label's probability drops when each word is removed.
    Works for any model with predict_proba. Returns [(word, drop)] sorted by importance."""
    words = text.split()
    if len(words) < 2:
        return []
    base = model.predict_proba([text])[0][label_index]
    variants = [' '.join(words[:i] + words[i + 1:]) for i in range(len(words))]
    probs = model.predict_proba(variants)[:, label_index]
    return sorted(zip(words, (base - probs).tolist()), key=lambda x: -x[1])
