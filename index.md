---
course: "Designing and Reading Experiments"
code: "DS-205"
version: "2027.1.0"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-205/index.html"
---

# Designing and Reading Experiments

تصميم التجارب وقراءة نتائجها

Data Science Track · 3 teaching days + capstone day · 21 hours · Level 200

Design a randomised experiment a public office can act on, size it, check it and read its result without fooling yourself

Participants design randomised experiments for a fictional municipal permits office and read the results without fooling themselves. They turn a decision question into a pre-registration with a hypothesis, primary and guardrail metrics, a stop rule and a unit of randomisation, compute sample size by formula and by simulation, analyse a synthetic experiment log, check that randomisation worked, and measure how peeking, many metrics and a mismatched unit inflate false wins. Variance reduction and sequential tests are left to DS-302.

**Who it is for:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.

**Format:** Intensive: 3 teaching days of four sessions and a capstone day, with guided pre-work and a tracked follow-up task

## The case study

**Mashraq Municipal Permits Office.** Mashraq Municipal Permits Office (مكتب المشرق للتصاريح البلدية) is a fictional city office that issues resident parking, market stall, outdoor seating and building works permits. Its director, Sahar Al-Wuhaibi, wants three changes tested before they are adopted: a reminder message for renewals, a redesigned online form and a new way of serving visitors at the counters of 24 branches. All data are synthetic and generated with a fixed seed: 26 weeks of notice traffic with a weekly cycle and a month-end peak, a reminder test on 60,000 notices over 28 days whose platform export has a planted fault, a form test logged page view by page view, and four baseline weeks of counter visits in branches of which three pairs share staff. Participants work as Juri Al-Asmari, a junior analyst; holders, applicants and visitors appear only as pseudonymised keys and every result is reported in aggregate.

## The course

### Day 1: Design

Slides: https://sdaiaacademy.github.io/ds-205/slides/day1.md

