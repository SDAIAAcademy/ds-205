<!-- academy:title -->
# Designing and Reading Experiments

تصميم التجارب وقراءة نتائجها

Data Science Track · SDAIA Academy · DS-205 · Level 200

Design a randomised experiment a public office can act on, size it, check it and read its result without fooling yourself

Participants design randomised experiments for a fictional municipal permits office and read the results without fooling themselves. They turn a decision question into a pre-registration with a hypothesis, primary and guardrail metrics, a stop rule and a unit of randomisation, compute sample size by formula and by simulation, analyse a synthetic experiment log, check that randomisation worked, and measure how peeking, many metrics and a mismatched unit inflate false wins. Variance reduction and sequential tests are left to DS-302.

**Format:** Intensive: 3 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

**Course page:** https://sdaiaacademy.github.io/ds-205/
<!-- /academy:title -->

## Outcomes

| | Outcomes | Level | Evidence |
|---|---|---|---|
| LO1 | Distinguish a randomised experiment, a quasi-experiment and an observational comparison, and explain the causal claim each supports, given six study descriptions from public services | Awareness | a classification with the supported claim, at least five of six correct |
| LO2 | Draft a pre-registration stating the decision, hypothesis, unit of randomisation, primary and guardrail metrics, stop rule and analysis plan, given the office's question about renewal reminders | Applied | a one-page pre-registration that passes a reviewer's checklist |
| LO3 | Compute the sample size and run time needed to detect a minimum effect of interest and check it by simulation, given baseline renewal rates, daily traffic and the office's minimum effect | Applied | a notebook with the formula result, a simulated power curve and the chosen duration |
| LO4 | Analyse a completed two-arm experiment with a difference in proportions, a confidence interval and a sample ratio mismatch test, given a synthetic log of 60,000 renewal notices | Applied | a result note with estimate, interval, checks and a recommendation |
| LO5 | Measure by simulation the false-positive rate caused by peeking, many metrics and analysis at the wrong unit, given simulated A/A tests with no true effect | Applied | a table of false-win rates for each trap, with and without the correct procedure |
| LO6 | Review a reported experiment and decide whether it supports the decision it claims to support, given write-ups with seeded flaws, one in class and one in the capstone | Performance | a review memo per write-up naming each flaw, its consequence and the decision the evidence does support, defended live |

<!-- academy:units -->
## Units

| Unit | Title | Sessions | Slides |
|---|---|---|---|
| Day 1 | Design | Which claims need an experiment; Decision, hypothesis and metrics; Choosing the unit of randomisation; Pre-registration | [`slides/day1.html`](slides/day1.html) |
| Day 2 | Size and run | Power and the minimum effect; Power by simulation; Cluster randomisation; Run time and seasonality | [`slides/day2.html`](slides/day2.html) |
| Day 3 | Read the result | Did randomisation work; Estimate, interval and effect; False wins by simulation; Reviewing a reported result | [`slides/day3.html`](slides/day3.html) |
| Capstone | Capstone: the design and analysis pack and its defence |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**Mashraq Municipal Permits Office (مكتب المشرق للتصاريح البلدية)** is a fictional city office that issues resident parking, market stall, outdoor seating and building works permits. Its director wants three changes tested before they are adopted, and each one teaches a different part of the course:

| Test | Unit | What it teaches | Data |
|---|---|---|---|
| A reminder message seven days before a permit expires | Permit holder | Pre-registration, sample size, run time, the ratio check, the result note | 26 weeks of notice traffic; a test on 60,000 notices over 28 days; the messaging platform's export, which has a planted fault |
| A redesigned online application form | Applicant | The unit of analysis, false wins, the review memo | A log with one row per page view, and a write-up with seeded flaws |
| A triage desk at the counters of 24 branches | Staff pool | Interference, cluster randomisation, the power lost | Four baseline weeks of counter visits; three pairs of branches share staff |

All data are synthetic and generated with a fixed seed by `labs/prepare_data.py`. No real office, permit holder, applicant or branch is described. Participants work as Juri Al-Asmari, a junior analyst; holders, applicants and visitors appear only as pseudonymised keys, and every result is reported in aggregate.

## How the course is organised

- **Pre-work**, about two hours: `labs/P0_prework_proportions_simulation.ipynb` rehearses proportions, intervals and a simulation loop before the supervised entry quiz.
- **Three teaching days** of four sessions. Each session has about 25 minutes of teaching, one checkpoint and a 25-minute lab that starts from supplied files and has a complete solution.
- **A capstone day**: each participant defends one design choice of a design and analysis pack.
- **A follow-up task**, tracked by the trainer: the design checklist applied to one real or planned experiment at work (`labs/followup/README.md`).

Every design in the course states who is in each arm, why withholding the change from the other arm is acceptable, how log data are minimised and which guardrail stops the test if a group is harmed.

**Assistant policy.** Supervised checks and the first pass of each sample-size and analysis step are done without an assistant. For simulation code a tutor instruction that only hints may be used (`labs/tutor_instruction.md`). The capstone is open to an assistant and is defended live without one.

**Assessment.** A supervised entry quiz and exit check done without an assistant (20%), the capstone pack marked on the rubric below (60%) and the live defence of one design choice (20%). Passing takes 70% overall and at least 60% on both the capstone rubric and the supervised check. The certificate is a certificate of completion with assessed work.

