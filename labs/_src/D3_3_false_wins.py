# %% [markdown]
# # Lab 3.3 · A thousand A/A tests
#
# Day 3 · Session 3 (False wins by simulation) · 25 min.
#
# An A/A test gives both arms the same thing. Nothing differs, so every "win" is false, and with one planned analysis about 5% of A/A tests win. You run 1,000 A/A tests under three habits that feel harmless, looking every day, looking at twenty metrics, and counting page views in place of applicants, and you count the false wins each habit produces, beside the count under the correct procedure.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** `data/form_pages.csv` for step 4. Steps 1 to 3 simulate their own data. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · One look at the end: the 5% you agreed to (4')
# - [ ] 2 · Peeking: a look every day for 28 days (7')
# - [ ] 3 · Twenty metrics: any win, then a correction (6')
# - [ ] 4 · Wrong unit: page views against applicants (5')
# - [ ] 5 · The table of false-win rates (3')
# - [ ] ✱ Stretch · Peek once a week only, four looks: how much of the damage remains?

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
from scipy import stats
import mashraq as U
print("mode:", U.MODE)

REPS = U.pick(1000, 300)
P = 0.6158          # on-time renewal in both arms: there is no effect anywhere in this lab
DAYS = 28
PER_DAY = 1070      # holders per arm per day, about 30,000 per arm in 28 days
print(f"{REPS} A/A tests; both arms renew at {P:.2%}; {PER_DAY:,} holders per arm per day for {DAYS} days")


def aa_daily(gen, reps=None):
    """Simulated A/A tests day by day. Returns cumulative on-time renewals of the two arms, shape (reps, 28), and cumulative holders per arm."""
    reps = reps or REPS
    a = gen.binomial(PER_DAY, P, size=(reps, DAYS)).cumsum(axis=1)
    b = gen.binomial(PER_DAY, P, size=(reps, DAYS)).cumsum(axis=1)
    n = PER_DAY * np.arange(1, DAYS + 1)
    return a, b, n


# %% [markdown]
# ## 1 · One look at the end: the 5% you agreed to (4')
#
# `U.z_test(x1, n1, x2, n2)` accepts arrays, so one call gives the p-value of every test on every day.
#
# ✏️ **Exercise** · Write `daily_p_values(a, b, n)` returning an array of shape (reps, 28): the p-value of each A/A test as it stood at the end of each day. Then `final_look(p)` returning the share of tests that are significant on day 28.

# %%
def daily_p_values(a, b, n):
    # BEGIN SOLUTION
    return U.z_test(a, n, b, n)[2]
    # END SOLUTION


def final_look(p):
    # BEGIN SOLUTION
    return float((p[:, -1] < U.ALPHA).mean())
    # END SOLUTION


# %%
a, b, n = aa_daily(U.rng(61))
try:
    p_daily = daily_p_values(a, b, n)
    one_look = final_look(p_daily)
except NotImplementedError:
    p_daily = None
    one_look = U.reference("d3_3", "one_look")
U.keep("d3_3", "one_look", one_look)
tol = 2.5 * np.sqrt(0.05 * 0.95 / REPS)
print(f"one planned analysis on day 28: {one_look:.1%} of {REPS} A/A tests are significant")
U.check(abs(one_look - 0.05) < tol, "with one look at the planned end, about 5% of A/A tests win")

# %% [markdown]
# ## 2 · Peeking: a look every day for 28 days (7')
#
# The dashboard shows the p-value every morning. The habit: stop the test, and announce the result, on the first day the p-value is below 0.05.
#
# ✏️ **Exercise** · Write `peeking(p, days)` returning the share of tests whose p-value is below 0.05 on **at least one** of the days in the list `days` (day numbers from 1).

# %%
def peeking(p, days):
    # BEGIN SOLUTION
    cols = np.array(days) - 1
    return float((p[:, cols] < U.ALPHA).any(axis=1).mean())
    # END SOLUTION


# %%
try:
    daily_peek = peeking(p_daily, list(range(1, DAYS + 1)))
    first_cross = (p_daily < U.ALPHA).argmax(axis=1)[(p_daily < U.ALPHA).any(axis=1)] + 1
    median_stop = float(np.median(first_cross))
except (NotImplementedError, TypeError):
    daily_peek, median_stop = U.reference("d3_3", "peek")
U.keep("d3_3", "peek", [daily_peek, median_stop])
print(f"stop at the first significant day among 28 daily looks: {daily_peek:.1%} of A/A tests declare a win")
print(f"half of those false wins are declared by day {median_stop:.0f}")
U.check(daily_peek > 0.20, "daily peeking with early stopping multiplies the false-win rate several times over")

# %% [markdown]
# **Look at.** A p-value wanders as data arrive. Given 28 chances, a wandering number crosses 0.05 far more often than once in twenty. The early days are the most dangerous: little data, large swings, and a false win declared then also reports a large "effect".

