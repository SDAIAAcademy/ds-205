# %% [markdown]
# # Lab 3.4 · Review a write-up
#
# Day 3 · Session 4 (Reviewing a reported result) · 25 min.
#
# Hattan Al-Sayed has written up the test of the redesigned form and recommends replacing every online form of the office. Rehab Al-Tayyar asks you to review it before it goes to the director. You mark the flaws against a catalogue, recompute two of the write-up's claims from the log, draft the memo and choose your capstone case.
#
# **AI policy.** AI-off for step 1: finding the flaws is the skill. From step 2 the tutor instruction may hint on code. The memo's judgement is yours; you will defend a memo like it in the capstone.
#
# **Reference state.** `data/writeup_form.md` and `data/form_pages.csv`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Read the write-up and mark the flaws (7')
# - [ ] 2 · Recompute two claims from the log (7')
# - [ ] 3 · Draft the memo: flaw, consequence, supported decision (8')
# - [ ] 4 · Choose your capstone case (3')
# - [ ] ✱ Stretch · Compare completion only on devices that were logged in both arms

# %%
import os, sys, subprocess, json
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

# %% [markdown]
# ## 1 · Read the write-up and mark the flaws (7')
#
# Read in the review order of the session: **design** (what was planned), **checks** (did the arms survive), **analysis** (unit, metric, looks), **claim** (does the recommendation follow).

# %%
print(U.text("writeup_form.md"))

# %% [markdown]
# The catalogue has ten kinds of flaw. Some are in the write-up and some are not.

# %%
U.flaw_catalogue()

# %% [markdown]
# ✏️ **Exercise** · Return a dictionary from each of the ten flaw ids to `True` (present in the write-up) or `False`.

# %%
def flaws_found():
    # BEGIN SOLUTION
    return {"metric_switch": True, "wrong_unit": True, "peeking": True, "ratio_mismatch": True, "many_comparisons": True,
            "short_run": True, "overclaim": True, "no_control": False, "not_random": False, "different_measurement": False}
    # END SOLUTION


# %%
try:
    found = flaws_found()
except NotImplementedError:
    found = U.reference("d3_4", "found")
U.keep("d3_4", "found", found)
hits, alarms = U.mark_flaws(found)
U.check(hits >= 6 and alarms <= 1, "at least six of the seven seeded flaws found, with at most one false alarm")

# %% [markdown]
# ## 2 · Recompute two claims from the log (7')
#
# A review that only reads is an opinion. The log is available, so check two claims.
#
# **Claim 1.** "The redesigned form logged fewer applicants. We put this down to chance."
#
# ✏️ **Exercise** · Write `applicants_by_arm(pages)` returning `(n_current, n_redesign, p_value)`: the number of distinct applicants in each arm and the p-value of the sample ratio check.

# %%
pages = U.form_pages()


def applicants_by_arm(pages):
    # BEGIN SOLUTION
    n = pages.drop_duplicates("applicant_key")["arm"].value_counts()
    return int(n["current"]), int(n["redesign"]), U.ratio_p(int(n["current"]), int(n["redesign"]))
    # END SOLUTION


# %%
try:
    n_cur, n_red, p_ratio = applicants_by_arm(pages)
except NotImplementedError:
    n_cur, n_red, p_ratio = U.reference("d3_4", "ratio")
U.keep("d3_4", "ratio", [n_cur, n_red, p_ratio])
print(f"applicants: current form {n_cur:,}, redesigned form {n_red:,}; sample ratio check p = {p_ratio:.1g}")
U.check(p_ratio < U.RATIO_ALPHA, "chance does not explain the missing applicants")
print()
print(pages.drop_duplicates("applicant_key").groupby(["device", "arm"]).size().unstack("arm", fill_value=0).to_string())

# %% [markdown]
# **Look at.** One cell of the device table is zero. The redesigned form never logged an applicant on an old mobile browser. Those applicants were assigned to it, could not use it, and left no trace. In the current arm, the same kind of applicant is present, makes more errors and completes less often.

# %% [markdown]
# **Claim 2.** "With 53,514 page views the difference is highly significant."
#
# ✏️ **Exercise** · Write `error_test_by_applicant(pages)` returning `(share_current, share_redesign, p_value)`: the mean over applicants of each applicant's own error share, in each arm, and the p-value of a Welch t-test on those per-applicant shares.

