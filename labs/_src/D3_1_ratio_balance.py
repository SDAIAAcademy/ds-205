# %% [markdown]
# # Lab 3.1 · Ratio and balance on the export
#
# Day 3 · Session 1 (Did randomisation work) · 25 min.
#
# The reminder test has run for 28 days. The messaging platform exports one row per notice with its arm and its outcome, and a colleague is about to compute the effect from it. Before anyone reads a result you run the two checks the pre-registration promised: the sample ratio and the balance of the arms. One of them fails, and you find out where and what it would have cost.
#
# **AI policy.** AI-tutor, hints only, for the dataframe code. The decision in step 5 is yours.
#
# **Reference state.** `data/notice_log.csv`, the platform's export, and `data/renewal_test.csv`, the test as assigned: 60,000 holders with the arm the seeded coin gave each. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · The sample ratio check on the export (5')
# - [ ] 2 · A balance table of four covariates (6')
# - [ ] 3 · Locate the fault by channel and week (6')
# - [ ] 4 · Compare with the test as assigned (4')
# - [ ] 5 · Measure what the faulty export would have claimed (4')
# - [ ] ✱ Stretch · How often does a healthy 50/50 assignment of 60,000 fail the check at 0.001? Simulate it

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

log = U.notice_log()
print(log.head(5).to_string(index=False))
print(f"\n{len(log):,} rows in the export")

# %% [markdown]
# ## 1 · The sample ratio check on the export (5')
#
# The coin was fair, so the two arms should be about equal. "About" has a test: a chi-square test of the two counts against a 50/50 split. The pre-registration set the line at p = 0.001.
#
# ✏️ **Exercise** · Write `ratio_check(df)` returning `(n_control, n_reminder, p_value)`. Use `stats.chisquare([n_control, n_reminder])`, which tests against equal counts.

# %%
def ratio_check(df):
    # BEGIN SOLUTION
    n_c = int((df["arm"] == "control").sum())
    n_r = int((df["arm"] == "reminder").sum())
    return n_c, n_r, float(stats.chisquare([n_c, n_r]).pvalue)
    # END SOLUTION


# %%
try:
    n_c, n_r, p_ratio = ratio_check(log)
except NotImplementedError:
    n_c, n_r, p_ratio = U.reference("d3_1", "ratio")
U.keep("d3_1", "ratio", [n_c, n_r, p_ratio])
print(f"control {n_c:,}, reminder {n_r:,}: {n_r / (n_c + n_r):.2%} in the reminder arm; p = {p_ratio:.2g}")
print("sample ratio check:", "FAILED" if p_ratio < U.RATIO_ALPHA else "passed")
U.check(p_ratio < U.RATIO_ALPHA, "the export fails the sample ratio check: a fair coin does not lose a thousand holders from one arm")

# %% [markdown]
# **Look at.** 49.05% does not look alarming. With 59,000 rows it is: a fair coin lands that far from 50% a few times in a million. A failed ratio check means the result must not be read until the cause is found. It says nothing yet about what the cause is.

# %% [markdown]
# ## 2 · A balance table of four covariates (6')
#
# If rows are missing, are they a random handful or a particular kind of holder? Compare the arms on four traits fixed before the test: e-mail channel, business holder, prior lateness, tenure in years.

# %%
log["is_email"] = (log["channel"] == "email").astype(int)
log["is_business"] = (log["holder_type"] == "business").astype(int)
SHARES = ["is_email", "is_business", "prior_late"]

# %% [markdown]
# ✏️ **Exercise** · Write `balance(df)` returning a dictionary from covariate to `(control_value, reminder_value, p_value)`. For the three 0/1 covariates in `SHARES` use shares and `U.z_test(x1, n1, x2, n2)`. For `tenure_years` use means and `stats.ttest_ind(..., equal_var=False)`.

# %%
def balance(df):
    # BEGIN SOLUTION
    c, r = df[df["arm"] == "control"], df[df["arm"] == "reminder"]
    out = {}
    for col in SHARES:
        p = U.z_test(c[col].sum(), len(c), r[col].sum(), len(r))[2]
        out[col] = (float(c[col].mean()), float(r[col].mean()), float(p))
    t = stats.ttest_ind(c["tenure_years"], r["tenure_years"], equal_var=False)
    out["tenure_years"] = (float(c["tenure_years"].mean()), float(r["tenure_years"].mean()), float(t.pvalue))
    return out
    # END SOLUTION


