# %% [markdown]
# # Lab 2.3 · 24 branches, 12 and 12
#
# Day 2 · Session 3 (Cluster randomisation) · 25 min.
#
# Mansour Al-Khelaiwi wants to test a triage desk at the counters. The outcome is the share of visitors served within 15 minutes, and he would adopt the desk for a gain of 5 points. Visitors in a hall share one queue, so whole branches must be randomised. Four baseline weeks hold 10,888 visits, which sounds like plenty. You simulate the test both ways, with visitors randomised and with 24 branches randomised, and measure the power lost.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** `data/counter_visits.csv` and `data/branches.csv`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Intraclass correlation and design effect from baseline visits (5')
# - [ ] 2 · Visitors randomised: power (5')
# - [ ] 3 · Branches randomised, analysed by branch: power (7')
# - [ ] 4 · The visitor-level analysis under no effect (4')
# - [ ] 5 · Pair branches by baseline and measure power again (4')
# - [ ] ✱ Stretch · Treat each pair of branches that share staff as one unit and measure the power of 21 units

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

visits = U.counter_visits()
br = U.branches()
per = visits.groupby("branch")["served_within_15"].agg(["mean", "size"])
RATE = per["mean"].to_numpy()        # each branch's baseline rate, used as its true rate in the simulated world
SIZE = per["size"].to_numpy()        # visits per branch in four weeks
B = len(per)
EFFECT = 0.05                        # Mansour's minimum effect: 5 points
REPS = U.pick(1000, 200)
print(f"{B} branches, {SIZE.sum():,} visits in four weeks, from {SIZE.min()} to {SIZE.max()} per branch; overall rate {visits['served_within_15'].mean():.1%}")


def branch_rates(gen):
    """Each branch's rate in one four-week period: its own level plus a little period-to-period movement."""
    return np.clip(RATE + gen.normal(0, 0.02, B), 0.02, 0.98)


# %% [markdown]
# ## 1 · Intraclass correlation and design effect from baseline visits (5')
#
# Visitors of one branch resemble each other: same staff, same hall, same neighbourhood. The **intraclass correlation** (ICC) is the share of the outcome's variance that lies between branches:
#
# ICC = between-branch variance of the true rates / (p(1 − p))
#
# The variance of the observed branch rates overstates the first term a little, because each observed rate also carries sampling noise p_b(1 − p_b)/n_b; subtract its mean. The **design effect**, 1 + (m − 1) × ICC with m the mean branch size, says how many times larger the variance of a branch-randomised estimate is.
#
# ✏️ **Exercise** · Write `icc_and_design_effect(per)` returning `(icc, mean_size, design_effect)` from the table `per` (columns `mean`, `size`).

# %%
def icc_and_design_effect(per):
    # BEGIN SOLUTION
    p_b, n_b = per["mean"].to_numpy(), per["size"].to_numpy()
    p = (p_b * n_b).sum() / n_b.sum()
    between = p_b.var(ddof=1) - (p_b * (1 - p_b) / n_b).mean()
    icc = between / (p * (1 - p))
    m = n_b.mean()
    return float(icc), float(m), float(1 + (m - 1) * icc)
    # END SOLUTION


# %%
try:
    icc, m, deff = icc_and_design_effect(per)
except NotImplementedError:
    icc, m, deff = U.reference("d2_3", "icc")
U.keep("d2_3", "icc", [icc, m, deff])
print(f"ICC {icc:.3f}; mean branch size {m:.0f} visits; design effect {deff:.1f}")
print(f"{SIZE.sum():,} visits in branches are worth about {SIZE.sum() / deff:,.0f} independent visits")
U.check(0.01 < icc < 0.06 and deff > 8, "a small ICC and large branches give a large design effect")

# %% [markdown]
# **Look at.** An ICC of three per cent looks negligible. Multiplied by a branch of several hundred visitors it is not.

# %% [markdown]
# ## 2 · Visitors randomised: power (5')
#
# First the test that cannot be run: a coin per visitor, as if visitors did not share a queue. In every branch half of the visitors get the desk.
#
# ✏️ **Exercise** · Write `visitor_test(gen, effect)` returning the p-value of one simulated test. In each branch, `SIZE // 2` visitors are treated; draw served-within-15 counts for both groups with `gen.binomial` from `branch_rates(gen)`, add `effect` for the treated, pool all branches and use `U.z_test`.

# %%
def visitor_test(gen, effect):
    # BEGIN SOLUTION
    p = branch_rates(gen)
    n_t = SIZE // 2
    n_c = SIZE - n_t
    x_c = gen.binomial(n_c, p)
    x_t = gen.binomial(n_t, np.clip(p + effect, 0, 1))
    return U.z_test(x_c.sum(), n_c.sum(), x_t.sum(), n_t.sum())[2]
    # END SOLUTION


