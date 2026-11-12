"""Team Ubuntu v2: the single final comparison on the FRESH test split (run once, after freezing).

Scores the frozen v1 model (artifacts/intent/model.joblib, trained on dataset v4) and every v2 candidate pack on
the test rows of the current CSV. Reports accuracy, macro-F1, per-label F1, confusion matrix, majority baseline and
a bootstrap 95% interval for macro-F1, overall and for the rows written by each author.

Refuses to run without --final, with uncommitted changes, or if it has already been run (artifacts/v2/test_run.lock).

  python compare.py --final --data data/contribution.csv --packs artifacts/v2 artifacts/v2_ablation_v4data
"""
import argparse, hashlib, json, subprocess, sys, datetime
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.metrics import f1_score
from validate import check
from core import INTENTS, classification_score

OUT = Path('artifacts/v2')
V1_SHA256 = '29f4510b2cef49556960f558d9a3f38ef44d83f897943275c71f2c45d853995d'  # frozen v1 model (release v1.0-final)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
LOCK = OUT / 'test_run.lock'


def bootstrap_ci(y, pred, n=2000, seed=42):
    rng = np.random.default_rng(seed); y = np.asarray(y); pred = np.asarray(pred); vals = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        vals.append(f1_score(y[i], pred[i], labels=INTENTS, average='macro', zero_division=0))
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def score(model, frame):
    s = classification_score(model, frame, INTENTS)
    pred = model.predict(frame.text)
    s['macro_f1_95ci'] = bootstrap_ci(frame.label, pred)
    s['per_label_f1'] = {l: s['report'][l]['f1-score'] for l in INTENTS}
    return s, pred


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--final', action='store_true')
    p.add_argument('--data', default='data/contribution.csv')
    p.add_argument('--packs', nargs='+', default=['artifacts/v2'])
    p.add_argument('--v1', default='artifacts/intent/model.joblib')
    a = p.parse_args()
    if not a.final:
        sys.exit('Refusing: this scores the fresh test split. Freeze (commit) everything, then rerun with --final.')
    if LOCK.exists():
        sys.exit(f'Refusing: the fresh test was already scored ({LOCK.read_text().strip()}). It must be run only once.')
    if subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip():
        sys.exit('Refusing: uncommitted changes. Commit the frozen state first so the run is traceable.')
    commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()

    # The packs are gitignored, so freeze them by hash: each folder's selection.json must be COMMITTED and list
    # the sha256 of every pack we load; the v1 model must be the frozen release file.
    if sha(a.v1) != V1_SHA256:
        sys.exit('Refusing: v1 model is not the frozen v1.0-final file.')
    frozen = {}
    for folder in a.packs:
        sel = Path(folder) / 'selection.json'
        if subprocess.run(['git', 'ls-files', '--error-unmatch', str(sel)], capture_output=True).returncode:
            sys.exit(f'Refusing: {sel} is not committed. Commit the selection (with pack hashes) first.')
        for name, c in json.loads(sel.read_text(encoding='utf-8'))['candidates'].items():
            f = Path(folder) / c['pack_file']
            if sha(f) != c['pack_sha256']:
                sys.exit(f'Refusing: {f} differs from the hash recorded in {sel} (retrained after freezing?).')
            frozen[f'{Path(folder).name}/{name}'] = f
    OUT.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(f"started {datetime.datetime.now().astimezone().isoformat(timespec='seconds')} at commit {commit}\n", encoding='utf-8')  # before scoring: no silent second look

    df = check(a.data, False, 'intent')
    tr, test = df[df.split.eq('train')], df[df.split.eq('test')].reset_index(drop=True)
    models = {'v1_frozen (kit baseline, dataset v4)': joblib.load(a.v1)['model']}  # our own trusted files only
    for key, f in frozen.items():
        models[key] = joblib.load(f)['model']
    models['majority_baseline'] = DummyClassifier(strategy='most_frequent').fit(tr.text, tr.label)

    result = {'run_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'commit': commit,
              'data': a.data, 'test_rows': len(test), 'authors': test.contributor_code.value_counts().to_dict(), 'models': {}}
    preds = test[['record_id', 'text', 'label', 'contributor_code']].copy()
    for name, model in models.items():
        overall, pred = score(model, test)
        by_author = {}
        for author, part in test.groupby('contributor_code'):
            by_author[author] = {'rows': len(part), 'accuracy': float((model.predict(part.text) == part.label).mean()),
                                 'macro_f1': float(f1_score(part.label, model.predict(part.text), labels=INTENTS, average='macro', zero_division=0))}
        overall['by_author'] = by_author
        result['models'][name] = overall
        preds[name] = pred
        print(f"{name:55s} acc {overall['accuracy']:.3f}  macro-F1 {overall['macro_f1']:.3f}  95% CI {overall['macro_f1_95ci'][0]:.3f}-{overall['macro_f1_95ci'][1]:.3f}")

    (OUT / 'test_metrics.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    preds.to_csv(OUT / 'test_predictions.csv', index=False)
    LOCK.write_text(LOCK.read_text(encoding='utf-8') + f"finished {result['run_at']}\n", encoding='utf-8')
    print(f'Saved {OUT}/test_metrics.json, test_predictions.csv and {LOCK.name}. Commit them now; do not rerun.')


if __name__ == '__main__':
    main()