The next course is DS-302 Online Experiments and A/B Testing, which adds variance reduction, sequential tests and designs for marketplaces.

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Six studies, three designs | [`D1_1_six_studies.ipynb`](labs/D1_1_six_studies.ipynb) |
| 1.2 | Day 1 · Session 2 | The first half of the pre-registration | [`D1_2_decision_metrics.ipynb`](labs/D1_2_decision_metrics.ipynb) |
| 1.3 | Day 1 · Session 3 | Three tests, three units | [`D1_3_three_units.ipynb`](labs/D1_3_three_units.ipynb) |
| 1.4 | Day 1 · Session 4 | Complete and review a pre-registration | [`D1_4_pre_registration.ipynb`](labs/D1_4_pre_registration.ipynb) |
| 2.1 | Day 2 · Session 1 | Sample sizes for three minimum effects | [`D2_1_sample_sizes.ipynb`](labs/D2_1_sample_sizes.ipynb) |
| 2.2 | Day 2 · Session 2 | Power by simulation | [`D2_2_power_simulation.ipynb`](labs/D2_2_power_simulation.ipynb) |
| 2.3 | Day 2 · Session 3 | 24 branches, 12 and 12 | [`D2_3_branch_clusters.ipynb`](labs/D2_3_branch_clusters.ipynb) |
| 2.4 | Day 2 · Session 4 | Choose the run time | [`D2_4_run_time.ipynb`](labs/D2_4_run_time.ipynb) |
| 3.1 | Day 3 · Session 1 | Ratio and balance on the export | [`D3_1_ratio_balance.ipynb`](labs/D3_1_ratio_balance.ipynb) |
| 3.2 | Day 3 · Session 2 | Analyse the reminder test | [`D3_2_reminder_result.ipynb`](labs/D3_2_reminder_result.ipynb) |
| 3.3 | Day 3 · Session 3 | A thousand A/A tests | [`D3_3_false_wins.ipynb`](labs/D3_3_false_wins.ipynb) |
| 3.4 | Day 3 · Session 4 | Review a write-up | [`D3_4_review_memo.ipynb`](labs/D3_4_review_memo.ipynb) |
<!-- /academy:labs -->

## Capstone

A design and analysis pack for one of three synthetic cases not used in class (a reminder message, a form redesign, a training programme), in a public repository, and an eight-minute defence followed by four minutes of questions. The cases, their data and their flawed write-ups are in `labs/capstone/`.

**Submission:** a link to a public GitHub repository with a one-page pre-registration, a sample-size notebook with the formula result and a simulated power curve, an analysis notebook that reruns from the raw files with a fixed seed, a result note with estimate, interval, checks and a recommendation, and a review memo on the case's flawed write-up, with the commit history and the seeded simulation log. In the questions the assessor changes the minimum effect or the unit, and the participant recomputes the sample size.

| Criterion | Weight |
|---|---|
| Design and pre-registration | 25 |
| Power and sample size | 25 |
| Analysis and checks | 20 |
| Review memo | 20 |
| Writing and reproducibility | 10 |

## Prerequisites

- DS-201 Statistical Inference by Simulation
- Computes a proportion, a difference in means and a confidence interval
- Writes a simulation loop in Python or R

<!-- academy:tools -->
## Tools

Each line is a capability; the examples are interchangeable.

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Statistics and power calculation:** SciPy and statsmodels, R with the pwr package
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas
<!-- /academy:tools -->

<!-- academy:sources -->
## Sources

### National references

- [Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf)
- [Implementing Regulation of the Personal Data Protection Law (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf)
- [General Rules for Secondary Use of Data (SDAIA)](https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf)
- [Principles of AI Ethics (SDAIA)](https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf)

### Libraries used in the labs

- [NumPy: random generators and seeds](https://numpy.org/doc/stable/reference/random/generator.html)
- [SciPy: scipy.stats.chisquare (the sample ratio check)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html)
- [SciPy: scipy.stats.ttest_ind](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
- [statsmodels: proportions_ztest](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html)
- [statsmodels: confint_proportions_2indep](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.confint_proportions_2indep.html)
- [statsmodels: NormalIndPower](https://www.statsmodels.org/stable/generated/statsmodels.stats.power.NormalIndPower.html)
- [statsmodels: proportion_effectsize](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_effectsize.html)
- [statsmodels: multipletests (Holm)](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)
- [uv: Python projects and environments](https://docs.astral.sh/uv/)

### Reading on experiments

- [Haynes, Service, Goldacre and Torgerson (2012): Test, Learn, Adapt: Developing Public Policy with Randomised Controlled Trials](https://www.gov.uk/government/publications/test-learn-adapt-developing-public-policy-with-randomised-controlled-trials)
- [Kohavi, Tang and Xu: Trustworthy Online Controlled Experiments (the book's site)](https://experimentguide.com/)
- [Fabijan and others (2019): Diagnosing Sample Ratio Mismatch in Online Controlled Experiments](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)
- [Johari, Pekelis and Walsh: Always Valid Inference: Bringing Sequential Analysis to A/B Testing](https://arxiv.org/abs/1512.04922)
- [Zhou, Lu and Shallah (2023): All about sample-size calculations for A/B testing](https://arxiv.org/abs/2305.16459)
- [Center for Open Science: Preregistration](https://www.cos.io/initiatives/prereg)
<!-- /academy:sources -->

### National references

- Personal Data Protection Law: https://sdaia.gov.sa/en/SDAIA/about/Documents/PersonalDataProtectionLaw.pdf
- Implementing Regulation of the Personal Data Protection Law: https://sdaia.gov.sa/en/SDAIA/about/Documents/ImplementingRegulationPersonalDataProtectionLaw.pdf
- General Rules for Secondary Use of Data: https://sdaia.gov.sa/Documents/GeneralRulesForSecondaryUseOfData_EN.pdf
- Principles of AI Ethics: https://sdaia.gov.sa/en/SDAIA/about/Documents/ai-principles.pdf

The course cites these texts and does not restate them. Read them before you design an experiment on a real service.
