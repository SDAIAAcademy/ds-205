# Answer key for the trainer

Everything here comes from `prepare_data.py` (seed 205) and from the solution runs in full mode.
The values the generator used are in `truth.json`. Quick mode gives the same data and noisier
simulated shares.

## What is planted, and which lab finds it

| Planted | Where | Found in |
|---|---|---|
| A hidden trait that drives both app use and renewal (simulated in the lab) | lab 1.1, step 4 | lab 1.1: volunteers +17.0 points, coin +2.5, truth +3.0 |
| Holders with several permits whose notices behave alike | `data/units_notices.csv` | lab 1.3: 20.0% of holders, 38.5% of notices; pairs agree 70.7% against 52.9% |
| Three pairs of branches that share counter staff: B03 and B04, B11 and B12, B19 and B20 | `data/branches.csv` | lab 1.3 (21 staff pools), lab 2.3 stretch |
| A neighbour's pre-registration that fails 8 of 12 checklist items | `data/prereg_neighbour.json` | lab 1.4: fails C3 to C9 and C11; the mechanical check wrongly passes C3 and C4 |
| A branch effect on being served within 15 minutes | `data/counter_visits.csv` | lab 2.3: ICC 0.033, design effect 15.8 |
| A weekly cycle and a month-end peak, in traffic and in the baseline rate | `data/history_daily.csv` | lab 2.4: Friday about half a working day; month-end days 2,974 notices against 1,978, rate 57.6% against 62.9% |
| The export fault: reminder-arm rows of the e-mail channel are missing for test days 1 to 7 (1,014 rows) | `data/notice_log.csv` | lab 3.1: ratio check p = 3.8e-06; e-mail share 15.0% against 12.0% |
| Attrition in the form test: no applicant on an old mobile browser is logged in the redesign arm (379 in the current arm) | `data/form_pages.csv` | lab 3.4, step 2: ratio check p = 1e-08 |
| Page views of one applicant resemble each other | `data/form_pages.csv` | lab 1.3 (busiest tenth: 28.8% of rows), lab 3.3 (34.0% false wins), lab 3.4 (p = 0.0002 by page view, 0.25 by applicant) |
| Seven flaws in the write-up, three absent ones in the catalogue | `data/writeup_form.md`, `data/writeup_form_key.json` | lab 3.4 |

The form test's data are the first generator draw in which the page-level test crosses 0.05
between days 8 and 11 while the applicant-level test does not (draw 68; draws 40 to 67 did not
fit). The write-up's story needs such a draw; say so if a participant asks how likely it was.

## Expected numbers, lab by lab (full mode)

**1.1** Key: S1 randomised / cause; S2 observational / association; S3 quasi / cause if; S4 quasi / cause if; S5 observational / association; S6 randomised / cause. 200 repetitions: volunteers mean +18.1 points (16.0 to 20.2), coin mean +3.0 (1.0 to 4.8). Stretch: +23.0 and +3.1.

**1.2** Baseline 61.6% (241,275 of 391,802). Break-even 0.40 / 20 = 2 points.

**1.3** 15,395 holders behind 20,000 notices. 5,068 applicants, 53,514 page views, median 8, maximum 70. Units: holder, applicant, staff pool (21). Stretch: 60.3%.

**1.4** Reference page: `prereg_reference.json`. Review key: pass C1, C2, C10, C12; fail the other eight.

**2.1** Baseline 61.58%, 2,153 notices a day. Per arm: 36,950 (1 point), 9,187 (2 points), 2,268 (4 points). statsmodels: 36,952, 9,189, 2,271. Days: 35, 9, 3. Stretch: 12,298 at 90% power.

**2.2** Simulated power at 9,187: 80.6% (±2.5). Curve: 23.6%, 46.8%, 60.5%, 78.7%, 88.4%, 95.2%, 100.0% at 2,000 to 30,000 per arm. Detectable with 30,000 per arm: 1.11 points. False-positive rate: 5.3%. Stretch: 78.6% at a 50% baseline, 84.1% at 70%.