- **Session 1: Which claims need an experiment**
  - Explain what random assignment removes from a comparison
  - Classify a study as a randomised experiment, a quasi-experiment or an observational comparison
  - State the causal claim a study supports and the assumption it rests on
  - [Lab 1.1: Six studies, three designs (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D1_1_six_studies.ipynb)
- **Session 2: Decision, hypothesis and metrics**
  - Write the decision an experiment informs, with the action for each result
  - Choose one primary metric and set a minimum effect of interest from costs
  - Write guardrails with thresholds and a stop rule that protects holders
  - [Lab 1.2: The first half of the pre-registration (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D1_2_decision_metrics.ipynb)
- **Session 3: Choosing the unit of randomisation**
  - Choose a unit of randomisation that keeps each person in one arm
  - Distinguish simple, stratified and cluster assignment
  - Recognise interference between units and choose a unit that contains it
  - [Lab 1.3: Three tests, three units (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D1_3_three_units.ipynb)
- **Session 4: Pre-registration**
  - Complete a one-page pre-registration with an analysis plan and planned checks
  - State who is in each arm, why withholding is acceptable and how log data are minimised
  - Review a pre-registration against a checklist and say what fails and why
  - [Lab 1.4: Complete and review a pre-registration (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D1_4_pre_registration.ipynb)

### Day 2: Size and run

Slides: https://sdaiaacademy.github.io/ds-205/slides/day2.md

- **Session 1: Power and the minimum effect**
  - Explain power and the two errors a test can make
  - Compute the sample size per arm for a minimum effect by formula
  - Show how the minimum effect drives the size and the days of traffic needed
  - [Lab 2.1: Sample sizes for three minimum effects (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D2_1_sample_sizes.ipynb)
- **Session 2: Power by simulation**
  - Simulate a planned two-arm test and its analysis with a seed
  - Estimate power by simulation and state its counting error
  - Draw a power curve and read the sample size from it
  - [Lab 2.2: Power by simulation (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D2_2_power_simulation.ipynb)
- **Session 3: Cluster randomisation**
  - Estimate the intraclass correlation and the design effect from baseline data
  - Measure by simulation the power lost when branches are randomised in place of visitors
  - Analyse a cluster-randomised test at the cluster level and improve it by pairing
  - [Lab 2.3: 24 branches, 12 and 12 (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D2_3_branch_clusters.ipynb)
- **Session 4: Run time and seasonality**
  - Describe the weekly cycle and the month-end peak in traffic and in the baseline rate
  - Turn a sample size into a duration of whole weeks that covers the month-end
  - Explain what a test estimates when it covers only part of a cycle
  - [Lab 2.4: Choose the run time (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D2_4_run_time.ipynb)

### Day 3: Read the result

Slides: https://sdaiaacademy.github.io/ds-205/slides/day3.md

- **Session 1: Did randomisation work**
  - Test whether the arm counts match the planned split
  - Read a balance table and locate the segment in which an assignment or logging fault sits
  - Decide which rows to analyse after a failed check and say why
  - [Lab 3.1: Ratio and balance on the export (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D3_1_ratio_balance.ipynb)
- **Session 2: Estimate, interval and effect**
  - Compute a difference in proportions with its standard error and 95% interval
  - Read an interval against the minimum effect and separate statistical from practical significance
  - Report guardrails and a subgroup without overstating either
  - [Lab 3.2: Analyse the reminder test (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D3_2_reminder_result.ipynb)
- **Session 3: False wins by simulation**
  - Simulate A/A tests and count false wins
  - Measure the false-win rate of peeking, of twenty metrics and of analysis at the wrong unit
  - Apply the correct procedure to each trap and show that the rate returns to 5%
  - [Lab 3.3: A thousand A/A tests (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D3_3_false_wins.ipynb)
- **Session 4: Reviewing a reported result**
  - Review a write-up in a fixed order: design, checks, analysis, claim
  - Name each flaw with its consequence for the reported result
  - State the decision the evidence does support and defend it
  - [Lab 3.4: Review a write-up (25 min)](https://sdaiaacademy.github.io/ds-205/labs/D3_4_review_memo.ipynb)

### Capstone: Capstone: the design and analysis pack and its defence

Slides: https://sdaiaacademy.github.io/ds-205/slides/capstone.md

## Capstone

A design and analysis pack for one of three synthetic cases (reminder message, form redesign, training programme): pre-registration, sample-size and analysis notebooks, result note and a review memo on a flawed write-up, in a public repository; eight-minute defence

**What you submit:** A link to a public GitHub repository with a one-page pre-registration, a sample-size notebook with the formula result and a simulated power curve, an analysis notebook that reruns from the raw files with a fixed seed, a result note with estimate, interval, checks and a recommendation, and a review memo on the case's flawed write-up, with the commit history and the seeded simulation log. Then an eight-minute live defence of one design choice and four minutes of questions, in which the assessor changes the minimum effect or the unit and the participant recomputes the sample size.

**Rubric:**

- Design and pre-registration: 25%
- Power and sample size: 25%
- Analysis and checks: 20%
- Review memo: 20%
- Writing and reproducibility: 10%

## Outcomes

- **LO1** Distinguish a randomised experiment, a quasi-experiment and an observational comparison, and explain the causal claim each supports, given six study descriptions from public services (Awareness) Evidence: a classification with the supported claim, at least five of six correct
- **LO2** Draft a pre-registration stating the decision, hypothesis, unit of randomisation, primary and guardrail metrics, stop rule and analysis plan, given the office's question about renewal reminders (Applied) Evidence: a one-page pre-registration that passes a reviewer's checklist
- **LO3** Compute the sample size and run time needed to detect a minimum effect of interest and check it by simulation, given baseline renewal rates, daily traffic and the office's minimum effect (Applied) Evidence: a notebook with the formula result, a simulated power curve and the chosen duration
- **LO4** Analyse a completed two-arm experiment with a difference in proportions, a confidence interval and a sample ratio mismatch test, given a synthetic log of 60,000 renewal notices (Applied) Evidence: a result note with estimate, interval, checks and a recommendation
- **LO5** Measure by simulation the false-positive rate caused by peeking, many metrics and analysis at the wrong unit, given simulated A/A tests with no true effect (Applied) Evidence: a table of false-win rates for each trap, with and without the correct procedure
- **LO6** Review a reported experiment and decide whether it supports the decision it claims to support, given write-ups with seeded flaws, one in class and one in the capstone (Performance) Evidence: a review memo per write-up naming each flaw, its consequence and the decision the evidence does support, defended live

## Tools

- **Analysis environment and notebooks:** Python with uv and JupyterLab or marimo, R with Quarto
- **Statistics and power calculation:** SciPy and statsmodels, R with the pwr package
- **Dataframes and analytical SQL engine:** DuckDB, Polars, pandas

## Prerequisites

- DS-201 Statistical Inference by Simulation
- Computes a proportion, a difference in means and a confidence interval
- Writes a simulation loop in Python or R
- Pre-work: about two hours on proportions, intervals and simulation, in the pre-work notebook of the labs folder (its name starts with P0), before the supervised entry quiz
- Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.

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

---

SDAIA Academy · Data Science Track · Designing and Reading Experiments

Course version 2027.1.0 · engine 1.0.0 · built 2026-11-15 · commit f9d5985
