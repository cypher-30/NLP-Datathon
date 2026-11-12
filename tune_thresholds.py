"""Choose the demo refusal thresholds for the v2 winner on DEV rows and English off-topic probes only (never test).
  python tune_thresholds.py
Result (12 Nov 2026, B_tuned_tfidf on v5): dev confidence >= 0.316, probes <= 0.231 -> MIN_CONFIDENCE 0.25, MIN_SIMILARITY 0.22."""
import sys, joblib, numpy as np, pandas as pd
sys.path.insert(0, '.'); import models_v2
from validate import check
p = joblib.load('artifacts/v2/B_tuned_tfidf.joblib'); m = p['model']
dev = check('data/contribution.csv', False, 'intent'); dev = dev[dev.split=='dev']
probes = ["Book me a flight to Nairobi tomorrow", "What is 245 times 12?", "Translate hello into French",
 "Send money to my brother", "Order a pizza", "Turn off the lights in the kitchen", "Call my mother",
 "How do I reset my password?", "Who won the election in 1980?", "Tell me a joke", "asdf qwerty zxcv",
 "Navigate to the nearest hospital", "Buy shares in Econet", "Write me a poem about rain", "ok", "Lock the front door"]
def feats(texts):
    pr = m.predict_proba(list(texts)); conf = pr.max(1)
    sim = (p['sim_vectorizer'].transform(list(texts)) @ p['train_matrix'].T).toarray().max(1)
    return conf, sim
dc, ds = feats(dev.text); pc, ps = feats(probes)
print("dev conf min/5%:", dc.min().round(3), np.percentile(dc,5).round(3), " dev sim min/5%:", ds.min().round(3), np.percentile(ds,5).round(3))
for t,c,s in sorted(zip(probes,pc,ps), key=lambda x:-x[1]): print(f"  probe conf {c:.3f} sim {s:.3f}  {t}")
for mc in [0.16,0.20,0.25,0.30,0.35]:
  for ms in [0.20,0.24,0.28]:
    rej_dev = ((dc<mc)|(ds<ms)).sum(); rej_pr = ((pc<mc)|(ps<ms)).sum()
    print(f"MIN_CONF {mc:.2f} MIN_SIM {ms:.2f}: dev refused {rej_dev}/50, probes refused {rej_pr}/{len(probes)}")
