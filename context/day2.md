---
course: "Designing and Reading Experiments"
code: "DS-205"
version: "2027.1.0"
deck: "day2"
day: 2
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-205/slides/day2.html"
---

# Designing and Reading Experiments

## Day 2: Size and run

How many units, for how long: the size a minimum effect demands, checked by simulation, and the calendar a test must cover

#### [day2#title] Size and run

*SDAIA Academy · Designing and Reading Experiments*

Day 2: How many units, for how long: the size a minimum effect demands, checked by simulation, and the calendar a test must cover

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-205

#### [day2#agenda] Size and run

*Today*

- **Session 1 · Power and the minimum effect**: Two errors, power, the minimum effect of interest and the sample-size formula for two proportions
- **Session 2 · Power by simulation**: Simulate the planned analysis many times to check power, draw a power curve and count false positives
- **Session 3 · Cluster randomisation**: When whole branches are randomised: intraclass correlation, the design effect, analysis at the branch level and pairing
- **Session 4 · Run time and seasonality**: Weekly cycles, the month-end peak, whole cycles and the outcome window decide how long a test runs

#### [day2#review-day1] Which page is ready to sign?

*Review of Day 1*

**Question:** Four pre-registrations for the reminder test differ in one line each. Which line is acceptable?

- A. Primary metric: on-time renewal or counter visits, whichever is clearer
- B. Unit: the renewal notice, since that is what the platform sends
- C. Stop rule: 28 days, one analysis at the end, a safety look at the guardrails on day 14
- D. Guardrail: we will keep an eye on complaints

### Session 1: Power and the minimum effect

#### [day2#s1] Power and the minimum effect

*Session 1*

- Explain power and the two errors a test can make
- Compute the sample size per arm for a minimum effect by formula
- Show how the minimum effect drives the size and the days of traffic needed

#### [day2#two-ways-to-be-wrong] A test can be wrong in two ways, and you choose both rates in advance

*Before any data*

|  | The test says "effect" | The test says "no clear effect" |
| --- | --- | --- |
| **The reminder does nothing** | *False win.* You accept 5% of these: the level, α. | Correct. |
| **The reminder adds 2 points** | Correct. The chance of landing here is the **power**: 80% by convention. | *Missed effect.* 20% of the time at 80% power. |

> **Both rates are prices.** A false win costs the office a reminder that does not pay. A missed effect costs it a reminder that would have.

#### [day2#power-is-about-many-tests] The same true effect gives a different estimate in every test

*Lab 2.2, step 1*

| Simulated test | Estimate | p-value |
| --- | --- | --- |
| 1 | +1.87 points | 0.0086 |
| 2 | +3.60 points | below 0.0001 |
| 3 | +1.75 points | 0.0144 |
| 4 | +1.90 points | 0.0077 |
| 5 | +0.83 points | 0.2466 |

- Five tests in one simulated world. The truth is +2 points in all five.
- Four find it. The fifth misses: an unlucky draw, not a wrong analysis.
- **Power** is the share of such tests that find the effect.
- It belongs to a design and an effect size, never to one result.

#### [day2#what-drives-the-size] Three things drive the sample size, and one of them is squared

*Two proportions, two arms*

```python
def n_per_arm(p1, delta,
              alpha=0.05, power=0.80):
    p2 = p1 + delta
    za = stats.norm.ppf(1 - alpha / 2)  # 1.96
    zb = stats.norm.ppf(power)          # 0.84
    spread = p1 * (1 - p1) + p2 * (1 - p2)
    return ceil((za + zb) ** 2
                * spread / delta ** 2)
```

- **The error rates** you accept: 1.96 and 0.84.
- **The spread** of a yes-or-no outcome, largest at 50%.
- **The minimum effect**, squared, in the denominator.
- Only the third is open to discussion with the director.

#### [day2#size-for-two-points] Two points on a baseline of 61.58% need 9,187 holders per arm

*Lab 2.1, steps 1 and 2*

- **61.58%** baseline on-time renewal, from 391,802 notices in 182 days
- **9,187** holders per arm for 2 points at 5% and 80%
- **18,374** holders in all: about 9 days of average traffic at 2,153 notices a day

> **The page said 9,200.** It was this calculation, rounded.

