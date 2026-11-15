# %% [markdown]
# # Lab 2.2 · Power by simulation
#
# Day 2 · Session 2 (Power by simulation) · 25 min.
#
# A formula says that 9,187 holders per arm give 80% power to detect 2 points. You test the claim the way DS-201 tested coverage: build a world in which the reminder truly adds 2 points, run the planned test in it 1,000 times and count how often the analysis says "significant". Then you draw the power curve and count false positives in a world with no effect.
#
# **AI policy.** AI-tutor: hints one step at a time, never the simulation.
#
# **Reference state.** No file. The baseline, 61.58%, and the planned size, 9,187 per arm, are given below, so nothing from lab 2.1 is needed.
#
# **Tasks**
# - [ ] 1 · Simulate one test and analyse it (5')
# - [ ] 2 · 1,000 tests at the planned size (6')
# - [ ] 3 · The counting error of the simulation (3')
# - [ ] 4 · A power curve over sample sizes (7')
# - [ ] 5 · No effect: the false-positive rate (4')
# - [ ] ✱ Stretch · Keep the planned size and let the true baseline be 50% or 70%: what happens to power?

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

P1 = 0.6158                                   # baseline on-time renewal over 182 days (lab 2.1)
DELTA = U.MIN_EFFECT                          # 2 points
N = U.n_per_arm(P1, DELTA)                    # 9,187 per arm
REPS = U.pick(1000, 300)
print(f"baseline {P1:.2%}, minimum effect {DELTA * 100:.0f} points, planned size {N:,} per arm, {REPS} simulated tests")

# %% [markdown]
# ## 1 · Simulate one test and analyse it (5')
#
# One simulated test: draw the number of on-time renewals in each arm, then run the analysis the pre-registration names. `U.z_test(x1, n1, x2, n2)` returns the difference, its standard error and the two-sided p-value.
#
# ✏️ **Exercise** · Write `one_test(gen, n, p1, delta)` returning `(difference, p_value)` for one simulated test with `n` holders per arm.

# %%
def one_test(gen, n, p1, delta):
    # BEGIN SOLUTION
    x_control = gen.binomial(n, p1)
    x_reminder = gen.binomial(n, p1 + delta)
    diff, _, p = U.z_test(x_control, n, x_reminder, n)
    return diff, p
    # END SOLUTION


# %%
gen = U.rng(25)
try:
    first = [one_test(gen, N, P1, DELTA) for _ in range(5)]
except NotImplementedError:
    first = [tuple(x) for x in U.reference("d2_2", "first")]
U.keep("d2_2", "first", [list(x) for x in first])
for i, (d, p) in enumerate(first, 1):
    print(f"test {i}: estimated effect {d * 100:+.2f} points, p = {p:.4f} {'significant' if p < U.ALPHA else 'not significant'}")
U.check(all(-0.01 < d < 0.05 for d, _ in first), "five tests in the same world give five different estimates around 2 points")

# %% [markdown]
# **Look at.** The truth is 2 points in every one of these five tests. The estimates differ, and a test can miss. Power is the share that do not.

# %% [markdown]
# ## 2 · 1,000 tests at the planned size (6')
#
# `gen.binomial(n, p, size=reps)` draws all the tests at once, and `U.z_test` accepts arrays.
#
# ✏️ **Exercise** · Write `power_sim(gen, n, p1, delta, reps)` returning the share of `reps` simulated tests with a p-value below 0.05.

# %%
def power_sim(gen, n, p1, delta, reps):
    # BEGIN SOLUTION
    x_control = gen.binomial(n, p1, size=reps)
    x_reminder = gen.binomial(n, p1 + delta, size=reps)
    _, _, p = U.z_test(x_control, n, x_reminder, n)
    return float((p < U.ALPHA).mean())
    # END SOLUTION


# %%
try:
    power = power_sim(U.rng(22), N, P1, DELTA, REPS)
except NotImplementedError:
    power = U.reference("d2_2", "power")
U.keep("d2_2", "power", power)
print(f"simulated power at {N:,} per arm: {power:.1%} of {REPS} tests were significant (the formula promised 80%)")
U.check(0.74 < power < 0.86, "the simulated power is close to the 80% the formula promised")

# %% [markdown]
# ## 3 · The counting error of the simulation (3')
#
# A share counted over 1,000 simulated tests is itself an estimate. Its standard error is √(p(1 − p)/reps).
#
# ✏️ **Exercise** · Write `counting_error(share, reps)` returning two standard errors of a simulated share.

# %%
def counting_error(share, reps):
    # BEGIN SOLUTION
    return float(2 * np.sqrt(share * (1 - share) / reps))
    # END SOLUTION


# %%
try:
    err = counting_error(power, REPS)
except NotImplementedError:
    err = U.reference("d2_2", "err")
U.keep("d2_2", "err", err)
print(f"simulated power {power:.1%}, give or take {err * 100:.1f} points: consistent with 80%? {'yes' if abs(power - 0.80) <= err else 'no'}")
U.check(abs(err - 2 * np.sqrt(power * (1 - power) / REPS)) < 1e-9, "two standard errors of a counted share")

# %% [markdown]
# **Look at.** The simulation and the formula agree within the simulation's own error. That is what "checked by simulation" means. To tighten the check, run more simulated tests: 10,000 give ±0.8 points.

# %% [markdown]
# ## 4 · A power curve over sample sizes (7')
#
# The formula can be turned around: for a given size it returns the power.

# %%
def power_formula(n, p1, delta, alpha=0.05):
    p2 = p1 + delta
    se = np.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n)
    return float(stats.norm.cdf(delta / se - stats.norm.ppf(1 - alpha / 2)))


SIZES = [2000, 4000, 6000, N, 12000, 16000, 30000]

