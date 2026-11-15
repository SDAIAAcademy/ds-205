# %% [markdown]
# # Lab 1.3 · Three tests, three units
#
# Day 1 · Session 3 (Choosing the unit of randomisation) · 25 min.
#
# Mashraq wants three tests: the renewal reminder, a redesigned online form (owner: Rehab Al-Tayyar, digital services) and a new way of serving visitors at the counters of 24 branches (owner: Mansour Al-Khelaiwi, branch services). For each you choose who or what the coin is tossed for. The logs suggest one answer, the rows; the data show why it is wrong each time.
#
# **AI policy.** AI-tutor, hints only, for the dataframe code. The choice of unit and its reason are yours.
#
# **Reference state.** `data/units_notices.csv`, `data/form_pages.csv`, `data/branches.csv`, `data/counter_visits.csv`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Reminder test: notices per holder and how alike they are (7')
# - [ ] 2 · Form test: page views per applicant (5')
# - [ ] 3 · Counter test: branches and shared staff (6')
# - [ ] 4 · Record the unit of each test with its reason (4')
# - [ ] 5 · Count the units each test really has (3')
# - [ ] ✱ Stretch · If the coin were tossed per notice, what share of holders with several permits would get both versions?

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

# %% [markdown]
# ## 1 · Reminder test: notices per holder and how alike they are (7')
#
# The messaging platform sends **notices**, one per permit. A holder with a parking permit and a market stall gets two. Here are 20,000 notices of last year with the key of the holder each belongs to.

# %%
notices = U.units_notices()
print(notices.head(5).to_string(index=False))
print(f"{len(notices):,} notices")

# %% [markdown]
# ✏️ **Exercise** · Write `notices_per_holder(df)` returning `(holders, share_of_holders_with_several, share_of_notices_from_them)`.

# %%
def notices_per_holder(df):
    # BEGIN SOLUTION
    per = df.groupby("holder_key").size()
    several = per[per > 1]
    return int(per.size), float(several.size / per.size), float(several.sum() / len(df))
    # END SOLUTION


# %%
try:
    holders, share_h, share_n = notices_per_holder(notices)
except NotImplementedError:
    holders, share_h, share_n = U.reference("d1_3", "per_holder")
U.keep("d1_3", "per_holder", [holders, share_h, share_n])
print(f"{holders:,} holders; {share_h:.1%} of them have several notices; those holders receive {share_n:.1%} of all notices")
U.check(holders < len(notices) and share_n > share_h, "holders with several permits are a minority of holders and a much larger share of notices")

# %% [markdown]
# Does it matter? Only if a holder's notices behave alike. Take the holders with exactly two notices. If the two renewals were unrelated, both would have the same outcome in a share of p² + (1 − p)² of pairs, where p is the on-time rate.
#
# ✏️ **Exercise** · Write `agreement(df)` returning `(observed, expected)` for holders with exactly two notices: the share of pairs with the same outcome, and the share expected if the two were unrelated.

# %%
def agreement(df):
    # BEGIN SOLUTION
    per = df.groupby("holder_key")["renewed_on_time"].agg(["size", "sum"])
    two = per[per["size"] == 2]
    observed = (two["sum"] != 1).mean()
    p = two["sum"].sum() / (2 * len(two))
    return float(observed), float(p ** 2 + (1 - p) ** 2)
    # END SOLUTION


# %%
try:
    obs, exp = agreement(notices)
except NotImplementedError:
    obs, exp = U.reference("d1_3", "agreement")
U.keep("d1_3", "agreement", [obs, exp])
print(f"pairs with the same outcome: {obs:.1%} observed, {exp:.1%} expected if the two notices were unrelated")
U.check(obs > exp + 0.10, "two notices of one holder agree far more often than two unrelated notices")

# %% [markdown]
# **Look at.** A holder renews everything on time or lets everything slip. Two notices of one holder are closer to one observation than to two. And a holder who gets the reminder for one permit has been reminded for the other as well: the control notice is no longer a control.

# %% [markdown]
# ## 2 · Form test: page views per applicant (5')
#
# The form's log has one row per **page view**. An applicant who corrects an error views the same page again.

