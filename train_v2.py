"""Team Ubuntu v2: train and select model candidates using the TRAIN and DEV splits only (never test).

For each candidate (see models_v2.py), settings are chosen by stratified 5-fold cross-validation on the train
split. The best setting is refitted on all train rows and scored on dev. The winner is the candidate with the
highest mean of (CV macro-F1, dev macro-F1); if LaBSE wins by less than 0.02 the lighter TF-IDF model is kept.

  python train_v2.py --data data/contribution.csv --out artifacts/v2
  python train_v2.py --data <older csv> --out artifacts/v2_ablation_v4data   # same models on the old data
"""
import argparse, hashlib, json, time
from pathlib import Path
import joblib
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from validate import check
from core import INTENTS, fingerprint, classification_score
from models_v2 import BUILDERS, GRIDS, similarity_index

TIE_MARGIN = 0.02


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='data/contribution.csv')
    p.add_argument('--out', default='artifacts/v2')
    p.add_argument('--candidates', nargs='+', default=list(BUILDERS))
    a = p.parse_args()

    df = check(a.data, False, 'intent')
    tr, dev = df[df.split.eq('train')], df[df.split.eq('dev')]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    summary = {'data': a.data, 'data_sha256': fingerprint(df), 'train_rows': len(tr), 'dev_rows': len(dev),
               'selection_rule': f'max mean(CV macro-F1 on train, dev macro-F1); LaBSE must win by >= {TIE_MARGIN}',
               'test_split_used': False, 'candidates': {}}

    for name in a.candidates:
        t0 = time.time(); trials = []
        for params in GRIDS[name]:
            scores = cross_val_score(BUILDERS[name](**params), tr.text, tr.label, cv=cv, scoring='f1_macro')
            trials.append({'params': params, 'cv_macro_f1': float(scores.mean()), 'cv_std': float(scores.std())})
        best = max(trials, key=lambda t: t['cv_macro_f1'])
        model = BUILDERS[name](**best['params']).fit(tr.text, tr.label)
        dev_score = classification_score(model, dev, INTENTS)
        vec, mat = similarity_index(tr.text)
        pack = {'name': name, 'params': best['params'], 'model': model, 'language': 'sn', 'practice': False,
                'track': 'intent', 'data_sha256': fingerprint(df), 'sim_vectorizer': vec, 'train_matrix': mat,
                'train_texts': tr.text.tolist(), 'train_labels': tr.label.tolist(), 'train_ids': tr.record_id.tolist()}
        joblib.dump(pack, out / f'{name}.joblib')
        pack_sha = hashlib.sha256((out / f'{name}.joblib').read_bytes()).hexdigest()
        summary['candidates'][name] = {'pack_file': f'{name}.joblib', 'pack_sha256': pack_sha, 'best_params': best['params'], 'cv_macro_f1': best['cv_macro_f1'],
                                       'cv_std': best['cv_std'], 'dev_accuracy': dev_score['accuracy'],
                                       'dev_macro_f1': dev_score['macro_f1'], 'dev_confusion_matrix': dev_score['confusion_matrix'],
                                       'all_trials': trials, 'seconds': round(time.time() - t0, 1)}
        print(f"{name}: CV macro-F1 {best['cv_macro_f1']:.3f} (+/-{best['cv_std']:.3f}), dev macro-F1 {dev_score['macro_f1']:.3f}, params {best['params']}")

    dummy = DummyClassifier(strategy='most_frequent').fit(tr.text, tr.label)
    summary['majority_baseline_dev'] = classification_score(dummy, dev, INTENTS)['macro_f1']
    score = {n: (c['cv_macro_f1'] + c['dev_macro_f1']) / 2 for n, c in summary['candidates'].items()}
    winner = max(score, key=score.get)
    if winner == 'C_labse':
        tfidf = max((n for n in score if n != 'C_labse'), key=score.get, default=None)
        if tfidf and score['C_labse'] - score[tfidf] < TIE_MARGIN:
            winner = tfidf
    summary['selection_scores'] = score
    summary['winner'] = winner
    (out / 'selection.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Winner (chosen on train CV + dev only): {winner}. Saved {out}/selection.json. Freeze before compare.py --final.')


if __name__ == '__main__':
    main()
