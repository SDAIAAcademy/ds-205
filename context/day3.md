---
course: "Designing and Reading Experiments"
code: "DS-205"
version: "2027.1.0"
deck: "day3"
day: 3
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-205/slides/day3.html"
---

# Designing and Reading Experiments

## Day 3: Read the result

The data are in: check the assignment, estimate with an interval, count the ways to fool yourself, review someone else's result

#### [day3#title] Read the result

*SDAIA Academy · Designing and Reading Experiments*

Day 3: The data are in: check the assignment, estimate with an interval, count the ways to fool yourself, review someone else's result

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-205

#### [day3#agenda] Read the result

*Today*

- **Session 1 · Did randomisation work**: Before any result is read: the sample ratio check, the balance table and analysis as assigned
- **Session 2 · Estimate, interval and effect**: The difference in proportions with its interval, read against the minimum effect, with guardrails and one subgroup
- **Session 3 · False wins by simulation**: How peeking, many metrics and the wrong unit of analysis manufacture wins when nothing differs, measured by A/A tests
- **Session 4 · Reviewing a reported result**: A review order for a reported experiment: from each flaw to its consequence to the decision the evidence supports

#### [day3#review-day2] Which plan gives the test a fair chance?

*Review of Day 2*

**Question:** A test needs 9,000 residents per arm for its minimum effect. Traffic is 2,000 residents a day, lower at weekends, with a surge at the month-end. Which plan do you accept?

- A. Run 9 days, until 18,000 residents are in
- B. Run 28 days: whole weeks, with the month-end inside
- C. Run 9 days with 4,500 per arm to finish sooner
- D. Run until the difference is significant

### Session 1: Did randomisation work

#### [day3#s1] Did randomisation work

*Session 1*

- Test whether the arm counts match the planned split
- Read a balance table and locate the segment in which an assignment or logging fault sits
- Decide which rows to analyse after a failed check and say why

#### [day3#checks-before-result] Check the assignment before you look at the outcome

*The order of reading*

1. **1 · Sample ratio** are the arms the size the coin should give?
2. **2 · Balance** do the arms look alike on traits fixed before the test?
3. **3 · Completeness** is every assigned unit there, with its outcome?
4. **4 · The result** only now

> **Why this order.** Once you have seen a pleasing result, every check that threatens it looks like pedantry. The page promised the checks first; keep the promise.

#### [day3#sample-ratio-check] 49.05% in the reminder arm is not what a fair coin gives

*Lab 3.1, step 1 · the platform's export*

- **30,054** rows in the control arm of the export
- **28,932** rows in the reminder arm
- **0.000004** p-value of a chi-square test against 50/50; the page set the line at 0.001

- A gap of one point looks harmless. With 59,000 rows a fair coin produces it about four times in a million.
- A failed check means: do not read the result until the cause is found.

#### [day3#balance-names-a-suspect] The balance table names a suspect

*Lab 3.1, step 2*

| Trait fixed before the test | Control | Reminder | p |
| --- | --- | --- | --- |
| **E-mail channel** | **15.04%** | **12.02%** | **below 0.0001** |
| Business holder | 38.57% | 38.34% | 0.56 |
| Late at the previous renewal | 21.95% | 21.96% | 0.97 |
| Tenure, years | 4.63 | 4.60 | 0.17 |

> **Reading it.** With four traits, one p-value near 0.05 would mean little. One that is far beyond any chance, on one trait, says where to look.

#### [day3#one-empty-cell] One cell of the export is empty

*Lab 3.1, step 3*

| Channel | Week | Control rows | Reminder rows | Share in the reminder arm |
| --- | --- | --- | --- | --- |
| **E-mail** | **1** | **1,071** | **0** | **0.0%** |
| E-mail | 2 | 1,017 | 1,075 | 51.4% |
| E-mail | 3 | 1,087 | 1,056 | 49.3% |
| E-mail | 4 | 1,345 | 1,347 | 50.0% |
| Text message | 1 to 4 | 25,534 | 25,454 | 49.9% |

> **What happened.** In week 1 the reminder job failed for e-mail. The export lists a notice only when its arm's messages completed, so those holders vanished from it.

#### [day3#coin-was-fair] The coin was fair. The export broke afterwards

*Lab 3.1, step 4*

- The assignment was recorded before any message went out: 30,054 and 29,946 holders. Ratio check: p = 0.66.
- 1,014 holders are missing from the export. All are reminder-arm e-mail holders of week 1.
- They are not a typical handful: 49.6% of them renewed on time, against 63.5% of all holders.

