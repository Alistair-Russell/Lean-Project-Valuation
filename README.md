# Lean Project Valuation

## Description

A real options valuation of multi-period R&D invesment with early entrepreneur pivot opportunities and early investor abandonment opportunities. The goal is to create a simple  model that describes the basic behaviour of this dynamic while providing a foundation for further analyses of more complex questions such as ownership division.

## Updates

Three Stage Model
- three period model with two distinct parties
- the entrepreneurs decides whether to pivot the project at T=1
- the investor chooses whether to abandon the project or continue with next stage investment at T=2
- a successful project pays out a three period growing annuity based on the expected valuation of the net cashflows as well as the development cost it took to get there (2*K)
- an abandoned project has negative npv which is simply the single stage development cost before abandonment

## Key Ideas

- We use Real Options to value the abandonment choice and the choice to pivot as financial options.
- For highly volatile project, this results in a higher project valuation than if we did a naive net present value calculation.
- Furthermore, the estimated cashflow shock given by the pivot induces additional volatility in the cashflows. The "effective volatility" is greater than the volatility in the cashflow processes, resulting in a higher valuation of the investor's option to abandon the project.

# Context and References

Real Options in R&D, investor behaviour
- (Schwartz, 2004)

Innovation project literature, pivot/persevere methodology, entrepreneur behaviour
- Lean Startup (Ries, 2011)

Pivot Behaviour
- We start by assuming that pivot mechanics are exogenous in order to simplify the problem
- However with a measure of effective volatility for the project as a whole, and given the pivot shock process induced on the expected cashflows (eg. scaled by a uniform distribution draw), we will be able to determine the optimal pivot strategy for the entrepreneur.

## Authors
Alistair Russell, Eduardo Schwartz
