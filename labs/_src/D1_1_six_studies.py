# %% [markdown]
# # Lab 1.1 · Six studies, three designs
#
# Day 1 · Session 1 (Which claims need an experiment) · 25 min.
#
# Sahar Al-Wuhaibi, director of Mashraq Municipal Permits Office, has six studies on her desk. Each ends with the word "works". You classify each one by its design and by the claim it can support, mark your sheet against the key, and then build two comparisons yourself: one of volunteers, one decided by a coin, in a small world where you know the true effect.
#
# **AI policy.** AI-off for steps 1 to 3: the classification is the evidence of the first course outcome. AI-tutor, hints only, for the simulation of step 4.
#
# **Reference state.** `data/studies.json`. Nothing from another lab is needed.
#
# **Tasks**
# - [ ] 1 · Read the six studies and name each design (7')
# - [ ] 2 · Name the claim each one supports (6')
# - [ ] 3 · Mark the sheet against the key (3')
# - [ ] 4 · Simulate volunteers beside a coin (6')
# - [ ] 5 · Write the claim the app survey supports (3')
# - [ ] ✱ Stretch · Make the hidden trait stronger and watch which of the two gaps moves

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
np.set_printoptions(precision=3, suppress=True)
print("mode:", U.MODE)

# %% [markdown]
# ## 1 · Read the six studies and name each design (7')
#
# Three designs:
#
# - `"randomised"`: chance alone decided who got the change.
# - `"quasi"`: nobody randomised, but a rule or a date created a comparison group, and the claim rests on an assumption you can state.
# - `"observational"`: people or managers chose, or were chosen, and the groups are compared as found.

# %%
studies = U.js("studies.json")
for s in studies:
    print(f"{s['id']}  {s['text']}\n")

# %% [markdown]
# ✏️ **Exercise** · Return a dictionary from study id to design. Decide alone before you talk to your neighbour.

# %%
def designs():
    # BEGIN SOLUTION
    return {"S1": "randomised", "S2": "observational", "S3": "quasi", "S4": "quasi", "S5": "observational", "S6": "randomised"}
    # END SOLUTION


# %%
try:
    d = designs()
except NotImplementedError:
    d = U.reference("d1_1", "designs")
U.keep("d1_1", "designs", d)
U.check(set(d) == {s["id"] for s in studies} and set(d.values()) <= set(U.DESIGNS), "every study has one of the three designs")

# %% [markdown]
# ## 2 · Name the claim each one supports (6')
#
# Three claims:

# %%
for k, v in U.CLAIMS.items():
    print(f"{k:<12} {v}")

# %% [markdown]
# ✏️ **Exercise** · Return a dictionary from study id to claim. For every `"cause_if"`, say the assumption aloud to your neighbour: it is part of the answer.

# %%
def claims():
    # BEGIN SOLUTION
    return {"S1": "cause", "S2": "association", "S3": "cause_if", "S4": "cause_if", "S5": "association", "S6": "cause"}
    # END SOLUTION


# %%
try:
    c = claims()
except NotImplementedError:
    c = U.reference("d1_1", "claims")
U.keep("d1_1", "claims", c)
U.check(set(c.values()) <= set(U.CLAIMS), "every study has one of the three claims")

# %% [markdown]
# ## 3 · Mark the sheet against the key (3')
#
# A study counts when both the design and the claim are right. The course outcome asks for at least five of six.

# %%
score = U.mark_studies({i: (d[i], c[i]) for i in d})
U.check(score >= 5, "at least five of the six studies are classified with the claim each supports")

# %% [markdown]
# **Look at.** S6 was run for fairness, not for research, and it is still an experiment: a lottery is a coin. S3 and S4 were never meant as studies at all. What makes a design is how the groups came to differ, not who planned it.

# %% [markdown]
# ## 4 · Simulate volunteers beside a coin (6')
#
# A small world you control. 20,000 permit holders. Some are **organised**: they are more likely to install the office's app and, quite apart from the app, more likely to renew on time. The app itself adds exactly **3 points** to the chance of renewing on time. That is the truth you are trying to recover.

# %%
TRUE_EFFECT = 0.03


def world(gen, n=20_000, trait_strength=0.30):
    """Holders with a hidden trait. Returns organised (0/1) and each holder's chance of renewing without the app."""
    organised = gen.binomial(1, 0.4, n)
    base = 0.50 + trait_strength * organised
    return organised, base


def renew(gen, base, has_app):
    return gen.binomial(1, np.clip(base + TRUE_EFFECT * has_app, 0, 1))


# %% [markdown]
# ✏️ **Exercise** · Write the two comparisons. Each returns the gap in on-time renewal, app minus no app.
#
# - `volunteer_gap`: holders choose. An organised holder installs the app with probability 0.7, another holder with probability 0.2.
# - `coin_gap`: a coin decides. Every holder gets the app with probability 0.5.

# %%
def volunteer_gap(gen, trait_strength=0.30):
    organised, base = world(gen, trait_strength=trait_strength)
    # BEGIN SOLUTION
    has_app = gen.binomial(1, np.where(organised == 1, 0.7, 0.2))
    y = renew(gen, base, has_app)
    return float(y[has_app == 1].mean() - y[has_app == 0].mean())
    # END SOLUTION