- **Attrition.** Units that drop out of one arm after assignment. When the ones that drop differ from the rest, the arms stop being comparable, and the coin's work is undone.

#### [day3#what-the-fault-would-claim] The faulty export adds half a point to the reminder's credit

*Lab 3.1, step 5*

- **+2.69** points: the effect computed from the export
- **+2.17** points: the effect as assigned, on all 60,000 holders
- **+0.53** points of bias from 1,014 missing rows

> **What to analyse.** Everyone the coin was tossed for, in the arm it chose, including the 1,014 the reminder never reached. That is "as assigned" on the page.

#### [day3#after-a-failed-check] A failed ratio check stops the reading, not necessarily the test

*What to do*

- **Stop reading results.** Nothing computed from a broken comparison is worth quoting.
- **Find the cell.** Split by segment and by time until the loss is located.
- **Go back to the assignment record.** If it is sound and outcomes exist for everyone, analyse as assigned.
- **If the assignment itself was faulty,** or outcomes are missing for the lost units, the test cannot be repaired. Fix the cause and run it again.
- **Write it in the result note,** whichever it was.

#### [day3#check-failed-ratio] The ratio check has failed. What now?

*Checkpoint*

**Question:** A form test planned a 50/50 split. The log shows 10,480 applicants on the old form and 9,720 on the new one (p below 0.0001). The new form shows a higher completion rate. What do you do first?

- A. Report the higher completion rate, with a note that the arms were unequal
- B. Delete 760 applicants at random from the old form's arm
- C. Reweight the new form's arm so that both arms count the same
- D. Find which applicants are missing from the new form's arm, and why

#### [day3#lab-3-1] Ratio and balance on the export

Lab 3.1 · 25 min

Run the sample ratio check and a balance table on the platform's export of the reminder test, find where rows went missing and decide what to analyse.

[D3_1_ratio_balance.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D3_1_ratio_balance.ipynb)

- [ ] The sample ratio check on the export (5 min)
- [ ] A balance table of four covariates (6 min)
- [ ] Locate the fault by channel and week (6 min)
- [ ] Compare with the test as assigned (4 min)
- [ ] Measure what the faulty export would have claimed (4 min)
- [ ] ✱ Stretch: How often does a healthy 50/50 assignment of 60,000 fail the check at 0.001? Simulate it

### Session 2: Estimate, interval and effect

#### [day3#s2] Estimate, interval and effect

*Session 2*

- Compute a difference in proportions with its standard error and 95% interval
- Read an interval against the minimum effect and separate statistical from practical significance
- Report guardrails and a subgroup without overstating either

#### [day3#estimate-and-interval] The reminder raised on-time renewal by 2.17 points, give or take 0.77

*Lab 3.2, steps 1 and 2 · 60,000 holders as assigned*

| Arm | Holders | Renewed on time | Rate |
| --- | --- | --- | --- |
| Control | 30,054 | 18,772 | 62.46% |
| Reminder | 29,946 | 19,353 | 64.63% |

- **+2.17** points: the difference
- **0.39** points: its standard error
- **1.40 to 2.94** the 95% interval

#### [day3#two-questions] "Is there an effect?" and "Is it large enough?" are different questions

*Lab 3.2, step 3*

Figure: The effect as assigned, and what the faulty export would have shown.

- **Is there an effect?** Yes. Zero is far outside the interval; p is below one in a million.
- **Is it at least 2 points?** The estimate says just. The interval says: between 1.4 and 2.9.
- The interval **straddles** the minimum effect.

#### [day3#reading-against-the-minimum] An interval can sit in four places, and each has its own sentence

*The interval against the minimum effect*

| Where the interval lies | What to say |
| --- | --- |
| Wholly above the minimum effect | The gain is at least the minimum, beyond reasonable doubt. |
| **Above zero, straddling the minimum** | **There is a gain. Whether it reaches the minimum is not settled.** |
| Above zero, wholly below the minimum | There is a gain, and it is too small to act on. |
| Containing zero | The data are consistent with no effect, and with effects up to the upper limit. Say which. |

> **What goes wrong.** All four are reported as "significant" or "not significant", which merges the first three and misdescribes the fourth.

#### [day3#guardrails-with-intervals] Guardrails are read with their intervals too

*Lab 3.2, step 4*

| Guardrail or metric | Effect of the reminder | 95% interval | Threshold |
| --- | --- | --- | --- |
| Complaint rate | +0.14 points | up to +0.30 | +0.50: held |
| On-time renewal, e-mail holders | +0.20 points | −1.86 to +2.26 | −3.00: held in every group |
| On-time renewal, text-message holders | +2.51 points | +1.68 to +3.33 |  |
| On-time renewal, business holders | +1.37 points | +0.11 to +2.63 |  |
| On-time renewal, resident holders | +2.65 points | +1.68 to +3.62 |  |
| Counter visits (secondary) | −1.79 points | −2.34 to −1.24 | none |

