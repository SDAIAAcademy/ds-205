# %% [markdown]
# # Pre-work · Proportions, intervals and a simulation loop
#
# Before Day 1 · about two hours, with the reading.
#
# The course assumes three things from DS-201: you can compute a proportion and the difference of two, you can put an interval around each, and you can write a simulation loop with a seed. This notebook rehearses all three on 182 days of renewal notices from Mashraq Municipal Permits Office, the fictional office of the course. The supervised entry quiz covers the same ground and is done without an assistant.
#
# **AI policy.** AI-tutor, hints only: paste `tutor_instruction.md` into an assistant your Academy has approved. Better still, do it alone and see where you stand.
#
# **Reference state.** `data/history_daily.csv`.
#
# **Tasks**
# - [ ] 1 · A proportion and its standard error
# - [ ] 2 · A 95% interval for a proportion
# - [ ] 3 · A difference of two proportions with its interval
# - [ ] 4 · A simulation loop: how far does a sample of 500 land from the truth?
# - [ ] 5 · Coverage: does the interval keep its promise?

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
print(hist.head(7).to_string(index=False))

# %% [markdown]
# ## 1 · A proportion and its standard error
#
# Take the first Sunday of the history: 2,272 notices, 1,449 renewed on time. The proportion is x/n and its standard error is √(p(1 − p)/n).
#
# ✏️ **Exercise** · Write `proportion(x, n)` returning `(p, standard_error)`.

# %%
def proportion(x, n):
    # BEGIN SOLUTION
    p = x / n
    return float(p), float(np.sqrt(p * (1 - p) / n))
    # END SOLUTION


# %%
X, N = int(hist.loc[0, "renewed_on_time"]), int(hist.loc[0, "notices_sent"])
try:
    p, se = proportion(X, N)
except NotImplementedError:
    p, se = U.reference("p0", "proportion")
U.keep("p0", "proportion", [p, se])
print(f"{X:,} of {N:,}: {p:.1%}, standard error {se * 100:.2f} points")
U.check(abs(p - X / N) < 1e-12 and abs(se - np.sqrt(p * (1 - p) / N)) < 1e-12, "proportion and standard error")

# %% [markdown]
# ## 2 · A 95% interval for a proportion
#
# ✏️ **Exercise** · Write `interval(x, n)` returning `(low, high)`: the proportion ± 1.96 standard errors.

# %%
def interval(x, n):
    # BEGIN SOLUTION
    p, se = proportion(x, n)
    return p - 1.96 * se, p + 1.96 * se
    # END SOLUTION


# %%
try:
    lo, hi = interval(X, N)
except NotImplementedError:
    lo, hi = U.reference("p0", "interval")
U.keep("p0", "interval", [lo, hi])
print(f"95% interval: {lo:.1%} to {hi:.1%}")
U.check(lo < p < hi and abs((hi - lo) / 2 - 1.96 * se) < 1e-9, "the interval is the proportion give or take 1.96 standard errors")

# %% [markdown]
# **Look at.** About two points either side, from more than two thousand notices. Keep that width in mind: the course is about detecting differences of two points.

# %% [markdown]
# ## 3 · A difference of two proportions with its interval
#
# Do holders renew on time less often when the notice goes out at the month-end? Compare all month-end days (the 26th and later) with all other days. The standard error of a difference is √(SE₁² + SE₂²).
#
# ✏️ **Exercise** · Write `difference(x1, n1, x2, n2)` returning `(difference, low, high)` for group 2 minus group 1.

# %%
def difference(x1, n1, x2, n2):
    # BEGIN SOLUTION
    p1, se1 = proportion(x1, n1)
    p2, se2 = proportion(x2, n2)
    d, se_d = p2 - p1, np.sqrt(se1 ** 2 + se2 ** 2)
    return float(d), float(d - 1.96 * se_d), float(d + 1.96 * se_d)
    # END SOLUTION