#### [day2#halve-the-effect] Halve the minimum effect and the test needs four times the holders

*Lab 2.1, steps 3 and 5*

| Minimum effect | Holders per arm | Against 2 points | Days of average traffic |
| --- | --- | --- | --- |
| 4 points | 2,268 | a quarter | 3 |
| **2 points** | **9,187** | 1 | **9** |
| 1 point | 36,950 | four times | 35 |

> **This table is the conversation with Sahar.** "Would you act on 4 points only? Three days. Do you need to see 1 point? Five weeks." She chooses the row; the size follows.

#### [day2#size-is-an-estimate] A sample size is an estimate, not a number to quote to the last holder

*Lab 2.1, step 4 and stretch*

| For 2 points | Per arm |
| --- | --- |
| The formula you wrote | 9,187 |
| statsmodels, same inputs | 9,189 |
| The formula at 90% power | 12,298 |

- Two honest methods differ by two holders: the library transforms the proportions first.
- The baseline is itself a guess about the test window.
- Ten more points of power cost a third more holders.
- Say "about 9,200 per arm".

#### [day2#check-halving] What does a smaller minimum effect cost?

*Checkpoint*

**Question:** A test needs 6,000 residents per arm to detect 3 points. The director now says she would act on 1.5 points. About how many residents per arm does the test need?

- A. 24,000
- B. 12,000
- C. 6,000
- D. 1,500

#### [day2#lab-2-1] Sample sizes for three minimum effects

Lab 2.1 · 25 min

Compute the sample size of the reminder test for minimum effects of 1, 2 and 4 points by formula, check it against a library and turn each size into days of traffic.

[D2_1_sample_sizes.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D2_1_sample_sizes.ipynb)

- [ ] Baseline rate and daily traffic from the history (4 min)
- [ ] The formula by hand for 2 points (7 min)
- [ ] Three minimum effects: 1, 2 and 4 points (5 min)
- [ ] Check against a library (4 min)
- [ ] Turn sizes into days of traffic (5 min)
- [ ] ✱ Stretch: Repeat for 90% power and say what the extra ten points cost

### Session 2: Power by simulation

#### [day2#s2] Power by simulation

*Session 2*

- Simulate a planned two-arm test and its analysis with a seed
- Estimate power by simulation and state its counting error
- Draw a power curve and read the sample size from it

#### [day2#simulate-the-plan] To check a design, run it a thousand times in a world you built

*The DS-201 habit, before the test*

1. **1 · Build a world** baseline 61.58%; the reminder truly adds 2 points
2. **2 · Run the plan** 9,187 holders per arm, the pre-registered test
3. **3 · Repeat** 1,000 times, with a seed
4. **4 · Count** the share of tests that say "significant"

> **That share is the power.** If the formula is right, it should be about 80%.

#### [day2#one-simulated-test] One simulated test is two binomial draws and the planned analysis

*Lab 2.2, steps 1 and 2*

```python
def power_sim(gen, n, p1, delta, reps):
    x_c = gen.binomial(n, p1, size=reps)
    x_r = gen.binomial(n, p1 + delta,
                       size=reps)
    _, _, p = U.z_test(x_c, n, x_r, n)
    return (p < 0.05).mean()

power_sim(U.rng(22), 9187,
          0.6158, 0.02, 1000)   # 0.806
```

- Each draw is the number of on-time renewals among n holders in one arm.
- The analysis is the one on the pre-registration, not a shortcut.
- `size=reps` runs all the tests at once.
- The seed makes your 0.806 your neighbour's 0.806.

#### [day2#simulated-power] The simulation agrees with the formula, within its own counting error

*Lab 2.2, steps 2 and 3*

- **80%** power promised by the formula at 9,187 per arm
- **80.6%** of 1,000 simulated tests were significant
- **±2.5** points: two standard errors of a share counted over 1,000 tests

- A simulated share is an estimate too. Quote it with its error.
- 10,000 simulated tests would narrow the error to ±0.8 points.

#### [day2#power-curve] The power curve is steep at first and flat at the end

*Lab 2.2, step 4*

Figure: Power to detect 2 points on a baseline of 61.58%.

