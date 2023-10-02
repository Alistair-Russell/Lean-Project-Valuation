# Lean Project Valuation

## Description
Lean Project Valuation - valuation of multi-period R&D invesment with early entrepreneur pivot opportunities and early investor abandonment opportunities.

## Updates

[Milestone: Paper 1 - Lean Project Valuation](https://gitlab.com/sfu3241618/research/lean-project-valuation/-/milestones/1#tab-issues)

Three Stage Model
- three period model with two distinct parties
- the entrepreneurs decides whether to pivot the project at T=1
- the investor chooses whether to abandon the project or continue with next stage investment at T=2

Key ideas
- a successful project pays out a three period growing annuity based on the expected valuation of the net cashflows as well as the development cost it took to get there (2*K)
- an abandoned project has negative npv which is simply the single stage development cost before abandonment

# Context

Real Options in R&D, investor behaviour
- (Schwartz, 2004)

Innovation project literature, pivot/persevere methodology, entrepreneur behaviour
- Lean Startup (Ries, 2011)

Pivot Behaviour
- Are pivot decisions exogenous or endogenous? we theorized that they could be either.
- Endog would be interesting because you could then determine an optimal criteria for electing to pivot, and probably solve analytically. 
    - Endog: pivots are positive only (you identify a better market/value prop that you previously weren't aware of), you know the distribution and you decide to take them under certain conditions of project valuation vs. next stage costs. This criteria is still unclear because as per R&D1 -ve valuation of the project would lead you to not undertake investment, and positive valuation would lead you to invest ending the project at stage 1.
- Exog might be simpler, but would necessitate simulation.
    - Exog: pivots can be -ve or +ve and those decisions are thrust upon you in a scenario (eg. venture capital, where positive net cashflow is not sufficient for investors, they want to 10x return to return the fund) so only extremely positive cashflows are deemed successful and you end up with a threshold band for pivoting in the event of moderate success


## Implementation
1. Define input parameters for the simulation.
    - **N**: the number of simulations to run in parallel
    - **T**: the number of periods in the interval
    - **STEP**: the number of time steps within each period
    - **DRIFT**: the drift term of the cashflow processes
    - **VOL**: the volatility term of the cashflow processes
    - **START**: the initial cashflow value where the simulation starts and the later values are compared back to

2. Add parameters as input to the LeanProjectValuation class that simulates net cashflows and determines optimal exercise.

3. Plot simulated net cashflow processes and dev cost processes.