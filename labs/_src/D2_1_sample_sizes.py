# %% [markdown]
# # Lab 2.1 · Sample sizes for three minimum effects
#
# Day 2 · Session 1 (Power and the minimum effect) · 25 min.
#
# The pre-registration of the reminder test says 9,200 holders per arm. You check that number. You take the baseline rate and the daily traffic from 182 days of history, write the sample-size formula yourself, apply it to minimum effects of 1, 2 and 4 points, compare with a library and turn each size into days of traffic.
#
# **AI policy.** AI-off for steps 1 to 3: this is the first pass of a sample-size step. From step 4 the tutor instruction may hint.
#
# **Reference state.** `data/history_daily.csv`. Nothing from Day 1 is needed: the minimum effect, 2 points, is `U.MIN_EFFECT`.
#
# **Tasks**
# - [ ] 1 · Baseline rate and daily traffic from the history (4')
# - [ ] 2 · The formula by hand for 2 points (7')
# - [ ] 3 · Three minimum effects: 1, 2 and 4 points (5')
# - [ ] 4 · Check against a library (4')
# - [ ] 5 · Turn sizes into days of traffic (5')
# - [ ] ✱ Stretch · Repeat for 90% power and say what the extra ten points cost
# - [ ] ✱ Stretch · A cheaper notice: size a test that shows it is not worse by more than 1 point

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

# %% [markdown]
# ## 1 · Baseline rate and daily traffic from the history (4')
#
# ✏️ **Exercise** · Write `baseline_and_traffic(hist)` returning `(baseline, mean_daily)`: the share of notices renewed on time over the whole history, and the mean number of notices sent per day.

# %%
hist = U.history()


def baseline_and_traffic(hist):
    # BEGIN SOLUTION
    baseline = hist["renewed_on_time"].sum() / hist["notices_sent"].sum()
    return float(baseline), float(hist["notices_sent"].mean())
    # END SOLUTION


# %%
try:
    P1, DAILY = baseline_and_traffic(hist)
except NotImplementedError:
    P1, DAILY = U.reference("d2_1", "baseline")
U.keep("d2_1", "baseline", [P1, DAILY])
print(f"baseline on-time renewal {P1:.2%}; {DAILY:,.0f} notices a day on average over {len(hist)} days")
U.check(0.60 < P1 < 0.63 and 2000 < DAILY < 2300, "the baseline is about 62% and the office sends about 2,150 notices a day")

# %% [markdown]
# ## 2 · The formula by hand for 2 points (7')
#
# To detect a difference δ between a baseline p₁ and p₂ = p₁ + δ, with a two-sided test at level α and power 1 − β, each arm needs
#
# n = (z₁₋α⁄₂ + z₁₋β)² × (p₁(1 − p₁) + p₂(1 − p₂)) / δ²
#
# With α = 0.05 the first z is 1.96; with power 0.80 the second is 0.84. Get them from `stats.norm.ppf`. Round **up**.
#
# ✏️ **Exercise** · Write `n_per_arm(p1, delta, alpha=0.05, power=0.80)` returning a whole number of holders per arm.

# %%
def n_per_arm(p1, delta, alpha=0.05, power=0.80):
    # BEGIN SOLUTION
    p2 = p1 + delta
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(power)
    return int(np.ceil((za + zb) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / delta ** 2))
    # END SOLUTION


# %%
try:
    n2 = n_per_arm(P1, U.MIN_EFFECT)
except NotImplementedError:
    n2 = U.reference("d2_1", "n2")
U.keep("d2_1", "n2", n2)
print(f"to detect {U.MIN_EFFECT * 100:.0f} points from a baseline of {P1:.2%}: {n2:,} holders per arm, {2 * n2:,} in all")
print("the pre-registration says 9,200 per arm")
U.check(n2 == U.n_per_arm(P1, U.MIN_EFFECT), "your formula agrees with the reference formula")
U.check(abs(n2 - 9200) < 100, "the provisional 9,200 was the same calculation, rounded")

# %% [markdown]
# **Look at.** Three things drive the number: the two error rates you accept, the spread of a yes-or-no outcome near 62%, and the square of the effect. Only the last one is under discussion with the director.