- 2,000 per arm: 23.6% simulated. A real effect is missed three times in four.
- 9,187 per arm: 78.7% on the curve's run, 80% by formula.
- 30,000 per arm: every simulated test found it.
- The first 9,000 buy 80 points of power. The next 21,000 buy 20.

#### [day2#false-positives-by-count] In a world with no effect, one test in twenty still wins

*Lab 2.2, step 5*

**5.3%** of 1,000 simulated tests were significant when the reminder did nothing

- That is the 5% you agreed to when you chose the level.
- It holds for **one** planned analysis of **one** metric at **one** moment.
- Tomorrow you break each of the three conditions and count again.

> **What goes wrong.** "Significant" is read as "true". At a 5% level, an office that tests twenty useless ideas adopts one of them.

#### [day2#when-the-formula-ends] The formula covers one design; a simulation covers the one you have

*What simulation is for*

- **The formula assumes.** Independent units. Two proportions. Equal arms. One look. The baseline you guessed.
- **Real designs break it.** Visitors inside branches. A baseline that turns out to be 50%: power 76.6%, not 80%. An effect that differs by weekday. An analysis on branch means.

> **The rule.** Use the formula for a first number and for the conversation about the minimum effect. Use a simulation of the planned analysis for the number you put on the page.

#### [day2#check-simulated-power] What does a simulated power of 81% tell you?

*Checkpoint*

**Question:** You simulate a planned test 1,000 times with a true effect of 2 points. 81% of the simulated tests are significant. Which statement is correct?

- A. There is an 81% chance that the reminder works
- B. If the real test is significant, the effect is real with probability 81%
- C. The reminder will raise on-time renewal by 81% of 2 points
- D. If the effect is really 2 points, a test of this design finds it about 81 times in 100

#### [day2#lab-2-2] Power by simulation

Lab 2.2 · 25 min

Simulate the reminder test and its analysis 1,000 times at the planned size, compare the simulated power with the formula, draw a power curve and count false positives when nothing differs.

[D2_2_power_simulation.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D2_2_power_simulation.ipynb)

- [ ] Simulate one test and analyse it (5 min)
- [ ] 1,000 tests at the planned size (6 min)
- [ ] The counting error of the simulation (3 min)
- [ ] A power curve over sample sizes (7 min)
- [ ] No effect: the false-positive rate (4 min)
- [ ] ✱ Stretch: Keep the planned size and let the true baseline be 50% or 70%: what happens to power?

### Session 3: Cluster randomisation

#### [day2#s3] Cluster randomisation

*Session 3*

- Estimate the intraclass correlation and the design effect from baseline data
- Measure by simulation the power lost when branches are randomised in place of visitors
- Analyse a cluster-randomised test at the cluster level and improve it by pairing

#### [day2#visitors-of-one-branch] Visitors of one branch resemble each other

*The counter test*

- Mansour's test: a triage desk at the entrance. Outcome: served within 15 minutes. Minimum effect: 5 points.
- Visitors share a queue, so **branches** are randomised: 12 with the desk, 12 without.
- Four baseline weeks: 10,888 visits, 62.2% served within 15 minutes.
- By branch the rate runs from 43.7% to 80.3%.

- **Intraclass correlation.** The share of the outcome's variance that lies **between** branches. Here 0.033: three per cent of the variation is about which branch you walked into.

#### [day2#design-effect] A small correlation times a large branch is a large penalty

*Lab 2.3, step 1*

- **0.033** intraclass correlation of the 15-minute outcome
- **454** visits per branch in four weeks, on average
- **15.8** design effect: 1 + (454 − 1) × 0.0326

- The **design effect** is how many times larger the variance of the estimate is when branches are randomised in place of visitors.
- 10,888 visits in 24 branches carry the information of about 691 independent visits.

#### [day2#power-lost] Randomising branches costs 77 points of power

*Lab 2.3, steps 2 and 3 · 1,000 simulated tests each*

- **100%** power for 5 points if 10,888 visitors could be randomised one by one
- **22.8%** power when 12 branches get the desk and 12 do not, analysed by branch

> **The same visits, the same effect, the same four weeks.** The test has 24 units, and branches differ from each other by far more than 5 points.