# %%
if p_daily is not None:
    plt = U.plt()
    crossing = np.flatnonzero((p_daily < U.ALPHA).any(axis=1) & (p_daily[:, -1] >= U.ALPHA))[:3]
    for i in crossing:
        plt.plot(np.arange(1, DAYS + 1), p_daily[i])
    plt.axhline(U.ALPHA, linestyle="--", color="grey")
    plt.yscale("log"); plt.xlabel("test day"); plt.ylabel("p-value so far")
    plt.title("Three A/A tests that dipped below 0.05 and came back")
    plt.show()

# %% [markdown]
# **The correct procedure in this course:** one analysis at the planned end. Methods that allow planned interim looks, by spending the 5% across them, exist and are the subject of DS-302.

# %% [markdown]
# ## 3 · Twenty metrics: any win, then a correction (6')
#
# One look, at the end, but at twenty metrics: on-time renewal, counter visits, complaints, days to renewal, and sixteen more. In an A/A test none of them differs.

# %%
def aa_metrics(gen, k=20, n=30_000, reps=None):
    """p-values of k unrelated yes-or-no metrics in each of reps A/A tests: shape (reps, k)."""
    reps = reps or REPS
    base = gen.uniform(0.05, 0.7, k)
    x1 = gen.binomial(n, base, size=(reps, k))
    x2 = gen.binomial(n, base, size=(reps, k))
    return U.z_test(x1, n, x2, n)[2]


# %% [markdown]
# ✏️ **Exercise** · Write `any_win(p)` returning the share of tests in which at least one of the metrics has p below 0.05. Then `any_win_holm(p)`: the same after Holm's correction, the one DS-201 used for thirty districts. Holm starts by comparing the smallest of the k p-values with 0.05/k and rejects nothing if that fails, so a test has at least one win after Holm exactly when its smallest p-value is below 0.05/k.

# %%
from statsmodels.stats.multitest import multipletests


def any_win(p):
    # BEGIN SOLUTION
    return float((p < U.ALPHA).any(axis=1).mean())
    # END SOLUTION


def any_win_holm(p):
    # BEGIN SOLUTION
    return float((p.min(axis=1) < U.ALPHA / p.shape[1]).mean())
    # END SOLUTION


# %%
p_metrics = aa_metrics(U.rng(62))
try:
    twenty = any_win(p_metrics)
    twenty_holm = any_win_holm(p_metrics)
    primary_only = float((p_metrics[:, 0] < U.ALPHA).mean())
except NotImplementedError:
    twenty, twenty_holm, primary_only = U.reference("d3_3", "metrics")
U.keep("d3_3", "metrics", [twenty, twenty_holm, primary_only])
print(f"twenty metrics, report any that is significant: {twenty:.1%} of A/A tests have a 'win' (1 − 0.95^20 = {1 - 0.95 ** 20:.1%})")
print(f"twenty metrics with Holm's correction:           {twenty_holm:.1%}")
print(f"one pre-registered primary metric:               {primary_only:.1%}")
U.check(twenty > 0.55, "with twenty metrics, most A/A tests show at least one significant difference")
example = int(np.flatnonzero((p_metrics < U.ALPHA).any(axis=1))[0])
kept = multipletests(p_metrics[example], alpha=U.ALPHA, method="holm")[0]
print(f"A/A test number {example + 1}: {(p_metrics[example] < U.ALPHA).sum()} of 20 metrics below 0.05 before the correction, {kept.sum()} after Holm (statsmodels)")
U.check(twenty_holm < 0.05 + tol and primary_only < 0.05 + tol, "a correction, or a single pre-registered primary metric, brings the rate back to about 5%")

# %% [markdown]
# **Look at.** Two honest ways out. Name one primary metric in advance and let it alone carry the decision: that is what the pre-registration does. Or, if several metrics must share the decision, correct for their number. Subgroups work the same way: six subgroups are six more chances.

# %% [markdown]
# ## 4 · Wrong unit: page views against applicants (5')
#
# The form test randomised applicants. Take its log, forget the real arms, and deal every applicant a fresh coin: an A/A test on real data. Then analyse validation errors twice: per page view, as the log tempts you to, and per applicant.

# %%
pages = U.form_pages()
per = pages.groupby("applicant_key")["validation_error"].agg(["sum", "size"])
ERR, VIEWS = per["sum"].to_numpy(), per["size"].to_numpy()
SHARE = ERR / VIEWS            # each applicant's own error share
print(f"{len(per):,} applicants, {VIEWS.sum():,} page views, {ERR.sum() / VIEWS.sum():.1%} of page views have a validation error")


def applicant_level_p(treated):
    """Welch t-test on the applicants' error shares: one number per applicant, the unit that was randomised."""
    return float(stats.ttest_ind(SHARE[treated], SHARE[~treated], equal_var=False).pvalue)


