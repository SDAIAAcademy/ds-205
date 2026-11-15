---
course: "Designing and Reading Experiments"
code: "DS-205"
version: "2027.1.0"
scope: "course"
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-205/"
---

# Designing and Reading Experiments

Design a randomised experiment a public office can act on, size it, check it and read its result without fooling yourself

Participants design randomised experiments for a fictional municipal permits office and read the results without fooling themselves. They turn a decision question into a pre-registration with a hypothesis, primary and guardrail metrics, a stop rule and a unit of randomisation, compute sample size by formula and by simulation, analyse a synthetic experiment log, check that randomisation worked, and measure how peeking, many metrics and a mismatched unit inflate false wins. Variance reduction and sequential tests are left to DS-302.

- **Audience:** Practitioners. Graduates and early-career analysts who have completed the FN courses or passed the placement test, and analysts moving into data science.
- **Prerequisites:** DS-201 Statistical Inference by Simulation; Computes a proportion, a difference in means and a confidence interval; Writes a simulation loop in Python or R; Pre-work: about two hours on proportions, intervals and simulation, in the pre-work notebook of the labs folder (its name starts with P0), before the supervised entry quiz; Setup: a laptop with uv, or Google Colab. Nothing calls or downloads a model. Run 00_setup_check before Day 1; see labs/README.md.
- **Case study:** Mashraq Municipal Permits Office: Mashraq Municipal Permits Office (مكتب المشرق للتصاريح البلدية) is a fictional city office that issues resident parking, market stall, outdoor seating and building works permits. Its director, Sahar Al-Wuhaibi, wants three changes tested before they are adopted: a reminder message for renewals, a redesigned online form and a new way of serving visitors at the counters of 24 branches. All data are synthetic and generated with a fixed seed: 26 weeks of notice traffic with a weekly cycle and a month-end peak, a reminder test on 60,000 notices over 28 days whose platform export has a planted fault, a form test logged page view by page view, and four baseline weeks of counter visits in branches of which three pairs share staff. Participants work as Juri Al-Asmari, a junior analyst; holders, applicants and visitors appear only as pseudonymised keys and every result is reported in aggregate.

## Outcomes

- LO1 (Awareness): Distinguish a randomised experiment, a quasi-experiment and an observational comparison, and explain the causal claim each supports, given six study descriptions from public services
- LO2 (Applied): Draft a pre-registration stating the decision, hypothesis, unit of randomisation, primary and guardrail metrics, stop rule and analysis plan, given the office's question about renewal reminders
- LO3 (Applied): Compute the sample size and run time needed to detect a minimum effect of interest and check it by simulation, given baseline renewal rates, daily traffic and the office's minimum effect
- LO4 (Applied): Analyse a completed two-arm experiment with a difference in proportions, a confidence interval and a sample ratio mismatch test, given a synthetic log of 60,000 renewal notices
- LO5 (Applied): Measure by simulation the false-positive rate caused by peeking, many metrics and analysis at the wrong unit, given simulated A/A tests with no true effect
- LO6 (Performance): Review a reported experiment and decide whether it supports the decision it claims to support, given write-ups with seeded flaws, one in class and one in the capstone

## Day 1: Design

A question becomes a design: what to compare, what to measure, whom to randomise, written down before any data exist

#### [day1#title] Design

*SDAIA Academy · Designing and Reading Experiments*

Day 1: A question becomes a design: what to compare, what to measure, whom to randomise, written down before any data exist

Data Science Track · 3 teaching days + capstone day · 4 sessions · 4 labs · DS-205

#### [day1#agenda] Design

*Today*

- **Session 1 · Which claims need an experiment**: What a randomised experiment, a quasi-experiment and an observational comparison can each claim, and why
- **Session 2 · Decision, hypothesis and metrics**: From the director's question to a decision, a hypothesis, one primary metric, guardrails and a stop rule
- **Session 3 · Choosing the unit of randomisation**: The unit that is randomised, the unit that is analysed, and what happens when units affect each other
- **Session 4 · Pre-registration**: What a pre-registration fixes before the data exist, how personal data are handled, and how a reviewer reads it