> **"No harm found" is weaker than "harm above the threshold ruled out".** Here the upper limit for complaints is below the threshold, so the stronger sentence holds.

#### [day3#subgroups-with-care] Compare subgroups by the interval of their difference

*Lab 3.2, step 5 · exploratory, as the page said*

| Holders | Effect | 95% interval |
| --- | --- | --- |
| Late before (13,163) | +2.94 | +1.23 to +4.65 |
| Not late before (46,837) | +1.94 | +1.09 to +2.79 |
| **Difference** | **+1.00** | **−0.91 to +2.91** |

- The smaller subgroup has the wider interval.
- The difference between the two could be zero, or nearly 3 points.
- Report it as a hypothesis for the next test, not as a finding of this one.

> **What goes wrong.** "It works for holders who were late before." Six subgroups are six more chances of a striking number.

#### [day3#result-in-two-sentences] The result note leads with two sentences the director can act on

*Lab 3.2, step 6*

- **The two sentences.** "The reminder raised on-time renewal by 2.2 points, and the data are consistent with a gain between 1.4 and 2.9 points. The estimate meets the minimum effect of 2 points, though the gain may be somewhat smaller, and no guardrail was crossed, so the evidence supports adopting the reminder."

- Estimate and interval first, in points.
- Then the reading against the minimum effect and the guardrails.
- Then what the pre-registered decision rule gives.
- The checks, the fault in the export and the subgroup follow underneath.

#### [day3#check-interval-reading] How do you report this result?

*Checkpoint*

**Question:** A test of a new letter has a minimum effect of 3 points. The result: +1.2 points, 95% interval +0.4 to +2.0, p = 0.003. Which sentence is right?

- A. The letter helps, by less than the 3 points that would justify it
- B. The letter is highly effective: the result is significant at 0.003
- C. The letter has no effect, since it missed the minimum effect
- D. The test is inconclusive and should run longer

#### [day3#lab-3-2] Analyse the reminder test

Lab 3.2 · 25 min

Analyse the 60,000 notices of the reminder test as assigned: estimate, interval, test, guardrails and one subgroup, then state the result in two sentences.

[D3_2_reminder_result.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D3_2_reminder_result.ipynb)

- [ ] Counts and rates by arm (4 min)
- [ ] Difference, standard error and 95% interval (6 min)
- [ ] The test and the minimum effect (4 min)
- [ ] Guardrails and the secondary metric (4 min)
- [ ] One subgroup, read with care (3 min)
- [ ] The result in two sentences (4 min)
- [ ] ✱ Stretch: Bootstrap the difference over holders and compare the two intervals

### Session 3: False wins by simulation

#### [day3#s3] False wins by simulation

*Session 3*

- Simulate A/A tests and count false wins
- Measure the false-win rate of peeking, of twenty metrics and of analysis at the wrong unit
- Apply the correct procedure to each trap and show that the rate returns to 5%

#### [day3#aa-tests] In an A/A test nothing differs, so every win is false

*The measuring instrument of this session*

- Both arms get the same thing. The true effect is zero by construction.
- Run 1,000 of them and count the "significant" ones.
- With one planned analysis of one metric at the right unit: **5.5%** of 1,000.
- That is the 5% you agreed to. Anything above it was added by a habit.

- **Three habits, three counts.** Looking every day. Looking at twenty metrics. Counting page views in place of applicants. Each feels harmless, and each can be found in reports written by careful people.

#### [day3#peeking] A p-value wanders, and 28 looks give it 28 chances to cross 0.05

*Lab 3.3, step 2*

Figure: Three A/A tests that dipped below 0.05 and came back.

- Rule: stop on the first day the p-value is below 0.05.
- **27.8%** of 1,000 A/A tests declare a win.
- Half of those false wins are declared by day 5.

#### [day3#one-planned-look] One analysis at the planned end restores the 5%

*The correct procedure, in this course*

- **27.8%** false wins: 28 daily looks, stop at the first p below 0.05
- **14.5%** false wins: four weekly looks
- **5.5%** false wins: one look, on day 28

- A test stopped early on a false win also reports a large "effect": only large swings cross the line with little data.
- Planned interim looks are possible with methods that spend the 5% across the looks. They are the subject of DS-302.

#### [day3#twenty-metrics] With twenty metrics, most tests of nothing show a "significant" one

*Lab 3.3, step 3*

