# %% [markdown]
# # Lab 3.2 · Analyse the reminder test
#
# Day 3 · Session 2 (Estimate, interval and effect) · 25 min.
#
# You analyse the reminder test as the pre-registration says: 60,000 holders as assigned, one primary metric, a difference in proportions with a 95% interval and a two-proportion z-test. You read the interval against the minimum effect of 2 points, report the guardrails and the secondary metric, look at one subgroup with care, and state the result in two sentences that Sahar can act on.
#
# **AI policy.** AI-off for steps 1 to 3: this is the first pass of an analysis step. The tutor instruction may hint from step 4.
#
# **Reference state.** `data/renewal_test.csv`, the test as assigned. Nothing from lab 3.1 is needed: its conclusion was to analyse this file.
#
# **Tasks**
# - [ ] 1 · Counts and rates by arm (4')
# - [ ] 2 · Difference, standard error and 95% interval (6')
# - [ ] 3 · The test and the minimum effect (4')
# - [ ] 4 · Guardrails and the secondary metric (4')
# - [ ] 5 · One subgroup, read with care (3')
# - [ ] 6 · The result in two sentences (4')
# - [ ] ✱ Stretch · Bootstrap the difference over holders and compare the two intervals

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

test = U.renewal_test()
print(test.head(5).to_string(index=False))
print(f"\n{len(test):,} holders; sample ratio check p = {U.ratio_p((test['arm'] == 'control').sum(), (test['arm'] == 'reminder').sum()):.2f} (passed in lab 3.1)")

# %% [markdown]
# ## 1 · Counts and rates by arm (4')
#
# ✏️ **Exercise** · Write `arm_counts(df, outcome)` returning `(x_control, n_control, x_reminder, n_reminder)`: the number of holders with `outcome` equal to 1, and the number of holders, in each arm.

# %%
def arm_counts(df, outcome):
    # BEGIN SOLUTION
    c, r = df[df["arm"] == "control"], df[df["arm"] == "reminder"]
    return int(c[outcome].sum()), len(c), int(r[outcome].sum()), len(r)
    # END SOLUTION


# %%
try:
    x_c, n_c, x_r, n_r = arm_counts(test, "renewed_on_time")
except NotImplementedError:
    x_c, n_c, x_r, n_r = U.reference("d3_2", "counts")
U.keep("d3_2", "counts", [x_c, n_c, x_r, n_r])
U.table(["arm", "holders", "renewed on time", "rate"], [["control", f"{n_c:,}", f"{x_c:,}", f"{x_c / n_c:.2%}"], ["reminder", f"{n_r:,}", f"{x_r:,}", f"{x_r / n_r:.2%}"]])
U.check(n_c + n_r == 60_000 and 0.60 < x_c / n_c < 0.63, "60,000 holders, and the control arm renews at about the historical baseline")

# %% [markdown]
# ## 2 · Difference, standard error and 95% interval (6')
#
# The estimate is the difference of the two rates. Its standard error, for the interval, is
#
# SE = √( p_c(1 − p_c)/n_c + p_r(1 − p_r)/n_r )
#
# and the 95% interval is the estimate ± 1.96 × SE.
#
# ✏️ **Exercise** · Write `diff_interval(x1, n1, x2, n2)` returning `(difference, standard_error, low, high)`, arm 2 minus arm 1.

# %%
def diff_interval(x1, n1, x2, n2):
    # BEGIN SOLUTION
    p1, p2 = x1 / n1, x2 / n2
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    d = p2 - p1
    z = stats.norm.ppf(0.975)
    return float(d), float(se), float(d - z * se), float(d + z * se)
    # END SOLUTION


# %%
try:
    d, se, lo, hi = diff_interval(x_c, n_c, x_r, n_r)
except NotImplementedError:
    d, se, lo, hi = U.reference("d3_2", "interval")
U.keep("d3_2", "interval", [d, se, lo, hi])
print(f"effect of the reminder on on-time renewal: {d * 100:+.2f} points, standard error {se * 100:.2f}, 95% interval {lo * 100:+.2f} to {hi * 100:+.2f} points")
ref = U.z_test(x_c, n_c, x_r, n_r)
U.check(abs(d - ref[0]) < 1e-12 and abs(se - ref[1]) < 1e-12, "difference and standard error agree with the reference")
U.check(lo > 0, "the whole interval is above zero")

# %% [markdown]
# ## 3 · The test and the minimum effect (4')
#
# The pre-registered test is the two-proportion z-test; `U.z_test` returns its p-value. The more useful reading is the interval against the **minimum effect of 2 points**.
#
# ✏️ **Exercise** · Write `read_against(low, high, minimum)` returning `"above"` if the whole interval is above the minimum effect, `"below"` if the whole interval is below it, and `"straddles"` otherwise.