### Session 1: Which claims need an experiment

#### [day1#s1] Which claims need an experiment

*Session 1*

- Explain what random assignment removes from a comparison
- Classify a study as a randomised experiment, a quasi-experiment or an observational comparison
- State the causal claim a study supports and the assumption it rests on

#### [day1#works-is-a-causal-claim] "It works" is a claim about what would have happened without it

*The word on every report*

- Sahar Al-Wuhaibi directs Mashraq Municipal Permits Office. Six studies on her desk end with "works".
- "Works" means: holders did better **than they would have done** without the change.
- Nobody can observe one holder with and without a reminder, so every study compares two groups.
- The question is how the groups came to differ.

- **The case of this course.** A fictional city permits office. Three changes wait for a decision: a renewal reminder, a redesigned online form, a new routine at the counters of 24 branches. You are Juri Al-Asmari, junior analyst. All data are synthetic.

#### [day1#groups-that-chose] Groups that chose differ in more than the thing they chose

*Lab 1.1, step 4*

- **+3.0** points: the true effect of the app on on-time renewal, set by us in a simulated world
- **+17.0** points: the gap between app users and the others when holders choose
- **+2.5** points: the gap when a coin decides who gets the app

- Organised holders install the app more often and renew on time more often, app or no app.
- The volunteer gap measures mostly that hidden trait. Statisticians call it **confounding**.

#### [day1#what-a-coin-buys] A coin makes the two groups alike in everything, seen and unseen

*Random assignment*

1. **1 · One pool** every holder due a notice in the window
2. **2 · A seeded coin** per holder, not per clerk, branch or weekday
3. **3 · Two arms** the same mix of organised and disorganised, old and new, apart from chance
4. **4 · One difference** the change itself; what remains is sampling error, which has a size

> **The coin does not know who is organised.** That is the whole point: it cannot favour a trait nobody measured.

#### [day1#bias-is-not-noise] More data cure noise. They do not cure bias

*Lab 1.1, step 4, repeated 200 times*

| Comparison | Mean gap over 200 repetitions | Smallest | Largest | True effect |
| --- | --- | --- | --- | --- |
| Holders choose | +18.1 points | +16.0 | +20.2 | +3.0 |
| A coin decides | +3.0 points | +1.0 | +4.8 |  |

- **Bias.** All 200 volunteer comparisons agree with each other, and all are wrong by about 15 points. A larger survey would be wrong more precisely.
- **Noise.** The coin comparisons scatter around the truth. Day 2 chooses a sample size that makes the scatter small enough.

#### [day1#three-designs] Three designs support three different claims

*The vocabulary of the first outcome*

| Design | How the groups came to differ | Claim it supports | Example at Mashraq |
| --- | --- | --- | --- |
| **Randomised experiment** | Chance alone | The change caused the difference, for the units in the test | A seeded coin per holder; a slot lottery |
| **Quasi-experiment** | A rule or a date nobody chose for themselves | Caused, *if* a stated assumption holds | A fee that starts at 10 square metres; booking switched on in six branches |
| **Observational comparison** | People or managers chose | The groups differ; the study cannot say why | App users against the others; volunteer branches |

> **The assignment makes the design, not the intention.** A lottery run for fairness is still an experiment.

#### [day1#quasi-rests-on-an-assumption] A quasi-experiment is as strong as the assumption you can defend

*Reading a quasi-experiment*

- **The fee line at 10 square metres.** Stalls of 9.9 and 10.0 square metres are alike, so the gap in renewal is the fee. **If** nothing else changes at the line, and **if** holders cannot pick their side of it.
- **Online booking in six branches.** Compare the change in missed appointments there with the change elsewhere. **If** both groups would have moved in parallel without it.

> **What goes wrong.** The assumption is left unsaid and the result is reported as if a coin had been tossed. Ask for the sentence that starts with "if".

#### [day1#when-not-to-randomise] Some questions should not be answered with an experiment

*Before you propose a test*

