"""ai-fixed-points: LLM-driven code improvement toward a fixed point.

The package provides a configurable agent (:class:`BaseAgent`), a concrete
code-improving agent (:class:`CodeImprover`), and an iterative improvement loop
(:func:`ai_fixed_points.improve_loop.multi_improve`).
"""

from importlib.metadata import PackageNotFoundError, version

from .base import BaseAgent
from .config import Config, Profile, load_config
from .improver import CodeImprover

try:
    __version__ = version("ai-fixed-points")
except PackageNotFoundError:  # pragma: no cover - only when not installed
    __version__ = "0.1.0"

__all__ = [
    "__version__",
    "BaseAgent",
    "CodeImprover",
    "Config",
    "Profile",
    "load_config",
]