# %%
pages = U.form_pages()
print(pages.head(5).to_string(index=False))
print(f"{len(pages):,} page views")

# %% [markdown]
# ✏️ **Exercise** · Write `views_per_applicant(df)` returning `(applicants, median_views, max_views, share_of_views_from_busiest_tenth)`.

# %%
def views_per_applicant(df):
    # BEGIN SOLUTION
    per = df.groupby("applicant_key").size().sort_values(ascending=False)
    top = per.head(int(np.ceil(per.size / 10)))
    return int(per.size), float(per.median()), int(per.max()), float(top.sum() / len(df))
    # END SOLUTION


# %%
try:
    applicants, med, mx, top_share = views_per_applicant(pages)
except NotImplementedError:
    applicants, med, mx, top_share = U.reference("d1_3", "views")
U.keep("d1_3", "views", [applicants, med, mx, top_share])
print(f"{applicants:,} applicants; median {med:.0f} page views, maximum {mx}; the busiest tenth of applicants produce {top_share:.1%} of all page views")
U.check(top_share > 0.25, "a tenth of the applicants produce more than a quarter of the rows")

# %%
err = pages.groupby("applicant_key")["validation_error"].agg(["mean", "size"])
many = err[err["size"] >= 10]
print(f"applicants with 10 or more page views: {len(many):,}")
print(f"  a quarter of them have an error on at most {many['mean'].quantile(0.25):.1%} of their page views")
print(f"  a quarter of them have an error on at least {many['mean'].quantile(0.75):.1%}")

# %% [markdown]
# **Look at.** Some applicants hardly ever trigger an error and some do it on every third page. A page view tells you mostly about its applicant. If page views were randomised, one applicant would see both forms; if page views are analysed, a few struggling applicants are counted dozens of times. Lab 3.3 measures what that does to a test.

# %% [markdown]
# ## 3 · Counter test: branches and shared staff (6')
#
# The counter-service change is a triage desk at the entrance that sorts visitors before they queue. It changes how the whole branch works, for staff and for every visitor in the hall.

# %%
br = U.branches()
visits = U.counter_visits()
print(br.to_string(index=False))

# %% [markdown]
# ✏️ **Exercise** · Write `staff_pools(br)` returning `(number_of_pools, shared)`, where `shared` is a list of the branch groups that share a pool, each as a sorted list of branch names.

# %%
def staff_pools(br):
    # BEGIN SOLUTION
    groups = br.groupby("staff_pool")["branch"].apply(lambda s: sorted(s))
    shared = sorted(g for g in groups if len(g) > 1)
    return int(groups.size), shared
    # END SOLUTION


# %%
try:
    pools, shared = staff_pools(br)
except NotImplementedError:
    pools, shared = U.reference("d1_3", "pools")
U.keep("d1_3", "pools", [pools, shared])
print(f"{len(br)} branches, {pools} staff pools; branches that share staff: {shared}")
U.check(pools == 21 and len(shared) == 3, "three pairs of branches share counter staff, so there are 21 separate pools")

# %%
rate = visits.groupby("branch")["served_within_15"].mean()
print(f"served within 15 minutes, by branch: from {rate.min():.1%} to {rate.max():.1%}; all visits {visits['served_within_15'].mean():.1%}")

# %% [markdown]
# **Look at.** Two questions decide the unit here.
#
# - Could one visitor get the triage desk and the next one not, in the same hall? No: they share the queue and the staff. One visitor's treatment changes the other's wait. That is **interference**, and it rules out the visitor as the unit.
# - Could B03 get the desk and B04 not? They share staff. A clerk trained on the new routine carries it to the other branch, and staff moved to cover the desk are missing next door. The pair is one unit.

# %% [markdown]
# ## 4 · Record the unit of each test with its reason (4')
#
# ✏️ **Exercise** · Return a dictionary with a `(unit, reason)` pair for each of `"reminder"`, `"form"` and `"counter"`. Units to choose from: `"notice"`, `"holder"`, `"page view"`, `"applicant"`, `"visitor"`, `"branch"`, `"staff pool"`. Each reason has at least 8 words.

