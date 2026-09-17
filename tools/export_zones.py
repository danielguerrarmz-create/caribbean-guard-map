"""RETIRED 2026-09-17. Superseded by tools/osm_coastline.py. IT REFUSES TO RUN.

WHAT IT DID. It rebuilt web/data/zones-geometry.json from tools/coastline.json,
the contour that tools/trace_coastline.py pulled out of the satellite mosaic's
water mask. The simplify / Chaikin / decimate pipeline in it was sound, and the
parts that still apply are carried over into the replacement.

WHY IT IS GONE. Its input is wrong on this coast, and no amount of smoothing
fixes a wrong input. The water mask thresholds on brightness (`v < 60` is sea),
and shallow water over live coral is BRIGHT, so the mask read every reef as land
and the contour walked around each reef patch instead of along the beach:

    zone           traced length      true coast      excess
    playa-negra         1618 m          1625 m          -0%
    salsa-brava         2303 m          1294 m         +78%
    cocles              4224 m          3202 m         +32%
    chiquita            4439 m          3055 m         +45%
    punta-uva           3119 m          2830 m         +10%

Playa Negra is the one zone with no reef near the shore and it is the one zone
that came out right, which is what turns this from a guess into a diagnosis.

WHY IT EXITS INSTEAD OF SAYING SO IN A COMMENT. Running it would overwrite the
corrected geometry with the reef trace again, in place, with no error and a
success message at the end. Something very close to that has already happened on
this repo: commit 7d6baa1 is titled "Stop redraw_zones.py reverting the coastline
fix, and label the stale data". A warning in a docstring does not survive
somebody skimming tools/ for the script whose name matches the file they want to
rebuild, and the cost of being wrong here is a hazard line in the wrong place on
a published safety map.

THE SOURCE IS NOT LOST. It is in git at 6be0f66:tools/export_zones.py, with its
own reasoning about why simplify has to run before Chaikin and why the zone ids
are read out of index.html rather than constructed. Both arguments survive in
tools/osm_coastline.py, which is where to read them now.

To rebuild the geometry:  python tools/osm_coastline.py
"""
import sys

sys.exit("\n".join([
    "tools/export_zones.py is RETIRED and refuses to run.",
    "",
    "It rebuilds web/data/zones-geometry.json from the satellite water-mask",
    "trace, which follows the reef rather than the coast. Use instead:",
    "",
    "    python tools/osm_coastline.py",
    "",
    "See the docstring at the top of this file, git 6be0f66 for the original",
    "source, and docs/handoffs/2026-09-17-linework-and-panels.md.",
]))
