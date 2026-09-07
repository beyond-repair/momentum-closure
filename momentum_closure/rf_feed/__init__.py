"""P0-C.1 — single-port SMA/coax RF feed into explicit Faraday boundary.

Classical Maxwell baseline only.  Ware parameters are excluded from
feed topology, port definition, and enclosure boundary conditions.
"""

from .params import FeedParams, FaradayEnclosure
from .topology import FeedTopology, build_sma_coax_feed
from .manifest import emit_feed_manifest, run_p0_c1

__all__ = [
    "FeedParams",
    "FaradayEnclosure",
    "FeedTopology",
    "build_sma_coax_feed",
    "emit_feed_manifest",
    "run_p0_c1",
]
