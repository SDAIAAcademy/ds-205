# %% [markdown]
# # Lab 1.2 · The first half of the pre-registration
#
# Day 1 · Session 2 (Decision, hypothesis and metrics) · 25 min.
#
# Sahar's question: "Would a reminder message, seven days before a permit expires, get more holders to renew on time?" Today every holder gets one renewal notice 30 days before expiry and nothing after it. You write the first half of the test's pre-registration as a record: the decision, the hypothesis, one primary metric with its baseline, the minimum effect, two guardrails and the stop rule. A checklist reads the record when you are done.
#
# **AI policy.** AI-off. The words are yours: a pre-registration written by an assistant is one you cannot defend.
#
# **Reference state.** `data/history_daily.csv`, 182 days of notices before the test. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Write the decision and the hypothesis (6')
# - [ ] 2 · Choose the primary metric and measure its baseline (5')
# - [ ] 3 · Set the minimum effect from the cost table (5')
# - [ ] 4 · Write two guardrails with thresholds and actions (5')
# - [ ] 5 · Write the stop rule and run the checklist (4')
# - [ ] ✱ Stretch · Add a secondary metric and say why it is not a second primary metric

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

record = {"title": "Does a reminder seven days before expiry raise on-time renewal?"}
PART = ("C1", "C2", "C4", "C5", "C6", "C7")   # the checklist items this lab writes; lab 1.4 writes the rest

# %% [markdown]
# ## 1 · Write the decision and the hypothesis (6')
#
# A test that cannot change what the office does is not worth running. Start from the decision: who decides, what they will do if the reminder helps enough, and what they will do if it does not.
#
# ✏️ **Exercise** · Return a dictionary with four texts:
#
# - `decision`: who decides, and the action for each result. Use the word "if". At least 15 words.
# - `hypothesis`: the change, the metric and the direction. At least 8 words.
# - `arms`: who gets what in each arm, and how holders are put into arms.
# - `withholding`: why it is acceptable that half of the holders do not get the reminder.

# %%
def decision_and_hypothesis():
    # BEGIN SOLUTION
    return {
        "decision": "Sahar Al-Wuhaibi decides whether every renewal notice is followed by a reminder message seven days before expiry. "
                    "If the reminder raises on-time renewal by at least 2 points and no guardrail is crossed, the office adopts it for all permit types. "
                    "If the effect is smaller, or a guardrail is crossed, the office keeps the standard notice.",
        "hypothesis": "Holders who get the reminder renew on time more often than holders who get only the standard notice.",
        "arms": "Control: the standard renewal notice 30 days before expiry, as today. Reminder: the same notice plus one reminder message "
                "seven days before expiry. A seeded coin per holder puts half in each arm.",
        "withholding": "Nobody loses a service they have today: the control arm gets the current notice. The reminder is untested, "
                       "so giving it to half of the holders for 28 days is how the office learns whether it helps.",
    }
    # END SOLUTION


# %%
try:
    part1 = decision_and_hypothesis()
except NotImplementedError:
    part1 = U.reference("d1_2", "part1")
U.keep("d1_2", "part1", part1)
record.update(part1)
got = U.prereg_check(record, items=("C1", "C2"))
U.check(all(got.values()), "the decision names an action for each result and the hypothesis has a direction")

# %% [markdown]
# **Look at.** Read your decision again and look for the number. "If the reminder helps" is not a decision rule; "by at least 2 points" is. Step 3 supplies the number if you left it out.

# %% [markdown]
# ## 2 · Choose the primary metric and measure its baseline (5')
#
# The history file has one row per day for the 182 days before the test.

# %%
hist = U.history()
print(hist.head(8).to_string(index=False))

# %% [markdown]
# ✏️ **Exercise** · Return `(primary, baseline)`: the primary metric as a dictionary with a `name` and a `definition` (who counts, by when), and its baseline over the 182 days as a share between 0 and 1. One metric only.

# %%
def primary_metric():
    # BEGIN SOLUTION
    primary = {"name": "on-time renewal",
               "definition": "the share of holders who renew on or before the expiry date of the permit named in the notice"}
    baseline = hist["renewed_on_time"].sum() / hist["notices_sent"].sum()
    return primary, float(baseline)
    # END SOLUTION


# %%
try:
    primary, baseline = primary_metric()
except NotImplementedError:
    primary, baseline = U.reference("d1_2", "primary")
U.keep("d1_2", "primary", [primary, baseline])
record["primary_metric"] = primary
print(f"primary metric: {primary['name']}; baseline {baseline:.1%} over {hist['notices_sent'].sum():,} notices")
U.check(abs(baseline - hist["renewed_on_time"].sum() / hist["notices_sent"].sum()) < 1e-9, "the baseline is all renewals over all notices, not the mean of 182 daily rates")

# %% [markdown]
# **Look at.** The mean of the daily rates would give busy days and quiet days the same weight. The metric counts holders, so the baseline does too.

# %% [markdown]
# ## 3 · Set the minimum effect from the cost table (5')
#
# The minimum effect of interest is the smallest gain that would change the decision. The finance team gives two figures, in riyals.

# %%
COST = {"reminder_per_holder": 0.40,    # the message, and handling the replies and complaints it brings
        "late_renewal": 20.00}          # staff time to process one late renewal and its fee
print(COST)

# %% [markdown]
# ✏️ **Exercise** · Return `(minimum_effect, reason)`. The reminder pays for itself when the late renewals it prevents cost more than the reminders sent. Work out the break-even gain in on-time renewal as a share, and give the reason in a sentence of at least 8 words.