# %% [markdown]
# ✏️ **Exercise** · Write `power_curve(sizes)` returning a list of `(n, simulated_power, formula_power)` for each size in `sizes`, with `REPS` simulated tests each. Use one generator, `U.rng(23)`, for the whole curve.

# %%
def power_curve(sizes):
    # BEGIN SOLUTION
    gen = U.rng(23)
    return [(n, power_sim(gen, n, P1, DELTA, REPS), power_formula(n, P1, DELTA)) for n in sizes]
    # END SOLUTION


# %%
try:
    curve = power_curve(SIZES)
except NotImplementedError:
    curve = [tuple(x) for x in U.reference("d2_2", "curve")]
U.keep("d2_2", "curve", [list(x) for x in curve])
U.table(["per arm", "simulated power", "formula"], [[f"{n:,}", f"{s:.1%}", f"{f:.1%}"] for n, s, f in curve])
U.check(all(abs(s - f) < 0.05 for _, s, f in curve), "simulation and formula agree at every size, within the counting error")
U.check(curve[0][1] < 0.40 and curve[-1][1] > 0.99, "2,000 per arm would miss a real 2-point effect most of the time; 30,000 per arm almost never")

plt = U.plt()
plt.plot([n for n, _, _ in curve], [f for _, _, f in curve], label="formula")
plt.scatter([n for n, _, _ in curve], [s for _, s, _ in curve], color="tab:red", label=f"simulation, {REPS} tests each")
plt.axhline(0.80, linestyle="--", color="grey")
plt.axvline(N, linestyle=":", color="grey")
plt.xlabel("holders per arm"); plt.ylabel("power to detect 2 points"); plt.legend()
plt.title("Power curve of the reminder test")
plt.show()

# %% [markdown]
# **Look at.** The curve is steep on the left and flat on the right. The first 9,000 holders per arm buy 80% power; the next 21,000 buy the remaining 20 points. A 28-day test has about 30,000 per arm, so its real question is not "is there a 2-point effect?" but "how large is the effect?". Day 3 answers with an interval.

# %%
def detectable(n, p1, alpha=0.05, power=0.80):
    """The effect a test of n per arm detects with the given power (a simple search)."""
    lo, hi = 0.0001, 0.2
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if power_formula(n, p1, mid, alpha) < power else (lo, mid)
    return hi


d30 = detectable(30_000, P1)
U.keep("d2_2", "detectable_30000", d30)
print(f"with 30,000 per arm the test detects {d30 * 100:.2f} points with 80% power")

# %% [markdown]
# ## 5 · No effect: the false-positive rate (4')
#
# Now a world in which the reminder does nothing. Every "significant" result is a false win.
#
# ✏️ **Exercise** · Return the share of `REPS` simulated tests that are significant when the true effect is zero, at the planned size. Use `U.rng(27)`.

# %%
def false_positive_rate():
    # BEGIN SOLUTION
    return power_sim(U.rng(27), N, P1, 0.0, REPS)
    # END SOLUTION


# %%
try:
    fpr = false_positive_rate()
except NotImplementedError:
    fpr = U.reference("d2_2", "fpr")
U.keep("d2_2", "fpr", fpr)
fpr_error = 2 * np.sqrt(0.05 * 0.95 / REPS)        # two standard errors of a share near 5% counted over REPS tests
print(f"no true effect: {fpr:.1%} of {REPS} tests were significant (the level promised 5%, give or take {fpr_error * 100:.1f} points)")
U.check(fpr < 0.05 + 1.5 * fpr_error, "with one planned analysis the false-positive rate is the 5% you agreed to")

# %% [markdown]
# **Look at.** One test in twenty wins when nothing is there. That is the price written into α, and it holds only for one planned analysis of one metric at one moment. Lab 3.3 breaks each of those three conditions and counts the damage.

# %% [markdown]
# ## ✱ Stretch · A wrong baseline
#
# The size was computed for a baseline of 61.58%. What is the power of the same test if the true baseline in the test window is 50%, or 70%?

# %%
def stretch():
    # BEGIN SOLUTION
    out = {}
    for b in (0.50, 0.70):
        out[b] = power_sim(U.rng(28), N, b, DELTA, REPS)
        print(f"true baseline {b:.0%}: simulated power {out[b]:.1%}, formula {power_formula(N, b, DELTA):.1%}")
    # p(1 - p) is largest at 50%: a baseline nearer 50% means more noise and less power for the same size.
    return out
    # END SOLUTION


try:
    U.keep("d2_2", "stretch", stretch())
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note(f"Checked by simulation: power at the planned size, {power:.1%} over {REPS} tests, against the formula's 80%.",
       f"Checked: the false-positive rate with one planned analysis, {fpr:.1%}.",
       f"The counts have an error of about ±{err * 100:.1f} points.",
       "Assumed: holders are independent and the effect is the same for all of them. Labs 2.3 and 2.4 drop both assumptions.")

# %% [markdown]
# ## Checkpoint
#
# 1. A simulation of 200 tests gives a power of 76%. Is the formula's 80% refuted?
#    <details><summary>Answer</summary>No. Two standard errors of 0.76 over 200 tests are about 6 points. Run more tests before concluding anything.</details>
# 2. Why simulate at all when a formula exists?
#    <details><summary>Answer</summary>The formula covers one design: independent units, one look, two proportions. A simulation checks the analysis you will really run, and it still works when the design leaves the formula behind, as in lab 2.3.</details>
# 3. What does a power of 80% say about one test that came out not significant?
#    <details><summary>Answer</summary>Little by itself. Read the interval: it says which effects the data are still consistent with.</details>
#
# ## Carry forward
#
# The capstone asks for a simulated power curve of your design. `power_sim` and `power_curve` are that curve; change the world they simulate to match your case.
