"""Write the synthetic data of Mashraq Municipal Permits Office into labs/data/ and labs/capstone/.

    uv run python prepare_data.py

Fixed seed, the same bytes on every run. Mashraq is fictional: no real office, permit holder,
applicant or branch is described. The files are committed; run this only to rebuild them.

What is planted, and which lab finds it, is listed in solutions/answer_key.md. The true values
the generator used are written to solutions/truth.json.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

SEED = 205
LABS = Path(__file__).resolve().parent
DATA = LABS / "data"
CAP = LABS / "capstone"
SOL = LABS / "solutions"

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
HISTORY_START = date(2026, 3, 1)   # a Sunday; 182 days of history
TEST_START = date(2026, 9, 6)      # a Sunday; the reminder test runs 28 days
N_TEST = 60_000
MIN_EFFECT = 0.02                  # the office's minimum effect of interest: 2 points of on-time renewal

TRUTH: dict = {}


def gen(k: int) -> np.random.Generator:
    return np.random.default_rng([SEED, k])


def keys(rng, n: int, prefix: str) -> np.ndarray:
    """Pseudonymised keys: a prefix and eight hexadecimal digits, unique, in no meaningful order."""
    out: set = set()
    while len(out) < n:
        out.update(f"{prefix}{v:08x}" for v in rng.integers(0, 16 ** 8, size=n - len(out)))
    arr = np.array(sorted(out))
    rng.shuffle(arr)
    return arr


def write(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, lineterminator="\n")


def write_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def write_json(obj, path: Path) -> None:
    write_text(json.dumps(obj, ensure_ascii=False, indent=1), path)


def z_p(x1, n1, x2, n2) -> float:
    """Two-sided p-value of the pooled two-proportion z-test."""
    p = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    return float(2 * stats.norm.sf(abs((x2 / n2 - x1 / n1) / se)))


# ------------------------------------------------------------------ calendar and traffic

def calendar(start: date, days: int) -> pd.DataFrame:
    d = [start + timedelta(days=i) for i in range(days)]
    cal = pd.DataFrame({"date": [x.isoformat() for x in d],
                        "weekday": [WEEKDAYS[x.weekday()] for x in d],
                        "day_of_month": [x.day for x in d]})
    cal["weekend"] = cal["weekday"].isin(["Fri", "Sat"]).astype(int)
    cal["month_end"] = (cal["day_of_month"] >= 26).astype(int)
    return cal


def expected_traffic(cal: pd.DataFrame) -> np.ndarray:
    base = cal["weekday"].map({"Sun": 2300, "Mon": 2350, "Tue": 2300, "Wed": 2250, "Thu": 2150, "Fri": 1100, "Sat": 1400}).to_numpy(float)
    return base * np.where(cal["month_end"] == 1, 1.5, 1.0)


def history_daily() -> pd.DataFrame:
    rng = gen(1)
    cal = calendar(HISTORY_START, 182)
    sent = rng.poisson(expected_traffic(cal))
    rate = 0.636 - 0.04 * cal["weekend"] - 0.05 * cal["month_end"] + rng.normal(0, 0.006, len(cal))
    cal["notices_sent"] = sent
    cal["renewed_on_time"] = rng.binomial(sent, rate)
    TRUTH["history"] = {"days": 182, "notices": int(sent.sum()), "baseline": round(float(cal["renewed_on_time"].sum() / sent.sum()), 4),
                        "mean_daily": round(float(sent.mean()), 1)}
    return cal


# ------------------------------------------------------------------ past notices with holder keys (lab 1.3)

def units_notices() -> pd.DataFrame:
    rng = gen(2)
    n_holders = 15_400
    permits = rng.choice([1, 2, 3, 4, 5], size=n_holders, p=[0.80, 0.13, 0.045, 0.018, 0.007])
    holder = np.repeat(keys(rng, n_holders, "H"), permits)
    propensity = np.repeat(rng.beta(1.1, 0.68, n_holders), permits)   # a holder renews everything on time, or little
    df = pd.DataFrame({"notice_key": keys(rng, len(holder), "N"), "holder_key": holder,
                       "permit_type": rng.choice(["resident parking", "market stall", "outdoor seating", "building works"], size=len(holder), p=[0.52, 0.2, 0.16, 0.12]),
                       "renewed_on_time": rng.binomial(1, propensity)})
    df = df.sample(frac=1.0, random_state=SEED).reset_index(drop=True).head(20_000)
    per = df.groupby("holder_key").size()
    TRUTH["units_notices"] = {"notices": len(df), "holders": int(per.size), "share_notices_multi": round(float(per[per > 1].sum() / len(df)), 4)}
    return df


# ------------------------------------------------------------------ the reminder test

def reminder_test() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rng = gen(3)
    cal = calendar(TEST_START, 28)
    w = expected_traffic(cal)
    per_day = rng.multinomial(N_TEST, w / w.sum())
    day = np.repeat(np.arange(28), per_day)
    n = N_TEST
    df = pd.DataFrame({"notice_key": keys(rng, n, "N"),
                       "sent_date": cal["date"].to_numpy()[day],
                       "test_day": day + 1,
                       "weekday": cal["weekday"].to_numpy()[day],
                       "month_end": cal["month_end"].to_numpy()[day]})
    weekend = cal["weekend"].to_numpy()[day]
    df["permit_type"] = rng.choice(["resident parking", "market stall", "outdoor seating", "building works"], size=n, p=[0.52, 0.2, 0.16, 0.12])
    df["holder_type"] = np.where(df["permit_type"] == "resident parking", "resident", np.where(rng.random(n) < 0.8, "business", "resident"))
    df["channel"] = rng.choice(["sms", "email"], size=n, p=[0.85, 0.15])
    df["prior_late"] = rng.binomial(1, 0.22, n)
    df["tenure_years"] = np.clip(np.round(rng.gamma(2.2, 2.1, n), 1), 0.1, 30)
    df["arm"] = np.where(rng.random(n) < 0.5, "reminder", "control")   # one seeded coin per holder

    treat = (df["arm"] == "reminder").to_numpy()
    email = (df["channel"] == "email").to_numpy()
    late = df["prior_late"].to_numpy()
    peak = df["month_end"].to_numpy()
    type_shift = df["permit_type"].map({"resident parking": 0.03, "market stall": -0.02, "outdoor seating": 0.0, "building works": -0.05}).to_numpy()
    undelivered = treat & email & (df["test_day"].to_numpy() <= 7)   # the planted fault: the reminder job failed for e-mail in week 1
    received = treat & ~undelivered

    p0 = 0.70 - 0.16 * email - 0.18 * late + type_shift - 0.04 * weekend - 0.05 * peak
    tau = 0.020 + 0.020 * peak + 0.025 * late - 0.010 * weekend
    p = np.clip(p0 + tau * received, 0.02, 0.98)
    df["renewed_on_time"] = rng.binomial(1, p)
    df["complained"] = rng.binomial(1, 0.009 + 0.002 * received)
    df["counter_visit"] = rng.binomial(1, np.clip(0.14 + 0.03 * late - 0.015 * received, 0, 1))

    assignment = df[["notice_key", "sent_date", "test_day", "weekday", "month_end", "permit_type", "holder_type", "channel", "prior_late", "tenure_years", "arm"]]
    log = df.loc[~undelivered, ["notice_key", "sent_date", "test_day", "arm", "permit_type", "holder_type", "channel", "prior_late", "tenure_years", "renewed_on_time"]]

    c, t = df[~treat], df[treat]
    lc, lt = log[log["arm"] == "control"], log[log["arm"] == "reminder"]
    TRUTH["reminder_test"] = {
        "notices": n, "control": int(len(c)), "reminder": int(len(t)),
        "true_effect_if_everyone_received": round(float(tau.mean()), 4),
        "true_effect_as_assigned": round(float((tau * ~(email & (df["test_day"].to_numpy() <= 7))).mean()), 4),
        "estimate_as_assigned": round(float(t["renewed_on_time"].mean() - c["renewed_on_time"].mean()), 4),
        "log_rows": int(len(log)), "log_control": int(len(lc)), "log_reminder": int(len(lt)), "missing_rows": int(undelivered.sum()),
        "estimate_from_log": round(float(lt["renewed_on_time"].mean() - lc["renewed_on_time"].mean()), 4),
        "srm_p_assignment": float(stats.chisquare([len(c), len(t)]).pvalue), "srm_p_log": float(stats.chisquare([len(lc), len(lt)]).pvalue),
        "complaints": [round(float(c["complained"].mean()), 4), round(float(t["complained"].mean()), 4)],
        "counter_visits": [round(float(c["counter_visit"].mean()), 4), round(float(t["counter_visit"].mean()), 4)],
    }
    return assignment, df, log


# ------------------------------------------------------------------ the form redesign, page-level log

def form_pages_once(k: int):
    rng = gen(k)
    rows = []
    planned_days = 28
    per_day = rng.poisson(np.tile([760, 780, 770, 740, 700, 380, 470], 4))   # starts on a Sunday
    n = int(per_day.sum())
    day = np.repeat(np.arange(1, planned_days + 1), per_day)
    arm = np.where(rng.random(n) < 0.5, "redesign", "current")
    device = rng.choice(["desktop", "mobile", "old mobile"], size=n, p=[0.55, 0.33, 0.12])
    kind = rng.choice(["resident", "business"], size=n, p=[0.64, 0.36])
    key = keys(rng, n, "A")
    e = rng.beta(0.6, 4.4, n) * np.where(device == "old mobile", 1.35, 1.0) * np.where(arm == "redesign", 0.97, 1.0)
    e = np.clip(e, 0, 0.95)
    views = 1 + rng.negative_binomial(1.3, 0.12, n)       # page views per applicant: most a few, some dozens
    views = np.clip(views, 1, 70)
    p_done = np.clip(0.60 - 0.9 * (e - 0.12) - 0.06 * (device == "old mobile") + 0.010 * (arm == "redesign"), 0.05, 0.95)
    done = rng.random(n) < p_done
    keep = ~((arm == "redesign") & (device == "old mobile"))   # the planted attrition: the redesign crashed on old mobile browsers, nothing was logged
    for i in np.flatnonzero(keep):
        last = 8 if done[i] else int(rng.integers(1, 8))
        pages = np.sort(rng.integers(1, last + 1, views[i]))
        if done[i]:
            pages[-1] = 8
        errs = rng.random(views[i]) < e[i]
        for j in range(views[i]):
            rows.append((key[i], arm[i], int(day[i]), device[i], kind[i], j + 1, int(pages[j]), int(errs[j]), int(done[i])))
    df = pd.DataFrame(rows, columns=["applicant_key", "arm", "day", "device", "applicant_type", "page_view", "page", "validation_error", "completed"])

    # the author looked every day and stopped at the first day (from day 6) with a page-level p below 0.05
    stop, daily = None, []
    for d in range(1, planned_days + 1):
        s = df[df["day"] <= d]
        a, b = s[s["arm"] == "current"], s[s["arm"] == "redesign"]
        p = z_p(a["validation_error"].sum(), len(a), b["validation_error"].sum(), len(b))
        daily.append(round(p, 4))
        if stop is None and d >= 8 and p < 0.05:
            stop = d
    if stop is None or stop > 11:
        return None
    out = df[df["day"] <= stop].reset_index(drop=True)
    s = form_summary(out)
    if s["error_p_applicant_level"] < 0.10 or s["completion_p"] < 0.15 or s["error_p_page_level"] > 0.02:
        return None
    TRUTH["form_test"] = {"planned_days": planned_days, "stop_day": stop, "daily_page_level_p": daily[:stop], "generator_draw": k, **s}
    return out, stop, s


def form_pages():
    """The write-up's story needs a draw in which the page-level test crosses 0.05 between days 8 and 11
    while the applicant-level test does not. Draws 40 to 67 did not fit; draw 68 is the first that does,
    and the search starts there so that a rebuild takes a minute."""
    for k in range(68, 140):
        got = form_pages_once(k)
        if got is not None:
            return got
    raise SystemExit("form test: no draw fits the write-up")


def form_summary(df: pd.DataFrame) -> dict:
    a, b = df[df["arm"] == "current"], df[df["arm"] == "redesign"]
    ua, ub = a.drop_duplicates("applicant_key"), b.drop_duplicates("applicant_key")
    per_a = a.groupby("applicant_key")["validation_error"].mean()
    per_b = b.groupby("applicant_key")["validation_error"].mean()
    common = df[df["device"] != "old mobile"]
    ca, cb = common[common["arm"] == "current"], common[common["arm"] == "redesign"]
    uca, ucb = ca.drop_duplicates("applicant_key"), cb.drop_duplicates("applicant_key")
    best = None
    for (kind, dev), g in common.groupby(["applicant_type", "device"]):
        ga, gb = g[g["arm"] == "current"], g[g["arm"] == "redesign"]
        red = 1 - gb["validation_error"].mean() / ga["validation_error"].mean()
        if best is None or red > best[2]:
            best = (kind, dev, float(red))
    return {
        "applicants": [int(len(ua)), int(len(ub))], "page_views": [int(len(a)), int(len(b))],
        "srm_p": float(stats.chisquare([len(ua), len(ub)]).pvalue),
        "error_rate_page": [round(float(a["validation_error"].mean()), 4), round(float(b["validation_error"].mean()), 4)],
        "error_p_page_level": z_p(a["validation_error"].sum(), len(a), b["validation_error"].sum(), len(b)),
        "error_p_applicant_level": float(stats.ttest_ind(per_a, per_b, equal_var=False).pvalue),
        "completion": [round(float(ua["completed"].mean()), 4), round(float(ub["completed"].mean()), 4)],
        "completion_p": z_p(ua["completed"].sum(), len(ua), ub["completed"].sum(), len(ub)),
        "old_mobile_applicants": [int((ua["device"] == "old mobile").sum()), int((ub["device"] == "old mobile").sum())],
        "completion_common_devices": [round(float(uca["completed"].mean()), 4), round(float(ucb["completed"].mean()), 4)],
        "completion_p_common_devices": z_p(uca["completed"].sum(), len(uca), ucb["completed"].sum(), len(ucb)),
        "best_subgroup": {"applicant_type": best[0], "device": best[1], "relative_reduction": round(best[2], 3)},
    }


FLAWS = [
    ("metric_switch", "The headline metric is not the pre-registered primary metric"),
    ("wrong_unit", "The analysis counts a different unit from the one that was randomised"),
    ("peeking", "The result was checked repeatedly and the test stopped when it turned significant"),
    ("ratio_mismatch", "The arms are not the size the design promised, and units are missing from one arm"),
    ("many_comparisons", "Many metrics or subgroups were examined and the best ones reported"),
    ("short_run", "The run covers no whole weekly cycle or month-end, and first-week behaviour may fade"),
    ("overclaim", "The recommendation reaches beyond the units, the metric or the period that were tested"),
    ("no_control", "There is no concurrent control group"),
    ("not_random", "Assignment was not random"),
    ("different_measurement", "The outcome was measured differently in the two arms"),
]


def form_writeup(s: dict, stop: int) -> tuple[str, list]:
    e0, e1 = s["error_rate_page"]
    c0, c1 = s["completion"]
    b = s["best_subgroup"]
    text = f"""
