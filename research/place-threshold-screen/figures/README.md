# ⚠ THESE PLATES ARE NOT THE CANDIDATE LIST — see `../figures_final/`

*Added Day 197, 2026-08-16.*

The ten PNGs in this directory were built by `code/site_figure.py` reading
`work/site_rank.json` — the **partial** screen of report 07, before the national run
finished. They are:

```
01 Madison · 02 Centennial · 03 Teton · 04 Sawatch · 05 Southern Sangre de Cristo
06 Mount Rose · 07 Helena Valley · 08 East Pintwater Range · 09 Wasatch
10 Northern Sangre de Cristo
```

The list the three lore experiments actually ran against is `data/top10_frozen_100km.json`:

```
01 Madison · 02 Round Valley · 03 Little Valley · 04 Helena valley · 05 Red Rock
06 Sand Springs Range · 07 Mosquito · 08 Sandia · 09 Bear River fz · 10 Teton
```

**Eight of ten differ.** Only Madison and Helena valley appear in both, and Teton moves from
#3 to #10. So these files are pictures of sites that carry no lore evidence, under filenames
(`01_`…`10_`) that read like the candidate ranking. Nothing pointed that out; the filenames
did the lying on their own.

They are kept rather than deleted because they are the honest output of report 07 and
deleting them would erase a stage of the work. **Current plates: `../figures_final/`**, built
by `code/dossier_figures.py`, which takes its site list from the frozen file and asserts each
rendered manifest name against it.

## Two further defects these plates carry, fixed only in `figures_final/`

1. **Panel D is a 30-day window captioned "all years".** The USGS FDSN event service defaults
   `starttime` to the last 30 days when omitted — no warning, small honest-looking number.
   The Sandia panel printed *"ZERO catalogued events (a real, reportable result)"*; with
   `starttime=1900-01-01` it is **92 events, M1.6–4.7**.
2. **Panel B reads `at trace: ?`** wherever the lithology row came from a stage that did not
   record `at_point_term` — which is 8 of the frozen 10. `figures_final` summarises the
   per-vertex `pts` instead and names the quantity it is actually showing.