# %%
g = hist.groupby("month_end")[["renewed_on_time", "notices_sent"]].sum()
try:
    d, dlo, dhi = difference(g.loc[0, "renewed_on_time"], g.loc[0, "notices_sent"], g.loc[1, "renewed_on_time"], g.loc[1, "notices_sent"])
except NotImplementedError:
    d, dlo, dhi = U.reference("p0", "difference")
U.keep("p0", "difference", [d, dlo, dhi])
print(f"month-end minus other days: {d * 100:+.2f} points ({dlo * 100:+.2f} to {dhi * 100:+.2f})")
U.check(dhi < 0, "holders notified at the month-end renew on time less often; the whole interval is below zero")

# %% [markdown]
# **Look at.** Is that a causal claim? Does a month-end notice *make* holders late? Nobody assigned holders to dates. Day 1 starts from this question.

# %% [markdown]
# ## 4 · A simulation loop
#
# Suppose the true on-time rate is 62%. Draw 2,000 samples of 500 holders each and record the proportion in each.
#
# ✏️ **Exercise** · Write `simulate(gen, n, p, reps)` returning an array of `reps` sample proportions. A loop is fine; `gen.binomial(n, p, size=reps)` does it in one line.

# %%
def simulate(gen, n, p, reps):
    # BEGIN SOLUTION
    return gen.binomial(n, p, size=reps) / n
    # END SOLUTION


# %%
REPS = U.pick(2000, 500)
try:
    props = simulate(U.rng(1), 500, 0.62, REPS)
    sim = [float(props.mean()), float(props.std()), float((np.abs(props - 0.62) > 0.04).mean())]
except NotImplementedError:
    sim = U.reference("p0", "sim")
U.keep("p0", "sim", sim)
print(f"{REPS} samples of 500: mean {sim[0]:.1%}, standard deviation {sim[1] * 100:.2f} points (formula: {np.sqrt(0.62 * 0.38 / 500) * 100:.2f})")
print(f"share of samples that miss the truth by more than 4 points: {sim[2]:.1%}")
U.check(abs(sim[1] - np.sqrt(0.62 * 0.38 / 500)) < 0.003, "the spread of the simulated proportions matches the standard-error formula")

# %% [markdown]
# ## 5 · Coverage
#
# ✏️ **Exercise** · Write `coverage(gen, n, p, reps)`: draw `reps` samples of `n`, build the 95% interval of step 2 in each, and return the share of intervals that contain `p`.

# %%
def coverage(gen, n, p, reps):
    # BEGIN SOLUTION
    x = gen.binomial(n, p, size=reps)
    ph = x / n
    se_ = np.sqrt(ph * (1 - ph) / n)
    return float(((ph - 1.96 * se_ <= p) & (p <= ph + 1.96 * se_)).mean())
    # END SOLUTION


# %%
try:
    cov = coverage(U.rng(2), 500, 0.62, REPS)
except NotImplementedError:
    cov = U.reference("p0", "coverage")
U.keep("p0", "coverage", cov)
print(f"the 95% interval contained the truth in {cov:.1%} of {REPS} samples")
U.check(0.92 < cov < 0.98, "the interval keeps its promise, within the counting error of the simulation")

# %%
U.note("Checked against formulas: the proportion, its standard error and the interval.",
       f"Checked by simulation: the spread of a sample proportion and the coverage of its interval, over {REPS} samples.",
       "If any step took you more than twenty minutes, revise DS-201 days 1 and 2 before the entry quiz.")

# %% [markdown]
# ## Ready?
#
# 1. Four times the sample: what happens to the standard error?
#    <details><summary>Answer</summary>It halves. The standard error falls with the square root of the sample size.</details>
# 2. An interval for a difference runs from −0.5 to +3.1 points. Is there a difference?
#    <details><summary>Answer</summary>The data are consistent with none, and with one of three points. The interval is the answer; "not significant" hides most of it.</details>
# 3. Why set a seed?
#    <details><summary>Answer</summary>So that you, your neighbour and your reviewer get the same numbers from the same code.</details>
