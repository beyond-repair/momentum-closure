"""Multidimensional convergence tensor.

This module makes the package importable. It records declared tolerances
*before* comparison and never certifies a physical residual by itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class AxisStatus(str, Enum):
    DECLARED = "DECLARED"
    MEASURED = "MEASURED"
    PASSED = "PASSED"
    FAILED = "FAILED"
    MISSING = "MISSING"
    NOT_CERTIFIED = "NOT_CERTIFIED"


@dataclass(frozen=True)
class ConvergenceAxis:
    name: str
    epsilon: float
    floor: float = 0.0
    declared_tolerance: float | None = None


@dataclass
class ConvergencePoint:
    axis: str
    value_coarse: float
    value_fine: float
    floor: float = 0.0

    @property
    def epsilon(self) -> float:
        denom = max(abs(self.value_fine), abs(self.value_coarse), self.floor, 1e-30)
        return abs(self.value_fine - self.value_coarse) / denom


@dataclass
class ConvergenceTensor:
    """C = [eps_mesh, eps_surface, eps_box, eps_radiation, eps_symmetry, eps_timestep]."""

    tolerances: Dict[str, float] = field(default_factory=dict)
    points: Dict[str, ConvergencePoint] = field(default_factory=dict)

    DEFAULT_AXES = ("mesh", "surface", "box", "radiation", "symmetry", "timestep")

    def declare(self, axis: str, tolerance: float) -> None:
        if tolerance <= 0:
            raise ValueError("tolerances must be positive and declared before measurement")
        self.tolerances[axis] = float(tolerance)

    def measure(self, axis: str, value_coarse: float, value_fine: float, floor: float = 0.0) -> float:
        if axis not in self.tolerances:
            raise RuntimeError(f"tolerance for axis '{axis}' was not declared before measurement")
        pt = ConvergencePoint(axis, float(value_coarse), float(value_fine), float(floor))
        self.points[axis] = pt
        return pt.epsilon

    def residual_closure(self, F_near, F_far, Pdot_matter, P_scale: float) -> float:
        import math
        s = [0.0, 0.0, 0.0]
        for vec in (F_near, F_far, Pdot_matter):
            for i, x in enumerate(vec):
                s[i] += float(x)
        num = math.sqrt(sum(x * x for x in s))
        return num / max(abs(P_scale), 1e-30)

    def status(self, axis: str) -> AxisStatus:
        if axis not in self.tolerances:
            return AxisStatus.MISSING
        if axis not in self.points:
            return AxisStatus.DECLARED
        if self.points[axis].epsilon <= self.tolerances[axis]:
            return AxisStatus.PASSED
        return AxisStatus.FAILED

    def as_vector(self) -> Dict[str, float | None]:
        out = {}
        for name in self.DEFAULT_AXES:
            out[name] = self.points[name].epsilon if name in self.points else None
        return out


@dataclass
class ConvergenceCertificate:
    tensor: ConvergenceTensor
    required: tuple[str, ...] = ("mesh", "surface")

    def certified(self) -> bool:
        return all(self.tensor.status(ax) == AxisStatus.PASSED for ax in self.required)

    def reason(self) -> str:
        if self.certified():
            return "CERTIFIED_NUMERICAL_CONVERGENCE_ONLY"
        missing = [ax for ax in self.required if self.tensor.status(ax) != AxisStatus.PASSED]
        return "NOT_CERTIFIED:" + ",".join(missing)