# %%
def units():
    # BEGIN SOLUTION
    return {
        "reminder": ("holder", "A holder with several permits would otherwise get both versions, and their notices behave alike."),
        "form": ("applicant", "An applicant must see one form throughout, and page views of one applicant resemble each other."),
        "counter": ("staff pool", "Visitors in a hall share the queue, and branches that share staff carry the change to each other."),
    }
    # END SOLUTION


# %%
try:
    chosen = units()
except NotImplementedError:
    chosen = {k: tuple(v) for k, v in U.reference("d1_3", "units").items()}
U.keep("d1_3", "units", {k: list(v) for k, v in chosen.items()})
for test, (unit, reason) in chosen.items():
    print(f"{test:<9} {unit:<11} {reason}")
U.check(chosen["reminder"][0] == "holder", "reminder test: the holder, not the notice")
U.check(chosen["form"][0] == "applicant", "form test: the applicant, not the page view")
U.check(chosen["counter"][0] == "staff pool", "counter test: the staff pool, which is a branch or a pair of branches that share staff")
U.check(all(len(r.split()) >= 8 for _, r in chosen.values()), "every choice has a reason")

# %% [markdown]
# ## 5 · Count the units each test really has (3')
#
# ✏️ **Exercise** · Return a dictionary from test to `(rows_in_the_log, units)` for the three files of this lab.

# %%
def rows_and_units():
    # BEGIN SOLUTION
    return {
        "reminder": (len(notices), notices["holder_key"].nunique()),
        "form": (len(pages), pages["applicant_key"].nunique()),
        "counter": (len(visits), br["staff_pool"].nunique()),
    }
    # END SOLUTION


# %%
try:
    counts = rows_and_units()
except NotImplementedError:
    counts = {k: tuple(v) for k, v in U.reference("d1_3", "counts").items()}
U.keep("d1_3", "counts", {k: [int(x) for x in v] for k, v in counts.items()})
U.table(["test", "rows in the log", "units to randomise", "rows per unit"],
        [[t, f"{r:,}", f"{u:,}", f"{r / u:.1f}"] for t, (r, u) in counts.items()])
U.check(counts["counter"][1] == 21 and counts["form"][1] == applicants, "the counter test has 21 units, however many visits are logged")

# %% [markdown]
# **Look at.** The reminder test loses a quarter of its rows, the form test nine tenths, the counter test all but 21. The size of a test is its number of units. Day 2 puts a price on that.

# %% [markdown]
# ## ✱ Stretch · Both versions for one holder
#
# Suppose the coin were tossed per notice. For a holder with k notices, the chance that all k land in the same arm is 2 × 0.5^k. What share of the holders with several notices would get both versions?

# %%
def stretch():
    # BEGIN SOLUTION
    per = notices.groupby("holder_key").size()
    several = per[per > 1]
    both = float((1 - 2 * 0.5 ** several).mean())
    print(f"{both:.1%} of the holders with several notices would receive both versions")
    return both
    # END SOLUTION


try:
    U.keep("d1_3", "stretch", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked in the data: notices per holder and their agreement, page views per applicant, staff pools.",
       "Checked: the three units and the count of each.",
       "Not checked: whether visitors move between branches that do not share staff. Mansour's team would know; ask before the test, not after.")

# %% [markdown]
# ## Checkpoint
#
# 1. The platform can only toss a coin per notice. What do you do?
#    <details><summary>Answer</summary>Toss it from the holder key, for example from a seeded hash of the key, so that every notice of a holder lands in the same arm. Or enrol each holder once, at the first notice in the window.</details>
# 2. Why not randomise page views? There are ten times as many.
#    <details><summary>Answer</summary>One applicant would see two forms, and the extra rows are not extra information: page views of one applicant resemble each other.</details>
# 3. What does it cost to make the staff pool the unit of the counter test?
#    <details><summary>Answer</summary>The test has 21 units. Lab 2.3 measures how much power is left.</details>
#
# ## Carry forward
#
# The unit you chose for the reminder test goes into the pre-registration of lab 1.4. Lab 2.3 sizes the counter test and lab 3.3 analyses the form log at the wrong unit on purpose.
