# Capstone: a design and analysis pack

You take one case that was not used in class through the whole course: design, size, analysis
and review. You submit the pack in a public repository and defend one design choice live.

## Choose one case

The three cases are described in `cases.json` (lab 3.4 prints them). All data are synthetic and
seeded. Each case has a history or baseline file for the sample size, a completed experiment
log, and a write-up with seeded flaws.

| | Case | Minimum effect | Files |
|---|---|---|---|
| A | A reminder message for the annual stall inspection | 3 points of booking within 14 days | `data/a_history.csv`, `data/a_experiment.csv`, `a_writeup.md` |
| B | A redesigned form for building-works permits | 3 points of completion | `data/b_history.csv`, `data/b_experiment.csv`, `b_writeup.md` |
| C | A training programme for counter staff in 20 service centres | 4 points of first-visit resolution | `data/c_centres.csv`, `data/c_visits.csv`, `c_writeup.md` |

In case C the first wave of training has already happened and was not randomised. Your
pre-registration and sample size are for the test the office should run for the second wave;
your analysis says what the existing data can and cannot show.

## What you submit

A link to a **public GitHub repository** with:

1. `preregistration.md`: one page, from `../prereg_template.md`, that passes the twelve items
   of `../checklist.md`. Date it before your analysis commits.
2. `sample_size.ipynb`: the formula result, a simulated power curve and the chosen duration,
   with the reason for the duration.
3. `analysis.ipynb`: reruns from the raw files to every number of the result note, with a fixed
   seed. It starts with the sample ratio check and a balance table.
4. `result_note.md`: at most one page. Estimate, interval, checks, guardrails and a
   recommendation read against the minimum effect.
5. `review_memo.md`: at most one page on the case's write-up. Each flaw, its consequence for
   the reported result, the decision the evidence does support, and the next step.
6. `simulation_log.txt`: the printed output of one complete seeded run of both notebooks.

The commit history is part of the evidence: commit as you work.

Every pack states who is in each arm, why withholding the change from the other arm is
acceptable, which fields of the logs are used and how they are minimised, and which guardrail
stops the test if a group is harmed.

## The defence

Eight minutes on one design choice, then four minutes of questions. During the questions the
assessor changes **the minimum effect or the unit** ("the director would act on 2 points, not
3", "randomise centres, not visitors"). You recompute the sample size and say what it does to
the duration.

## Rubric

| Criterion | Weight | Full marks look like |
|---|---|---|
| Design and pre-registration | 25 | A decision with a number in it, the right unit with its reason, one primary metric, guardrails with thresholds including one for a group, a fixed stop rule, and a page that passes all twelve checklist items when read by a person |
| Power and sample size | 25 | The formula result with its inputs, a simulation that reproduces it within its counting error, a power curve, and a duration of whole cycles; for a cluster design, the design effect and the power of the units you really have |
| Analysis and checks | 20 | The sample ratio check and a balance table first, then the pre-registered analysis at the unit that was randomised, an interval read against the minimum effect, and guardrails with their intervals |
| Review memo | 20 | Every seeded flaw named with what it does to the reported number, at least one claim recomputed from the log, the decision the evidence supports and a next step |
| Writing and reproducibility | 10 | One command reruns everything from the raw files with a seed; the simulation log matches the notes; points are called points |

Assistant policy: open (AI-full) for the work. The defence is yours alone.

The capstone pack counts for 60% of the course mark and the live defence for 20%; the
supervised entry quiz and exit check make up the remaining 20%.
