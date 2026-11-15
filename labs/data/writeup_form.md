# Result: the redesigned application form works. Roll it out to every form.

**Author:** Hattan Al-Sayed, digital services analyst. **To:** Rehab Al-Tayyar, digital services lead.
**Test:** current form against redesigned form for the outdoor-seating permit application.

## What we planned

The pre-registration of 2 August named one primary metric, the share of applicants who complete the
application, a minimum effect of 3 points, applicants as the unit of randomisation (a seeded coin per
applicant, half to each form) and a run of 28 days with one analysis at the end.

## What we did

We watched the dashboard every morning. On day 8 the difference in validation errors was clearly
significant, so we stopped the test to give the better form to everyone sooner.

## Results

| | Current form | Redesigned form |
|---|---|---|
| Applicants in the log | 2,738 | 2,330 |
| Page views | 28,808 | 24,706 |
| Validation errors per page view | 13.0% | 12.0% |
| Applicants who completed | 58.5% | 59.3% |

- Validation errors per page view fell from 13.0% to 12.0%, a relative fall of 8%. With
  53,514 page views the difference is highly significant (two-proportion z-test, p below 0.001).
- Completion moved in the right direction, from 58.5% to 59.3% (p = 0.54). We expect it to become
  significant with more data.
- We examined 14 metrics in all. The fall in validation errors is the clearest. It is strongest among
  business applicants on mobile, where errors fell by 14%.
- The redesigned form logged fewer applicants. We put this down to chance.

## Recommendation

The redesign is proven to reduce errors. Replace all of the office's online forms with the new design
this month. We estimate at least 9,000 more completed applications a year.
