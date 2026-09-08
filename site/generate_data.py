#!/usr/bin/env python3
"""Regenerate site/data.js from the analysis.

Every number rendered on the case-study site comes from this script, so the
page can never drift from the notebook. Run from the repository root:

    python site/generate_data.py
"""
import json
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

RANDOM_STATE = 42
OUTLIER_ID = 6390605          # 49,854 rounds in 14 days: bot or logging error

raw = pd.read_csv("cookie_cats.csv")
df = raw[raw["userid"] != OUTLIER_ID].copy()
D = {}

# ---- sample ratio check (computed on the raw assignment) ----
counts = raw["version"].value_counts()
n, k = len(raw), int(counts["gate_30"])
mean, sd = n * 0.5, (n * 0.25) ** 0.5
D["meta"] = {
    "n_total": int(n), "n_gate30": int(counts["gate_30"]), "n_gate40": int(counts["gate_40"]),
    "pct_gate30": round(counts["gate_30"] / n * 100, 2),
    "pct_gate40": round(counts["gate_40"] / n * 100, 2),
    "srm_p": round(float(stats.binomtest(k, n, 0.5).pvalue), 4),
    "srm_expected": round(mean, 1), "srm_observed": k,
    "srm_sd_players": round(sd, 1), "srm_z": round((k - mean) / sd, 2),
    "srm_dev_pp": round(abs(counts["gate_30"] / n - 0.5) * 100, 2),
    "sd_pp": round(sd / n * 100, 3),
    "outlier_rounds": int(raw["sum_gamerounds"].max()),
    "outlier_perday": int(round(raw["sum_gamerounds"].max() / 14)),
    "second_highest": int(raw["sum_gamerounds"].nlargest(2).iloc[1]),
}
xs = np.linspace(mean - 4 * sd, mean + 4 * sd, 121)
pdf = np.exp(-0.5 * ((xs - mean) / sd) ** 2)
D["srm_curve"] = {
    "x": [round(float(v), 1) for v in xs],
    "y": [round(float(v), 4) for v in pdf / pdf.max()],
    "lo2sd": round(float(mean - 2 * sd), 1), "hi2sd": round(float(mean + 2 * sd), 1),
}

# ---- engagement ----
sg = df["sum_gamerounds"]
hist, edges = np.histogram(sg[sg < 100], bins=50, range=(0, 100))
D["engagement"] = {
    "bins": [int(v) for v in hist], "edges": [float(round(e, 1)) for e in edges],
    "pct_zero": round(float((sg == 0).mean() * 100), 1),
    "median": int(sg.median()), "mean": round(float(sg.mean()), 1),
    "max": int(sg.max()), "p99": int(sg.quantile(0.99)),
}

# ---- retention, both horizons ----
def retention(col):
    g = df.groupby("version")[col]
    rates, ns = g.mean(), g.count()
    ci = 1.96 * np.sqrt(rates * (1 - rates) / ns)
    chi2, p, _, _ = chi2_contingency(pd.crosstab(df["version"], df[col]))
    succ = g.sum().loc[["gate_30", "gate_40"]].values
    nobs = g.count().loc[["gate_30", "gate_40"]].values
    z, _ = proportions_ztest(succ, nobs)
    out = {}
    for v in ("gate_30", "gate_40"):
        out[v] = {"rate": round(float(rates[v]) * 100, 2), "n": int(ns[v]),
                  "lo": round(float((rates - ci)[v]) * 100, 2),
                  "hi": round(float((rates + ci)[v]) * 100, 2)}
    out.update({
        "diff_pp": round(float(rates["gate_30"] - rates["gate_40"]) * 100, 2),
        "rel_pct": round(float((rates["gate_40"] - rates["gate_30"]) / rates["gate_30"]) * 100, 1),
        "chi2": round(float(chi2), 3), "p": float(f"{p:.5f}"),
        "z": round(float(z), 3), "significant": bool(p < 0.05),
    })
    return out

D["retention7"] = retention("retention_7")
D["retention1"] = retention("retention_1")
D["overall"] = {"r1": round(float(df["retention_1"].mean()) * 100, 2),
                "r7": round(float(df["retention_7"].mean()) * 100, 2)}

# ---- bootstrap ----
r7 = df["retention_7"].to_numpy().astype(float)
is30 = df["version"].to_numpy() == "gate_30"
N = len(df)
obs = r7[is30].mean() - r7[~is30].mean()
rng = np.random.default_rng(RANDOM_STATE)
boot = np.empty(1000)
for i in range(1000):
    idx = rng.integers(0, N, N)
    s7, s30 = r7[idx], is30[idx]
    boot[i] = s7[s30].mean() - s7[~s30].mean()
bpp = boot * 100
bh, bedges = np.histogram(bpp, bins=36)
D["bootstrap"] = {
    "values": [round(float(v), 3) for v in bpp],
    "bins": [int(v) for v in bh], "edges": [round(float(e), 3) for e in bedges],
    "ahead": int((boot > 0).sum()), "n": 1000,
    "ci_lo": round(float(np.percentile(bpp, 2.5)), 2),
    "ci_hi": round(float(np.percentile(bpp, 97.5)), 2),
    "observed": round(float(obs * 100), 2),
}

# ---- model, with and without the leaking feature ----
df["version_gate40"] = (df["version"] == "gate_40").astype(int)
df["retention_1_int"] = df["retention_1"].astype(int)
y = df["retention_7"].astype(int)

def fit(features):
    X = df[features].astype(float)
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
    sc = StandardScaler().fit(Xtr)
    m = LogisticRegression(max_iter=1000).fit(sc.transform(Xtr), ytr)
    proba = m.predict_proba(sc.transform(Xte))[:, 1]
    return m, roc_auc_score(yte, proba), float((m.predict(sc.transform(Xte)) == yte).mean())

feats = ["sum_gamerounds", "retention_1_int", "version_gate40"]
model, auc_leaky, acc = fit(feats)
_, auc_honest, _ = fit(["retention_1_int", "version_gate40"])
D["model"] = {
    "auc_leaky": round(float(auc_leaky), 3), "auc_honest": round(float(auc_honest), 3),
    "drop": round(float(auc_leaky - auc_honest), 3),
    "accuracy": round(acc, 3), "baseline": round(float(1 - y.mean()), 3),
    "coefs": [{"name": "sum_gamerounds", "v": round(float(model.coef_[0][0]), 3)},
              {"name": "retention_1", "v": round(float(model.coef_[0][1]), 3)},
              {"name": "version_gate40", "v": round(float(model.coef_[0][2]), 3)}],
}

with open("site/data.js", "w") as f:
    f.write("window.CC = " + json.dumps(D, separators=(",", ":")) + ";\n")
print("wrote site/data.js")