#### [day2#visit-level-analysis] Analysing visits from a branch-randomised test manufactures wins

*Lab 2.3, step 4*

**68.9%** of tests were "significant" when the desk did nothing and visits were analysed as if each had its own coin

- The tempting repair: "we have 10,888 visits, use them all".
- The visit-level test reads the luck of which branches landed in which arm as an effect of the desk.
- It is not a more powerful analysis. It is a wrong one.

> **Analyse what you randomised.** One rate per branch, 24 numbers.

#### [day2#pairing-recovers-power] Pairing like branches recovers much of the lost power

*Lab 2.3, step 5*

| Design | Analysis | Power for 5 points | False wins, no effect |
| --- | --- | --- | --- |
| Visitors randomised (not possible here) | Visits | 100% | about 5% |
| 12 and 12 branches | Branch rates, t-test | 22.8% | 4.5% |
| 12 and 12 branches | Visits, z-test | meaningless | 68.9% |
| **12 pairs of like branches** | Pair differences, paired t-test | **62.2%** | 5.8% |

- Sort branches by baseline rate, pair neighbours, toss a coin inside each pair.
- The stable differences between branches cancel inside the pairs.

#### [day2#what-buys-power-in-clusters] More branches help; more visits per branch hardly do

*When power is still short*

- **More units:** the strongest lever, and here there are no more branches.
- **A longer test:** helps a little; the difference between branches stays.
- **Pairing or a baseline:** removes the stable part of that difference.
- **A larger minimum effect:** an honest answer if the desk is only worth having for a large gain.

- **And fewer units than you think.** Three pairs of branches share staff, so the test has 21 units, not 24. Randomised 10 against 11 without pairing, its power is 20.6%.

> **Not on the list:** a cleverer analysis of the same coin tosses.

#### [day2#check-clusters] How large is this test?

*Checkpoint*

**Question:** A ministry tests a new enrolment procedure in 16 schools, 8 with it and 8 without. Each school enrols about 600 pupils. The outcome is whether a pupil's file is complete on the first day. What decides the power of the test most?

- A. The 9,600 pupils
- B. The 16 schools and how much schools differ from each other
- C. The 600 pupils in each school
- D. The 5% significance level

#### [day2#lab-2-3] 24 branches, 12 and 12

Lab 2.3 · 25 min

Simulate the counter-service test with visitors randomised and with 24 branches randomised, measure the power lost, see what a visitor-level analysis does and recover power by pairing branches.

[D2_3_branch_clusters.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D2_3_branch_clusters.ipynb)

- [ ] Intraclass correlation and design effect from baseline visits (5 min)
- [ ] Visitors randomised: power (5 min)
- [ ] Branches randomised, analysed by branch: power (7 min)
- [ ] The visitor-level analysis under no effect (4 min)
- [ ] Pair branches by baseline and measure power again (4 min)
- [ ] ✱ Stretch: Treat each pair of branches that share staff as one unit and measure the power of 21 units

### Session 4: Run time and seasonality

#### [day2#s4] Run time and seasonality

*Session 4*

- Describe the weekly cycle and the month-end peak in traffic and in the baseline rate
- Turn a sample size into a duration of whole weeks that covers the month-end
- Explain what a test estimates when it covers only part of a cycle

#### [day2#two-cycles] The office's traffic has a weekly cycle and a month-end peak

*Lab 2.4, step 1 · eight weeks of the history*

Figure: Notices sent per day, Sunday 1 March to Saturday 25 April of the synthetic history.

- Sunday to Thursday: about 2,300 notices a day.
- Friday and Saturday, the weekend: about 1,100 and 1,400.
- From the 26th: about one and a half times a normal day, because most permits fall due at the month-end.

#### [day2#cycles-move-the-rate] The cycles move the baseline rate, not only the traffic

*Lab 2.4, step 1*

| Notices sent on | Mean notices a day | Renewed on time |
| --- | --- | --- |
| Sunday to Thursday | 2,360 to 2,534 | 62.1% to 62.6% |
| Friday | 1,203 | 58.3% |
| Saturday | 1,505 | 58.4% |
| The 26th and later | 2,974 | 57.6% |
| Before the 26th | 1,978 | 62.9% |