# Result: the redesigned application form works. Roll it out to every form.

**Author:** Hattan Al-Sayed, digital services analyst. **To:** Rehab Al-Tayyar, digital services lead.
**Test:** current form against redesigned form for the outdoor-seating permit application.

## What we planned

The pre-registration of 2 August named one primary metric, the share of applicants who complete the
application, a minimum effect of 3 points, applicants as the unit of randomisation (a seeded coin per
applicant, half to each form) and a run of 28 days with one analysis at the end.

## What we did

We watched the dashboard every morning. On day {stop} the difference in validation errors was clearly
significant, so we stopped the test to give the better form to everyone sooner.

## Results

| | Current form | Redesigned form |
|---|---|---|
| Applicants in the log | {s['applicants'][0]:,} | {s['applicants'][1]:,} |
| Page views | {s['page_views'][0]:,} | {s['page_views'][1]:,} |
| Validation errors per page view | {e0:.1%} | {e1:.1%} |
| Applicants who completed | {c0:.1%} | {c1:.1%} |

- Validation errors per page view fell from {e0:.1%} to {e1:.1%}, a relative fall of {1 - e1 / e0:.0%}. With
  {sum(s['page_views']):,} page views the difference is highly significant (two-proportion z-test, p {('= %.3f' % s['error_p_page_level']) if s['error_p_page_level'] >= 0.001 else 'below 0.001'}).