# %%
def read_against(low, high, minimum):
    # BEGIN SOLUTION
    if low > minimum:
        return "above"
    if high < minimum:
        return "below"
    return "straddles"
    # END SOLUTION


# %%
p_value = ref[2]
try:
    reading = read_against(lo, hi, U.MIN_EFFECT)
except NotImplementedError:
    reading = U.reference("d3_2", "reading")
U.keep("d3_2", "reading", reading)
print(f"z-test: p = {p_value:.1e}. Statistically significant: {'yes' if p_value < U.ALPHA else 'no'}")
print(f"interval {lo * 100:.2f} to {hi * 100:.2f} points against the minimum effect of {U.MIN_EFFECT * 100:.0f} points: {reading}")
U.check(p_value < 0.001, "the reminder has an effect: zero is far outside the interval")
U.check(reading == "straddles", "the interval contains the minimum effect: the data do not settle whether the gain reaches 2 points")

# %% [markdown]
# **Look at.** Two different questions, two different answers. "Is there an effect?" Yes, beyond reasonable doubt. "Is it at least the 2 points that pay for the messages?" The estimate says just, and the interval says: somewhere between 1.4 and 2.9. A p-value below one in a million tells Sahar nothing about the second question.

# %% [markdown]
# ## 4 · Guardrails and the secondary metric (4')
#
# The pre-registration has two guardrails: the complaint rate (stop if the reminder arm exceeds control by more than 0.5 points) and on-time renewal in each group by channel and holder type (stop for a group that falls more than 3 points below control).
#
# ✏️ **Exercise** · Write `complaints_guardrail(df)` returning `(difference, high)`: the difference in complaint rate, reminder minus control, and the upper end of its 95% interval. Reuse `arm_counts` and `diff_interval`.

# %%
def complaints_guardrail(df):
    # BEGIN SOLUTION
    dd, _, _, h = diff_interval(*arm_counts(df, "complained"))
    return dd, h
    # END SOLUTION


# %%
try:
    g_diff, g_hi = complaints_guardrail(test)
except NotImplementedError:
    g_diff, g_hi = U.reference("d3_2", "complaints")
U.keep("d3_2", "complaints", [g_diff, g_hi])
print(f"complaint rate: {g_diff * 100:+.2f} points, at most {g_hi * 100:+.2f} at the upper end of the interval; threshold +0.50: {'held' if g_hi < 0.005 else 'check'}")
U.check(g_hi < 0.005, "the complaint guardrail holds even at the upper end of its interval")

try:
    groups = []
    for col in ("channel", "holder_type"):
        for level, g in test.groupby(col):
            gd, _, glo, ghi = diff_interval(*arm_counts(g, "renewed_on_time"))
            groups.append([f"{col} = {level}", f"{len(g):,}", f"{gd * 100:+.2f}", f"{glo * 100:+.2f} to {ghi * 100:+.2f}"])
    s_diff, _, s_lo, s_hi = diff_interval(*arm_counts(test, "counter_visit"))
except NotImplementedError:
    groups = U.reference("d3_2", "groups")
    s_diff, s_lo, s_hi = U.reference("d3_2", "counter")
U.keep("d3_2", "groups", groups)
U.table(["group", "holders", "effect, points", "95% interval"], groups)
worst = min(float(r[2]) for r in groups)
U.keep("d3_2", "worst_group", worst)
U.check(worst > -3.0, "no group falls more than 3 points below control: the group guardrail holds")

U.keep("d3_2", "counter", [s_diff, s_lo, s_hi])
print(f"secondary metric, counter visits: {s_diff * 100:+.2f} points ({s_lo * 100:+.2f} to {s_hi * 100:+.2f})")

# %% [markdown]
# **Look at.** A guardrail is read with its interval too: "no increase found" is weaker than "an increase above the threshold is ruled out". Here both hold. Look at the e-mail row: almost no effect, with a wide interval. No harm, so the guardrail holds, but a quarter of the e-mail holders in the reminder arm never got the reminder (lab 3.1). The secondary metric moved in a helpful direction, which supports the story and does not change the decision rule.

# %% [markdown]
# ## 5 · One subgroup, read with care (3')
#
# The pre-registration named prior lateness as an exploratory subgroup.
#
# ✏️ **Exercise** · Write `subgroup_effects(df, col)` returning a dictionary from each level of `col` to `(difference, low, high)`.

# %%
def subgroup_effects(df, col):
    # BEGIN SOLUTION
    out = {}
    for level, g in df.groupby(col):
        dd, _, l, h = diff_interval(*arm_counts(g, "renewed_on_time"))
        out[level] = (dd, l, h)
    return out
    # END SOLUTION


# %%
try:
    sub = subgroup_effects(test, "prior_late")
except NotImplementedError:
    sub = {int(k): tuple(v) for k, v in U.reference("d3_2", "subgroups").items()}