- **The benefit is already known.** Withholding something proven from half of the citizens is not acceptable.
- **No decision depends on it.** If the office will adopt the change whatever the result, do not test it.
- **There are too few units.** Three regions cannot be randomised into anything a test can read.
- **The harm cannot be undone.** A test needs a guardrail that can stop it in time.

> **At Mashraq every design answers four questions.** Who is in each arm? Why is withholding acceptable? Which data are used? Which guardrail stops the test if a group is harmed?

#### [day1#check-which-design] Which study lets the office say "caused"?

*Checkpoint*

**Question:** Mansour Al-Khelaiwi wants to know whether evening opening shortens waits. Four studies are possible. Which one supports "evening opening caused shorter waits" without a further assumption?

- A. Compare the branches whose managers asked for evening opening with the rest
- B. Draw 12 of the 24 branches by a recorded lottery for evening opening and compare with the other 12
- C. Open all branches in the evening from June and compare waits before and after
- D. Compare the waits of evening visitors with those of daytime visitors

#### [day1#lab-1-1] Six studies, three designs

Lab 1.1 · 25 min

Classify six studies from public services by design and by the causal claim each supports, mark the sheet, then simulate a comparison of volunteers beside a randomised one.

[D1_1_six_studies.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D1_1_six_studies.ipynb)

- [ ] Read the six studies and name each design (7 min)
- [ ] Name the claim each one supports (6 min)
- [ ] Mark the sheet against the key (3 min)
- [ ] Simulate volunteers beside a coin (6 min)
- [ ] Write the claim the app survey supports (3 min)
- [ ] ✱ Stretch: Make the hidden trait stronger and watch which of the two gaps moves

### Session 2: Decision, hypothesis and metrics

#### [day1#s2] Decision, hypothesis and metrics

*Session 2*

- Write the decision an experiment informs, with the action for each result
- Choose one primary metric and set a minimum effect of interest from costs
- Write guardrails with thresholds and a stop rule that protects holders

#### [day1#decision-first] Start from the decision the result will change

*Where a design starts*

1. **1 · Decision** who decides, and what they do for each result
2. **2 · Hypothesis** the change, the metric, the direction
3. **3 · Metrics** one primary, guardrails, a minimum effect
4. **4 · Stop rule** when the test ends and what may end it sooner

> **Sahar's question.** "Would a reminder seven days before a permit expires get more holders to renew on time?" Today a holder gets one notice, 30 days before expiry, and nothing after it.

#### [day1#hypothesis-and-estimand] The estimand says exactly which number the test estimates

*One number in a named population*

- **Hypothesis:** holders who get the reminder renew on time more often than holders who get only the standard notice.
- **Estimand:** the difference in the share renewing on time, reminder minus control, among holders sent a notice in the test window.
- It names the metric, the two arms, the direction of the subtraction and the population.

- **What it leaves out on purpose.** Other permit offices. Other seasons. Holders who got no notice in the window. The result will be about the holders in the test; everything else is an argument you make afterwards, in words.

#### [day1#one-primary-metric] One metric carries the decision; the others explain or protect

*Three jobs*

| Kind | Its job | In the reminder test |
| --- | --- | --- |
| **Primary** | Decides. Exactly one, defined with its time window. | On-time renewal: renewed on or before the expiry date. Baseline 61.6%. |
| **Secondary** | Explains the result. Reported whatever it shows. | Counter visits within 30 days of the notice. |
| **Guardrail** | Must not get worse. Has a threshold and an action. | Complaint rate; on-time renewal in each group of holders. |

> **What goes wrong.** Two "primary" metrics, and the report leads with whichever improved. Two metrics are two chances of a false win.

#### [day1#minimum-effect-from-costs] The minimum effect is the smallest gain that changes the decision

*Lab 1.2, step 3*

- **0.40** riyals per holder: the reminder and the replies and complaints it brings
- **20** riyals: staff time to process one late renewal and its fee
- **2 points** break-even: 0.40 / 20. Below it the reminder costs more than it saves

- It comes from costs and from what the director would act on, never from what the data can detect.
- Say **points**: from 61.6% to 63.6%. "2 per cent" could also mean 2% of 61.6%, which is 1.2 points.

