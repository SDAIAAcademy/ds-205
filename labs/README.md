# Designing and Reading Experiments: labs

Hands-on notebooks for the SDAIA Academy course **DS-205 Designing and Reading Experiments (تصميم التجارب وقراءة نتائجها)**. Every lab works on **Mashraq Municipal Permits Office (مكتب المشرق للتصاريح البلدية)**, a fictional city office that wants three changes tested before it adopts them: a renewal reminder, a redesigned online form and a new routine at the counters of 24 branches. Each lab starts from supplied files, so none depends on an earlier one, and each ends with a short verification note: what was checked and what was not.

**Nothing calls or downloads a model.** A laptop processor or a Colab CPU runtime is enough. The optional hint-only tutor is an instruction file, `tutor_instruction.md`, that you paste into an assistant your Academy has approved.

## Quick start

**Google Colab.** Open a notebook from the [course page](https://sdaiaacademy.github.io/ds-205/), or directly: `https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/<notebook>.ipynb`. Run the first cell: it clones this repository and installs `requirements-colab.txt`.

**Local**
```bash
git clone https://github.com/SDAIAAcademy/ds-205
cd ds-205/labs
uv sync                          # creates the environment from pyproject.toml (uv.lock pins every version)
uv run jupyter lab
```
Run `00_setup_check.ipynb` once before Day 1. It imports the libraries and reads the data files.

| Setting | Default | Meaning |
|---|---|---|
| `DS205_QUICK` | `0` | `1` runs fewer simulated tests, for a fast pass |

## Notebooks

| Day | Session | Notebook |
|---|---|---|
| 0 | Setup | [`00_setup_check.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/00_setup_check.ipynb) |
| 0 | Pre-work: proportions, intervals and simulation | [`P0_prework_proportions_simulation.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/P0_prework_proportions_simulation.ipynb) |
| 1 | Six studies, three designs | [`D1_1_six_studies.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_1_six_studies.ipynb) |
| 1 | The first half of the pre-registration | [`D1_2_decision_metrics.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_2_decision_metrics.ipynb) |
| 1 | Three tests, three units | [`D1_3_three_units.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_3_three_units.ipynb) |
| 1 | Complete and review a pre-registration | [`D1_4_pre_registration.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D1_4_pre_registration.ipynb) |
| 2 | Sample sizes for three minimum effects | [`D2_1_sample_sizes.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_1_sample_sizes.ipynb) |
| 2 | Power by simulation | [`D2_2_power_simulation.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_2_power_simulation.ipynb) |
| 2 | 24 branches, 12 and 12 | [`D2_3_branch_clusters.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_3_branch_clusters.ipynb) |
| 2 | Choose the run time | [`D2_4_run_time.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D2_4_run_time.ipynb) |
| 3 | Ratio and balance on the export | [`D3_1_ratio_balance.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_1_ratio_balance.ipynb) |
| 3 | Analyse the reminder test | [`D3_2_reminder_result.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_2_reminder_result.ipynb) |
| 3 | A thousand A/A tests | [`D3_3_false_wins.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_3_false_wins.ipynb) |
| 3 | Review a write-up | [`D3_4_review_memo.ipynb`](https://colab.research.google.com/github/SDAIAAcademy/ds-205/blob/main/labs/D3_4_review_memo.ipynb) |

Exercises are marked **✏️ Exercise** and raise `NotImplementedError` until you fill them in; the cell after each one then uses a stored reference result, so the rest of the notebook still runs. Complete reference versions are in `solutions/`. Cells marked **✱ Stretch** are optional. Self-checks print ✅ or ❌.

**Assistant policy.** Quizzes, the classification of lab 1.1, the two pre-registration labs (1.2 and 1.4), the first pass of the sample size (lab 2.1, steps 1 to 3) and of the analysis (lab 3.2, steps 1 to 3) and the flaw-finding of lab 3.4 are done without an assistant. In the simulation labs and the stretch items the tutor instruction may hint one step at a time; it never writes the simulation and never chooses a design. The capstone is open to an assistant and is defended live.

## The case study: Mashraq Municipal Permits Office

Synthetic and deterministic (seed 205), written by `prepare_data.py`. No real office, permit holder, applicant or branch is described.

| Data | File | Contents |
|---|---|---|
| Notice history | `data/history_daily.csv` | 182 days before the test: notices sent and renewed on time per day, with a weekly cycle and a month-end peak |
| Past notices with holders | `data/units_notices.csv` | 20,000 notices of last year with the pseudonymised key of the holder each belongs to |
| The reminder test, as assigned | `data/renewal_test.csv` | 60,000 holders over 28 days: arm, permit type, holder type, channel, prior lateness, tenure, on-time renewal, complaint, counter visit |
| The platform's export | `data/notice_log.csv` | the same test as the messaging platform exported it; lab 3.1 finds what is wrong with it |
| The form test | `data/form_pages.csv` | one row per page view of an applicant-randomised test of the redesigned form, stopped early |
| The form test's write-up | `data/writeup_form.md`, `data/writeup_form_key.json` | the report reviewed in lab 3.4 and its key |
| Branches and counters | `data/branches.csv`, `data/counter_visits.csv` | 24 branches with their staff pools; four baseline weeks of counter visits |
| Six studies | `data/studies.json`, `data/studies_key.json` | the study descriptions of lab 1.1 and their key |
| Pre-registrations | `data/prereg_start.json`, `data/prereg_neighbour.json`, `data/prereg_neighbour_key.json` | the first half of the reminder test's page, a flawed page to review, and its key |
| Reference results | `data/reference/` | what each exercise returns in the solution run, for the safety nets (full and quick mode) |

**Handled as personal data.** The logs are synthetic, and the labs still treat them as service logs about people, under the Personal Data Protection Law and the General Rules for Secondary Use of Data: holders, applicants and visitors appear only as pseudonymised keys, only the fields a test needs are extracted, results are reported in aggregate, and every design says who is in each arm and which guardrail stops the test if a group is harmed.

What is planted and which lab finds it is in `solutions/answer_key.md`, for the trainer.

## Forms, capstone and follow-up

- `checklist.md`: the twelve-item design checklist. `prereg_template.md`: the one-page pre-registration as a form.
- `capstone/README.md`: the three cases, what the pack must contain and the rubric.
- `followup/README.md`: the follow-up task, the checklist applied to an experiment at your workplace.

## For authors

The notebooks are generated from the percent-format sources in `_src/` by `_tools/py2nb.py` (`uv run python _tools/py2nb.py` from `labs/`), which also writes the solutions to `solutions/`. Edit the sources, not the notebooks. A solution run with `DS205_STRICT=1` stops at the first failed check; with `DS205_WRITE_REF=1` it rewrites `data/reference/`.