- **64.1%** of A/A tests have at least one of twenty metrics below 0.05
- **5.5%** after Holm's correction for twenty
- **5.5%** with one pre-registered primary metric

- The chance that none of twenty unrelated metrics crosses is 0.95 to the power 20: 36%.
- Two honest ways out: one primary metric named in advance, or a correction for the number examined.
- Subgroups count the same way.

#### [day3#wrong-unit-of-analysis] Counting page views for applicants turns luck into significance

*Lab 3.3, step 4 · the form log, with applicants dealt a fresh coin*

- **34.0%** of A/A tests are significant when 53,514 page views are analysed as independent
- **5.8%** when the 5,068 applicants are analysed, as randomised

- The page-level test believes it has ten times the information it has, so its standard error is too small.
- Ordinary luck in which struggling applicants landed where then looks like an effect.

#### [day3#false-win-table] Each habit multiplies the false-win rate; each correct procedure restores it

*Lab 3.3, step 5*

| Trap | False wins with the trap | With the correct procedure |
| --- | --- | --- |
| Peeking: 28 daily looks, stop at the first p below 0.05 | 27.8% | 5.5% (one look at the planned end) |
| Many metrics: any of twenty | 64.1% | 5.5% (Holm, or one primary metric) |
| Wrong unit: page views for applicants | 34.0% | 5.8% (analyse applicants) |

> **They combine.** A report that peeked at many metrics per page view is close to a machine for producing wins. None of the three needs a wrong formula.

#### [day3#novelty-and-attrition] Novelty fades and attrition unbalances, even when the analysis is right

*Two traps that no A/A test shows*

- **Novelty.** A first-week reaction to anything new, which can fade. A test of eight days measures the reaction at its peak. Look for the effect by week, and distrust short tests of visible changes.
- **Attrition.** Units that drop out of one arm after assignment: a reminder that never arrived, a form that crashed on some devices. The remaining arms differ in who is left. Look at the sample ratio and at who is missing.

> **Both change the true comparison,** not the false-win rate. They are found by reading the design and the checks, which is the next session.

#### [day3#check-which-trap] Which habit produced this win?

*Checkpoint*

**Question:** A team planned a 4-week test of a new queue screen in 30 branches with one primary metric. They analysed it once, at the end, and report: "average wait fell, p = 0.01, n = 41,000 visits". Which trap should you check first?

- A. Peeking
- B. Many metrics
- C. Wrong unit of analysis
- D. Novelty

#### [day3#lab-3-3] A thousand A/A tests

Lab 3.3 · 25 min

Run 1,000 A/A tests with no true effect under three traps, daily peeking, twenty metrics and page views analysed in place of applicants, and tabulate the false-win rate with and without the correct procedure.

[D3_3_false_wins.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D3_3_false_wins.ipynb)

- [ ] One look at the end: the 5% you agreed to (4 min)
- [ ] Peeking: a look every day for 28 days (7 min)
- [ ] Twenty metrics: any win, then a correction (6 min)
- [ ] Wrong unit: page views against applicants (5 min)
- [ ] The table of false-win rates (3 min)
- [ ] ✱ Stretch: Peek once a week only, four looks: how much of the damage remains?

### Session 4: Reviewing a reported result

#### [day3#s4] Reviewing a reported result

*Session 4*

- Review a write-up in a fixed order: design, checks, analysis, claim
- Name each flaw with its consequence for the reported result
- State the decision the evidence does support and defend it

#### [day3#review-order] Review in a fixed order: design, checks, analysis, claim

*Reading someone else's result*

1. **1 · Design** what did the page promise: unit, primary metric, size, stop rule?
2. **2 · Checks** did the arms survive: ratio, balance, missing units?
3. **3 · Analysis** was the promised analysis run, at the unit that was randomised, once?
4. **4 · Claim** does the recommendation follow, for the units and the period tested?

> **Read the result last.** A reviewer who starts with the headline spends the rest of the page defending or attacking it.

#### [day3#the-write-up] "The redesigned form works. Roll it out to every form."

*Lab 3.4 · the form redesign test*

- **What was planned.** Primary metric: the share of applicants who complete the application. Minimum effect: 3 points. Unit: the applicant. A run of 28 days with one analysis at the end.
- **What the write-up reports.** "We watched the dashboard every morning. On day 8 the difference in validation errors was clearly significant, so we stopped." Errors per page view fell from 13.0% to 12.0%, "highly significant" with 53,514 page views. Completion 58.5% against 59.3%, p = 0.54. "We examined 14 metrics." "The redesigned form logged fewer applicants. We put this down to chance."