- Completion moved in the right direction, from {c0:.1%} to {c1:.1%} (p = {s['completion_p']:.2f}). We expect it to become
  significant with more data.
- We examined 14 metrics in all. The fall in validation errors is the clearest. It is strongest among
  {b['applicant_type']} applicants on {b['device']}, where errors fell by {b['relative_reduction']:.0%}.
- The redesigned form logged fewer applicants. We put this down to chance.

## Recommendation

The redesign is proven to reduce errors. Replace all of the office's online forms with the new design
this month. We estimate at least 9,000 more completed applications a year.
"""
    key = [
        {"flaw": "metric_switch", "present": True, "where": "Results, first bullet, against 'What we planned'",
         "consequence": "The pre-registered primary metric, completion, shows no clear effect. The headline was chosen after seeing the data, so its p-value is not the test that was planned.",
         },
        {"flaw": "wrong_unit", "present": True, "where": "Results, first bullet: a z-test on page views",
         "consequence": "Applicants were randomised and each produced many page views that resemble each other. Counting page views as independent makes the standard error too small. At the applicant level the difference in errors is not significant."},
        {"flaw": "peeking", "present": True, "where": "What we did: watched every morning, stopped on the first significant day",
         "consequence": f"Stopping at the first p below 0.05 among {stop} daily looks gives a false-win rate far above 5% when nothing differs (lab 3.3 measures it)."},
        {"flaw": "ratio_mismatch", "present": True, "where": "Results table, first row, and the last bullet",
         "consequence": "A fair coin does not produce these two counts. No applicant on an old mobile browser is logged in the redesigned arm: the form failed for them. The arms no longer hold comparable applicants, and the missing ones make more errors."},
        {"flaw": "many_comparisons", "present": True, "where": "Results, third bullet: 14 metrics and the best subgroup",
         "consequence": "With 14 metrics and several subgroups, some difference will look large by chance. The subgroup was chosen because it was the largest."},
        {"flaw": "short_run", "present": True, "where": f"What we did: {stop} days of a planned 28",
         "consequence": "No second weekend, no month-end, and applicants seeing a new form for the first time: the estimate describes one unusual stretch."},
        {"flaw": "overclaim", "present": True, "where": "Recommendation",
         "consequence": "One form was tested. 'Proven', 'all forms' and '9,000 a year' are not supported by any number in the write-up."},
        {"flaw": "no_control", "present": False, "where": "", "consequence": "There is a concurrent control arm: the current form."},
        {"flaw": "not_random", "present": False, "where": "", "consequence": "Assignment was a seeded coin per applicant. The arms went wrong after assignment, not in it."},
        {"flaw": "different_measurement", "present": False, "where": "", "consequence": "Both arms use the same log and the same definitions."},
    ]
    return text, key


# ------------------------------------------------------------------ 24 branches and their counters

def branches() -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = gen(5)
    b = 24
    name = [f"B{i + 1:02d}" for i in range(b)]
    weekly = np.round(rng.lognormal(np.log(115), 0.45, b)).astype(int)
    weekly = np.clip(weekly, 45, 320)
    rate = np.clip(rng.normal(0.60, 0.085, b), 0.38, 0.82)
    pool = [f"P{i + 1:02d}" for i in range(b)]
    for x, y in ((2, 3), (10, 11), (18, 19)):       # three pairs of neighbouring branches share counter staff
        pool[y] = pool[x]
    br = pd.DataFrame({"branch": name, "district": [f"D{1 + i // 4}" for i in range(b)], "weekly_visitors": weekly, "staff_pool": pool})
    rows = []
    for i in range(b):
        for week in range(1, 5):
            nv = int(rng.poisson(weekly[i]))
            pw = np.clip(rate[i] + rng.normal(0, 0.02), 0.05, 0.95)
            ok = rng.binomial(1, pw, nv)
            wait = np.where(ok == 1, rng.uniform(1, 15, nv), 15 + rng.gamma(2.0, 9.0, nv))
            for j in range(nv):
                rows.append((name[i], week, int(ok[j]), round(float(wait[j]), 1)))
    v = pd.DataFrame(rows, columns=["branch", "week", "served_within_15", "wait_minutes"])
    v.insert(0, "visit_key", keys(rng, len(v), "V"))
    TRUTH["branches"] = {"branches": b, "visits": int(len(v)), "overall_rate": round(float(v["served_within_15"].mean()), 4),
                         "true_branch_rates": dict(zip(name, np.round(rate, 3).tolist())), "shared_pools": ["B03+B04", "B11+B12", "B19+B20"]}
    return br, v


# ------------------------------------------------------------------ six studies (lab 1.1)

STUDIES = [
    {"id": "S1", "text": "The office wants to know whether a rewritten renewal message works. A seeded random number generator picks 5,000 permit holders for the rewritten message; another 5,000, picked the same way, get the standard one. On-time renewal is compared between the two groups.",
     "design": "randomised", "claim": "cause",
     "why": "Chance alone decided who got which message, so the two groups differ only in the message, apart from sampling error. The difference is the effect of the message for these holders."},
    {"id": "S2", "text": "Eight branch managers volunteered to install a queue kiosk in spring. By autumn the average wait in their branches is 6 minutes shorter than in the 16 branches without a kiosk.",
     "design": "observational", "claim": "association",
     "why": "Managers who volunteer differ from those who do not, and so do their branches. The gap mixes the kiosk with everything else that goes with volunteering."},
    {"id": "S3", "text": "Market stalls under 10 square metres pay no inspection fee; larger stalls pay it. An analyst compares on-time renewal among stalls of 9.0 to 9.9 square metres with stalls of 10.0 to 10.9 square metres.",
     "design": "quasi", "claim": "cause_if",
     "why": "Nobody randomised the fee, but stalls just under and just over the line are alike. The gap is the effect of the fee for stalls near 10 square metres, if nothing else changes at the line and holders cannot pick their side of it."},
    {"id": "S4", "text": "Online booking was switched on in the six northern branches in June and nowhere else. An analyst compares the change in missed appointments from May to July in the northern branches with the change over the same months in the 18 other branches.",
     "design": "quasi", "claim": "cause_if",
     "why": "A comparison of changes, with a group that did not get the change. It supports a causal claim if the two groups would have moved in parallel without online booking."},
    {"id": "S5", "text": "A survey of 2,000 permit holders finds that 81% of those who use the office's mobile app renewed on time, against 58% of those who do not use it.",
     "design": "observational", "claim": "association",
     "why": "Holders chose whether to use the app. Organised holders may do both things. The survey shows that the two go together, not that the app causes renewal."},
    {"id": "S6", "text": "The office has 400 fast-track inspection slots and 1,900 applicants. A recorded lottery allocates the slots. Days from application to permit are compared between applicants who won a slot and those who did not.",
     "design": "randomised", "claim": "cause",
     "why": "A lottery is randomisation, whoever ran it and for whatever reason. The difference is the effect of the fast track for these applicants."},
]


# ------------------------------------------------------------------ the capstone cases

def capstone_a() -> None:
    """Case A: a reminder message for the annual stall inspection. The first draw whose estimate lies
    between 1.5 and 2.6 points is kept: a real effect, smaller than the minimum effect."""
    for k in range(110, 200):
        if capstone_a_once(k):
            return
    raise SystemExit("case A: no draw fits")


def capstone_a_once(k: int) -> bool:
    rng = gen(k)
    cal = calendar(date(2026, 3, 1), 84)
    exp = cal["weekday"].map({"Sun": 520, "Mon": 540, "Tue": 530, "Wed": 500, "Thu": 470, "Fri": 210, "Sat": 300}).to_numpy(float) * np.where(cal["month_end"] == 1, 1.35, 1.0)
    cal["holders_notified"] = rng.poisson(exp)
    cal["booked_within_14_days"] = rng.binomial(cal["holders_notified"], 0.41 - 0.05 * cal["weekend"] - 0.03 * cal["month_end"])
    write(cal.drop(columns=["weekend"]), CAP / "data" / "a_history.csv")

    tcal = calendar(date(2026, 9, 6), 28)
    w = exp[:28] * 1.0
    per_day = rng.multinomial(13_000, w / w.sum())
    day = np.repeat(np.arange(28), per_day)
    n = len(day)
    n_h = 11_900
    holder = keys(rng, n_h, "H")
    hk = np.concatenate([holder, rng.choice(holder, n - n_h, replace=False)])   # some holders have two stalls: two notices
    rng.shuffle(hk)
    arm_h = dict(zip(holder, np.where(rng.random(n_h) < 0.5, "deadline message", "standard message")))
    prop_h = dict(zip(holder, rng.normal(0, 0.10, n_h)))
    arm = np.array([arm_h[k] for k in hk])
    peak = tcal["month_end"].to_numpy()[day]
    wk = tcal["weekend"].to_numpy()[day]
    lang = rng.choice(["ar", "en"], size=n, p=[0.78, 0.22])
    p = np.clip(0.41 - 0.05 * wk - 0.03 * peak + np.array([prop_h[k] for k in hk]) + 0.022 * (arm == "deadline message"), 0.02, 0.98)
    df = pd.DataFrame({"notice_key": keys(rng, n, "N"), "holder_key": hk, "sent_date": tcal["date"].to_numpy()[day], "test_day": day + 1,
                       "arm": arm, "language": lang, "stall_district": rng.choice([f"D{i}" for i in range(1, 7)], size=n),
                       "booked_within_14_days": rng.binomial(1, p), "complained": rng.binomial(1, 0.006 + 0.007 * (arm == "deadline message"))})
    c, t = df[df["arm"] == "standard message"], df[df["arm"] == "deadline message"]
    est = t["booked_within_14_days"].mean() - c["booked_within_14_days"].mean()
    if not 0.015 <= est <= 0.026:
        return False
    write(df, CAP / "data" / "a_experiment.csv")
    first = df[df["test_day"] <= 10]
    fc, ft = first[first["arm"] == "standard message"], first[first["arm"] == "deadline message"]
    TRUTH["capstone_a"] = {"notices": n, "holders": n_h, "true_effect": 0.022, "minimum_effect": 0.03,
                           "estimate": round(float(t["booked_within_14_days"].mean() - c["booked_within_14_days"].mean()), 4),
                           "p_notice_level": z_p(c["booked_within_14_days"].sum(), len(c), t["booked_within_14_days"].sum(), len(t)),
                           "complaints": [round(float(c["complained"].mean()), 4), round(float(t["complained"].mean()), 4)],
                           "planted": "holders with two stalls appear twice (the unit is the holder); the complaint guardrail is breached; the true effect is below the minimum effect"}
    write_text(f"""
