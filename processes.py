"""Stochastic Processes

This module contains the code for common stochastic processes.
Sourced from: https://github.com/luphord/longstaff_schwartz 

Typical usage examples:
  t = np.linspace(0, 10, 20)
  rnd = RandomState(seed=1234)

  bm = BrownianMotion(mu=0.5, sigma=np.sqrt(3))
  arithmetic_process = bm.simulate(t, 200, rnd)

  gbm = GeometricBrownianMotion(mu, sigma)
  geometric_process = X = gbm.simulate(t, 1000, rnd)

"""

import numpy as np
from scipy.stats.distributions import norm, lognorm, rv_frozen


class ArithmeticBrownianMotion:
    """Arithmetic Brownian Motion (Wiener Process) with optional drift."""

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        self.mu = mu
        self.sigma = sigma

    def simulate(self, t: np.ndarray, n: int, initial_vals: np.ndarray, rnd: np.random.RandomState) -> np.ndarray:
        # assertions for input parameters
        assert t.ndim == 1, "One dimensional time vector required"
        assert t.size > 0, "At least one time point is required"
        dt = np.concatenate((t[0:1], np.diff(t)))
        assert (dt >= 0).all(), "Increasing time vector required"

        # transposed simulation for automatic broadcasting
        W = rnd.normal(size=(n, t.size))
        W_drift = (W * np.sqrt(dt) * self.sigma + self.mu * dt).T
        return initial_vals + np.cumsum(W_drift, axis=0)

    def distribution(self, t: float) -> rv_frozen:
        return norm(self.mu * t, self.sigma * np.sqrt(t))


class GeometricBrownianMotion:
    """Geometric Brownian Motion with optional drift."""

    def __init__(self, mu: float = 0.0, sigma: float = 1.0):
        self.mu = mu
        self.sigma = sigma

    def simulate(self, t: np.ndarray, n: int, initial_vals: np.ndarray, rnd: np.random.RandomState) -> np.ndarray:
        # assertions for input parameters
        assert t.ndim == 1, "One dimensional time vector required"
        assert t.size > 0, "At least one time point is required"
        dt = np.concatenate((t[0:1], np.diff(t)))
        assert (dt >= 0).all(), "Increasing time vector required"

        # transposed simulation for automatic broadcasting
        dW = (rnd.normal(size=(t.size, n)).T * np.sqrt(dt)).T
        W = np.cumsum(dW, axis=0)
        return initial_vals * np.exp(self.sigma * W.T + (self.mu - self.sigma**2 / 2) * t).T

    def distribution(self, t: float) -> rv_frozen:
        mu_t = (self.mu - self.sigma**2 / 2) * t
        sigma_t = self.sigma * np.sqrt(t)
        return lognorm(scale=np.exp(mu_t), s=sigma_t)