U.keep("d3_2", "subgroups", {int(k): list(v) for k, v in sub.items()})
for level, (dd, l, h) in sub.items():
    print(f"prior_late = {level}: {dd * 100:+.2f} points ({l * 100:+.2f} to {h * 100:+.2f}), {int((test['prior_late'] == level).sum()):,} holders")
gap = sub[1][0] - sub[0][0]
gap_se = np.sqrt(((sub[1][2] - sub[1][1]) / 3.92) ** 2 + ((sub[0][2] - sub[0][1]) / 3.92) ** 2)
U.keep("d3_2", "gap", [gap, gap - 1.96 * gap_se, gap + 1.96 * gap_se])
print(f"difference between the two subgroups: {gap * 100:+.2f} points ({(gap - 1.96 * gap_se) * 100:+.2f} to {(gap + 1.96 * gap_se) * 100:+.2f})")
U.check((sub[1][2] - sub[1][1]) > 1.5 * (sub[0][2] - sub[0][1]), "the smaller subgroup has the wider interval")

# %% [markdown]
# **Look at.** Compare the subgroups by the interval of their **difference**, never by "significant in one and not in the other". One subgroup having a larger estimate is what you would see by chance in most splits. Report it as exploratory, as the page promised, and as a hypothesis for the next test.

# %% [markdown]
# ## 6 · The result in two sentences (4')
#
# ✏️ **Exercise** · Return two sentences for Sahar. The first gives the estimate and its interval, in points, to one decimal. The second reads them against the minimum effect and the guardrails and says what the evidence supports. Use the word "points" and name the "minimum effect".

# %%
def two_sentences():
    # BEGIN SOLUTION
    return (f"The reminder raised on-time renewal by {d * 100:.1f} points, and the data are consistent with a gain between {lo * 100:.1f} and {hi * 100:.1f} points. "
            f"The estimate meets the minimum effect of 2 points, though the gain may be somewhat smaller, and no guardrail was crossed, so the evidence supports adopting the reminder.")
    # END SOLUTION


# %%
try:
    text = two_sentences()
except NotImplementedError:
    text = U.reference("d3_2", "sentences")
U.keep("d3_2", "sentences", text)
print(text)
print()
U.sentence_check(text, {"estimate": f"{d * 100:.1f}", "lower limit": f"{lo * 100:.1f}", "upper limit": f"{hi * 100:.1f}"},
                 ["points", "minimum effect", ("guardrail", "complaint")])

# %% [markdown]
# **Look at.** The decision rule on the page was "adopt if the reminder raises on-time renewal by at least 2 points and no guardrail is crossed". The estimate clears it, narrowly. An honest note says both things: the rule is met, and the true gain may sit a little below break-even. What it must not say is "highly significant, p below 0.001", which answers a question the director did not ask.

# %% [markdown]
# ## ✱ Stretch · A bootstrap interval
#
# Resample holders within each arm, 2,000 times, and take the percentile interval of the difference, as in DS-201.

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(51)
    b = U.pick(2000, 400)
    diffs = gen.binomial(n_r, x_r / n_r, size=b) / n_r - gen.binomial(n_c, x_c / n_c, size=b) / n_c
    l, h = np.percentile(diffs, [2.5, 97.5])
    print(f"bootstrap interval {l * 100:+.2f} to {h * 100:+.2f} points; formula interval {lo * 100:+.2f} to {hi * 100:+.2f}")
    # Resampling 0/1 outcomes with replacement inside an arm is a binomial draw, so no loop over holders is needed.
    return [float(l), float(h)]
    # END SOLUTION


try:
    U.keep("d3_2", "bootstrap", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked: the difference and its standard error against the reference function; the interval, {lo * 100:.2f} to {hi * 100:.2f} points.",
       "Checked: both guardrails, each with its interval.",
       "Not checked here: the sample ratio and the balance (lab 3.1 did), and whether outcomes for the last notices were complete when the file was cut.",
       "Exploratory, not confirmed: the larger effect among holders who were late before.")

# %% [markdown]
# ## Checkpoint
#
# 1. The p-value is tiny and the interval straddles the minimum effect. Which do you report first?
#    <details><summary>Answer</summary>The estimate and its interval, against the minimum effect. The p-value answers "is it zero?", which nobody doubted after 60,000 holders.</details>
# 2. The effect is "significant" among holders who were late before and "not significant" among the others. Do the subgroups differ?
#    <details><summary>Answer</summary>That comparison cannot tell. Compute the difference between the two effects with its own interval.</details>
# 3. Why does the result note quote the guardrail's upper limit and not only its estimate?
#    <details><summary>Answer</summary>A guardrail asks whether harm above the threshold can be ruled out. Only the upper end of the interval answers that.</details>
#
# ## Carry forward
#
# The capstone's result note has this shape: estimate, interval, checks, recommendation.