#### [day1#guardrails-with-thresholds] A guardrail has a metric, a threshold and an action

*What must not get worse*

- **Complaint rate.** **Threshold:** the reminder arm exceeds control by more than 0.5 points.
  **Action:** stop the test and review the wording.
- **On-time renewal in each group.** **Groups:** channel (text message, e-mail) and holder type.
  **Threshold:** a group falls more than 3 points below control.
  **Action:** stop the reminder for that group and tell the data protection officer.

> **An average can hide a harmed group.** The second guardrail is how the design applies fairness: it names the groups before anyone looks.

#### [day1#stop-rule-before-start] The stop rule fixes the end and says what may end the test sooner

*Written before the first notice goes out*

- The test runs 28 days and ends on the planned date.
- One analysis of the primary metric, at the end.
- One safety look on day 14 reads the guardrails only.
- No early stop for a good result.

- **Who is in each arm.** **Control:** the standard notice, as today. **Reminder:** the same notice plus one message seven days before expiry. Nobody loses a service; the reminder is untested.

> **What goes wrong.** "We stop when the result is significant." Day 3 counts how often that rule declares a win when nothing differs.

#### [day1#check-primary-metric] Which metric should carry the decision?

*Checkpoint*

**Question:** Rehab Al-Tayyar's team redesigned the online application form so that more applicants finish it. Which is the primary metric of the test?

- A. Mean time spent on each page of the form
- B. Validation errors per page view
- C. Whichever of completion, errors and time improves most
- D. The share of applicants who complete the application

#### [day1#lab-1-2] The first half of the pre-registration

Lab 1.2 · 25 min

Write the decision, hypothesis, primary metric, minimum effect, guardrails and stop rule of the reminder test as a record that a checklist can read.

[D1_2_decision_metrics.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D1_2_decision_metrics.ipynb)

- [ ] Write the decision and the hypothesis (6 min)
- [ ] Choose the primary metric and measure its baseline (5 min)
- [ ] Set the minimum effect from the cost table (5 min)
- [ ] Write two guardrails with thresholds and actions (5 min)
- [ ] Write the stop rule and run the checklist (4 min)
- [ ] ✱ Stretch: Add a secondary metric and say why it is not a second primary metric

### Session 3: Choosing the unit of randomisation

#### [day1#s3] Choosing the unit of randomisation

*Session 3*

- Choose a unit of randomisation that keeps each person in one arm
- Distinguish simple, stratified and cluster assignment
- Recognise interference between units and choose a unit that contains it

#### [day1#unit-is-the-coin] The unit of randomisation is whoever the coin is tossed for

*Two units that must agree*

- **Unit of randomisation:** the thing that lands in an arm as a whole: a holder, an applicant, a branch.
- **Unit of analysis:** the thing you count when you compute the result.
- They should be the same. When the analysis counts something smaller, the test looks larger than it is.

- **The log tempts you.** Logs have one row per notice, per page view, per visit. Rows are what systems record. They are rarely what a person experiences as "getting the new version".

#### [day1#notices-of-one-holder] One holder in five has several permits, and their notices move together

*Lab 1.3, step 1 · 20,000 past notices*

- **20.0%** of holders have several notices
- **38.5%** of all notices go to those holders
- **70.7%** of pairs share one outcome; 52.9% would if two notices of a holder were unrelated

- A coin per notice would send both versions to 60.3% of these holders. Once reminded, a holder is reminded for every permit.
- The unit is the **holder**. The test enrols each holder once, at the first notice in the window.

#### [day1#pages-of-one-applicant] 53,514 page views come from 5,068 applicants

*Lab 1.3, step 2 · the form log*

| Per applicant | Page views |
| --- | --- |
| Median | 8 |
| Maximum | 70 |
| Share of all rows from the busiest tenth | 28.8% |

- Among applicants with 10 or more page views, a quarter never trigger a validation error and a quarter trigger one on at least 20% of their views.
- A page view tells you mostly about its applicant.
- The unit is the **applicant**: one form from the first page to the last.

#### [day1#simple-stratified-cluster] Simple, stratified and cluster assignment answer different needs