#### [day3#seven-flaws] Seven flaws, each with a place in the text

*Lab 3.4, step 1*

| Flaw | Where in the write-up |
| --- | --- |
| Metric switch | The headline is errors per page view; the page promised completion |
| Wrong unit | A z-test on page views; applicants were randomised |
| Peeking | Watched every morning, stopped on a significant day |
| Ratio mismatch and attrition | 2,738 against 2,330 applicants, "put down to chance" |
| Many comparisons | 14 metrics, and the strongest subgroup |
| Short run | 8 days of a planned 28: one weekend, no month-end |
| Overclaim | "Proven"; all forms; 9,000 more applications a year |

> **And three it does not have:** a control arm exists, a seeded coin assigned, both arms were measured alike. A review that cries wolf loses its reader.

#### [day3#recompute-two-claims] A review that only reads is an opinion: recompute

*Lab 3.4, step 2*

- **"We put this down to chance".** 2,738 against 2,330 applicants: ratio check p = 0.00000001. By device: 379 applicants on old mobile browsers in the current arm, **none** in the redesigned arm.
- **"Highly significant with 53,514 page views".** Per page view: 13.0% against 12.0%, p = 0.0002. Per applicant, as randomised: 13.0% against 12.3%, **p = 0.25**.

> **Two lines of code each.** The log was available to the author too.

#### [day3#flaw-consequence-decision] The memo goes from each flaw to its consequence to a decision

*Lab 3.4, step 3*

- **1 · Flaw and consequence.** Not "the unit is wrong" but "counted per applicant, the difference in errors is not significant".
- **2 · What the evidence supports.** "The test does not support a roll-out. It shows no reliable difference in completion, and a redesign that fails on old mobile browsers."
- **3 · The next step.** "Fix the browser fault. Run the full 28 days as pre-registered, one analysis, completion as primary, applicants as the unit, ratio check first."

> **What goes wrong.** A memo that ends at "the analysis is flawed" leaves the director with a decision and nothing to make it with.

#### [day3#finding-nobody-wanted] The test did find something, and the write-up put it down to chance

*Lab 3.4, steps 2 and stretch*

- The redesigned form does not work on old mobile browsers. 379 of them used the current form in eight days; a roll-out would turn away about twice that.
- On devices logged in both arms, completion is 61.0% on the current form and 59.3% on the redesign: the "right direction" disappears.
- That second comparison is a repair made after the fact. It shows how fragile the claim is; it does not prove the reverse.

- **A reviewer's best contribution.** Not the list of errors. The thing the data were saying that the author did not want to hear.

#### [day3#check-supported-decision] Which decision does the evidence support?

*Checkpoint*

**Question:** A write-up reports a randomised test of a new appointment text, analysed as pre-registered: missed appointments fell by 1.9 points (0.4 to 3.4), against a minimum effect of 1.5. It then recommends the text "for all clinics, and for vaccination reminders too". The test ran in the city's eight clinics. What do you write?

- A. Reject the write-up: the claim goes beyond the evidence
- B. Adopt the text for appointments in the eight clinics; test vaccination reminders separately
- C. Accept the recommendation as written: the test was sound
- D. Ask for a longer test before deciding anything

#### [day3#lab-3-4] Review a write-up

Lab 3.4 · 25 min

Find the seeded flaws in the write-up of the form test, recompute two of its claims from the log, draft the review memo and choose a capstone case.

[D3_4_review_memo.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D3_4_review_memo.ipynb)

- [ ] Read the write-up and mark the flaws (7 min)
- [ ] Recompute two claims from the log (7 min)
- [ ] Draft the memo: flaw, consequence, supported decision (8 min)
- [ ] Choose your capstone case (3 min)
- [ ] ✱ Stretch: Compare completion only on devices that were logged in both arms

#### [day3#wrap-up] Three things to keep

*Day 3*

- **Checks before results.** A ratio of 49.05% hid 1,014 missing holders and half a point of bias. Analyse everyone as assigned.
- **Intervals over verdicts.** +2.17 points, 1.40 to 2.94, against a minimum of 2. Say what is settled and what is not.
- **Wins are cheap.** Peeking 27.8%, twenty metrics 64.1%, page views 34.0%. One look, one metric, the right unit: about 5%.

#### [day3#next] One case, the whole course

*Before the capstone day*

Your pack: a pre-registration, a sample-size notebook with a power curve, an analysis notebook, a result note and a review memo, in a public repository.

- Start with the pre-registration, and commit it before you open the experiment log.
- You may use an assistant for the work. You defend it without one.
- Rehearse the question you will be asked: "the minimum effect is now half; what is the size?"
