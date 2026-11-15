# %% [markdown]
# # Lab 1.4 · Complete and review a pre-registration
#
# Day 1 · Session 4 (Pre-registration) · 25 min.
#
# You complete the one-page pre-registration of the reminder test and then review another one, written for the same test by a colleague in a hurry. The reviewer's checklist has twelve items; the same list is in `checklist.md` and will be used on your capstone.
#
# **AI policy.** AI-off. You will defend this page; write it yourself.
#
# **Reference state.** `data/prereg_start.json`, the first half of the page as lab 1.2 leaves it, and `data/prereg_neighbour.json`, the page you review. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Load the first half; add the unit, the size and the duration (5')
# - [ ] 2 · Write the analysis plan and the planned checks (6')
# - [ ] 3 · Write the data paragraph (4')
# - [ ] 4 · Run the checklist on your page (3')
# - [ ] 5 · Review the neighbour's page against the checklist (7')
# - [ ] ✱ Stretch · Rewrite the neighbour's primary metric and stop rule so that they pass

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

for cid, name, meaning in U.CHECKLIST:
    print(f"{cid:<4}{name:<20}{meaning}")

# %% [markdown]
# ## 1 · Load the first half; add the unit, the size and the duration (5')
#
# The first half holds the decision, hypothesis, arms, primary metric, minimum effect, guardrails and stop rule. If you finished lab 1.2 you may paste your own texts over it.

# %%
record = U.js("prereg_start.json")
U.show_prereg(record)

# %% [markdown]
# The office's statistics unit gives a provisional figure: about 9,200 holders per arm to detect 2 points, reached in about nine days of traffic. Day 2 checks both numbers. For today:
#
# ✏️ **Exercise** · Return a dictionary with `unit`, `unit_reason` (at least 8 words), `sample_size_per_arm` and `duration_days`. The duration must cover whole weeks and one month-end. The stop rule already on the page says how long the test runs: the two must agree.

# %%
def unit_size_duration():
    # BEGIN SOLUTION
    return {
        "unit": "permit holder",
        "unit_reason": "A holder with several permits would otherwise receive both versions. Each holder is enrolled once, at the first notice in the window.",
        "sample_size_per_arm": 9200,
        "duration_days": 28,
    }
    # END SOLUTION


# %%
try:
    part = unit_size_duration()
except NotImplementedError:
    part = U.reference("d1_4", "unit_size")
U.keep("d1_4", "unit_size", part)
record.update(part)
got = U.prereg_check(record, items=("C3", "C8"))
U.check(all(got.values()), "the unit has a reason and the duration is a whole number of weeks")
U.check("28" in record["stop_rule"] and record["duration_days"] == 28, "the duration agrees with the stop rule: 28 days")

# %% [markdown]
# **Look at.** Nine days would reach the size. Twenty-eight is what the calendar asks for: four whole weeks and one month-end. The larger of the two wins, and lab 2.4 shows why.

# %% [markdown]
# ## 2 · Write the analysis plan and the planned checks (6')
#
# The analysis plan is written now so that nobody, you included, can choose the analysis after seeing which one wins.
#
# ✏️ **Exercise** · Return a dictionary with two texts.
#
# - `analysis_plan`: the test, the interval, the unit of analysis, and that holders are analysed **as assigned**, whether or not the reminder reached them. Say how subgroups will be treated.
# - `checks`: what is checked before the result is read: the sample ratio and the balance of named covariates.

# %%
def plan_and_checks():
    # BEGIN SOLUTION
    return {
        "analysis_plan": "A two-proportion z-test and a 95% interval for the difference in on-time renewal, with holders as the unit, "
                         "analysed as assigned whether or not the reminder was delivered. Subgroups by channel and by prior lateness are "
                         "exploratory and are reported as such.",
        "checks": "Before the result is read: a sample ratio check against 50/50, failed below p = 0.001, and a balance table of channel, "
                  "holder type, prior lateness and tenure.",
    }
    # END SOLUTION


# %%
try:
    part = plan_and_checks()
except NotImplementedError:
    part = U.reference("d1_4", "plan")
U.keep("d1_4", "plan", part)
record.update(part)
got = U.prereg_check(record, items=("C9", "C10"))
U.check(all(got.values()), "the plan names the test, the interval and analysis as assigned; the checks name the ratio and the balance")

# %% [markdown]
# ## 3 · Write the data paragraph (4')
#
# The test uses the office's service logs for a purpose beyond sending notices, and the logs describe people. Abdullah Al-Hogail, the data protection officer, signs the page only if it says which fields are used, how holders are kept unidentifiable to the analyst, how results are reported and when the extract is deleted. The course treats the logs under the Personal Data Protection Law and the General Rules for Secondary Use of Data; read both before you write such a paragraph at work.
#
# ✏️ **Exercise** · Return the `data` paragraph: at least 15 words, naming the fields, pseudonymised keys and aggregate reporting.