# %%
def error_test_by_applicant(pages):
    # BEGIN SOLUTION
    per = pages.groupby(["applicant_key", "arm"])["validation_error"].mean().reset_index()
    cur = per.loc[per["arm"] == "current", "validation_error"]
    red = per.loc[per["arm"] == "redesign", "validation_error"]
    return float(cur.mean()), float(red.mean()), float(stats.ttest_ind(cur, red, equal_var=False).pvalue)
    # END SOLUTION


# %%
try:
    s_cur, s_red, p_applicant = error_test_by_applicant(pages)
except NotImplementedError:
    s_cur, s_red, p_applicant = U.reference("d3_4", "applicant_test")
U.keep("d3_4", "applicant_test", [s_cur, s_red, p_applicant])
a, b = pages[pages["arm"] == "current"], pages[pages["arm"] == "redesign"]
p_page = U.z_test(a["validation_error"].sum(), len(a), b["validation_error"].sum(), len(b))[2]
U.keep("d3_4", "p_page", p_page)
print(f"per page view, as in the write-up: {a['validation_error'].mean():.1%} against {b['validation_error'].mean():.1%}, p = {p_page:.4f}")
print(f"per applicant, as randomised:      {s_cur:.1%} against {s_red:.1%}, p = {p_applicant:.2f}")
U.check(p_page < 0.01 and p_applicant > 0.05, "significant when page views are counted, not significant when applicants are")

# %% [markdown]
# **Look at.** The same log, the same metric, and the "highly significant" result is gone once the unit of analysis is the unit that was randomised. And this is before the missing applicants are dealt with, who make the comparison lean towards the redesign.

# %% [markdown]
# ## 3 · Draft the memo: flaw, consequence, supported decision (8')
#
# A review memo has three parts. For each flaw: what it is and what it does to the reported result. Then the decision the evidence **does** support. Then what would settle the question. "The analysis is flawed" is not a memo; a director cannot act on it.
#
# ✏️ **Exercise** · Return a dictionary with
#
# - `flaws`: a list of at least five `(flaw_id, consequence)` pairs, each consequence at least 10 words;
# - `supported_decision`: at least 20 words on what the office can and cannot decide from this test;
# - `next_step`: at least 15 words on the test that would answer the question.

# %%
def memo():
    # BEGIN SOLUTION
    return {
        "flaws": [
            ("ratio_mismatch", "The redesigned form logged no applicant on an old mobile browser, so the arms no longer hold comparable applicants and every comparison leans towards the redesign."),
            ("wrong_unit", "Applicants were randomised but page views were analysed; counted per applicant, the difference in validation errors is not significant."),
            ("metric_switch", "The pre-registered primary metric, completion, shows no clear effect; the headline metric was chosen after the data were seen."),
            ("peeking", "The test was stopped on day 8 of 28 at a significant daily look, a rule that declares a win in a large share of tests with no effect."),
            ("many_comparisons", "Fourteen metrics and several subgroups were examined and the best were reported, so some apparent gain is expected by chance alone."),
            ("short_run", "Eight days cover one weekend and no month-end, and first reactions to a new form may fade."),
            ("overclaim", "One form was tested for eight days; nothing supports replacing all forms or the figure of 9,000 completed applications a year."),
        ],
        "supported_decision": "The evidence does not support rolling out the redesign. It supports one finding the write-up dismissed: the redesigned form "
                              "does not work on old mobile browsers, which must be fixed before any further test. On completion, the pre-registered metric, "
                              "the test shows no reliable difference.",
        "next_step": "Fix the old-browser fault, then run the test again for the full 28 days as pre-registered, with one analysis at the end, "
                     "completion as the primary metric, applicants as the unit of analysis and a sample ratio check before the result is read.",
    }
    # END SOLUTION


# %%
try:
    m = memo()
except NotImplementedError:
    m = U.reference("d3_4", "memo")
    m["flaws"] = [tuple(x) for x in m["flaws"]]
U.keep("d3_4", "memo", {**m, "flaws": [list(x) for x in m["flaws"]]})
print("REVIEW MEMO · to Rehab Al-Tayyar · the form redesign test\n")
for i, (flaw, consequence) in enumerate(m["flaws"], 1):
    print(f"{i}. {flaw}: {consequence}")