def share_significant(test, effect, seed):
    gen = U.rng(seed)
    return float(np.mean([test(gen, effect) < U.ALPHA for _ in range(REPS)]))


# %%
try:
    power_visitor = share_significant(visitor_test, EFFECT, 31)
except NotImplementedError:
    power_visitor = U.reference("d2_3", "power_visitor")
U.keep("d2_3", "power_visitor", power_visitor)
print(f"visitors randomised: power to detect {EFFECT * 100:.0f} points {power_visitor:.1%}")
U.check(power_visitor > 0.95, "with 10,888 independent visitors a 5-point effect is found almost every time")

# %% [markdown]
# ## 3 · Branches randomised, analysed by branch: power (7')
#
# Now the test that can be run: 12 branches drawn at random get the desk, 12 do not. The analysis counts what was randomised: one rate per branch, and a t-test on 12 rates against 12.
#
# ✏️ **Exercise** · Write `branch_test(gen, effect)` returning the p-value of one simulated test. Choose 12 of the 24 branches with `gen.permutation`, draw each branch's count with its own rate (plus `effect` if treated), compute the 24 branch rates and compare the two groups with `stats.ttest_ind(..., equal_var=False)`.

# %%
def branch_test(gen, effect):
    # BEGIN SOLUTION
    treated = np.zeros(B, bool)
    treated[gen.permutation(B)[:B // 2]] = True
    p = np.clip(branch_rates(gen) + effect * treated, 0, 1)
    rate = gen.binomial(SIZE, p) / SIZE
    return float(stats.ttest_ind(rate[treated], rate[~treated], equal_var=False).pvalue)
    # END SOLUTION


# %%
try:
    power_branch = share_significant(branch_test, EFFECT, 32)
    fpr_branch = share_significant(branch_test, 0.0, 33)
except NotImplementedError:
    power_branch, fpr_branch = U.reference("d2_3", "branch")
U.keep("d2_3", "branch", [power_branch, fpr_branch])
print(f"branches randomised, analysed by branch: power {power_branch:.1%}; false-positive rate with no effect {fpr_branch:.1%}")
print(f"power lost by randomising branches: {(power_visitor - power_branch) * 100:.0f} points")
U.check(power_branch < 0.50, "with 24 branches a real 5-point effect is missed more often than it is found")
U.check(fpr_branch < 0.11, "the branch-level analysis keeps the false-positive rate near 5%")

# %% [markdown]
# **Look at.** Same visits, same effect, same four weeks. The power fell from near certainty to well under a half, because the test has 24 units, and branches differ from each other by far more than 5 points.

# %% [markdown]
# ## 4 · The visitor-level analysis under no effect (4')
#
# The tempting repair: branches were randomised, but analyse the 10,888 visits as if each had its own coin. Run that analysis in a world where the desk does nothing.
#
# ✏️ **Exercise** · Write `naive_test(gen, effect)`: branches randomised as in step 3, but the p-value comes from `U.z_test` on the pooled visits of the two groups.

# %%
def naive_test(gen, effect):
    # BEGIN SOLUTION
    treated = np.zeros(B, bool)
    treated[gen.permutation(B)[:B // 2]] = True
    p = np.clip(branch_rates(gen) + effect * treated, 0, 1)
    x = gen.binomial(SIZE, p)
    return U.z_test(x[~treated].sum(), SIZE[~treated].sum(), x[treated].sum(), SIZE[treated].sum())[2]
    # END SOLUTION


# %%
try:
    fpr_naive = share_significant(naive_test, 0.0, 34)
except NotImplementedError:
    fpr_naive = U.reference("d2_3", "fpr_naive")
U.keep("d2_3", "fpr_naive", fpr_naive)
print(f"branches randomised, visits analysed: with no true effect, {fpr_naive:.1%} of tests are 'significant'")
U.check(fpr_naive > 0.30, "the visitor-level analysis of a branch-randomised test declares a win far more often than 5%")

# %% [markdown]
# **Look at.** The visitor-level analysis is not a more powerful version of the branch-level one. It finds "effects" whether or not there are any: it reads the luck of which branches landed in which arm as if it were the desk.

# %% [markdown]
# ## 5 · Pair branches by baseline and measure power again (4')
#
# Most of the noise is the difference between branches, and the baseline already tells you which branches are alike. **Pairing**, the smallest form of stratified assignment: observe a baseline period, sort the branches by baseline rate, pair neighbours, and toss a coin inside each pair. The analysis is a paired t-test on the 12 within-pair differences.

# %%
def paired_test(gen, effect):
    """One simulated paired test: a simulated baseline period decides the pairs, a second period is the test."""
    baseline = gen.binomial(SIZE, branch_rates(gen)) / SIZE
    order = np.argsort(baseline)
    first, second = order[0::2], order[1::2]
    flip = gen.random(B // 2) < 0.5
    treated_idx = np.where(flip, first, second)
    control_idx = np.where(flip, second, first)
    p = branch_rates(gen)
    rate_t = gen.binomial(SIZE[treated_idx], np.clip(p[treated_idx] + effect, 0, 1)) / SIZE[treated_idx]
    rate_c = gen.binomial(SIZE[control_idx], p[control_idx]) / SIZE[control_idx]
    return float(stats.ttest_rel(rate_t, rate_c).pvalue)


# %% [markdown]
# ✏️ **Exercise** · Return `(power, false_positive_rate)` of the paired design, using `share_significant` with seeds 35 and 36.

# %%
def paired_results():
    # BEGIN SOLUTION
    return share_significant(paired_test, EFFECT, 35), share_significant(paired_test, 0.0, 36)
    # END SOLUTION


# %%
try:
    power_paired, fpr_paired = paired_results()
except NotImplementedError:
    power_paired, fpr_paired = U.reference("d2_3", "paired")
U.keep("d2_3", "paired", [power_paired, fpr_paired])
U.table(["design", "analysis", "power for 5 points", "false wins, no effect"],
        [["visitors randomised (not possible here)", "visits", f"{power_visitor:.1%}", "about 5%"],
         ["12 and 12 branches", "branch rates, t-test", f"{power_branch:.1%}", f"{fpr_branch:.1%}"],
         ["12 and 12 branches", "visits, z-test", "meaningless", f"{fpr_naive:.1%}"],
         ["12 pairs of like branches", "pair differences, paired t-test", f"{power_paired:.1%}", f"{fpr_paired:.1%}"]])
U.check(power_paired > power_branch + 0.25, "pairing by baseline recovers much of the power that branch randomisation lost")
U.check(fpr_paired < 0.11, "the paired analysis keeps the false-positive rate near 5%")

# %% [markdown]
# **Look at.** Pairing cost nothing but four weeks of baseline data the office already had. It works because a branch's level is stable from one period to the next. The remaining options when power is still short: more branches, a longer test, or a larger minimum effect. A cleverer analysis of the same 24 coin tosses is not on the list.

# %% [markdown]
# ## ✱ Stretch · 21 staff pools
#
# B03 and B04, B11 and B12, B19 and B20 share staff, so each pair is one unit. Merge them and measure the power of a test that randomises 21 units, 10 against 11.

# %%
def stretch():
    # BEGIN SOLUTION
    pool = br.set_index("branch").loc[per.index, "staff_pool"].to_numpy()
    pools = np.unique(pool)
    gen, hits = U.rng(37), 0
    for _ in range(REPS):
        treated_pools = set(gen.permutation(pools)[:len(pools) // 2])
        treated = np.array([p_ in treated_pools for p_ in pool])
        p = np.clip(branch_rates(gen) + EFFECT * treated, 0, 1)
        x = gen.binomial(SIZE, p)
        t = pd.DataFrame({"pool": pool, "x": x, "n": SIZE, "t": treated}).groupby("pool").agg(x=("x", "sum"), n=("n", "sum"), t=("t", "first"))
        r = (t["x"] / t["n"]).to_numpy()
        hits += stats.ttest_ind(r[t["t"].to_numpy()], r[~t["t"].to_numpy()], equal_var=False).pvalue < U.ALPHA
    print(f"21 staff pools, 10 against 11: power {hits / REPS:.1%} (24 branches gave {power_branch:.1%})")
    return hits / REPS
    # END SOLUTION


try:
    U.keep("d2_3", "pools21", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked by simulation over {REPS} tests each: the power of three designs for a 5-point effect and the false-positive rate of three analyses.",
       "Assumed: each branch's baseline rate is its true rate, and a branch moves by about 2 points from one period to the next. With real data, estimate that movement from several periods.",
       "Not modelled: staff shared between branches. The stretch treats shared pools as single units.")

# %% [markdown]
# ## Checkpoint
#
# 1. A colleague says: "The ICC is only 0.03, so clustering can be ignored." What do you answer?
#    <details><summary>Answer</summary>The design effect multiplies the ICC by the cluster size. With several hundred visits per branch, 0.03 turns the variance into more than ten times the naive one.</details>
# 2. Which helps a branch-randomised test more: twice the visits per branch, or twice the branches?
#    <details><summary>Answer</summary>Twice the branches. More visits per branch shrink only the small sampling part of each branch's rate; the difference between branches stays.</details>
# 3. Why does pairing help?
#    <details><summary>Answer</summary>The comparison is made inside pairs of branches that started at the same level, so the stable differences between branches cancel out of it.</details>
#
# ## Carry forward
#
# The capstone's training-programme case is a cluster design. Its sample-size notebook is this lab with your case's centres.