**2.3** Power for 5 points: visitors randomised 100.0%; 12 and 12 branches, branch-level t-test, 22.8% (false wins 4.5%); visitor-level analysis of the branch test, 68.9% false wins; 12 pairs, 62.2% (false wins 5.8%). Stretch: 21 pools, 20.6%.

**2.4** Size reached on test day 9, a Monday. Duration 28 days, about 60,700 holders expected. Expected estimates under the planning assumption: 1.86 points (9 days), 1.82 (14 days), 2.35 (28 days). Stretch: 3.23.

**3.1** Export: control 30,054, reminder 28,932, p = 3.8e-06. As assigned: 30,054 and 29,946, p = 0.66. Missing: 1,014 reminder-arm e-mail holders of week 1, who renew on time at 49.6%. Effect from the export +2.69 points, as assigned +2.17. Stretch: about 0.1% false alarms.

**3.2** Control 18,772 of 30,054 (62.46%), reminder 19,353 of 29,946 (64.63%). Difference +2.17 points, standard error 0.39, interval 1.40 to 2.94, p = 3.6e-08. Reading against 2 points: straddles. Complaints +0.14 points (at most +0.30). Groups: e-mail +0.20, text message +2.51, business +1.37, resident +2.65. Counter visits −1.79 points. Prior lateness: +2.94 against +1.94, difference +1.00 (−0.91 to +2.91).

**3.3** One look 5.5%; 28 daily looks 27.8% (median stopping day 5); twenty metrics 64.1%, with Holm 5.5%; page views 34.0%, applicants 5.8%. Stretch: four weekly looks 14.5%.

**3.4** All seven seeded flaws present; `no_control`, `not_random` and `different_measurement` absent. Applicants 2,738 and 2,330. Stretch: completion on devices logged in both arms 61.0% against 59.3%.

## The truth behind the reminder test

The generator gave the reminder a true effect of 2.9 points for holders who received it: 2.0
points on an ordinary day, 2 more at the month-end, 2.5 more for holders who were late before,
1 less on weekends. Because 1,014 holders never received it, the true effect as assigned is 2.8
points. The estimate, 2.17, is a slightly unlucky draw, about 1.6 standard errors low. That is
worth saying in class after lab 3.2: the interval, 1.40 to 2.94, contains the truth, and a
single test's estimate is one draw.

## Capstone cases

| Case | True effect in the generator | What a sound pack finds |
|---|---|---|
| A | +2.2 points of booking; complaints +0.7 points | 1,100 holders have two stalls and two notices, always in one arm: the unit is the holder. At the holder level (first notice): 5,901 and 5,999 holders, +2.69 points (+0.93 to +4.46), which straddles the minimum effect of 3. The complaint guardrail is crossed: +0.42 points (+0.10 to +0.75) against a threshold of a quarter of a point. The write-up analyses notices, kept looking daily, highlights a subgroup, ignores the guardrail and extends the claim to all permit types. Supported decision: do not adopt this wording as it is. Size for 3 points: about 4,210 per arm, 19 days of traffic, so 28 days with the month-end. |
| B | +3.5 points of completion | Applicants 2,964 and 3,036, ratio check passes. Completion, the pre-registered primary metric at the right unit: +5.54 points (+3.01 to +8.06). The write-up's headline, time on page analysed per page view, was not pre-registered and counts contractors about twice. Its conclusion survives; its reasoning does not. Supported decision: launch, on the strength of completion, and report the saving in time as exploratory. Size for 3 points: about 4,350 per arm, 35 days of traffic. |
| C | +2.5 points of first-visit resolution | The trained centres were chosen, not drawn, and already led by 10 points at baseline (76.4% against 66.4%). The visit-level comparison of 78.7% with 66.1% is an observational comparison. The change from baseline, compared at the centre level, is +3.62 points (+0.97 to +6.28): a quasi-experimental estimate that rests on parallel trends; the estimate is below the minimum effect of 4 and its interval straddles it. C05 and C06 share staff. ICC 0.027, design effect about 15. The pack's design for the second wave: randomise the remaining centres in pairs matched on baseline, analyse centre-level changes, and state how little power ten centres give. |

The reference numbers of the three cases were computed once by the course author with a script
that is not part of the repository; recompute them after any rebuild of the data.
