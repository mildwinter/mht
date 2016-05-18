"""Kalman Filter implementation for MHT target."""

from math import log as ln
from math import sqrt
from math import pi
from numpy.linalg import det


def from_report(r):
    """Init KFilter from report."""
    return KFilter()


class KFilter:
    """Kalman-filter target."""

    def __init__(self, model, x0, P0):
        """Init."""
        self.model = model
        self.x = x0
        self.P = P0

    def __repr__(self):
        """Return string representation of measurement."""
        return "T({}, P)".format(self.x)

    def predict(self, dT):
        """Perform motion prediction."""
        self.x, self.P = self.model(self.x, self.P, dT)

    def correct(self, m):
        """Perform correction (measurement) update."""
        zhat, H = m.mfn(self.x)
        dz = m.z - zhat
        S = H * self.P * H.T + m.R
        K = self.P * H.T * S.I
        self.x += K * dz
        self.P -= K * H * self.P

        # FIXME: lambda_ex / PD according to Bar-Shalom 2007
        score = dz.T * S.I * dz / 2.0 + ln(2 * pi * sqrt(det(S)))
        return float(score)

    def score(self, m):
        """Get the score of assigning a measurement to the filter."""
        zhat, H = m.mfn(self.x)
        dz = m.z - zhat
        S = H * self.P * H.T + m.R
        # FIXME: lambda_ex / PD according to Bar-Shalom 2007
        score = dz.T * S.I * dz / 2.0 + ln(2 * pi * sqrt(det(S)))
        return float(score)