# Write-up A: the deadline message doubles as a quick win

**Author:** an analyst of the inspections team. **Test:** standard inspection notice against a notice that
states the deadline and the fine, sent to market-stall holders for 28 days.

The pre-registration named the share of holders who book an inspection within 14 days as the primary
metric, a minimum effect of 3 points, complaints as a guardrail (stop if the new message raises the
complaint rate by more than a quarter of a point) and the holder as the unit.

After 10 days the booking rate was {fc['booked_within_14_days'].mean():.1%} with the standard notice and {ft['booked_within_14_days'].mean():.1%} with the deadline message
({len(first):,} notices). We kept looking each day after that. Over the full 28 days and {n:,} notices the rates were
{c['booked_within_14_days'].mean():.1%} and {t['booked_within_14_days'].mean():.1%} (z-test on notices, p = {z_p(c['booked_within_14_days'].sum(), len(c), t['booked_within_14_days'].sum(), len(t)):.3f}).

Among English-language notices in district D3 the gain was much larger. Complaints were rare in both arms
and we did not analyse them further.

**Recommendation.** The deadline message improves booking. Adopt it for all permit types.
""", CAP / "a_writeup.md")
    return True


def capstone_b() -> None:
    """Case B: a redesigned form for building-works permits."""
    rng = gen(12)
    hist = calendar(date(2026, 3, 1), 84)
    hist["applicants"] = rng.poisson(hist["weekday"].map({"Sun": 300, "Mon": 310, "Tue": 300, "Wed": 290, "Thu": 270, "Fri": 120, "Sat": 160}).to_numpy(float))
    hist["completed"] = rng.binomial(hist["applicants"], 0.47 - 0.03 * hist["weekend"])
    write(hist.drop(columns=["weekend", "month_end"]), CAP / "data" / "b_history.csv")

    n = 6_000
    day = np.sort(rng.integers(1, 29, n))
    arm = np.where(rng.random(n) < 0.5, "redesign", "current")
    role = rng.choice(["owner", "contractor"], size=n, p=[0.7, 0.3])
    e = np.clip(rng.beta(0.7, 4.0, n) * np.where(arm == "redesign", 0.80, 1.0), 0, 0.95)
    views = np.clip(1 + rng.negative_binomial(1.2, 0.14, n) * np.where(role == "contractor", 2, 1), 1, 90)
    p_done = np.clip(0.47 - 0.8 * (e - 0.15) + 0.035 * (arm == "redesign"), 0.05, 0.95)
    done = (rng.random(n) < p_done)
    key = keys(rng, n, "A")
    rows = []
    for i in range(n):
        errs = rng.random(views[i]) < e[i]
        secs = np.round(rng.gamma(2.0, 30 if arm[i] == "current" else 27, views[i]))
        for j in range(views[i]):
            rows.append((key[i], arm[i], int(day[i]), role[i], j + 1, int(errs[j]), int(secs[j]), int(done[i])))
    df = pd.DataFrame(rows, columns=["applicant_key", "arm", "day", "applicant_role", "page_view", "validation_error", "seconds_on_page", "completed"])
    write(df, CAP / "data" / "b_experiment.csv")
    u = df.drop_duplicates("applicant_key")
    a, b = u[u["arm"] == "current"], u[u["arm"] == "redesign"]
    pa, pb = df[df["arm"] == "current"], df[df["arm"] == "redesign"]
    TRUTH["capstone_b"] = {"applicants": n, "page_views": int(len(df)), "true_effect_completion": 0.035, "minimum_effect": 0.03,
                           "completion": [round(float(a["completed"].mean()), 4), round(float(b["completed"].mean()), 4)],
                           "completion_p": z_p(a["completed"].sum(), len(a), b["completed"].sum(), len(b)),
                           "planted": "contractors produce twice the page views, so page-level analysis weights them double and overstates precision; the write-up reports seconds per page view at the page level and a metric that was not pre-registered"}
    write_text(f"""