# %%
def data_paragraph():
    # BEGIN SOLUTION
    return ("Fields used: a pseudonymised notice key, send date, permit type, holder type, channel, prior lateness, tenure, arm and outcomes. "
            "No name, phone number or address leaves the messaging platform. Results are reported in aggregate, never by holder, "
            "and the extract is deleted when the report is signed.")
    # END SOLUTION


# %%
try:
    data_text = data_paragraph()
except NotImplementedError:
    data_text = U.reference("d1_4", "data")
U.keep("d1_4", "data", data_text)
record["data"] = data_text
print(data_text)

# %% [markdown]
# ## 4 · Run the checklist on your page (3')

# %%
mine = U.prereg_check(record)
U.check(all(mine.values()), "your page passes all twelve items of the mechanical check")
print()
U.show_prereg(record)

# %% [markdown]
# ## 5 · Review the neighbour's page against the checklist (7')
#
# Here is another page for the same test. Read it as its reviewer. In class, swap pages with a real neighbour afterwards and do the same.

# %%
neighbour = U.js("prereg_neighbour.json")
U.show_prereg(neighbour)

# %% [markdown]
# ✏️ **Exercise** · Return a dictionary from checklist id (`"C1"` to `"C12"`) to `"pass"` or `"fail"`. Judge the sense, not only the presence: a unit can be stated and still be wrong.

# %%
def review():
    # BEGIN SOLUTION
    return {"C1": "pass", "C2": "pass", "C3": "fail", "C4": "fail", "C5": "fail", "C6": "fail",
            "C7": "fail", "C8": "fail", "C9": "fail", "C10": "pass", "C11": "fail", "C12": "pass"}
    # END SOLUTION


# %%
try:
    verdicts = review()
except NotImplementedError:
    verdicts = U.reference("d1_4", "review")
U.keep("d1_4", "review", verdicts)
score = U.mark_review(verdicts)
U.check(score >= 10, "your review agrees with the key on at least 10 of the 12 items")

# %%
machine = U.prereg_check(neighbour, quiet=True)
key = U.js("prereg_neighbour_key.json")
differ = [cid for cid in machine if machine[cid] != (key[cid]["verdict"] == "pass")]
print("items the mechanical check passes and a reader fails:", ", ".join(differ) or "none")
U.keep("d1_4", "differ", differ)
U.check("C3" in differ, "the mechanical check accepts the neighbour's unit because a unit is written; a reader sees that it is the wrong one")

# %% [markdown]
# **Look at.** The mechanical check sees that a unit, a primary metric and an action are written down. It cannot see that the coin is tossed per notice, that the "primary metric" is two metrics, or that the decision has no number in it. A checklist is a list of questions for a reader. Never sign a page because a script printed twelve ticks.

# %% [markdown]
# ## ✱ Stretch · Repair two items
#
# Rewrite the neighbour's primary metric and stop rule so that items C4 and C7 pass, keeping the neighbour's own duration.

# %%
def stretch():
    # BEGIN SOLUTION
    fixed = dict(neighbour)
    fixed["primary_metric"] = {"name": "on-time renewal", "definition": "the share of holders who renew on or before the expiry date of the permit in the notice"}
    fixed["stop_rule"] = "The test ends on the planned date with one analysis of the primary metric. There is no early stop for a good result; a guardrail may stop it."
    got = U.prereg_check(fixed, items=("C4", "C7"))
    return all(got.values())
    # END SOLUTION


try:
    U.keep("d1_4", "stretch", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked mechanically: all twelve items are present and specific on your page.",
       f"Checked against the key: your review of the neighbour's page, {score} of 12.",
       "Not checked: the sample size and the duration. They are provisional until labs 2.1 to 2.4, and a pre-registration is amended, with a date, before the test starts, never after.")

# %% [markdown]
# ## Checkpoint
#
# 1. The test is running and you realise a better primary metric exists. May you switch?
#    <details><summary>Answer</summary>Not for this test. Report the pre-registered metric as primary and the new one as exploratory, and pre-register the new one for the next test.</details>
# 2. Why does the page say "analysed as assigned"?
#    <details><summary>Answer</summary>The coin made the arms comparable. Dropping holders the reminder did not reach removes them from one arm only, and the arms stop being comparable.</details>
# 3. What does the data protection officer look for on the page?
#    <details><summary>Answer</summary>Which fields are used and why, that the analyst cannot identify a holder, that results are aggregate, and when the extract is deleted.</details>
#
# ## Carry forward
#
# The complete reference page is `solutions/prereg_reference.json`. Day 2 checks its two numbers, 9,200 per arm and 28 days. `prereg_template.md` is the same page as a form for your capstone.
