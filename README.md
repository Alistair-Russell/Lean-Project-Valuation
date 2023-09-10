# Lean Project Valuation

## Description
Lean Project Valuation - modelling valuation of multi-period R&D invesment with early pivot/abandon/completion options.


## Updates
### 09/08/23
R&D1
- Reviewed R&D1 to understand how that paper achieved valuation decisions while considering marginal cost
- You need to understand what the time 0 value of the project is at time 1 by npv-ing the cost to get there (integral of cost to completion) and the expected forward net cashflows
- We should use this model as a starting point with deterministic cost to completion that is driven down each period
    - Periods are still deterministic as a result

Pivot Behaviour
- Are pivot decisions exogenous or endogenous? we theorized that they could be either.
- Endog would be interesting because you could then determine an optimal criteria for electing to pivot, and probably solve analytically. Exog might be simpler, but would necessitate simulation.
    - Endog: pivots are positive only (you identify a better market/value prop that you previously weren't aware of), you know the distribution and you decide to take them under certain conditions of project valuation vs. next stage costs. This criteria is still unclear because as per R&D1 -ve valuation of the project would lead you to not undertake investment, and positive valuation would lead you to invest ending the project at stage 1.
    - Exog: pivots can be -ve or +ve and those decisions are thrust upon you in a scenario (eg. venture capital, where positive net cashflow is not sufficient for investors, they want to 10x return to return the fund) so only extremely positive cashflows are deemed successful and you end up with a threshold band for pivoting in the event of moderate success


## Implementation
1. Define input parameters for the simulation.
    - **N**: the number of simulations to run in parallel
    - **T**: the number of periods in the interval
    - **STEP**: the number of time steps within each period
    - **DRIFT**: the drift term of the cashflow processes
    - **VOL**: the volatility term of the cashflow processes
    - **START**: the initial cashflow value where the simulation starts and the later values are compared back to

2. Define net cashflow and cost processes with built in shocks at each period
    - **CashflowProcess**(mu=DRIFT, sigma=VOL)
    - **cost**(t) constant over interval t

3. Plot simulated net cashflow processes and dev cost processes.