# Write-up B: the redesigned building-works form saves applicants time

**Author:** an analyst of the digital services team. **Test:** current against redesigned application form
for building-works permits, 28 days, a seeded coin per applicant.

The pre-registration named completion of the application as the primary metric, with a minimum effect
of 3 points, and validation errors per applicant as the secondary metric.

Results over {len(df):,} page views: mean time on a page fell from {pa['seconds_on_page'].mean():.1f} to {pb['seconds_on_page'].mean():.1f} seconds
(t-test on page views, p below 0.001). Validation errors per page view fell from {pa['validation_error'].mean():.1%} to {pb['validation_error'].mean():.1%}
(z-test on page views, p below 0.001). Completion was {a['completed'].mean():.1%} against {b['completed'].mean():.1%}.

Because time on page is the most sensitive metric, we made it the headline. With more than {len(df) // 1000 * 1000:,}
observations the evidence is overwhelming.

**Recommendation.** Launch the redesign. Applicants will save about {(pa['seconds_on_page'].mean() - pb['seconds_on_page'].mean()) * df.groupby('applicant_key').size().mean() / 60:.1f} minutes each.
""", CAP / "b_writeup.md")


def capstone_c() -> None:
    """Case C: a training programme for counter staff in 20 service centres."""
    rng = gen(13)
    c = 20
    name = [f"C{i + 1:02d}" for i in range(c)]
    weekly = np.clip(np.round(rng.lognormal(np.log(130), 0.4, c)).astype(int), 50, 330)
    rate = np.clip(rng.normal(0.71, 0.07, c), 0.5, 0.9)                # resolved at the first visit
    order = np.argsort(-rate)
    trained = np.zeros(c, bool)
    trained[order[:10]] = True                                          # planted: the ten best centres were sent to training first
    centres = pd.DataFrame({"centre": name, "weekly_visitors": weekly, "trained": np.where(trained, "yes", "no"),
                            "shares_staff_with": ["" for _ in range(c)]})
    centres.loc[4, "shares_staff_with"], centres.loc[5, "shares_staff_with"] = "C06", "C05"
    write(centres, CAP / "data" / "c_centres.csv")
    rows = []
    for period, eff in (("baseline", 0.0), ("after training", 0.025)):
        for i in range(c):
            nv = int(rng.poisson(weekly[i] * 4))
            p = np.clip(rate[i] + rng.normal(0, 0.02) + eff * trained[i], 0.05, 0.97)
            ok = rng.binomial(1, p, nv)
            rows += [(name[i], period, int(x)) for x in ok]
    v = pd.DataFrame(rows, columns=["centre", "period", "resolved_first_visit"])
    v.insert(0, "visit_key", keys(rng, len(v), "V"))
    write(v, CAP / "data" / "c_visits.csv")
    after = v[v["period"] == "after training"].merge(centres[["centre", "trained"]], on="centre")
    base = v[v["period"] == "baseline"].merge(centres[["centre", "trained"]], on="centre")
    r = after.groupby("trained")["resolved_first_visit"].agg(["sum", "count"])
    rb = base.groupby("trained")["resolved_first_visit"].mean()
    TRUTH["capstone_c"] = {"centres": c, "visits": int(len(v)), "true_effect": 0.025, "minimum_effect": 0.04,
                           "after": {k: round(float(r.loc[k, "sum"] / r.loc[k, "count"]), 4) for k in ("no", "yes")},
                           "baseline": {k: round(float(rb[k]), 4) for k in ("no", "yes")},
                           "planted": "the trained centres were chosen for their results, not by chance, and already led at baseline; visits are analysed as if visitors had been randomised; C05 and C06 share staff"}
    write_text(f"""
# Write-up C: the training programme lifts first-visit resolution

**Author:** an analyst of the branch services team. **Programme:** two days of training for counter staff.

Ten of the 20 service centres were trained in the first wave. We chose the centres whose managers we
could rely on to release staff. Four weeks after training we compared visits.

Visitors of trained centres had their request resolved at the first visit in {r.loc['yes', 'sum'] / r.loc['yes', 'count']:.1%} of {int(r.loc['yes', 'count']):,} visits,
against {r.loc['no', 'sum'] / r.loc['no', 'count']:.1%} of {int(r.loc['no', 'count']):,} visits in the other centres (z-test on visits, p below 0.001).

**Recommendation.** The experiment shows that training causes a gain of {(r.loc['yes', 'sum'] / r.loc['yes', 'count'] - r.loc['no', 'sum'] / r.loc['no', 'count']) * 100:.0f} points. Train the remaining ten
centres and expect the same gain there.
""", CAP / "c_writeup.md")


PREREG = {
    "title": "Does a reminder seven days before expiry raise on-time renewal?",
    "decision": "Sahar Al-Wuhaibi decides whether every renewal notice is followed by a reminder message seven days before expiry. If the reminder raises on-time renewal by at least 2 points and no guardrail is crossed, the office adopts it for all permit types. If the effect is smaller, or a guardrail is crossed, the office keeps the standard notice.",
    "hypothesis": "Holders who get the reminder renew on time more often than holders who get only the standard notice.",
    "arms": "Control: the standard renewal notice 30 days before expiry, as today. Reminder: the same notice plus one reminder message seven days before expiry. A seeded coin per holder puts half in each arm.",
    "withholding": "Nobody loses a service they have today: the control arm gets the current notice. The reminder is untested, so giving it to half of the holders for 28 days is how the office learns whether it helps.",
    "primary_metric": {"name": "on-time renewal", "definition": "the share of holders who renew on or before the expiry date of the permit named in the notice"},
    "minimum_effect": 0.02,
    "minimum_effect_reason": "Below 2 points the late fees avoided do not cover the cost of the messages and of the complaints they bring.",
    "secondary_metrics": ["counter visits within 30 days of the notice"],
    "guardrails": [
        {"metric": "complaint rate", "threshold": 0.005, "action": "stop the test if the reminder arm exceeds control by more than this, and review the wording"},
        {"metric": "on-time renewal in each group (channel, holder type)", "threshold": -0.03, "action": "stop the reminder for a group whose rate falls below control by more than this, and tell the data protection officer"},
    ],
    "stop_rule": "The test runs 28 days and ends on the planned date. There is one analysis of the primary metric, at the end. One safety look on day 14 reads the guardrails only. There is no early stop for a good result.",
    "unit": "permit holder",
    "unit_reason": "A holder with several permits would otherwise receive both versions. Each holder is enrolled once, at the first notice in the window.",
    "sample_size_per_arm": 9200,
    "duration_days": 28,
    "analysis_plan": "A two-proportion z-test and a 95% interval for the difference in on-time renewal, with holders as the unit, analysed as assigned whether or not the reminder was delivered. Subgroups by channel and by prior lateness are exploratory and are reported as such.",
    "checks": "Before the result is read: a sample ratio check against 50/50, failed below p = 0.001, and a balance table of channel, holder type, prior lateness and tenure.",
    "data": "Fields used: a pseudonymised notice key, send date, permit type, holder type, channel, prior lateness, tenure, arm and outcomes. No name, phone number or address leaves the messaging platform. Results are reported in aggregate, never by holder, and the extract is deleted when the report is signed.",
}
PREREG_DAY1_PART = ("title", "decision", "hypothesis", "arms", "withholding", "primary_metric", "minimum_effect", "minimum_effect_reason", "secondary_metrics", "guardrails", "stop_rule")

NEIGHBOUR = {
    "title": "Reminder test",
    "decision": "Sahar Al-Wuhaibi decides whether to add the reminder. If on-time renewal improves, the office adopts the reminder; if it does not improve, the office keeps the standard notice.",
    "hypothesis": "The reminder raises on-time renewal among permit holders.",
    "arms": "Control gets the standard notice, as today. The other arm gets the standard notice and a reminder seven days before expiry. Half of the notices go to each arm.",
    "withholding": "The control arm keeps the service it has today, and the reminder has not been shown to help yet, so nobody is denied a proven benefit.",
    "primary_metric": {"name": "on-time renewal and counter visits", "definition": "we will report whichever of the two shows the clearer improvement"},
    "minimum_effect": None,
    "minimum_effect_reason": "Any improvement is worth having.",
    "secondary_metrics": ["complaints"],
    "guardrails": [{"metric": "complaint rate", "threshold": None, "action": "we will keep an eye on it"}],
    "stop_rule": "We check the dashboard daily and stop as soon as the difference is significant, so that holders benefit sooner.",
    "unit": "renewal notice",
    "unit_reason": "Notices are what the platform sends, so the coin is tossed per notice.",
    "sample_size_per_arm": 9200,
    "duration_days": 10,
    "analysis_plan": "We will explore the data when the test ends and choose the test that fits best.",
    "checks": "A sample ratio check against 50/50 and a balance table of channel and holder type before the result is read.",
    "data": "Pseudonymised notice keys only; no names or phone numbers leave the platform. Results are reported in aggregate, never by holder.",
}
NEIGHBOUR_KEY = {
    "C1": ("pass", "It names who decides and what happens either way, although the word improves still needs the number that C5 asks for."),
    "C2": ("pass", "Change, metric and direction are all there."),
    "C3": ("fail", "The coin is tossed per notice. A holder with three permits can get the reminder for one and not for another, so one person sits in both arms."),
    "C4": ("fail", "Two primary metrics, with the choice left until the data are in. That is a second chance at a win."),
    "C5": ("fail", "Any improvement is not a number. Without one there is no sample size and no line between a result worth acting on and noise."),
    "C6": ("fail", "One guardrail with no threshold and no action. Keeping an eye on it stops nothing."),
    "C7": ("fail", "Stopping at the first significant day is peeking. The false-win rate is far above 5%."),
    "C8": ("fail", "Ten days cover one whole week and part of another, and no month-end. The size has no stated source because there is no minimum effect."),
    "C9": ("fail", "The test is chosen after the data are seen. Nothing says which unit is analysed or that holders are analysed as assigned."),
    "C10": ("pass", "Both checks are planned before the result is read."),
    "C11": ("fail", "Arms and the reason for withholding are stated, but no guardrail protects any group of holders from harm."),
    "C12": ("pass", "Fields, pseudonymised keys and aggregate reporting are stated. A retention date would make it better."),
}


def main() -> None:
    write(history_daily().drop(columns=["weekend"]), DATA / "history_daily.csv")
    write(units_notices(), DATA / "units_notices.csv")
    assignment, full, log = reminder_test()
    write(full, DATA / "renewal_test.csv")
    write(log, DATA / "notice_log.csv")
    pages, stop, s = form_pages()
    write(pages, DATA / "form_pages.csv")
    text, key = form_writeup(s, stop)
    write_text(text, DATA / "writeup_form.md")
    write_json({"catalogue": [{"flaw": f, "meaning": m} for f, m in FLAWS], "key": key}, DATA / "writeup_form_key.json")
    br, visits = branches()
    write(br, DATA / "branches.csv")
    write(visits, DATA / "counter_visits.csv")
    write_json([{k: s_[k] for k in ("id", "text")} for s_ in STUDIES], DATA / "studies.json")
    write_json(STUDIES, DATA / "studies_key.json")
    write_json({k: PREREG[k] for k in PREREG_DAY1_PART}, DATA / "prereg_start.json")
    write_json(PREREG, SOL / "prereg_reference.json")
    write_json(NEIGHBOUR, DATA / "prereg_neighbour.json")
    write_json({k: {"verdict": v, "reason": r} for k, (v, r) in NEIGHBOUR_KEY.items()}, DATA / "prereg_neighbour_key.json")
    capstone_a()
    capstone_b()
    capstone_c()
    TRUTH["minimum_effect"] = MIN_EFFECT
    write_json(TRUTH, SOL / "truth.json")
    for name in sorted(TRUTH):
        print(name, json.dumps(TRUTH[name], ensure_ascii=False)[:900])


if __name__ == "__main__":
    main()