*How the coin is tossed*

- **Simple.** One coin per unit. Right when units are many and independent: 60,000 holders.
- **Stratified.** Sort units into groups that matter (channel, baseline level), then toss within each group. The arms match on that trait by construction. Worth it when units are few.
- **Cluster.** Toss for a whole group: a branch and everyone who visits it. Needed when people in a group affect each other. It costs power: Day 2 measures how much.

> **Whichever you choose, the coin is seeded and recorded.** Alternating days, odd and even keys chosen by hand, or "the first half of the list" are not coins.

#### [day1#interference-between-units] If one unit's treatment reaches another, the unit is too small

*When units touch each other*

- **Inside a branch.** The counter change is a triage desk at the entrance. Visitors share one queue and one team. Sending every second visitor to the desk changes the wait of the others too. The visitor cannot be the unit.
- **Between branches.** B03 and B04 share counter staff, as do B11 and B12, B19 and B20. A clerk carries the new routine next door, and staff moved to the desk are missing there. Each pair is one unit.

> **24 branches, 21 staff pools.** The unit of the counter test is the staff pool.

#### [day1#rows-are-not-units] The size of a test is its number of units, not its number of rows

*Lab 1.3, step 5*

| Test | Rows in the log | Unit | Units | Rows per unit |
| --- | --- | --- | --- | --- |
| Reminder | 20,000 notices | Holder | 15,395 | 1.3 |
| Form | 53,514 page views | Applicant | 5,068 | 10.6 |
| Counter | 10,888 visits | Staff pool | 21 | 518.5 |

> **What goes wrong.** "We have over ten thousand visits, so the test is well powered." It has 21 coin tosses.

#### [day1#check-unit] Whom do you toss the coin for?

*Checkpoint*

**Question:** The office wants to test a shorter text on the ticket that the queue machine prints. All visitors of a branch wait in one hall and watch one display. What is the unit of randomisation?

- A. The branch, or the staff pool where branches share staff
- B. The visitor: each ticket printed gets a coin
- C. The day: the short text on alternate days in every branch
- D. The ticket: it is what the machine logs

#### [day1#lab-1-3] Three tests, three units

Lab 1.3 · 25 min

Choose the unit for the reminder test, the form test and the counter test from evidence in the data: notices per holder, page views per applicant and branches that share staff.

[D1_3_three_units.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D1_3_three_units.ipynb)

- [ ] Reminder test: notices per holder and how alike they are (7 min)
- [ ] Form test: page views per applicant (5 min)
- [ ] Counter test: branches and shared staff (6 min)
- [ ] Record the unit of each test with its reason (4 min)
- [ ] Count the units each test really has (3 min)
- [ ] ✱ Stretch: If the coin were tossed per notice, what share of holders with several permits would get both versions?

### Session 4: Pre-registration

#### [day1#s4] Pre-registration

*Session 4*

- Complete a one-page pre-registration with an analysis plan and planned checks
- State who is in each arm, why withholding is acceptable and how log data are minimised
- Review a pre-registration against a checklist and say what fails and why

#### [day1#why-write-it-down] A pre-registration removes the choices you would make after seeing the data

*The reason for the page*

- Which metric leads the report? Which holders are excluded? When does the test stop? Which subgroup is shown?
- Each choice is reasonable. Made after the data are in, each one leans towards the result you hoped for.
- Nobody has to cheat. An honest analyst who chooses late still finds too many wins.

- **What the page is.** One page, dated, written before the first unit is assigned, that fixes the decision, the unit, the metrics, the size, the stop rule and the analysis. It can be amended, with a date and a reason, before the test starts. Not after.

#### [day1#one-page-twelve-items] One page, twelve items

*The reviewer's checklist*

- **C1 Decision:** the action for each result
- **C2 Hypothesis:** change, metric, direction
- **C3 Unit:** nobody in both arms
- **C4 Primary metric:** exactly one, with its window
- **C5 Minimum effect:** a number with its reason
- **C6 Guardrails:** metric, threshold, action

