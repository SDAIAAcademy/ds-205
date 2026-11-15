# Designing and Reading Experiments: labs

## Quick start

- Google Colab: open a notebook from the course page; its first cell clones this repository.
- Locally: clone the repository, then open the notebooks in `labs/` with Jupyter.

| Unit | Session | Notebook |
|---|---|---|
| Day 1 | Session 1 · Which claims need an experiment | [`D1_1_classify_six_studies.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_1_classify_six_studies.ipynb) |
| Day 1 | Session 2 · Decision, hypothesis and metrics | [`D1_2_write_decision_hypothesis.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_2_write_decision_hypothesis.ipynb) |
| Day 1 | Session 3 · Choosing the unit of randomisation | [`D1_3_choose_units_three.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_3_choose_units_three.ipynb) |
| Day 1 | Session 4 · Pre-registration | [`D1_4_complete_pre_registration.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_4_complete_pre_registration.ipynb) |
| Day 2 | Session 1 · Power and the minimum effect | [`D2_1_compute_sample_sizes.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_1_compute_sample_sizes.ipynb) |
| Day 2 | Session 2 · Power by simulation | [`D2_2_simulate_analysis_1.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_2_simulate_analysis_1.ipynb) |
| Day 2 | Session 3 · Cluster randomisation | [`D2_3_simulate_randomisation_across.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_3_simulate_randomisation_across.ipynb) |
| Day 2 | Session 4 · Run time and seasonality | [`D2_4_choose_duration_covering.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_4_choose_duration_covering.ipynb) |
| Day 3 | Session 1 · Did randomisation work | [`D3_1_check_balance_sample.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_1_check_balance_sample.ipynb) |
| Day 3 | Session 2 · Estimate, interval and effect | [`D3_2_analyse_reminder_test.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_2_analyse_reminder_test.ipynb) |
| Day 3 | Session 3 · False wins by simulation | [`D3_3_run_1_000.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_3_run_1_000.ipynb) |
| Day 3 | Session 4 · Reviewing a reported result | [`D3_4_find_seeded_flaws.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_4_find_seeded_flaws.ipynb) |

The notebooks are generated from the percent-format sources in `labs/_src/` by `labs/_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `labs/solutions/`. Edit the sources, not the notebooks.