# %% [markdown]
# ✏️ **Exercise** · Write `page_level_p(treated)`: the p-value of a two-proportion z-test that counts every page view as an independent observation. `treated` is a boolean array with one entry per applicant.

# %%
def page_level_p(treated):
    # BEGIN SOLUTION
    return U.z_test(ERR[~treated].sum(), VIEWS[~treated].sum(), ERR[treated].sum(), VIEWS[treated].sum())[2]
    # END SOLUTION


# %%
try:
    gen = U.rng(63)
    wins_page = wins_applicant = 0
    for _ in range(REPS):
        treated = gen.random(len(per)) < 0.5
        wins_page += page_level_p(treated) < U.ALPHA
        wins_applicant += applicant_level_p(treated) < U.ALPHA
    unit = [wins_page / REPS, wins_applicant / REPS]
except NotImplementedError:
    unit = U.reference("d3_3", "unit")
U.keep("d3_3", "unit", unit)
print(f"page views analysed as independent: {unit[0]:.1%} of A/A tests are significant")
print(f"applicants analysed, as randomised: {unit[1]:.1%}")
U.check(unit[0] > 0.15, "the page-level analysis of an applicant-randomised test wins far more often than 5%")
U.check(unit[1] < 0.05 + tol, "the applicant-level analysis keeps the rate at about 5%")

# %% [markdown]
# **Look at.** The page-level test believes it has more than fifty thousand independent observations. It has about five thousand applicants, some of whom contribute dozens of similar rows. The standard error is too small, so ordinary luck in who landed where looks like an effect.

# %% [markdown]
# ## 5 · The table of false-win rates (3')
#
# ✏️ **Exercise** · Return the table as a list of rows `[trap, rate_with_the_trap, rate_with_the_correct_procedure]`, one row for each of the three traps, from the numbers above.

# %%
def false_win_table():
    # BEGIN SOLUTION
    return [["peeking: 28 daily looks, stop at the first p < 0.05", daily_peek, one_look],
            ["many metrics: any of twenty", twenty, twenty_holm],
            ["wrong unit: page views for applicants", unit[0], unit[1]]]
    # END SOLUTION


# %%
try:
    rows = false_win_table()
except NotImplementedError:
    rows = U.reference("d3_3", "table")
U.keep("d3_3", "table", rows)
U.table(["trap", "false wins with the trap", "with the correct procedure"], [[t, f"{x:.1%}", f"{y:.1%}"] for t, x, y in rows])
U.check(len(rows) == 3 and all(x > 2 * y for _, x, y in rows), "each trap at least doubles the false-win rate; each correct procedure restores about 5%")

# %% [markdown]
# **Look at.** Each of these habits can be found in honest reports written by careful people. None of them requires a wrong formula, only a formula applied to a situation it was not built for. And they combine: a report that peeked at twenty metrics per page view is close to a machine for producing wins.

# %% [markdown]
# ## ✱ Stretch · Four weekly looks

# %%
def stretch():
    # BEGIN SOLUTION
    weekly = peeking(p_daily, [7, 14, 21, 28])
    print(f"stop at the first significant weekly look: {weekly:.1%} (daily looks: {daily_peek:.1%}; one look: {one_look:.1%})")
    # Fewer looks do less damage, but four uncorrected looks still more than double the 5%.
    return weekly
    # END SOLUTION


try:
    U.keep("d3_3", "weekly", stretch())
except (NotImplementedError, TypeError):
    print("✱ stretch not done")

# %%
U.note(f"Measured over {REPS} A/A tests each: the false-win rate of three traps and of the correct procedure for each.",
       f"Each rate is a count with an error of about ±{2 * np.sqrt(0.05 * 0.95 / REPS) * 100:.1f} points near 5% and about ±{2 * np.sqrt(0.25 / REPS) * 100:.1f} points near 50%.",
       "Not measured: the traps in combination, and tests with a real effect, where peeking also inflates the reported size of the effect.")

# %% [markdown]
# ## Checkpoint
#
# 1. A team looks at its dashboard daily but changes nothing until the planned end. Is that peeking?
#    <details><summary>Answer</summary>Looking is harmless. Acting on the look is the problem: stopping, extending, or switching metric because of what was seen.</details>
# 2. A write-up says "we examined 14 metrics and two were significant". How many would you expect in an A/A test?
#    <details><summary>Answer</summary>About 0.7 on average, and at least one in about half of all A/A tests. Two of 14 is weak evidence unless they were named in advance.</details>
# 3. Why does analysing page views give too small a standard error?
#    <details><summary>Answer</summary>The formula assumes independent observations. Page views of one applicant share that applicant's habits, so they carry less information than the same number of independent rows.</details>
#
# ## Carry forward
#
# The table of step 5 is the evidence of the fifth course outcome. Lab 3.4 finds all three traps in one write-up.