# %% [markdown]
# ## 3 · Three minimum effects: 1, 2 and 4 points (5')
#
# ✏️ **Exercise** · Return a dictionary from minimum effect (0.01, 0.02, 0.04) to holders per arm.

# %%
def three_sizes():
    # BEGIN SOLUTION
    return {d: n_per_arm(P1, d) for d in (0.01, 0.02, 0.04)}
    # END SOLUTION


# %%
try:
    sizes = three_sizes()
except NotImplementedError:
    sizes = {float(k): v for k, v in U.reference("d2_1", "sizes").items()}
U.keep("d2_1", "sizes", sizes)
U.table(["minimum effect", "per arm", "in all", "times the size for 2 points"],
        [[f"{d * 100:.0f} point{'s' if d > 0.01 else ''}", f"{n:,}", f"{2 * n:,}", f"{n / sizes[0.02]:.2f}"] for d, n in sizes.items()])
U.check(3.9 < sizes[0.01] / sizes[0.02] < 4.1 and 3.9 < sizes[0.02] / sizes[0.04] < 4.2, "halving the minimum effect multiplies the size by about four")

# %% [markdown]
# **Look at.** This table is the conversation to have with Sahar. "Could you act on 4 points only? Then four days are enough. Do you need to see 1 point? Then it is seven weeks." The minimum effect is her decision; the size follows from it.

# %% [markdown]
# ## 4 · Check against a library (4')
#
# statsmodels computes the same quantity from a standardised effect size. Its answer differs from yours by a few holders, because it transforms the two proportions before taking the difference.

# %%
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def n_library(p1, delta, alpha=0.05, power=0.80):
    h = proportion_effectsize(p1 + delta, p1)
    return int(np.ceil(NormalIndPower().solve_power(effect_size=h, alpha=alpha, power=power, ratio=1.0)))


lib = {d: n_library(P1, d) for d in sizes}
U.keep("d2_1", "library", lib)
U.table(["minimum effect", "your formula", "statsmodels", "difference"],
        [[f"{d * 100:.0f} point{'s' if d > 0.01 else ''}", f"{sizes[d]:,}", f"{lib[d]:,}", f"{(lib[d] - sizes[d]) / sizes[d]:+.2%}"] for d in sizes])
U.check(all(abs(lib[d] - sizes[d]) / sizes[d] < 0.01 for d in sizes), "the library and the formula agree within 1%")

# %% [markdown]
# **Look at.** Two honest methods, two slightly different numbers. A sample size is an estimate built on a guessed baseline; quoting it to the last holder is false precision. Session 2 checks it a third way, by simulation.

# %% [markdown]
# ## 5 · Turn sizes into days of traffic (5')
#
# Every holder due a notice enters the test, half in each arm.
#
# ✏️ **Exercise** · Write `days_needed(n_arm, daily)` returning the whole number of days of average traffic that fill both arms.

# %%
def days_needed(n_arm, daily):
    # BEGIN SOLUTION
    return int(np.ceil(2 * n_arm / daily))
    # END SOLUTION


# %%
try:
    days = {d: days_needed(n, DAILY) for d, n in sizes.items()}
except NotImplementedError:
    days = {float(k): v for k, v in U.reference("d2_1", "days").items()}
U.keep("d2_1", "days", days)
U.table(["minimum effect", "per arm", "days of average traffic"], [[f"{d * 100:.0f} point{'s' if d > 0.01 else ''}", f"{sizes[d]:,}", days[d]] for d in sizes])
U.check(days[0.02] == 9, "2 points need 9 days of average traffic")
print(f"the pre-registration says 28 days. In 28 average days the office sends {28 * DAILY:,.0f} notices, {28 * DAILY / 2:,.0f} per arm.")

# %% [markdown]
# **Look at.** Nine days are enough for the size, and the page says 28. An "average day" does not exist: Fridays are quiet and month-ends are busy. Lab 2.4 settles the duration.

# %% [markdown]
# ## ✱ Stretch · 90% power

