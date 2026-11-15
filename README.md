<!-- academy:title -->
# Designing and Reading Experiments

تصميم التجارب وقراءة نتائجها

Data Science Track · SDAIA Academy · DS-205 · Level 200

REPLACE: one line under the title: what participants can do after the course

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
| Capstone | Capstone project presentations |  | [`slides/capstone.html`](slides/capstone.html) |
<!-- /academy:units -->

## Case study

**REPLACE: the name of the fictional organisation every lab works on.** REPLACE: two sentences on the case study and its synthetic data

<!-- academy:labs -->
## Labs

Every lab is a notebook in `labs/`. Open it in Google Colab from the course page, or run it locally with `uv`. Exercises raise `NotImplementedError` until they are done; the reference versions are in `labs/solutions/`.

| | Session | Lab | File |
|---|---|---|---|
| 1.1 | Day 1 · Session 1 | Classify six studies by design and the causal claim each supports | [`D1_1_classify_six_studies.ipynb`](labs/D1_1_classify_six_studies.ipynb) |
| 1.2 | Day 1 · Session 2 | Write decision, hypothesis, metrics, guardrails and a stop rule | [`D1_2_write_decision_hypothesis.ipynb`](labs/D1_2_write_decision_hypothesis.ipynb) |
| 1.3 | Day 1 · Session 3 | Choose units for three tests, one in branches sharing staff | [`D1_3_choose_units_three.ipynb`](labs/D1_3_choose_units_three.ipynb) |
| 1.4 | Day 1 · Session 4 | Complete a pre-registration; review a neighbour's against the checklist | [`D1_4_complete_pre_registration.ipynb`](labs/D1_4_complete_pre_registration.ipynb) |
| 2.1 | Day 2 · Session 1 | Compute sample sizes for three minimum effects | [`D2_1_compute_sample_sizes.ipynb`](labs/D2_1_compute_sample_sizes.ipynb) |
| 2.2 | Day 2 · Session 2 | Simulate the analysis 1,000 times; compare power with the formula | [`D2_2_simulate_analysis_1.ipynb`](labs/D2_2_simulate_analysis_1.ipynb) |
| 2.3 | Day 2 · Session 3 | Simulate randomisation across 24 branches; measure the power lost | [`D2_3_simulate_randomisation_across.ipynb`](labs/D2_3_simulate_randomisation_across.ipynb) |
| 2.4 | Day 2 · Session 4 | Choose a duration covering weekly cycles and the month-end peak | [`D2_4_choose_duration_covering.ipynb`](labs/D2_4_choose_duration_covering.ipynb) |
| 3.1 | Day 3 · Session 1 | Check balance and sample ratio on a log with a planted fault | [`D3_1_check_balance_sample.ipynb`](labs/D3_1_check_balance_sample.ipynb) |
| 3.2 | Day 3 · Session 2 | Analyse the reminder test; state the result in two sentences | [`D3_2_analyse_reminder_test.ipynb`](labs/D3_2_analyse_reminder_test.ipynb) |
| 3.3 | Day 3 · Session 3 | Run 1,000 A/A tests with peeking, twenty metrics and wrong units | [`D3_3_run_1_000.ipynb`](labs/D3_3_run_1_000.ipynb) |
| 3.4 | Day 3 · Session 4 | Find seeded flaws in a write-up, draft the memo, choose the capstone | [`D3_4_find_seeded_flaws.ipynb`](labs/D3_4_find_seeded_flaws.ipynb) |
<!-- /academy:labs -->

## Capstone

A design and analysis pack for one of three synthetic cases (reminder message, form redesign, training programme): pre-registration, sample-size and analysis notebooks, result note and a review memo on a flawed write-up, in a public repository; eight-minute defence

**Submission:** REPLACE: what participants submit and how: a public repository link, or a shared folder for a course without code

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

- REPLACE: every source the course cites, with its address, in course.json under "sources"; this list is written from there
<!-- /academy:sources -->

### National references

- Personal Data Protection Law and its implementing regulations: REPLACE: the address of the official text
- General Rules for Secondary Use of Data: REPLACE: the address of the official text
- SDAIA AI Ethics Principles: REPLACE: the address of the official text
