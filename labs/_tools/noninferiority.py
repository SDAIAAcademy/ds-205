"""Figures of the not-worse (non-inferiority) slides of Day 2, session 1, and of the practice question.

    uv run python _tools/noninferiority.py      (from labs/)

The slides use a parallel case, outdoor seating permits, with numbers of their own; lab 2.1's
stretch works on the reminder test. Decision rule: the new version is shown not worse when the
lower end of the 95% interval of (new minus old), unpooled standard error, lies above minus the
margin. That is a one-sided test at 2.5%.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mashraq as U  # noqa: E402

ALPHA_ONE_SIDED = 0.025
POWER = 0.80


def n_not_worse(p_old: float, margin: float, true_diff: float = 0.0,
                alpha: float = ALPHA_ONE_SIDED, power: float = POWER) -> int:
    """Units per arm to show new >= old - margin, when the true difference is true_diff."""
    p_new = p_old + true_diff
    za, zb = stats.norm.ppf(1 - alpha), stats.norm.ppf(power)
    spread = p_old * (1 - p_old) + p_new * (1 - p_new)
    return int(np.ceil((za + zb) ** 2 * spread / (margin + true_diff) ** 2))


def interval(x_old, n_old, x_new, n_new):
    """Difference new minus old, its 95% interval (unpooled) and the p-value for no difference."""
    diff, se, p = U.z_test(x_old, n_old, x_new, n_new)
    return diff, diff - 1.96 * se, diff + 1.96 * se, p


def share_not_worse(gen, n, p_old, true_diff, margin, reps):
    x_o = gen.binomial(n, p_old, size=reps)
    x_n = gen.binomial(n, p_old + true_diff, size=reps)
    diff, se, _ = U.z_test(x_o, n, x_n, n)
    return float(((diff - 1.96 * se) > -margin).mean())


def verdict(lo, hi, margin):
    if lo > 0:
        return "not worse, and better"
    if lo > -margin:
        return "not worse"
    if hi < -margin:
        return "worse by more than the margin"
    return "not shown"


def main():
    # ---- slides: outdoor seating permits, dropping the second posted letter
    p_old, margin = 0.74, 0.02
    n0 = n_not_worse(p_old, margin)
    n_half = n_not_worse(p_old, margin, true_diff=-0.005)
    n_sup = U.n_per_arm(p_old, margin)  # two-sided, to detect a 2-point gain
    print(f"[slides] outdoor seating: baseline {p_old:.0%}, margin {margin * 100:.0f} points")
    print(f"  per arm, assuming no true difference: {n0:,}")
    print(f"  per arm, if the new version is truly 0.5 points worse: {n_half:,} ({n_half / n0:.2f} times)")
    print(f"  for comparison, two-sided test to detect a 2-point gain: {n_sup:,}")
    reps = 4000
    pw = share_not_worse(U.rng(901), n0, p_old, 0.0, margin, reps)
    fa = share_not_worse(U.rng(902), n0, p_old, -margin, margin, reps)
    print(f"  simulated, {reps:,} tests at {n0:,} per arm: shown not worse when truly equal {pw:.1%} "
          f"(±{2 * np.sqrt(pw * (1 - pw) / reps):.1%}); when truly 2 points worse {fa:.1%} "
          f"(±{2 * np.sqrt(fa * (1 - fa) / reps):.1%})")

    # four finished tests at n0 per arm, renewals on time out of n0 in each arm
    n = n0
    x_old = round(p_old * n)
    four = {"A": x_old - 23, "B": x_old - 91, "C": x_old - 272, "D": x_old + 121}
    print(f"  four results, {n:,} per arm, old arm {x_old:,} on time ({x_old / n:.2%}):")
    for k, x_new in four.items():
        d, lo, hi, p = interval(x_old, n, x_new, n)
        print(f"   {k}: new {x_new:,} ({x_new / n:.2%})  diff {d * 100:+.1f}  95% [{lo * 100:+.1f}, {hi * 100:+.1f}]"
              f"  p(no difference) {p:.2g}  -> {verdict(lo, hi, margin)}")

    # ---- practice question: building works permits, an e-mail notice in place of a posted one
    nq, pq, mq = 5000, 0.68, 0.015
    xq_old = round(pq * nq)
    xq_new = xq_old - 20
    d, lo, hi, p = interval(xq_old, nq, xq_new, nq)
    print(f"[question] building works: {nq:,} per arm, old {xq_old:,}, new {xq_new:,}: diff {d * 100:+.1f}"
          f"  95% [{lo * 100:+.1f}, {hi * 100:+.1f}]  p(no difference) {p:.2f}  margin {mq * 100:.1f}"
          f"  -> {verdict(lo, hi, mq)}")


if __name__ == "__main__":
    main()