print(f"\nWhat the evidence supports. {m['supported_decision']}")
print(f"\nNext step. {m['next_step']}")
print()
key = {k["flaw"]: k["present"] for k in U.js("writeup_form_key.json")["key"]}
U.check(len(m["flaws"]) >= 5 and all(key.get(f, False) for f, _ in m["flaws"]), "the memo names at least five flaws, all of them really in the write-up")
U.check(all(len(c.split()) >= 10 for _, c in m["flaws"]), "every flaw comes with its consequence")
U.check(len(m["supported_decision"].split()) >= 20 and len(m["next_step"].split()) >= 15, "the memo says what the evidence supports and what would settle the question")
U.sentence_check(m["supported_decision"] + " " + m["next_step"], {}, [("not support", "does not show", "cannot"), ("browser", "old mobile"), ("28", "full", "planned")])

# %% [markdown]
# **Look at.** The most useful sentence of the memo is not about statistics. The test found a real fault in the redesigned form, and the write-up put it down to chance. A reviewer who only lists errors would have missed it too.

# %% [markdown]
# ## 4 · Choose your capstone case (3')
#
# Three cases, none used in class. Each has a history file for the sample size, a completed experiment log and a flawed write-up. The capstone pack is everything you did in this course, on your case: a pre-registration, a sample-size notebook, an analysis notebook, a result note and a review memo.

# %%
cases = json.loads((U.LABS / "capstone" / "cases.json").read_text(encoding="utf-8"))
for c in cases:
    print(f"Case {c['id']} · {c['title']}\n   {c['question']}\n   Minimum effect: {c['minimum_effect']}. {c['design_challenge']}\n")

# %% [markdown]
# ✏️ **Exercise** · Return `(case_id, reason)`: `"A"`, `"B"` or `"C"`, and one sentence of at least 10 words on why this case and what you expect to be hardest.

# %%
def my_case():
    # BEGIN SOLUTION
    return "C", "The training programme needs a cluster design, which I found hardest in lab 2.3, so I want to do it once more."
    # END SOLUTION


# %%
try:
    case_id, reason = my_case()
except NotImplementedError:
    case_id, reason = U.reference("d3_4", "case")
U.keep("d3_4", "case", [case_id, reason])
print(f"capstone case {case_id}: {reason}")
U.check(case_id in {c["id"] for c in cases} and len(reason.split()) >= 10, "a case is chosen, with a reason")

# %% [markdown]
# ## ✱ Stretch · Completion on devices logged in both arms
#
# Drop the applicants on old mobile browsers from the current arm too and compare completion again. What happens to the "right direction"?

# %%
def stretch():
    # BEGIN SOLUTION
    u = pages.drop_duplicates("applicant_key")
    both = u[u["device"] != "old mobile"]
    c, r = both[both["arm"] == "current"], both[both["arm"] == "redesign"]
    d, se, p = U.z_test(c["completed"].sum(), len(c), r["completed"].sum(), len(r))
    print(f"completion on devices logged in both arms: current {c['completed'].mean():.1%}, redesign {r['completed'].mean():.1%}, difference {d * 100:+.1f} points, p = {p:.2f}")
    # This comparison is a repair made after the fact, not the pre-registered analysis. It shows how fragile the write-up's direction is; it does not prove the reverse.
    return float(d)
    # END SOLUTION


try:
    U.keep("d3_4", "common_devices", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked against the key: {hits} of 7 seeded flaws found, {alarms} false alarm(s).",
       f"Recomputed from the log: the sample ratio (p = {p_ratio:.1g}) and the error difference per applicant (p = {p_applicant:.2f}).",
       "Not recomputed: the 14 metrics and the subgroup. The write-up does not list them, which is itself a finding for the memo.")

# %% [markdown]
# ## Checkpoint
#
# 1. A write-up has one serious flaw and a clear result. Is the result void?
#    <details><summary>Answer</summary>Not automatically. Ask what the flaw does to the number. A recomputation at the right unit, or as assigned, may confirm the result or remove it.</details>
# 2. Why does the memo end with a next step?
#    <details><summary>Answer</summary>The director still has a decision to make. A review that stops at "do not trust this" leaves her with nothing to do.</details>
# 3. The author objects: "the redesign is obviously better." What do you say?
#    <details><summary>Answer</summary>It may be. The test as run cannot show it, and it did show that the redesign fails on some devices. A second, complete test costs four weeks.</details>
#
# ## Carry forward
#
# Your capstone case is chosen. Open `capstone/README.md` for what the pack must contain and for the rubric.
