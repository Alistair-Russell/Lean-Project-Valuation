"""Lean Project Valuation Model - a three-stage cashflow model.

This simulates an expected net cashflow and development cost process with
pivot decisions for the entrepreneur and early exercise decisions for the
investor.

Usage:

  cashflow = BrownianMotion(...)
  cost = BrownianMotion(...)
  project = LeanProjectValuation(cashflow, 1.0, cost, 1.0, 1234, 25)

"""

import numpy as np
import pandas as pd
from numpy.random import RandomState, Generator
from numpy.polynomial import Polynomial
from matplotlib import pyplot as plt
from matplotlib import patches as ptc
from ipywidgets import interact, IntSlider
from itertools import zip_longest
from scipy.stats.distributions import lognorm, rv_frozen
from pathlib import Path
from typing import Dict, Tuple, Sequence
from processes import GeometricBrownianMotion


# Helper Functions
def pv_growing_annuity(payoffs: np.ndarray, g: float, r: float, periods: int, start: int = 1):
    """Valuation of growing annuity, payments starting at a specified period"""
    # Create an array of periods, discount factors, and growth factors
    period_arr = np.arange(start, start + periods)
    discount_factors = 1 / (1 + r) ** period_arr
    growth_factors = (1 + g) ** (period_arr - 1)
    # Calculate the present value of each payment
    pv_payments = payoffs[:, np.newaxis] * growth_factors * discount_factors
    # Sum the present values to get the NPV for each payment
    values = np.nansum(pv_payments, axis=1)
    return values.reshape(payoffs.shape)


class LeanProjectValuation:
    """Lean project valuation"""

    def __init__(self,
                 cashflow_mu: float,
                 cashflow_sigma: float,
                 cashflow_initial_vals: np.ndarray,
                 cost_initial_vals: np.ndarray,
                 risk_free_rate: float,
                 rand_seed: int,
                 no_sims: int = 20):
        """Initializes the project with a set of cost and cash flow process
        """
        self.cashflow = GeometricBrownianMotion(cashflow_mu, cashflow_sigma)
        self.cost = GeometricBrownianMotion(mu=0.0, sigma=0.0)
        self.nobs = no_sims
        self.seed = rand_seed

        # initial values for cashflows, costs, threshold
        self.cf_mu = cashflow_mu
        self.rfr = risk_free_rate
        self.cf_inits = cashflow_initial_vals
        self.co_inits = cost_initial_vals
        self.threshold = cashflow_initial_vals

        # decision periods
        self.entrepreneur_decision_periods = (1,)
        self.investor_decision_periods = (2,)

        # exercise time and value series
        self.completion_times, self.completion_vals = {}, {}
        self.abandon_times, self.abandon_vals = {}, {}
        self.pivot_times, self.pivot_vals = {}, {}

        # path and decision results
        self.paths = []
        self.unaltered_paths = []
        self.exercise_decisions = []
        self.pivot_decisions = {}

    def _generate_pivot_shocks(self, period: int, stage_values: np.ndarray) -> np.ndarray:
        """Generates an array of shocks for a pivot stage given a threshold
        """
        rnd = RandomState(self.seed)
        cols = stage_values.shape[0]
        shocks = np.zeros(cols)
        
        # only apply shocks to values below the pivot threshold
        draws = rnd.uniform(0, 2, size=cols)
        draws = np.ones(cols)  # TODO: temporarily remove shocks
        mask = np.ma.masked_where(stage_values > self.threshold, stage_values)
        diff_mask = (mask * draws) - stage_values
        # create shocks by filling the array, store it
        shocks = diff_mask.filled(0.0)
        self.pivot_vals[period] = shocks

        # initialize decision, exercise values, and continuation value arrays
        continuation_vals = stage_values + shocks

        # update decisions with pivots and continuations
        decision_vals = np.zeros(stage_values.shape).astype(int)
        decision_vals[stage_values > self.threshold] = 1
        
        # store the pivot decisions
        self.pivot_decisions[period] = [
                (dec, val, cont)
                for dec, val, cont
                in zip(decision_vals, stage_values, continuation_vals)
        ]
        return shocks

    def _generate_optimal_exercise(self, t: np.ndarray):
        """Determine optimal exercise decisions based on stored paths and their
        resulting valuations less development costs
        """
        # iterate over period indices, npv each project path to determine current valuation
        for p in self.investor_decision_periods:
            idx = np.where(t == p)[0][0]
            cashflows = self.paths[idx,:]
            remaining_cashflows = self.paths[idx+1:,:]
            # TODO: build a function that will just take the forward paths as input to npv them
            # TODO: that way we can simply simulate further stages and then pv the path
            path_valuation = pv_growing_annuity(cashflows,
                                                self.cf_mu, self.rfr, 3, start=2)
            is_abandoned = path_valuation <= self.co_inits

            # drop abandoned paths completely
            self.paths[idx+1:,is_abandoned] = np.nan

            decisions = np.ones(cashflows.shape).astype(int)
            decisions[is_abandoned] = -1

            continues = cashflows.copy()
            continues[is_abandoned] = 0
        
            # store the pivot decisions
            self.exercise_decisions = [
                (p, d, cf, c)
                for d, cf, c
                in zip(decisions, cashflows, continues)
            ]

    def generate_paths(self, t: np.ndarray, periods: int) -> np.ndarray:
        """Simulates cashflow paths for a single period, returns unaltered
        simulated paths and invokes methods to optimally exercise.
        """
        # [0,1] indices from the time array
        idx_start = np.where(t == 0)[0][0]
        idx_end = np.where(t == 1)[0][0]

        arrays = []
        init_vals = self.cf_inits
        for i in range(1, periods+1):
            # use a new seed for each interval
            rnd = RandomState(self.seed+i)
            subinterval = t[idx_start:idx_end+1]
            cf_sim = self.cashflow.simulate(subinterval, self.nobs, init_vals, rnd)

            # pivot decision
            end_vals = cf_sim[-1,:]
            if i in self.entrepreneur_decision_periods:
                pivot_shocks = self._generate_pivot_shocks(i, end_vals)
                end_vals += pivot_shocks
            
            # replace final cashflow values for use in next stage simulation
            init_vals = end_vals
            if i < periods:
                arrays.append(cf_sim[:-1,:])
            else:
                arrays.append(cf_sim)

        # store paths
        simulated_paths = np.vstack(arrays)
        self.paths = simulated_paths
        self.unaltered_paths = np.copy(simulated_paths)

        # generate exercise decisions to alter existing paths
        self._generate_optimal_exercise(t)

        # return unaltered paths rather than exercised paths
        return self.unaltered_paths

    def valuation(self, time_array, stages, unaltered: bool=False):
        """Returns npv of the project, averaging all paths less their costs
        """
        _ = self.generate_paths(time_array, stages)
        if unaltered:
            paths = self.unaltered_paths
        else:
            paths = self.paths

        payoffs = pv_growing_annuity(paths[-1,:], self.cf_mu, self.rfr, 3)
        payoffs = payoffs / (1+self.rfr)**(3)

        # TODO: also needs pathwise valuation function
        costs = np.full_like(payoffs, self.co_inits)
        costs[payoffs != 0] += self.co_inits / (1+self.rfr)**(2)
        return np.average(payoffs - costs)

