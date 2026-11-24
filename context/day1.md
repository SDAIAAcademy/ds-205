---
course: "Designing and Reading Experiments"
code: "DS-205"
version: "2027.2.0"
deck: "day1"
day: 1
language: "en"
view: "trainee"
source: "https://sdaiaacademy.github.io/ds-205/slides/day1.html"
---

# Designing and Reading Experiments

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