# %%
try:
    bal = balance(log)
except NotImplementedError:
    bal = {k: tuple(v) for k, v in U.reference("d3_1", "balance").items()}
U.keep("d3_1", "balance", {k: list(v) for k, v in bal.items()})
U.table(["covariate", "control", "reminder", "p"], [[k, f"{a:.4f}", f"{b:.4f}", f"{p:.2g}"] for k, (a, b, p) in bal.items()])
U.check(bal["is_email"][2] < 0.001 and bal["is_email"][1] < bal["is_email"][0], "the reminder arm of the export has too few e-mail holders")
U.check(all(bal[k][2] > 0.001 for k in ("is_business", "prior_late", "tenure_years")), "the other three covariates are balanced")

# %% [markdown]
# **Look at.** One covariate is badly out of balance and it names a suspect. With four covariates, one p-value near 0.05 would mean little; this one is far beyond that.

# %% [markdown]
# ## 3 · Locate the fault by channel and week (6')
#
# ✏️ **Exercise** · Write `counts_by(df, cols)` returning a table with one row per combination of the columns in `cols`, and the columns `control`, `reminder` and `share_reminder`.

# %%
log["week"] = (log["test_day"] - 1) // 7 + 1


def counts_by(df, cols):
    # BEGIN SOLUTION
    t = df.groupby(cols + ["arm"]).size().unstack("arm", fill_value=0)
    t["share_reminder"] = t["reminder"] / (t["control"] + t["reminder"])
    return t[["control", "reminder", "share_reminder"]]
    # END SOLUTION


# %%
try:
    by_channel = counts_by(log, ["channel"])
    by_cell = counts_by(log, ["channel", "week"])
except NotImplementedError:
    by_cell = pd.DataFrame(U.reference("d3_1", "by_cell"))
    by_cell.index = pd.MultiIndex.from_tuples([tuple([k.split("|")[0], int(k.split("|")[1])]) for k in by_cell.index], names=["channel", "week"])
    by_channel = by_cell.groupby("channel")[["control", "reminder"]].sum()
    by_channel["share_reminder"] = by_channel["reminder"] / (by_channel["control"] + by_channel["reminder"])
U.keep("d3_1", "by_cell", {c: {f"{k[0]}|{k[1]}": float(v) for k, v in by_cell[c].items()} for c in by_cell})
print(by_channel.round(4).to_string())
print()
print(by_cell.round(4).to_string())
U.check(by_cell.loc[("email", 1), "reminder"] == 0, "in week 1 the export holds no reminder row for the e-mail channel")
U.check(abs(by_cell.loc[("sms", 1), "share_reminder"] - 0.5) < 0.02, "every other cell is close to 50/50")

# %% [markdown]
# **Look at.** One cell is empty. The platform team confirms it: in the first week the reminder job failed for e-mail, and the export lists a notice only when its arm's messages completed. Those holders got the standard notice and no reminder, and then vanished from the export.

# %% [markdown]
# ## 4 · Compare with the test as assigned (4')
#
# The assignment was recorded before any message went out. `renewal_test.csv` has every holder the coin was tossed for, with the outcome from the permit register.
#
# ✏️ **Exercise** · Write `missing_rows(full, log)` returning the rows of `full` whose `notice_key` is not in `log`.

# %%
full = U.renewal_test()


def missing_rows(full, log):
    # BEGIN SOLUTION
    return full[~full["notice_key"].isin(log["notice_key"])]
    # END SOLUTION


# %%
try:
    miss = missing_rows(full, log)
    miss_summary = [len(miss), sorted(miss["arm"].unique()), sorted(miss["channel"].unique()), int(miss["test_day"].max()), float(miss["renewed_on_time"].mean())]
except NotImplementedError:
    miss_summary = U.reference("d3_1", "missing")
