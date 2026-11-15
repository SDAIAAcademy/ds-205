"""Helpers for the DS-205 labs: the data of Mashraq Municipal Permits Office, checks and safety nets.

    import mashraq as U

Plain NumPy, pandas, SciPy and the standard library. Nothing calls a model.

Environment variables
    DS205_QUICK=1      fewer simulated tests, for a fast run
    DS205_STRICT=1     solution runs: a failed check stops the run
    DS205_WRITE_REF=1  the trainer's run that writes data/reference/ (the safety nets read it)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

for _stream in (sys.stdout, sys.stderr):  # a Windows console or a redirected run may not default to UTF-8
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
REF = DATA / "reference"

QUICK = os.environ.get("DS205_QUICK", "0") == "1"
STRICT = os.environ.get("DS205_STRICT", "0") == "1"
WRITE_REF = os.environ.get("DS205_WRITE_REF", "0") == "1"
MODE = "quick" if QUICK else "full"
SEED = 205

MIN_EFFECT = 0.02    # the office's minimum effect of interest: 2 points of on-time renewal
ALPHA = 0.05         # two-sided
POWER = 0.80
RATIO_ALPHA = 0.001  # a sample ratio check fails below this p-value


def pick(full, quick):
    """The full value, or the small one in quick mode."""
    return quick if QUICK else full


def rng(offset: int = 0) -> np.random.Generator:
    """A seeded generator. The same offset gives the same draws on every run."""
    return np.random.default_rng(SEED + offset)


# ---------------------------------------------------------------- checks and safety nets

def check(ok, what: str) -> bool:
    """Print a tick or a cross. In a solution run (DS205_STRICT=1) a cross stops the run."""
    ok = bool(ok)
    print(("✅ " if ok else "❌ ") + what)
    if STRICT and not ok:
        raise AssertionError(what)
    return ok


def _jsonable(v):
    if isinstance(v, np.ndarray):
        return {"__array__": v.tolist()}
    if isinstance(v, (np.floating, np.integer, np.bool_)):
        return v.item()
    if isinstance(v, dict):
        return {str(k): _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def _unjson(v):
    if isinstance(v, dict):
        if "__array__" in v:
            return np.array(v["__array__"])
        return {k: _unjson(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_unjson(x) for x in v]
    return v


def keep(lab: str, name: str, value):
    """Return value. In the trainer's run, also store it as the reference of this exercise."""
    if WRITE_REF:
        REF.mkdir(parents=True, exist_ok=True)
        path = REF / f"{lab}.{MODE}.json"
        store = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        store[name] = _jsonable(value)
        path.write_text(json.dumps(store, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return value


def reference(lab: str, name: str):
    """The reference result of an exercise, so the cells after it run when it is not done yet."""
    if STRICT:
        raise AssertionError(f"the solution run reached the safety net of {lab}/{name}")
    print(f"↪ exercise not done yet: using the reference result for {name}")
    store = json.loads((REF / f"{lab}.{MODE}.json").read_text(encoding="utf-8"))
    return _unjson(store[name])


# ---------------------------------------------------------------- the data of the office

def history() -> pd.DataFrame:
    """182 days before the test: date, weekday, day_of_month, month_end, notices_sent, renewed_on_time."""
    return pd.read_csv(DATA / "history_daily.csv")


def units_notices() -> pd.DataFrame:
    """20,000 past notices with the key of the holder each belongs to (lab 1.3)."""
    return pd.read_csv(DATA / "units_notices.csv")


def renewal_test() -> pd.DataFrame:
    """The reminder test as assigned: 60,000 notices, one per holder, with arm, covariates and outcomes."""
    return pd.read_csv(DATA / "renewal_test.csv")


def notice_log() -> pd.DataFrame:
    """The messaging platform's export of the reminder test (lab 3.1). Something is wrong with it."""
    return pd.read_csv(DATA / "notice_log.csv")


def form_pages() -> pd.DataFrame:
    """The form redesign test: one row per page view; applicants were randomised."""
    return pd.read_csv(DATA / "form_pages.csv")


def branches() -> pd.DataFrame:
    """24 branches: branch, district, weekly_visitors, staff_pool (branches with the same pool share counter staff)."""
    return pd.read_csv(DATA / "branches.csv")


def counter_visits() -> pd.DataFrame:
    """Four baseline weeks of counter visits: visit_key, branch, week, served_within_15, wait_minutes."""
    return pd.read_csv(DATA / "counter_visits.csv")


def js(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def text(name: str) -> str:
    return (DATA / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------- statistics every lab may use

def n_per_arm(p1: float, delta: float, alpha: float = ALPHA, power: float = POWER) -> int:
    """Units per arm to detect p1 against p1 + delta with a two-sided two-proportion test."""
    p2 = p1 + delta
    za, zb = stats.norm.ppf(1 - alpha / 2), stats.norm.ppf(power)
    return int(np.ceil((za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / delta ** 2))


def z_test(x1, n1, x2, n2):
    """Two-proportion z-test, arm 2 minus arm 1. Works on numbers or arrays.

    Returns (difference, standard error for the interval, two-sided p-value). The p-value uses the
    pooled standard error, the interval the unpooled one, as most libraries do.
    """
    x1, n1, x2, n2 = (np.asarray(v, dtype=float) for v in (x1, n1, x2, n2))
    p1, p2 = x1 / n1, x2 / n2
    pooled = (x1 + x2) / (n1 + n2)
    se0 = np.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = np.where(se0 > 0, (p2 - p1) / se0, 0.0)
    p = 2 * stats.norm.sf(np.abs(z))
    if p.ndim == 0:
        return float(p2 - p1), float(se), float(p)
    return p2 - p1, se, p


def ratio_p(n1: int, n2: int) -> float:
    """p-value of the chi-square test that two arm counts come from a 50/50 split."""
    return float(stats.chisquare([n1, n2]).pvalue)


# ---------------------------------------------------------------- lab 1.1: six studies

DESIGNS = ("randomised", "quasi", "observational")
CLAIMS = {"cause": "the difference was caused by the change, for the units in the study",
          "cause_if": "the difference was caused by the change only if a stated assumption holds",
          "association": "the groups differ, and the study cannot say why"}


def mark_studies(sheet: dict) -> int:
    """Score a sheet {study id: (design, claim)} against the key. A study counts when both are right."""
    key = {s["id"]: s for s in js("studies_key.json")}
    score = 0
    for i in sorted(key):
        design, claim = sheet.get(i, ("", ""))
        ok = design == key[i]["design"] and claim == key[i]["claim"]
        score += ok
        print(f"{'✅' if ok else '❌'} {i}: you said {design or 'nothing'} / {claim or 'nothing'}; the key says {key[i]['design']} / {key[i]['claim']}")
        print(f"   {key[i]['why']}")
    print(f"score: {score} of {len(key)} (the outcome asks for at least 5)")
    return score


# ---------------------------------------------------------------- labs 1.2 and 1.4: the pre-registration and its checklist

CHECKLIST = [
    ("C1", "Decision", "The decision is written down, with what the office will do for each possible result"),
    ("C2", "Hypothesis", "The hypothesis names the change, the metric and the direction"),
    ("C3", "Unit", "The unit of randomisation is stated, and no person can land in both arms"),
    ("C4", "Primary metric", "There is exactly one primary metric, with its definition and time window"),
    ("C5", "Minimum effect", "The minimum effect of interest is a number, with the reason for it"),
    ("C6", "Guardrails", "Each guardrail has a metric, a threshold and the action when it is crossed"),
    ("C7", "Stop rule", "The stop rule fixes the end in advance and allows no early stop for a good result"),
    ("C8", "Size and duration", "The sample size comes from the minimum effect, and the run covers whole weeks and the month-end"),
    ("C9", "Analysis plan", "The analysis plan names the test, the interval, the unit of analysis and analysis as assigned"),
    ("C10", "Checks", "A sample ratio check and a balance check are planned before the result is read"),
    ("C11", "Arms and fairness", "It says who is in each arm, why withholding is acceptable and which guardrail protects a group from harm"),
    ("C12", "Data", "It says which fields are used, how they are minimised and pseudonymised, and that results are reported in aggregate"),
]


def _words(v) -> int:
    return len(str(v or "").split())


def _has(v, *needles) -> bool:
    low = str(v or "").lower()
    return all(any(x in low for x in (n if isinstance(n, tuple) else (n,))) for n in needles)


def prereg_check(r: dict, items=None, quiet: bool = False) -> dict:
    """The mechanical half of the reviewer's checklist: is each part there and specific?

    It cannot judge whether the choices are wise: that is the neighbour's review. `items` limits
    the check to some checklist ids, as in lab 1.2, which writes C1, C2, C4 to C7 and C11.
    """
    g = r.get("guardrails") or []
    primary = r.get("primary_metric")
    res = {
        "C1": _words(r.get("decision")) >= 15 and _has(r.get("decision"), "if"),
        "C2": _words(r.get("hypothesis")) >= 8 and _has(r.get("hypothesis"), ("raise", "increase", "lower", "reduce", "higher", "more", "fewer", "less")),
        "C3": _words(r.get("unit")) >= 1 and _words(r.get("unit_reason")) >= 8,
        "C4": isinstance(primary, dict) and _words(primary.get("name")) >= 2 and _words(primary.get("definition")) >= 8,
        "C5": isinstance(r.get("minimum_effect"), (int, float)) and 0 < r["minimum_effect"] < 1 and _words(r.get("minimum_effect_reason")) >= 8,
        "C6": len(g) >= 2 and all(_words(x.get("metric")) >= 1 and isinstance(x.get("threshold"), (int, float)) and _words(x.get("action")) >= 3 for x in g),
        "C7": _words(r.get("stop_rule")) >= 12 and _has(r.get("stop_rule"), ("no early", "not stop early", "fixed", "one analysis", "single analysis")),
        "C8": isinstance(r.get("sample_size_per_arm"), (int, float)) and r["sample_size_per_arm"] > 0 and isinstance(r.get("duration_days"), int) and r["duration_days"] % 7 == 0,
        "C9": _has(r.get("analysis_plan"), ("z-test", "test of two proportions", "two-proportion"), "interval", ("as assigned", "as randomised", "intention")),
        "C10": _has(r.get("checks"), "ratio", "balance"),
        "C11": _words(r.get("arms")) >= 12 and _words(r.get("withholding")) >= 10 and any(_has(x.get("metric"), ("group", "channel", "holder type", "subgroup")) for x in g),
        "C12": _words(r.get("data")) >= 15 and _has(r.get("data"), ("pseudonym", "key"), ("aggregate", "group", "never by holder")),
    }
    if items is not None:
        res = {k: v for k, v in res.items() if k in items}
    if not quiet:
        for cid, name, meaning in CHECKLIST:
            if cid in res:
                print(f"{'✅' if res[cid] else '❌'} {cid} {name}: {meaning}")
        print(f"passed: {sum(res.values())} of {len(res)}")
    return res


def mark_review(review: dict) -> int:
    """Score a review {checklist id: 'pass' or 'fail'} of the neighbour's pre-registration against the key."""
    key = js("prereg_neighbour_key.json")
    score = 0
    for cid, name, _ in CHECKLIST:
        said = review.get(cid, "")
        ok = said == key[cid]["verdict"]
        score += ok
        print(f"{'✅' if ok else '❌'} {cid} {name}: you said {said or 'nothing'}; the key says {key[cid]['verdict']}. {key[cid]['reason']}")
    print(f"score: {score} of {len(CHECKLIST)}")
    return score


def show_prereg(r: dict) -> None:
    """Print a pre-registration record as the one-page form."""
    for k, v in r.items():
        if isinstance(v, list):
            print(f"{k}:")
            for x in v:
                print("   -", json.dumps(x, ensure_ascii=False) if isinstance(x, dict) else x)
        elif isinstance(v, dict):
            print(f"{k}: " + "; ".join(f"{a}: {b}" for a, b in v.items()))
        else:
            print(f"{k}: {v}")


# ---------------------------------------------------------------- lab 3.2: the result in two sentences

def sentence_check(text_: str, numbers: dict, words: list) -> bool:
    """Does the text quote every number (as formatted) and use every required word?"""
    ok = True
    for name, shown in numbers.items():
        found = str(shown) in text_
        ok &= found
        print(f"{'✅' if found else '❌'} quotes the {name}: {shown}")
    low = text_.lower()
    for w in words:
        alts = w if isinstance(w, tuple) else (w,)
        found = any(a.lower() in low for a in alts)
        ok &= found
        print(f"{'✅' if found else '❌'} says: {' or '.join(alts)}")
    n_sent = sum(text_.count(c) for c in ".!?") - sum(text_.count(f"{d}.{e}") for d in "0123456789" for e in "0123456789")
    print(f"length: {len(text_.split())} words, about {max(n_sent, 1)} sentences")
    if STRICT and not ok:
        raise AssertionError("the text misses a number or a required statement")
    return ok


# ---------------------------------------------------------------- lab 3.4: flaws in a write-up

def flaw_catalogue() -> None:
    for f in js("writeup_form_key.json")["catalogue"]:
        print(f"{f['flaw']:<22} {f['meaning']}")


def mark_flaws(found: dict) -> tuple:
    """Score {flaw id: True or False} against the key. Returns (flaws found, false alarms)."""
    key = {k["flaw"]: k for k in js("writeup_form_key.json")["key"]}
    hits = alarms = 0
    for f, k in key.items():
        said = bool(found.get(f, False))
        if k["present"] and said:
            hits += 1
        if not k["present"] and said:
            alarms += 1
        mark = "✅" if said == k["present"] else "❌"
        print(f"{mark} {f}: you said {'present' if said else 'absent'}; the key says {'present' if k['present'] else 'absent'}")
        print(f"   {(k['where'] + '. ') if k['where'] else ''}{k['consequence']}")
    total = sum(k["present"] for k in key.values())
    print(f"found {hits} of {total} seeded flaws, with {alarms} false alarm(s)")
    return hits, alarms


# ---------------------------------------------------------------- plotting and tables

def plt():
    """matplotlib.pyplot with the course defaults; draws to nothing when run as a script."""
    import matplotlib
    if "ipykernel" not in sys.modules:
        import warnings
        matplotlib.use("Agg")
        warnings.filterwarnings("ignore", message=".*non-interactive.*")
    import matplotlib.pyplot as p
    p.rcParams.update({"figure.figsize": (7, 4), "axes.spines.top": False, "axes.spines.right": False,
                       "axes.grid": True, "grid.alpha": 0.25, "font.size": 11})
    return p


def table(header: list, rows: list, fmt: str = "{:.4g}") -> None:
    """Print a small aligned table."""
    cells = [[fmt.format(v) if isinstance(v, (float, np.floating)) else str(v) for v in r] for r in rows]
    widths = [max(len(h), *(len(r[i]) for r in cells)) for i, h in enumerate(header)]
    print("  ".join(h.ljust(w) for h, w in zip(header, widths)))
    for r in cells:
        print("  ".join(c.rjust(w) for c, w in zip(r, widths)))


def note(*lines: str) -> None:
    """The verification note that closes every lab: what was checked, and what was not."""
    print("VERIFICATION NOTE")
    for line in lines:
        print(" ·", line)