# %%
def stretch():
    # BEGIN SOLUTION
    n90 = n_per_arm(P1, U.MIN_EFFECT, power=0.90)
    print(f"90% power: {n90:,} per arm, {n90 / n2 - 1:+.0%} against 80% power")
    # A third more holders buys ten points of power: halving the chance of missing a real 2-point effect, from 20% to 10%.
    return n90
    # END SOLUTION


try:
    U.keep("d2_1", "n90", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %% [markdown]
# ## ✱ Stretch · A cheaper notice, not worse by more than 1 point
#
# This is a non-inferiority test. The messaging platform offers a shorter renewal notice at a lower price per message. Sahar would adopt it if on-time renewal falls by **less than 1 point**; she signs that margin before the test starts. The test must now show "not worse": the lower end of the 95% interval of (new minus current) must lie above −1 point, a one-sided test at 2.5%.
#
# Per arm, with true rates p_cur and p_new = p_cur + d (d is the true difference you plan for):
#
# n = (z₁₋₀.₀₂₅ + z₁₋β)² × (p_cur(1 − p_cur) + p_new(1 − p_new)) / (margin + d)²
#
# ✏️ **Exercise** · Write `n_not_worse(p_cur, margin, d=0.0)` with 80% power. Compute it for a margin of 1 point when the two notices are truly equal (d = 0) and when the new one is truly 0.25 points worse. Then simulate tests at the first size with d = 0 and count how often the lower end clears −1 point.

# %%
def stretch_not_worse(reps):
    # BEGIN SOLUTION
    def n_not_worse(p_cur, margin, d=0.0):
        p_new = p_cur + d
        z = stats.norm.ppf(0.975) + stats.norm.ppf(0.80)
        return int(np.ceil(z ** 2 * (p_cur * (1 - p_cur) + p_new * (1 - p_new)) / (margin + d) ** 2))

    n_eq = n_not_worse(P1, 0.01)
    n_worse = n_not_worse(P1, 0.01, d=-0.0025)
    gen = U.rng(211)
    x_cur = gen.binomial(n_eq, P1, size=reps)
    x_new = gen.binomial(n_eq, P1, size=reps)
    diff, se, _ = U.z_test(x_cur, n_eq, x_new, n_eq)
    shown = float(((diff - 1.96 * se) > -0.01).mean())
    print(f"equal notices: {n_eq:,} per arm; new notice 0.25 points worse: {n_worse:,} per arm ({n_worse / n_eq:.2f} times)")
    print(f"simulated, {reps:,} tests at {n_eq:,} per arm: 'not worse' shown in {shown:.1%}")
    # The margin plays the part of the minimum effect: 1 point needs about as many holders as detecting a 1-point gain.
    # Planning for a slightly worse notice shrinks the denominator from 1 to 0.75 points squared: 1.78 times the holders.
    return {"n_equal": n_eq, "n_worse": n_worse, "shown": shown}
    # END SOLUTION


try:
    reps_ni = U.pick(1000, 200)
    ni = U.keep("d2_1", "not_worse", stretch_not_worse(reps_ni))
    U.check(abs(ni["shown"] - 0.80) < 3 * np.sqrt(0.16 / reps_ni), "the simulated share agrees with the planned 80% within its counting error")
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked: the formula result for 2 points, {n2:,} per arm, against the reference formula and against statsmodels (within 1%).",
       "Not checked yet: whether a test of this size really finds a 2-point effect 80 times in 100. Lab 2.2 simulates it.",
       "Assumed: the baseline of the test window equals the 182-day baseline, and every day is an average day.")

# %% [markdown]
# ## Checkpoint
#
# 1. The director asks for a minimum effect of 0.5 points. What happens to the size for 1 point?
#    <details><summary>Answer</summary>It is multiplied by four: about 148,000 per arm, close to five months of traffic.</details>
# 2. The baseline turns out to be 70%, not 62%. Does the test need more or fewer holders?
#    <details><summary>Answer</summary>Slightly fewer: p(1 − p) is largest at 50% and shrinks towards the ends.</details>
# 3. Why round up?
#    <details><summary>Answer</summary>Rounding down gives a little less than the power you promised. A holder cannot be half enrolled.</details>
#
# ## Carry forward
#
# The capstone asks for this calculation on your case, with the formula result and a simulated power curve. In the defence the assessor changes the minimum effect and you recompute.