U.keep("d3_1", "missing", miss_summary)
n_miss, arms, channels, last_day, miss_rate = miss_summary
a_c, a_r = int((full["arm"] == "control").sum()), int((full["arm"] == "reminder").sum())
print(f"as assigned: {len(full):,} holders, control {a_c:,}, reminder {a_r:,}; ratio check p = {U.ratio_p(a_c, a_r):.2f}")
print(f"missing from the export: {n_miss:,} rows; arms {arms}; channels {channels}; last test day {last_day}")
print(f"on-time renewal among the missing holders: {miss_rate:.1%}; among all holders: {full['renewed_on_time'].mean():.1%}")
U.check(U.ratio_p(a_c, a_r) > 0.05, "the assignment itself passes the ratio check: the coin was fair")
U.check(arms == ["reminder"] and channels == ["email"] and last_day <= 7, "every missing row is a reminder-arm e-mail holder of the first week")

# %% [markdown]
# **Look at.** The randomisation worked. The export broke afterwards. And the missing holders are not typical: e-mail holders renew on time less often. Removing them from one arm makes that arm look better.

# %% [markdown]
# ## 5 · Measure what the faulty export would have claimed (4')
#
# ✏️ **Exercise** · Write `effect(df)` returning the difference in on-time renewal, reminder minus control. Then compare the export with the test as assigned.

# %%
def effect(df):
    # BEGIN SOLUTION
    r = df.groupby("arm")["renewed_on_time"].mean()
    return float(r["reminder"] - r["control"])
    # END SOLUTION


# %%
try:
    e_log, e_full = effect(log), effect(full)
except NotImplementedError:
    e_log, e_full = U.reference("d3_1", "effects")
U.keep("d3_1", "effects", [e_log, e_full])
print(f"effect from the export:      {e_log * 100:+.2f} points")
print(f"effect as assigned:          {e_full * 100:+.2f} points")
print(f"the fault adds               {(e_log - e_full) * 100:+.2f} points to the reminder's credit")
U.check(e_log > e_full + 0.003, "the faulty export overstates the effect")

# %% [markdown]
# **What to analyse.** All 60,000 holders, in the arm the coin gave them, including the 1,014 whom the reminder never reached. That is "as assigned" on the pre-registration. It estimates the effect of *deciding to send* reminders through this platform, failures included, which is the decision Sahar faces. The tempting alternative, dropping the unreached holders, is what the export did by accident.

# %% [markdown]
# ## ✱ Stretch · False alarms of the ratio check
#
# Assign 60,000 holders with a fair coin, 20,000 times, and count how often the check fails at 0.001.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(41)
    reps = U.pick(20_000, 4_000)
    n_r = gen.binomial(60_000, 0.5, size=reps)
    p = stats.chi2.sf((2 * n_r - 60_000) ** 2 / 60_000, 1)
    share = float((p < U.RATIO_ALPHA).mean())
    print(f"a healthy assignment fails the check in {share:.2%} of {reps:,} simulated tests")
    return share
    # END SOLUTION


try:
    U.keep("d3_1", "false_alarms", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: the sample ratio of the export (failed) and of the assignment (passed); the balance of four covariates.",
       f"Found: {n_miss:,} reminder-arm e-mail holders of week 1 are missing from the export, which adds {(e_log - e_full) * 100:.2f} points to the estimate.",
       "Not checked: whether outcomes in the permit register are complete for both arms. Ask the register's owner before the result note is signed.")

# %% [markdown]
# ## Checkpoint
#
# 1. The ratio check fails with p = 0.000004. A colleague says the difference is "only one per cent". What do you answer?
#    <details><summary>Answer</summary>The size of the gap is not the point. A fair coin does not produce it, so something other than the coin removed or added units, and that something may be related to the outcome.</details>
# 2. Why not simply delete the same kind of holder from the control arm?
#    <details><summary>Answer</summary>That repairs the comparison only if you know exactly which holders were lost and why. Here you do, and the cleaner course is still to analyse everyone as assigned, which needs no such argument.</details>
# 3. The ratio check passes. Is the test sound?
#    <details><summary>Answer</summary>Not necessarily. Equal counts do not prove that the right holders are in each arm or that outcomes were recorded alike. The check catches one family of faults.</details>
#
# ## Carry forward
#
# Lab 3.2 analyses `renewal_test.csv`, the test as assigned. It does not need your result.
