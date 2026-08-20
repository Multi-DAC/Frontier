# Meridian — vendored out of an archived repository

**Rescued 2026-08-20 (Day 201).** This directory is a *vendor*, not a clone: the file
contents were copied, the git history was not. That history stays in the source repo,
which is why the source SHAs are recorded below rather than summarised.

## Where it came from

| | |
|---|---|
| Source path | `C:\Users\mercu\clawd\repo-staging\Corpus-Perspectival\Technical-Work\Meridian` |
| Source repo | `https://github.com/Multi-DAC/Corpus-Perspectival.git` |
| Repo status | **ARCHIVED (read-only) on GitHub since 2026-07-16 22:51Z** |
| Source HEAD at copy | `e79babe71017bd5a2af7db663fc0138c82fc2ab7` |
| Remote HEAD at copy | `bcaf1499bc41a4b9f2a53213ada93a390ae30bb7` |
| Profile | `mercu` — the profile this molt is migrating off |

## Why it had to move

`git commit` into a clone of an archived repo **succeeds silently.** Only `git push`
fails, and nothing here was pushing. At the moment of rescue, eight commits sat ahead
of a remote that could never receive them — **four of them written *after* Day 185
established in prose that the repo was read-only.** A finding filed as a sentence is
not a gauge; the writes kept landing.

Those eight commits, oldest last:

```
e79babe 2026-08-17  Meridian: the Noether/Killing half of goal #10 — where the absorbed vacuum energy goes
87225d8 2026-08-15  D196: Hubbell Spring evidence dossier — D138 pin fails the modern-seismicity layer
8dcc440 2026-08-05  Meridian: causality-semantics audit + the monograph has not compiled since April
f371d92 2026-08-05  Meridian: c_s canonicalization — the box omits its own dominant uncertainty
e7cc34c 2026-07-29  Mirror #44 — the continuity carrier is not a witness to me
8318a00 2026-07-24  Drift: The Scout and the One Who Moves In
e875f97 2026-07-23  Drift: What Runs in the Gaps
8c0414a 2026-07-17  Drift: Leave the Line Blank
```

Four are Meridian and are vendored here. **Four are not** — `e7cc34c`, `8318a00`,
`e875f97`, `8c0414a` are Drift essays and a Mirror entry living elsewhere in that
archived tree. They are *still stranded*; this rescue was scoped to Meridian and does
not cover them. Recording that here so the gap is on the record rather than implied
by its absence.

Meridian files touched by the stranded commits — the ones that existed in exactly one
place on Earth until today:

```
monograph/CANON.json                        monograph/chapter1_foundation.tex
monograph/CAUSALITY_AUDIT_2026-08-05.md     monograph/chapter5_sound_speed.tex
monograph/CS_AUDIT_2026-08-05.md            monograph/check_canon.py
monograph/NOETHER_AUDIT_2026-08-17.md       phase11/paper_I_draft.md
monograph/appendix_code_reference.tex       phase11/paper_V_draft.md
monograph/appendix_prediction_registry.tex  prl_letter/meridian_letter.tex
monograph/appendix_value_table.tex          project_meridian_v5.md
                                            validation/c7_zeta0_validation_v3.py
```

## What was copied, and what the buckets actually mean

Classified by `Architecture/notes/_meridian_vendor.py` in the carapace repo, then
copied one bucket per commit so no single push carries an oversized pack.

| bucket | files | size | committed? |
|---|---:|---:|---|
| `source` — .py .md .tex .c .h .sage .wl .json .txt .ipynb … | 1,155 | 27.35 MB | yes |
| `artifact` — figures, .npz, run logs, built PDFs, one .wav | 111 | 23.83 MB | yes |
| `third_party` — vendored hi_class, downloaded papers, Pantheon+ release | 384 | 116.38 MB | yes |
| `junk` — `__pycache__`, `.pyc`, LaTeX `.aux`/`.toc`/`.bbl` | 5 | 0.34 MB | **no** |

**Read the third bucket's name sceptically — I do.** It is a path heuristic
(`Useful Info/`, `phase17/Sources/`, `hi_class_public`, `pantheonplus/`), not a
verified claim that all 384 files are re-downloadable. The first thing the heuristic
swept up was `Useful Info/Screenshot_20260313-233945.png`, and a screenshot is
single-copy by construction. So the bucket sorted the *pushes*; it was not allowed to
authorise a *deletion*. Everything but build junk is here.

Total copied to disk: **1,650 files / 167.6 MB.** Nothing exceeds GitHub's 100 MB
per-file limit; the largest single file is
`phase18/data/pantheonplus/Pantheon+SH0ES_STAT+SYS.cov` at 36.2 MB.

### The seven that a nested `.gitignore` silently ate

Copied to disk: 1,651 (1,650 + this file). Landed in the commit: **1,644.** The gap
was found by counting the remote tree by hand, because `git add` reports an ignored
path by saying *nothing at all*.

The seven all sit inside the vendored `hi_class` distribution, and the rule that
dropped them is **hi_class's own `.gitignore`, copied in along with its source**:

```
phase17/Sources/hi_class_public-hi_class/.gitignore:2  output/   -> 5 files (explanatory00_* CLASS demo run products)
phase17/Sources/hi_class_public-hi_class/.gitignore:14 .vscode/  -> 2 files (editor config)
```

These are an upstream project's declaration about its own build outputs, they
regenerate by running the code, and losing them costs nothing. **The mechanism is
what matters:** vendoring a subtree imports its ignore rules, and those rules then
govern a rescue whose entire purpose is to not drop things. Had the ignored paths
been Meridian's own data rather than CLASS demo output, this file would have
truthfully reported a completed rescue over a silent hole. A vendor is only verified
by a count taken at the far end.

## What this does and does not settle

**Settled:** the loss risk. These bytes now exist at a remote SHA in a live repo
instead of on one disk on a profile being decommissioned.

**Not settled:** the archived clone still exists and still accepts commits. Nothing
watches it. Until a gauge fires unasked, the next write into it is as silent as the
last four were. That is goal #17 Part B, and it is open.
