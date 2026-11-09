"""Turn the repaired draft into a working CSV: fills split, reviewer and source_url only.

Never touches source_method, licence_or_permission or contributor_code (provenance stays as Mukundi wrote it).
Split is a stratified 60/20/20 per label with a fixed seed, so it is reproducible.
Usage: python prepare_working.py [--in data/contribution_draft.csv] [--out data/contribution_working.csv]
"""
import argparse, csv, random
from collections import defaultdict

p = argparse.ArgumentParser()
p.add_argument('--in', dest='inp', default='data/contribution_draft.csv')
p.add_argument('--out', default='data/contribution_working.csv')
p.add_argument('--seed', type=int, default=42)
a = p.parse_args()

rows = list(csv.DictReader(open(a.inp, encoding='utf-8', newline='')))
by_label = defaultdict(list)
for r in rows:
    by_label[r['label']].append(r)

rng = random.Random(a.seed)
for label, items in by_label.items():
    rng.shuffle(items)
    n = len(items)
    n_train, n_dev = round(n * 0.6), round(n * 0.2)
    for i, r in enumerate(items):
        r['split'] = 'train' if i < n_train else 'dev' if i < n_train + n_dev else 'test'

for r in rows:
    if not r['source_url'].strip():
        r['source_url'] = 'not_applicable'
    if not r['reviewer_code'].strip():
        r['reviewer_code'] = 'pending'   # no independent reviewer yet

with open(a.out, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

from collections import Counter
print(len(rows), 'rows ->', a.out)
print(Counter(r['split'] for r in rows))
