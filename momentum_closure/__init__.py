"""Momentum Closure — physics-integrity and certification framework."""

__version__ = "1.7.0-dev"

from .convergence.tensor import (
    ConvergenceAxis,
    ConvergencePoint,
    ConvergenceTensor,
    ConvergenceCertificate,
    AxisStatus,
)

__all__ = [
    "ConvergenceAxis",
    "ConvergencePoint",
    "ConvergenceTensor",
    "ConvergenceCertificate",
    "AxisStatus",
    "__version__",
]
