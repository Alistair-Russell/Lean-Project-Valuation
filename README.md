# Lean Project Valuation

## Description
Lean Project Valuation - a paper investigating the effects of market sentiment at fixed intervals on project valuation.

## Code Structure
1. Define input parameters for the simulation.
    - **N**: the number of simulations to run in parallel
    - **T**: the number of periods in the interval
    - **STEP**: the number of time steps within each period
    - **DRIFT**: the drift term of the cashflow processes
    - **VOL**: the volatility term of the cashflow processes
    - **START**: the initial cashflow value where the simulation starts and the later values are compared back to

2. Define cashflow and cost processes with built in shocks at each period
    - **CashflowProcess**(mu=DRIFT, sigma=VOL)
    - **cost**(t) constant over interval t

3. Plot simulated cashflow processes, development and operations cost processes.
    - cashflows that end more successfully are darker blue

4. Our decision function compares the cashflow at each period against a comparison array - currently just an array of c0s (START), the starting value of each cashflow. This generates a decision value (1,0,-1) at each period.
    - 1: cashflow exceeds the comparison
    - 0: cashflow equals the comparison
    - -1: cashflows is less than the comparison

5. We also generate a history array that holds the cumulative sum of decisions so that we have memory of past cashflow evaluations at each point.

6. Identify early completion exercise, early abandon exercise, success, failure.
    - Completion: Two successive positive shocks - realize cashflows at T=2 and complete project
    - Abandon: Two negative shocks - abandon project at T=2
    - Success: Neither completion/abandonment occurs so we proceed to T=3 and find that the cashflow exceeds c0 - realize cashflows and complete project
    - Failure: Neither completion/abandonment so we proceed to T=3 and find that the cashflow does not exceed c0 - abandon the project

    - TODO: Replace the paths after any exercise so that we realize cashflows rather than continuing simulation. I am working on this so that the plot displays the paths correctly.
    - TODO: We have an issue where our decision-making is based on market sentiment shocks and also cashflow values relative to the initial c0 cashflow. Due to the volatility of the CF process, this can give results where we complete a project at T=2 due to two positive shocks but the cashflows is below c0 due to the volatility jumps... ie. the project shows promising market sentiment, but happens to be less profitable than assumed.

## Tasks
- [ ] Add path replacement on early completion, success
- [ ] Refine decision criteria so that shocks don't conflict with c0 comparison