> **Different days, different holders.** If the baseline differs by 5 points between day types, the effect of a reminder may differ too.

#### [day2#size-reached-on-day-nine] The planned size is reached on day 9, a Monday

*Lab 2.4, step 2*

- The test starts on Sunday 6 September. A forecast gives each day its expected traffic.
- 18,374 holders are reached on test day 9.
- Stopping there, the test has seen two Sundays, two Mondays, one Friday and no month-end.

- **What a 9-day test would estimate.** The effect of the reminder for holders notified in early September, with Sundays and Mondays counted twice. Nobody asked that question.

#### [day2#whole-cycles] Run whole weeks, and cover the month-end

*Lab 2.4, step 3*

- **28 days** four whole weeks from 6 September; the five month-end days fall inside
- **60,694** holders expected, about 30,000 per arm
- **1.11** points: the effect such a test detects with 80% power

- The calendar set the duration; the formula set only its minimum.
- The extra holders are not wasted: they narrow the interval around the estimate.

#### [day2#short-test-different-question] A short test answers a different question

*Lab 2.4, step 4 · a planning assumption*

| Test | Holders | Month-end days | Expected estimate | 95% margin |
| --- | --- | --- | --- | --- |
| 9 days from 6 September | 18,484 | 0 | 1.86 points | ±1.40 |
| 14 days from 6 September | 27,682 | 0 | 1.82 points | ±1.15 |
| **28 days from 6 September** | **60,694** | **5** | **2.35 points** | **±0.77** |
| 9 days from 24 September | 22,430 | 5 | 3.23 points | ±1.27 |

> **If** the reminder adds 2 points on an ordinary day, 4 at the month-end and 1 on a weekend. Two short tests of the same reminder would report 1.9 and 3.2, and both would be called "the effect".

#### [day2#outcome-window-and-novelty] Two more clocks run: the outcome window and the fading of novelty

*After the last notice*

- **The outcome window.** A notice goes out 30 days before expiry. On-time renewal is known only at the expiry date. The last holders complete the metric 30 days after day 28. A result read earlier misses the holders who renew late in their window.
- **Novelty.** People react to anything new, and the reaction can fade. A short test catches the reaction at its peak. A longer test averages over it and can show the effect week by week.

> **On the page:** the duration, the date on which the primary metric is complete, and a plan to report the effect by week.

#### [day2#check-stop-date] How long should this test run?

*Checkpoint*

**Question:** A test of a new payment page starts on a Sunday. The planned size is reached on day 11. Traffic is low at weekends and salaries arrive on the 27th, after which payments surge. Day 11 is the 16th of the month. What duration do you choose?

- A. 11 days
- B. 14 days
- C. 28 days
- D. As long as it takes to reach significance

#### [day2#lab-2-4] Choose the run time

Lab 2.4 · 25 min

Read the weekly cycle and the month-end peak in 26 weeks of traffic, turn the planned size into days, and choose a duration of whole weeks that covers the month-end.

[D2_4_run_time.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D2_4_run_time.ipynb)

- [ ] Traffic and renewal rate by weekday and at month-end (6 min)
- [ ] Days needed for the planned size (4 min)
- [ ] Whole weeks that cover the month-end (4 min)
- [ ] What tests of 9, 14 and 28 days would estimate (7 min)
- [ ] Record the duration and its reason (4 min)
- [ ] ✱ Stretch: Start the 9-day test on the 24th of the month and compare its estimate

#### [day2#wrap-up] Three things to keep

*Day 2*

- **The effect is squared.** 2 points need 9,187 per arm; 1 point needs 36,950. The minimum effect is the director's choice, made from costs.
- **Simulate the plan.** 1,000 runs of the planned analysis gave 80.6% power and 5.3% false wins. When the design leaves the formula, only the simulation is left.
- **Units and calendars.** 24 branches gave 22.8% power; pairing gave 62.2%. Nine days reach the size; 28 cover the weeks and the month-end.

#### [day2#next] The test has run

*Before Day 3*

Tomorrow the 28 days are over. The platform has exported its log, a colleague is about to compute the effect, and something in the export is wrong.

- Reread the checks you promised on your page: the sample ratio and the balance.
- Recall from DS-201: the interval for a difference, and Holm's correction.
