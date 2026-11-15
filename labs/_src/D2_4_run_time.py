# %% [markdown]
# # Lab 2.4 · Choose the run time
#
# Day 2 · Session 4 (Run time and seasonality) · 25 min.
#
# The sample size says nine days. The pre-registration says 28. You read the weekly cycle and the month-end peak in 26 weeks of history, forecast the traffic of the test window, find the day on which the planned size is reached, and choose a duration of whole weeks that covers the month-end. Then you work out what shorter tests would estimate if the reminder helps more on some days than on others.
#
# **AI policy.** AI-tutor: hints one step at a time on the dataframe code.
#
# **Reference state.** `data/history_daily.csv`. The planned size, 9,187 per arm, is given below, so nothing from labs 2.1 to 2.3 is needed.
#
# **Tasks**
# - [ ] 1 · Traffic and renewal rate by weekday and at month-end (6')
# - [ ] 2 · Days needed for the planned size (4')
# - [ ] 3 · Whole weeks that cover the month-end (4')
# - [ ] 4 · What tests of 9, 14 and 28 days would estimate (7')
# - [ ] 5 · Record the duration and its reason (4')
# - [ ] ✱ Stretch · Start the 9-day test on the 24th of the month and compare its estimate

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-205.git"
    if not Path("/content/ds-205").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-205"], check=True)
    os.chdir("/content/ds-205/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("mashraq.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

import numpy as np
import pandas as pd
import mashraq as U
print("mode:", U.MODE)

hist = U.history()
P1 = hist["renewed_on_time"].sum() / hist["notices_sent"].sum()
N_ARM = U.n_per_arm(P1, U.MIN_EFFECT)      # 9,187 per arm for 2 points
WEEK = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
print(hist.head(9).to_string(index=False))
print(f"\nplanned size {N_ARM:,} per arm, {2 * N_ARM:,} holders in all")

# %% [markdown]
# ## 1 · Traffic and renewal rate by weekday and at month-end (6')
#
# The office's weekend is Friday and Saturday. `month_end` marks the 26th of the month and later, when most permits fall due.
#
# ✏️ **Exercise** · Write `cycle_table(hist, by)` returning a table with one row per value of the column `by`, and two columns: `mean_notices` (mean notices per day) and `rate` (renewals over notices, pooled over the days of the group).

# %%
def cycle_table(hist, by):
    # BEGIN SOLUTION
    g = hist.groupby(by).agg(mean_notices=("notices_sent", "mean"), renewed=("renewed_on_time", "sum"), sent=("notices_sent", "sum"))
    g["rate"] = g["renewed"] / g["sent"]
    return g[["mean_notices", "rate"]]
    # END SOLUTION


# %%
try:
    by_day = cycle_table(hist, "weekday").reindex(WEEK)
    by_peak = cycle_table(hist, "month_end")
except NotImplementedError:
    by_day = pd.DataFrame(U.reference("d2_4", "by_day")).reindex(WEEK)
    by_peak = pd.DataFrame(U.reference("d2_4", "by_peak"))
    by_peak.index = by_peak.index.astype(int)
U.keep("d2_4", "by_day", {c: by_day[c].to_dict() for c in by_day})
U.keep("d2_4", "by_peak", {c: {str(k): v for k, v in by_peak[c].items()} for c in by_peak})
print(by_day.round({"mean_notices": 0, "rate": 3}).to_string())
print()
print(by_peak.round({"mean_notices": 0, "rate": 3}).to_string())
U.check(by_day.loc["Fri", "mean_notices"] < 0.6 * by_day.loc["Sun", "mean_notices"], "Friday carries about half the traffic of a working day")
U.check(by_peak.loc[1, "mean_notices"] > 1.3 * by_peak.loc[0, "mean_notices"] and by_peak.loc[1, "rate"] < by_peak.loc[0, "rate"], "month-end days are busier and their holders renew on time less often")

# %% [markdown]
# **Look at.** Two cycles, and both move the traffic **and** the baseline rate. Holders whose notice goes out on a weekend or in the month-end rush are different holders, or the same holders in a different week.

# %% [markdown]
# ## 2 · Days needed for the planned size (4')
#
# The test starts on Sunday 6 September 2026. The forecast below gives each day of the following five weeks its expected traffic: the mean of its weekday, times the month-end factor on the 26th and later.

# %%
def forecast(start="2026-09-06", days=35):
    d = pd.date_range(start, periods=days)
    f = pd.DataFrame({"date": d.strftime("%Y-%m-%d"), "weekday": d.strftime("%a"), "day_of_month": d.day})
    f["month_end"] = (f["day_of_month"] >= 26).astype(int)
    f["weekend"] = f["weekday"].isin(["Fri", "Sat"]).astype(int)
    normal = hist[hist["month_end"] == 0].groupby("weekday")["notices_sent"].mean()
    factor = by_peak.loc[1, "mean_notices"] / by_peak.loc[0, "mean_notices"]
    f["expected"] = f["weekday"].map(normal) * np.where(f["month_end"] == 1, factor, 1.0)
    f.index = np.arange(1, days + 1)
    f.index.name = "test_day"
    return f


fc = forecast()
print(fc.head(10).round({"expected": 0}).to_string())

# %% [markdown]
# ✏️ **Exercise** · Write `days_to_reach(total, fc)` returning the first test day on which the cumulative expected traffic reaches `total` holders.

# %%
def days_to_reach(total, fc):
    # BEGIN SOLUTION
    cum = fc["expected"].cumsum()
    return int(cum[cum >= total].index[0])
    # END SOLUTION


# %%
try:
    need = days_to_reach(2 * N_ARM, fc)
except NotImplementedError:
    need = U.reference("d2_4", "need")
U.keep("d2_4", "need", need)
print(f"the planned size is reached on test day {need}, a {fc.loc[need, 'weekday']}")
U.check(8 <= need <= 10, "the size for 2 points is reached in the second week")

# %% [markdown]
# ## 3 · Whole weeks that cover the month-end (4')
#
# A test that stops on day 9 has seen two Sundays and one Friday, and no month-end.
#
# ✏️ **Exercise** · Write `choose_duration(need, fc)` returning the smallest number of days that (a) is at least `need`, (b) is a multiple of 7 and (c) includes every month-end day (the 26th and later) of the first month-end in the forecast.

# %%
def choose_duration(need, fc):
    # BEGIN SOLUTION
    # the first run of month-end days ends where the day of the month falls back to 1
    last_peak = int(fc.index[(fc["month_end"] == 1) & (fc["month_end"].shift(-1, fill_value=0) == 0)][0])
    d = 7
    while d < need or d < last_peak:
        d += 7
    return d
    # END SOLUTION


# %%
try:
    duration = choose_duration(need, fc)
except NotImplementedError:
    duration = U.reference("d2_4", "duration")
U.keep("d2_4", "duration", duration)
window = fc.loc[:duration]
total = window["expected"].sum()
print(f"duration: {duration} days, {duration // 7} whole weeks, ending {window['date'].iloc[-1]}; month-end days inside: {int(window['month_end'].sum())}")
print(f"expected holders in the test: {total:,.0f}, about {total / 2:,.0f} per arm")
U.check(duration == 28, "four whole weeks, which contain the month-end of September")

# %% [markdown]
# **Look at.** The calendar, not the formula, set the duration. The extra holders are not wasted: with about 30,000 per arm the test can detect an effect of about 1.1 points and will estimate a 2-point effect with a narrow interval. One more clock runs after the last notice: a holder notified on day 28 has 30 days to renew, so the primary metric is complete 30 days after the test ends.

# %% [markdown]
# ## 4 · What tests of 9, 14 and 28 days would estimate (7')
#
# Nobody knows yet whether the reminder helps equally on all days. Sahar's team suspects it helps most in the month-end rush and least on weekends. Take that as a planning assumption, in points of on-time renewal:

# %%
ASSUMED = {"ordinary day": 2.0, "month-end day": 4.0, "weekend day": 1.0, "weekend day at month-end": 3.0}


def assumed_effect(fc):
    """The assumed effect, in points, for the holders notified on each day of the forecast."""
    return 2.0 + 2.0 * fc["month_end"] - 1.0 * fc["weekend"]


print(ASSUMED)

# %% [markdown]
# ✏️ **Exercise** · Write `expected_estimate(fc, days, first=1)`: the effect a test covering test days `first` to `first + days − 1` would estimate, which is the traffic-weighted mean of the daily assumed effects, in points.

# %%
def expected_estimate(fc, days, first=1):
    # BEGIN SOLUTION
    w = fc.loc[first:first + days - 1]
    return float((assumed_effect(w) * w["expected"]).sum() / w["expected"].sum())
    # END SOLUTION


# %%
try:
    est = {d: expected_estimate(fc, d) for d in (9, 14, 28)}
except NotImplementedError:
    est = {int(k): v for k, v in U.reference("d2_4", "est").items()}
U.keep("d2_4", "est", est)
rows = []
for d in (9, 14, 28):
    w = fc.loc[:d]
    n_arm = w["expected"].sum() / 2
    se = np.sqrt(2 * P1 * (1 - P1) / n_arm) * 100
    rows.append([d, f"{w['expected'].sum():,.0f}", int(w["month_end"].sum()), f"{est[d]:.2f}", f"±{1.96 * se:.2f}"])
U.table(["days", "holders", "month-end days", "expected estimate, points", "95% margin, points"], rows)
U.check(est[28] > est[9] + 0.2, "the 28-day test estimates a larger effect than the 9-day test, because only it contains the month-end")
U.check(abs(est[9] - est[14]) < 0.15, "9 and 14 days, both without a month-end, estimate nearly the same thing")

# %% [markdown]
# **Look at.** None of the three numbers is wrong. Each is the effect for the holders notified in its window. The office will send the reminder all year, so the decision needs the effect over a whole cycle, and only the 28-day test covers one. A short test answers a question nobody asked.

# %% [markdown]
# ## 5 · Record the duration and its reason (4')
#
# ✏️ **Exercise** · Return a dictionary with `duration_days` and a `reason` of at least 15 words that mentions the weekly cycle and the month-end.

# %%
def record_duration():
    # BEGIN SOLUTION
    return {"duration_days": 28,
            "reason": "The size for 2 points is reached on day 9, but the test runs four whole weeks so that every weekday counts "
                      "equally and the month-end peak, when traffic and behaviour differ, is inside the window."}
    # END SOLUTION


# %%
try:
    rec = record_duration()
except NotImplementedError:
    rec = U.reference("d2_4", "record")
U.keep("d2_4", "record", rec)
print(rec["duration_days"], "days ·", rec["reason"])
low = rec["reason"].lower()
U.check(rec["duration_days"] == duration, "the recorded duration is the one you computed")
U.check(len(rec["reason"].split()) >= 15 and "week" in low and "month" in low, "the reason names the weekly cycle and the month-end")

# %% [markdown]
# ## ✱ Stretch · A 9-day test in the rush
#
# Start the 9-day test on 24 September, test day 19 of the forecast.

# %%
def stretch():
    # BEGIN SOLUTION
    e = expected_estimate(fc, 9, first=19)
    print(f"9 days from 24 September: expected estimate {e:.2f} points (9 days from 6 September: {est[9]:.2f}; 28 days: {est[28]:.2f})")
    # Two short tests of the same reminder, one in each half of the month, would disagree, and both would be reported as "the effect".
    return e
    # END SOLUTION


try:
    U.keep("d2_4", "stretch", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked in the history: the weekly cycle and the month-end peak, in traffic and in the baseline rate.",
       f"Checked: the planned size is reached on day {need}; the duration is {duration} days.",
       "Assumed, not known: that the reminder's effect differs by day type as in the table of step 4. The lesson holds for any pattern; the numbers do not.",
       "Not in the synthetic calendar: public holidays. On a real calendar, check for holidays in the window before fixing the dates.")

# %% [markdown]
# ## Checkpoint
#
# 1. The planned size is reached on a Monday. Why not stop there?
#    <details><summary>Answer</summary>The window would hold two Sundays and two Mondays and one of every other day. Days differ in traffic and in behaviour, so the estimate would lean towards Sunday and Monday holders.</details>
# 2. Why is the result not final on day 28?
#    <details><summary>Answer</summary>On-time renewal is known only at each permit's expiry date, 30 days after its notice. The last holders complete the metric 30 days after the last notice.</details>
# 3. Holders react strongly to a new message in its first week and less afterwards. Which durations are fooled most?
#    <details><summary>Answer</summary>The shortest. A novelty effect fades; a longer test averages over it and can show it by week.</details>
#
# ## Carry forward
#
# The pre-registration is now confirmed: about 9,200 per arm is the minimum, 28 days is the duration. Tomorrow the test has run, and you read its 60,000 notices.
