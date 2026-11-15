# The design checklist

Twelve questions a reviewer asks of a pre-registration before a test starts. Used in lab 1.4,
on the capstone pack and in the follow-up task. Answer each in your own words; a tick without a
sentence is not a review.

| | Item | The question |
|---|---|---|
| C1 | Decision | Is the decision written down, with what the organisation will do for each possible result? |
| C2 | Hypothesis | Does the hypothesis name the change, the metric and the direction? |
| C3 | Unit | Is the unit of randomisation stated, and can any person land in both arms? |
| C4 | Primary metric | Is there exactly one primary metric, with its definition and time window? |
| C5 | Minimum effect | Is the minimum effect of interest a number, with the reason for it? |
| C6 | Guardrails | Does each guardrail have a metric, a threshold and the action when it is crossed? |
| C7 | Stop rule | Is the end fixed in advance, with no early stop for a good result? |
| C8 | Size and duration | Does the sample size come from the minimum effect, and does the run cover whole weeks and the month-end? |
| C9 | Analysis plan | Does the plan name the test, the interval, the unit of analysis and analysis as assigned? |
| C10 | Checks | Are a sample ratio check and a balance check planned before the result is read? |
| C11 | Arms and fairness | Does it say who is in each arm, why withholding is acceptable and which guardrail protects a group from harm? |
| C12 | Data | Does it say which fields are used, how they are minimised and pseudonymised, and that results are reported in aggregate? |

## Reading a finished test

The same list read backwards is the review order of lab 3.4:

1. **Design.** What did the page promise (C1 to C8)?
2. **Checks.** Did the arms survive: sample ratio, balance, missing units (C10)?
3. **Analysis.** Was the promised analysis run: the unit, the primary metric, one look (C3, C4, C7, C9)?
4. **Claim.** Does the recommendation follow from the estimate and its interval, for the units and the period tested (C1, C5)?