# %%
def minimum_effect():
    # BEGIN SOLUTION
    effect = COST["reminder_per_holder"] / COST["late_renewal"]
    reason = "Below 2 points the late renewals avoided do not cover the cost of the messages and of the complaints they bring."
    return effect, reason
    # END SOLUTION


# %%
try:
    mde, mde_reason = minimum_effect()
except NotImplementedError:
    mde, mde_reason = U.reference("d1_2", "mde")
U.keep("d1_2", "mde", [mde, mde_reason])
record["minimum_effect"], record["minimum_effect_reason"] = mde, mde_reason
print(f"minimum effect of interest: {mde:.1%} of holders, which is {mde * 100:.0f} points on a baseline of {baseline:.1%}")
U.check(abs(mde - 0.02) < 1e-9, "the break-even gain is 2 points: 0.40 riyals over 20 riyals")

# %% [markdown]
# **Look at.** Points, not per cent. A gain of 2 points takes on-time renewal from about 62% to about 64%. A gain of "2%" could also be read as 2% of 62%, which is 1.2 points. Write "points" every time.

# %% [markdown]
# ## 4 · Write two guardrails with thresholds and actions (5')
#
# A guardrail is a metric that must not get worse while the primary metric improves. Each one needs a metric, a threshold and the action when the threshold is crossed. One of yours must protect a **group** of holders: a reminder that helps on average can still harm holders reached by one channel.
#
# ✏️ **Exercise** · Return a list of two dictionaries with `metric`, `threshold` (a number) and `action`.

# %%
def guardrails():
    # BEGIN SOLUTION
    return [
        {"metric": "complaint rate", "threshold": 0.005,
         "action": "stop the test if the reminder arm exceeds control by more than this, and review the wording"},
        {"metric": "on-time renewal in each group (channel, holder type)", "threshold": -0.03,
         "action": "stop the reminder for a group whose rate falls below control by more than this, and tell the data protection officer"},
    ]
    # END SOLUTION


# %%
try:
    g = guardrails()
except NotImplementedError:
    g = U.reference("d1_2", "guardrails")
U.keep("d1_2", "guardrails", g)
record["guardrails"] = g
got = U.prereg_check(record, items=("C4", "C5", "C6"))
U.check(all(got.values()), "one primary metric, a numeric minimum effect, and guardrails with thresholds and actions")
U.check(any(U._has(x.get("metric"), ("group", "channel", "holder type", "subgroup")) for x in g), "one guardrail protects a group of holders")

# %% [markdown]
# ## 5 · Write the stop rule and run the checklist (4')
#
# The stop rule says when the test ends and what could end it sooner. Two things must be in it: the end is fixed in advance, and a good-looking result does not end the test early. A guardrail may.
#
# ✏️ **Exercise** · Return the stop rule: at least 12 words, for a test of 28 days with one safety look at the guardrails.

# %%
def stop_rule():
    # BEGIN SOLUTION
    return ("The test runs 28 days and ends on the planned date. There is one analysis of the primary metric, at the end. "
            "One safety look on day 14 reads the guardrails only. There is no early stop for a good result.")
    # END SOLUTION


# %%
try:
    stop = stop_rule()
except NotImplementedError:
    stop = U.reference("d1_2", "stop")
U.keep("d1_2", "stop", stop)
record["stop_rule"] = stop
got = U.prereg_check(record, items=PART)
U.check(all(got.values()), "the first half passes the six checklist items it covers")
print()
U.show_prereg(record)

# %% [markdown]
# **Look at.** The checklist is mechanical: it finds a missing threshold, not a foolish one. Read your neighbour's record and ask one question the checklist cannot: "would Sahar know what to do on the last day?"

# %% [markdown]
# ## ✱ Stretch · A secondary metric
#
# Counter visits may fall if more holders renew on time online. Add it as a secondary metric and write one sentence on why it is not a second primary metric.

# %%
def stretch():
    # BEGIN SOLUTION
    record["secondary_metrics"] = ["counter visits within 30 days of the notice"]
    why = ("Two primary metrics give two chances of a win. The decision rests on on-time renewal alone; "
           "counter visits are reported to help explain the result, whatever they show.")
    print(why)
    return why
    # END SOLUTION


try:
    U.keep("d1_2", "stretch", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked: six checklist items (decision, hypothesis, primary metric, minimum effect, guardrails, stop rule) are present and specific.",
       f"Checked against the history: the baseline, {baseline:.1%}, and the break-even gain, {mde * 100:.0f} points.",
       "Not checked: whether the thresholds are wise. That is a judgement for Sahar and the data protection officer, and for your neighbour's review in lab 1.4.")

# %% [markdown]
# ## Checkpoint
#
# 1. Why one primary metric and not two?
#    <details><summary>Answer</summary>Each extra primary metric is another chance of a false win. One metric carries the decision; the others explain.</details>
# 2. The complaint rate rises by 0.2 points in the reminder arm. The threshold is 0.5. What happens?
#    <details><summary>Answer</summary>Nothing stops. The guardrail is reported in the result note. A threshold written in advance is what keeps this from becoming an argument.</details>
# 3. Why is withholding the reminder from half of the holders acceptable here?
#    <details><summary>Answer</summary>The control arm keeps the service it has today, and nobody knows yet whether the reminder helps. If the office already knew, a test would not be acceptable, or needed.</details>
#
# ## Carry forward
#
# Lab 1.4 completes this record. It starts from `data/prereg_start.json`, so it does not need your result.