def coin_gap(gen, trait_strength=0.30):
    organised, base = world(gen, trait_strength=trait_strength)
    # BEGIN SOLUTION
    has_app = gen.binomial(1, 0.5, len(base))
    y = renew(gen, base, has_app)
    return float(y[has_app == 1].mean() - y[has_app == 0].mean())
    # END SOLUTION


# %%
try:
    gaps = (volunteer_gap(U.rng(11)), coin_gap(U.rng(12)))
except NotImplementedError:
    gaps = U.reference("d1_1", "gaps")
U.keep("d1_1", "gaps", list(gaps))
print(f"true effect of the app:            {TRUE_EFFECT * 100:+.1f} points")
print(f"gap when holders choose:           {gaps[0] * 100:+.1f} points")
print(f"gap when a coin decides:           {gaps[1] * 100:+.1f} points")
U.check(gaps[0] > 0.10, "the volunteer comparison shows a gap several times the true effect")
U.check(abs(gaps[1] - TRUE_EFFECT) < 0.02, "the coin comparison lands near the true 3 points")

# %% [markdown]
# **Look at.** Nothing in the volunteer data is wrong. Every number is measured correctly. The comparison answers a different question: "how do app users differ from the others?", which is mostly "how do organised holders differ?".

# %%
REPS = U.pick(200, 40)
gen = U.rng(13)
vol = np.array([volunteer_gap(gen) for _ in range(REPS)])
coin = np.array([coin_gap(gen) for _ in range(REPS)])
print(f"{REPS} repetitions. Volunteers: mean gap {vol.mean():+.1%}, from {vol.min():+.1%} to {vol.max():+.1%}")
print(f"{REPS} repetitions. Coin:       mean gap {coin.mean():+.1%}, from {coin.min():+.1%} to {coin.max():+.1%}")
U.keep("d1_1", "rep_means", [float(vol.mean()), float(coin.mean())])
U.check(abs(coin.mean() - TRUE_EFFECT) < 0.005, "over many repetitions the coin comparison is centred on the truth: it is unbiased")

# %% [markdown]
# **Look at.** More data do not rescue the volunteer comparison: its repetitions agree with each other, and all of them are wrong by the same amount. That is bias. The coin comparison wobbles around the truth. That is sampling error, and Day 2 sizes it.

# %% [markdown]
# ## 5 · Write the claim the app survey supports (3')
#
# Study S5 is the survey: 81% of app users renewed on time against 58% of the others.
#
# ✏️ **Exercise** · Return one sentence, of at least 15 words, that Sahar could read aloud without claiming more than the survey shows. It must not contain "because", "causes" or "leads to".

# %%
def survey_sentence():
    # BEGIN SOLUTION
    return ("Holders who use the app renewed on time more often than those who do not, 81% against 58%, "
            "but holders chose whether to use it, so the survey cannot say how much of the gap is the app.")
    # END SOLUTION


# %%
try:
    sentence = survey_sentence()
except NotImplementedError:
    sentence = U.reference("d1_1", "sentence")
U.keep("d1_1", "sentence", sentence)
print(sentence)
low = sentence.lower()
U.check(len(sentence.split()) >= 15 and "81" in sentence and "58" in sentence, "the sentence quotes both numbers")
U.check(not any(w in low for w in ("because", "causes", "leads to")), "the sentence makes no causal claim")

# %% [markdown]
# ## ✱ Stretch · A stronger hidden trait
#
# Raise `trait_strength` from 0.30 to 0.40 and run both comparisons again. Which gap moves, and why does the other stay?

# %%
def stretch():
    # BEGIN SOLUTION
    gen = U.rng(14)
    v = np.mean([volunteer_gap(gen, 0.40) for _ in range(U.pick(100, 20))])
    c_ = np.mean([coin_gap(gen, 0.40) for _ in range(U.pick(100, 20))])
    print(f"trait strength 0.40: volunteers {v:+.1%}, coin {c_:+.1%}")
    # The coin spreads organised holders evenly over both groups, whatever the trait is worth.
    return float(v), float(c_)
    # END SOLUTION


try:
    U.keep("d1_1", "stretch", list(stretch()))
except NotImplementedError:
    print("✱ stretch not done")

# %%
U.note("Checked against the key: the six classifications, design and claim.",
       f"Checked against a known truth: the coin comparison recovers the 3 points over {REPS} repetitions; the volunteer comparison does not.",
       "Not checked: the assumptions of S3 and S4. A quasi-experiment is only as good as the argument for its assumption.")

# %% [markdown]
# ## Checkpoint
#
# 1. The office compares renewal before and after a new website went live. Which design is that?
#    <details><summary>Answer</summary>Observational, or a weak quasi-experiment at best: there is no group that did not get the change, so anything else that changed that month is mixed in.</details>
# 2. Why is a lottery for scarce inspection slots an experiment?
#    <details><summary>Answer</summary>Chance alone decided who got a slot, so winners and losers differ only by the slot and by sampling error.</details>
# 3. In step 4 the volunteer gap was about the same in every repetition. Does that make it trustworthy?
#    <details><summary>Answer</summary>No. Agreement between repetitions shows low sampling error, not absence of bias. All repetitions share the same hidden trait.</details>
#
# ## Carry forward
#
# The words "cause", "cause if" and "association" return in lab 3.4 and in the capstone memo, where you state which decision a write-up's evidence supports.
