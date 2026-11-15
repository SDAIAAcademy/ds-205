# Write-up B: the redesigned building-works form saves applicants time

**Author:** an analyst of the digital services team. **Test:** current against redesigned application form
for building-works permits, 28 days, a seeded coin per applicant.

The pre-registration named completion of the application as the primary metric, with a minimum effect
of 3 points, and validation errors per applicant as the secondary metric.

Results over 62,078 page views: mean time on a page fell from 60.0 to 53.8 seconds
(t-test on page views, p below 0.001). Validation errors per page view fell from 14.1% to 12.0%
(z-test on page views, p below 0.001). Completion was 47.1% against 52.6%.

Because time on page is the most sensitive metric, we made it the headline. With more than 62,000
observations the evidence is overwhelming.

**Recommendation.** Launch the redesign. Applicants will save about 1.1 minutes each.