- **C7 Stop rule:** a fixed end, no early stop for success
- **C8 Size and duration:** from the minimum effect; whole weeks and the month-end
- **C9 Analysis plan:** test, interval, unit, as assigned
- **C10 Checks:** sample ratio and balance, before the result
- **C11 Arms and fairness:** who, why withholding is acceptable, the group guardrail
- **C12 Data:** fields, pseudonymised keys, aggregate reporting

#### [day1#analysis-plan] The analysis plan is one paragraph that leaves you no choice later

*C9*

- **The paragraph.** "A two-proportion z-test and a 95% interval for the difference in on-time renewal, with holders as the unit, analysed as assigned whether or not the reminder was delivered. Subgroups by channel and by prior lateness are exploratory and are reported as such."

- **The test and the interval** are named, so they cannot be picked afterwards.
- **The unit of analysis** is the unit of randomisation.
- **As assigned:** every holder counts in the arm the coin chose.
- **Subgroups** are named now and labelled exploratory.

#### [day1#planned-checks] Two checks are promised before anyone reads the result

*C10*

- **Sample ratio.** A fair coin over 60,000 holders gives about 30,000 in each arm. The page states the test and the line: a chi-square test against 50/50, failed below p = 0.001.
- **Balance.** The arms should look alike on traits fixed before the test: channel, holder type, prior lateness, tenure. The page names the traits.

> **Why promise them in advance?** A check that runs only when the result disappoints is not a check. It is a search for an excuse.

#### [day1#data-paragraph] The page says which data are used and how holders stay unidentifiable

*C12 · the logs describe people*

| Question | On the reminder test's page |
| --- | --- |
| Which fields? | Notice key, send date, permit type, holder type, channel, prior lateness, tenure, arm, outcomes. Nothing else. |
| Can the analyst identify a holder? | No. Keys are pseudonymised; no name, phone number or address leaves the messaging platform. |
| How are results reported? | In aggregate, never by holder; small groups are not shown. |
| When is the extract deleted? | When the report is signed. |

> **Who signs.** Abdullah Al-Hogail, the data protection officer. The logs were collected to send notices; analysing them for a test is a further use, and he decides whether the page covers it.

#### [day1#checklist-needs-a-reader] A script can check that a unit is written, not that it is the right one

*Lab 1.4, step 5*

- The neighbour's page states a unit: the renewal notice. The mechanical check gives it a tick.
- A reader fails it: a holder with three permits sits in both arms.
- Its "primary metric" is two metrics with the choice left open. The script sees a name and a definition.
- By the key, the page fails 8 of the 12 items.

- **The rule for reviews.** The checklist is a list of questions for a person. Read the page, answer each question in your own words, and sign only what you could defend to the director.

#### [day1#check-after-data] The test is running. What may still change?

*Checkpoint*

**Question:** On day 10 of the reminder test the team has three ideas. Which one is compatible with the pre-registration?

- A. Make counter visits the primary metric, because they are moving more clearly
- B. End the test today, because the difference is already significant
- C. Add days until renewal as an exploratory metric, labelled as added on day 10
- D. Drop holders whose reminder bounced from the reminder arm

#### [day1#lab-1-4] Complete and review a pre-registration

Lab 1.4 · 25 min

Complete the one-page pre-registration of the reminder test from a supplied first half, run the checklist on it, then review a neighbour's page against the same checklist.

[D1_4_pre_registration.ipynb](https://sdaiaacademy.github.io/ds-205/labs/D1_4_pre_registration.ipynb)

- [ ] Load the first half; add the unit, the size and the duration (5 min)
- [ ] Write the analysis plan and the planned checks (6 min)
- [ ] Write the data paragraph (4 min)
- [ ] Run the checklist on your page (3 min)
- [ ] Review the neighbour's page against the checklist (7 min)
- [ ] ✱ Stretch: Rewrite the neighbour's primary metric and stop rule so that they pass

#### [day1#wrap-up] Three things to keep

*Day 1*

- **The coin makes the claim.** Only random assignment removes what you did not measure. A volunteer comparison was wrong by 15 points in every one of 200 repetitions.
- **The unit is who lands in an arm.** Holders, applicants, staff pools. 10,888 visits are 21 units.
- **Decide before you look.** One primary metric, a minimum effect with a reason, guardrails with thresholds, a fixed end, an analysis plan. On one page, read by someone else.

#### [day1#next] Is 9,200 per arm right?

*Before Day 2*

Your page says 9,200 holders per arm and 28 days. Tomorrow you compute the first number, check it by simulation, and find out why the second is three times longer than the first requires.

- Keep your completed pre-registration at hand.
- Recall from DS-201: the standard error of a proportion, and what a p-value is.

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

## Capstone: Capstone: the design and analysis pack and its defence

Each participant defends one design choice of a pack on one of three synthetic cases in eight minutes, then answers four minutes of questions

#### [capstone#title] Capstone: the design and analysis pack and its defence

*SDAIA Academy · Designing and Reading Experiments*

Capstone: Each participant defends one design choice of a pack on one of three synthetic cases in eight minutes, then answers four minutes of questions

Data Science Track · 3 teaching days + capstone day · 8 min talk and demo · 4 min Q&A · DS-205

#### [capstone#agenda] How the defences run

*Capstone*

- **Expectations and final prep**: the rubric, a last rerun of the notebooks, then the first defences
- **Defences**: eight minutes on one design choice, then four minutes of questions
- **Review and closing**: peer feedback, the trainer's review, the follow-up task

#### [capstone#rubric] The rubric

*How the pack and its defence are scored*

| Item | Value |
| --- | --- |
| Design and pre-registration | 25% |
| Power and sample size | 25% |
| Analysis and checks | 20% |
| Review memo | 20% |
| Writing and reproducibility | 10% |

> **Every number in the notes comes out of a seeded rerun.** The pre-registration is committed before the experiment log is opened.

#### [capstone#format] 8 minutes for the defence, then 4 minutes of questions

*Format*

- **1 · The decision.** The case, the decision in one sentence with its number, and the unit you randomise with the reason.
- **2 · One design choice.** The unit, the size or the duration: what you chose, the evidence from your notebooks, and a live rerun with the seed.
- **3 · The reading.** Checks first, then the estimate with its interval against the minimum effect, and what the write-up got wrong.

> **In the questions,** the assessor changes the minimum effect or the unit. You say what happens to the size and the duration, then recompute and show it.

#### [capstone#three-cases] Three cases, one pack each

*The cases*

|  | Case | Minimum effect | What makes it hard |
| --- | --- | --- | --- |
| A | A reminder message for the annual stall inspection | 3 points of booking within 14 days | A guardrail that needs its interval |
| B | A redesigned form for building-works permits | 3 points of completion | A sound result inside a poor write-up |
| C | A training programme for counter staff in 20 service centres | 4 points of first-visit resolution | Clusters, and a first wave that was not randomised |

> **All data are synthetic and seeded.** Each case has a history file, a completed experiment log and a write-up to review.

#### [capstone#running-order] Who presents when

*Running order*

| # | Presenter | Case and design choice |
| --- | --- | --- |
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |
| 6 |  |  |
| 7 |  |  |
| 8 |  |  |

#### [capstone#final-prep] Final prep · 20 minutes

*Before the first defence*

Rerun both notebooks from the raw files, check that the numbers match your notes, and choose the design choice you will defend.

#### [capstone#now-presenting] Defence

*Now presenting*

##### Questions

#### [capstone#review] What the defences showed

*Trainer review*

- **Strongest patterns.** What several packs got right.
- **Common gaps.** What most packs would fix next.
- **One surprise.** Something nobody expected.

#### [capstone#what-next] Keep going

*After the course*

- **Your pack stays yours:** keep it reproducible. It is a template for the next test at work.
- **The follow-up task:** apply the twelve-item checklist to one experiment or pilot in your own organisation, and send the one-page review.
- **Next Academy course:** DS-302 Online Experiments and A/B Testing, which adds variance reduction, sequential tests and designs for units that interfere.

#### [capstone#thanks] Thank you

*SDAIA Academy*

Designing and Reading Experiments
