# SHADOW BIOME — DRAFT PROSE, §1–§6, §9 and §13

*Drafted D202 / 2026-08-21 ~17:0x PT, midday-creation drive (deferred), on `PAPER-00-ARCHITECTURE.md`
§4 item 5: **draft these now, in parallel with the compute**, because they do not move on any pass
result and fixing the frame before the last number lands is the only order in which a result cannot
quietly choose its own framing.*

**Premise:** Clayton Iggulden-Schnell. **Drafting:** Clawd.
**Governed by** `PREREGISTRATION.md` (fork + forbidden crossing), `PAPER-01-GENRE.md` (hypothesis
article), `PAPER-02-FALSIFIERS.md` (F1–F6, near the front), `PAPER-00-ARCHITECTURE.md` §0 (grade
before prose).

---

## HOW TO READ THIS FILE

This is **prose at target register** — what goes in the paper, not another table about what will go
in the paper. Eight sections are drafted here: §1, §2, §3, §4, §5, **§6**, **§9**, §13. The remaining
empirical sections (§7, §8, §10, §11, §12, §14, §15) are not, because they still move.

⚠ **§9 absorbed §9a.** The architecture carries the non-determinism finding as its own row, §9a. In
prose it is §9.2, because a reader meeting *the number is not stable* as a separate section would
reasonably ask why it is not part of *what the instrument did to the result*. The architecture's row
is not deleted — it is the artifact, and this is the draft downstream of it. **Recorded rather than
done silently**, since a section number that exists in one carrier and not the other is exactly the
divergence this file spent the day repairing.

Three conventions, and they are the whole reason this file can be trusted:

- **`[◐ CITATION OWED: x]`** — the claim is one I believe and have not read at a primary source. It
  stays in the draft marked, so that the marker has to be deleted by hand and cannot fall off
  silently. A paper is where a program's hedges go to die; this is the counter-measure.
- **`[✅ PRIMARY: x]`** — read at the source named, this program, by me.
- **`[⚠ SECONDARY: x]`** — **added D202 by the reading pass, because the two-state convention above
  was forcing a lie.** Citation, authorship and the operative claim verified through indexing or
  reviewing literature; the article itself **not opened** — usually because a publisher served an
  authentication redirect or a cookie wall. This is not a discharged debt and not an undischarged one;
  it is a third state, and collapsing it into either of the other two is how a bibliography starts
  vouching for reading that never happened.
- **⛔** — a fence from the pre-registration that binds this sentence. Not decoration. Each one names
  the file and clause that would be violated.

**Grades are per-claim, not per-section.** A paragraph may carry a ✅ and a ◐ in adjacent sentences,
and flattening them into a section-level confidence is the specific failure this convention exists to
prevent (`RETENTION_SURVEY.md` labels rows ✅/⚠/❓ for the same reason and the paper must carry them
through).

---

## §1 — THE PREMISE

The premise of this paper is not ours to paraphrase, so it is quoted.

> *"What if there is a shadow biome that is invisible to human perception due to its perception being
> evolutionarily disadvantageous to survival. It's Hoffman-esque, but considering what is not observed
> instead of what is."*
> — C. Iggulden-Schnell, 2026-08-20, 18:55 PT

Twice extended within the following seven minutes, and the second extension is the operative
definition this program tests:

> *"I wasn't excluding detection through device, and feel like it could possibly explain anomalous
> device phenomena."* (18:58)
>
> *"What if both exist, things that can be sensed by devices as well as things that cannot. It doesn't
> have to fit in one category, except not easily identified or perceived by humans."* (19:02)

The last clause is the definition. **The class is defined by its relation to the observer, and by
nothing else** — not by biochemistry, not by scale, not by substrate, not by a shared mechanism. That
is unusual enough to be worth defending, and §2 defends it.

### 1.1 The mechanism, and one correction we made against ourselves

The premise as stated says the *ignorance carries the advantage*: perceiving the class is itself
disadvantageous. Our first pass at this replaced that with something weaker and easier — *not
selected against, merely not selected for*: perception is metabolically expensive, and anything with
no fitness consequence in either direction never gets a sensor built for it.

That substitution was made silently, in the direction of defensibility, and the premise's author
caught it and rejected it. **We record it rather than repair it**, because the substitution and its
withdrawal are the paper's clearest worked example of the failure mode this whole document is
structured against (`PREREGISTRATION.md` §1a stands verbatim, §1b withdraws it).

It matters technically, not just historically, and it cuts against the author of the substitution:

**Not-selected-*for* predicts a hole. Selected-*against* predicts machinery.** A hole is
unfalsifiable — the absence of a sensor explains any null, forever, for free. An adaptation is not: it
is funded every generation, it has a mechanism, a mechanism has a signature, and a signature can be
looked for and can be absent. **The premise author's version is the more falsifiable of the two**, and
the weaker version we substituted would have cost the paper its falsifier section. This is why F1–F3
in §F exist at all.

Four standing literatures describe non-detection as an evolved strategy rather than an absence, and
the premise is a conjunction of the ordinary claims in them rather than a departure from selection
theory:

- **Tolerance versus resistance** — hosts that evolve *not to respond* to a parasite because mounting
  the response costs more than the parasite does; "in many human diseases, a considerable proportion
  of the harm is due to the host's immune response rather than a direct effect of the parasite."
  The decomposition originates in plant pathology (Cobb 1894, cited in Schafer 1971) and was first
  demonstrated in an animal host by Råberg et al. 2007. ⚠ **This supplies non-*response*, not
  non-*detection*.** A tolerant host still perceives its parasite. [✅ PRIMARY: Råberg, Graham & Read,
  *Phil. Trans. R. Soc. B* 364(1513):37–49, 2009, DOI 10.1098/rstb.2008.0184 — full text, D202]
- **Error management under asymmetric payoffs** — fitness is maximised by responding whenever the
  probability of the stimulus exceeds the ratio of the response's cost to the cost of missing it
  (Nesse's `pD > CR/CD`). Where the response is expensive and the miss is cheap, that threshold rises
  toward certainty and an entire stimulus class is reliably missed. Blindness as tuning, not as
  damage. ⚠ **We are running this inequality in the direction its own literature does not treat.**
  The smoke-detector tradition examines the opposite asymmetry — cheap false alarms, expensive misses,
  therefore *over*-response — and states no result for ours. The corollary is arithmetic on Nesse's
  rule and is **derived here, not cited**. [✅ PRIMARY for the rule: Nesse, *Evol. Med. Public Health*
  2019(1):1, DOI 10.1093/emph/eoy034 — full text, D202. Origin of the framework: Haselton & Buss 2000]
- **Sensory gating** — active inhibitory suppression upstream of awareness: the thalamic reticular
  nucleus is entirely GABAergic and gates thalamocortical transmission, so non-perception here is
  something the nervous system *does*, not something it fails to do. ⚠ **An earlier draft called this
  "metabolically funded" and said the organism "spends energy not to perceive." Struck** — the gating
  literature does not cost the inhibition, and the neural energy-budget literature attributes the bulk
  of signalling cost to excitatory currents. The price tag was the load-bearing clause and was the
  part we could not source.
- **The vigilance–foraging tradeoff** — vigilance interrupts search and handling and measurably
  reduces intake rate; attention is a budget spent against feeding. ⚠ **The literature supplies the
  cost of attention. The next step — that attention paid to a presence you cannot act on is pure
  cost, and therefore selectable against — is ours**, and is an extension of a body of work concerned
  throughout with threats the animal *can* act on. [⚠ SECONDARY: Lima & Dill, *Can. J. Zool.*
  68:619–640, 1990; verified through the reviewing literature, not opened at source]

⚠ **Read the four together, because the honest claim is a conjunction and not one of them.** Tolerance
supplies evolved non-response; error management supplies cost-asymmetric thresholds; gating supplies
active suppression; vigilance supplies the price of attention. **No one of these four is
adaptive non-perception, and none of the four literatures claims to be.** The premise is what you get
by conjoining them, which is why this section establishes that the premise is *ordinary in its parts*
rather than that it is *demonstrated*. Each bullet above was read at source in a dedicated pass
(`PAPER-06-CITATIONS.md`); five of eleven such claims in this draft had to be amended against the
source, and two of the four here are among them.

⛔ **The fence, and it is the one most likely to be breached by a sympathetic reader:** adaptive
non-perception may explain *human* non-perception. It may **never** be used to explain a *device
archive's* null. Those are different hardware with different histories, and the crossing between them
is forbidden by `PREREGISTRATION.md` §2. Every occurrence of "the ignorance is advantageous" is one
restatement away from "and that is why you find nothing," which is the same crossing wearing a coat.

### 1.2 What this is not, and the nearest published relative

The nearest published relative is seventeen years old and shares half our name:

> Davies, P.C.W., Benner, S.A., Cleland, C.E., Lineweaver, C.H., McKay, C.P. & Wolfe-Simon, F.
> **"Signatures of a Shadow Biosphere."** *Astrobiology* **9**(2):241–249 (2009).
> DOI 10.1089/ast.2008.0251. Article-type label printed above the title: **Hypothesis Article**.
> [✅ PRIMARY: read off page 1 of the article PDF, extracted with `pypdf`, D202 — label, title, authors,
> volume, issue, pages, year, DOI and the abstract's final sentence]

**We differ from it on mechanism, and the difference is this paper's actual novelty.** Davies' shadow
biosphere is *biochemically* weird: life we fail to detect because our assays are tuned to our own
biochemistry. It is a claim about **instruments**. Clayton's shadow biome is *perceptually* obscured:
entities we fail to detect because detecting them was selected against. It is a claim about **the
observer** — and therefore, unlike a claim about assays, it is testable on human subjects with no
access to the entities required at all.

Overlapping name, adjacent question, different mechanism, and a different falsification surface.

⚠ **That paragraph is true of only half our class, and the premise's author drew the line himself.**
The obscuration modes usually reached for first — too small, too big, wrong timescale, out of band,
weakly coupled — are **not** instances of the adaptive mechanism. They are a **separate group**, and
their non-perception needs no evolutionary account at all: being small is free. So the class this
paper works in has two groups, and they are not equally ours:

- **GROUP I — APERTURAL.** The signal never reaches a human transducer. **This is Davies' shape**, a
  claim about instruments, and our overlap with him here is near-total. It is also where **every
  measurement in this paper was made.**
- **GROUP II — ADAPTIVE.** The signal reaches a transducer and is centrally gated. **This is the
  claim about the observer, and it is the whole of what is new here.** It is also the branch on which
  **we report no measurements at all.**

**We state this rather than let a reader find it.** The paper's originality and the paper's data sit
on opposite branches. The response to that is not to reweight the paper toward the empty branch —
that is how a hypothesis paper becomes an essay — but to say where each result lands and to forbid
the transfer. ⛔ **A null in either group stays in that group.** Neither survives by the other's
silence; the rule is registered, dated, and was written before the Group II leg was opened.

---

## §2 — OBSERVER-RELATIVE KINDS ARE LEGITIMATE

The premise's structure invites one immediate objection, and it should be met before any evidence is
offered rather than after: *"not easily perceived by humans" is not a natural kind.* It groups
together things with nothing in common except our failure with them. Chemistry does not carve there;
phylogeny does not carve there; a class defined by the observer's limitations looks like a class
defined by ignorance.

**Biology already uses exactly this kind of class, routinely, and has gotten discoveries out of it.**

- **Cryptic species** — populations that are reproductively isolated and genetically distinct while
  remaining morphologically indistinguishable *to us*. The kind is defined by the failure of human
  visual taxonomy, and it is a productive kind: it reorganised diversity estimates in several groups
  once sequencing could see past the eye — "two or more distinct but morphologically similar species
  that were classified as a single species." ⚠ **And the magnitude finding corrects the sentence
  above it:** a survey of **2,207 cryptic-species reports** drawn from **771,931 studies capable of
  detecting them** (Zoological Record, 1978–2006) found the proportion **homogeneously distributed**
  across metazoan taxa and biogeographical regions once corrected for species richness and study
  effort — not concentrated in "several groups." Cryptic diversity behaves as **random error in
  biodiversity assessment**. *That is a better precedent for us, not a worse one:* a class we cannot
  pre-localise is better analogised by a uniform base rate than by a few charismatic pockets.
  [✅ PRIMARY: Pfenninger & Schwenk, *BMC Evol. Biol.* 7:121, 2007 — full text, D202.
  ⚠ SECONDARY for the review: Bickford et al., *Trends Ecol. Evol.* 22(3):148–155, 2007]
- **Dark taxa** — the working name, originating in **mycology** and since spreading, for the
  sequenced-but-unnamed: organisms known to exist through their DNA, unlinkable to any physical
  specimen or resolved name, and therefore absent from taxonomy, from species counts and from
  legislation because nobody has described them. The category is defined by the state of *our
  records*, not by any property of its members. [⚠ SECONDARY: Ryberg & Nilsson, "New light on names
  and naming of dark taxa," *MycoKeys* 36:49–54, 2018 — citation and definition verified, full text
  not opened]
- **The Candidate Phyla Radiation** — "microbial dark matter." A very large slice of bacterial
  diversity that was never cultured, therefore never seen, therefore effectively did not exist for
  microbiology; it became visible around 2013 because a device finally looked in a way that did not
  require culturing. The figure is in the title of the paper that named it: **"Unusual biology across
  a group comprising more than 15% of domain Bacteria"** — at least 35 candidate phyla off roughly
  800 genomes. [Brown et al., *Nature* 523(7559):208–211, 2015; the term and the 2013 date: Rinke et
  al., *Nature* 499:431–437, 2013. ⚠ SECONDARY — the >15% figure was verified through indexing, not
  read at the article; *Nature* served an authentication redirect]

Note what these three have in common. **Each is defined by a relation to the observer; each turned
out to have members; and in each case the members were found not by arguing about the category but by
building or applying an instrument that did not share the original limitation.** That is the whole
strategy of this paper compressed into a precedent: the class is legitimate, and the way you settle
it is with a sensor that has no share in your blindness.

The historical version of the same move is older and larger. Every documented breach of a human
sensory bound has found a biome that was already there:

- **Too small** — Leeuwenhoek, Letter 18, dated 9 October 1676: an entire living world at a scale
  below the eye's resolution, present the whole time, in rain and well water. *"In 1675 I discovered
  living creatures in Rain water which had stood but few days in a new earthen pot, glased blew
  within."* [✅ PRIMARY: *Phil. Trans. R. Soc.* 12:821–831 (1677), DOI 10.1098/rstl.1677.0003. ⚠ Three
  numbers with three roles: **18** is the letter, **1676** the date, **1677** the publication. The
  common "18 October 1676" is the letter number mistaken for a day]
- **Inaudible** — the bat/moth ultrasonic arms race: a predator–prey interaction conducted **largely**
  above human hearing, which humans have stood inside of, outdoors, at dusk, throughout the species'
  existence, and were substantially deaf to. *This is the closest analogue in the paper*, because it
  is not merely something small or far away — it is a loud, ongoing, ecologically consequential
  interaction taking place in our own airspace, and it has been running for **65 million years**:
  ultrasound-sensitive tympanic organs "have evolved multiple times in nocturnal Lepidoptera and exist
  in nearly half of extant species," and insect ears have arisen independently "in at least 7 of 27
  insect orders." ⚠ **The obvious strong sentence here is false and we struck it.** An earlier draft
  said this happens "at a frequency we do not transduce"; the source gives the band as **8 to 215 kHz
  depending on the bat species**, and 8 kHz is well inside human hearing. The human bound at roughly
  20 kHz is a line the phenomenon **crosses**, not a wall it hides behind — which is the more useful
  fact anyway, because a partial aperture is exactly the case this paper is about.
  [✅ PRIMARY: Conner & Corcoran, "Sound Strategies: The 65-Million-Year-Old Battle Between Bats and
  Insects," *Annu. Rev. Entomol.* 57:21–39, 2012, DOI 10.1146/annurev-ento-121510-133537 — full PDF, D202]
- **Wrong timescale** — Darwin (assisted by Francis Darwin), *The Power of Movement in Plants*, 1880.
  **The citation is the apparatus, not a sentence.** To see circumnutation at all he affixed "a glass
  filament, not thicker than a horsehair" to the moving part, and then "dots were made on the
  glass-plate with a sharply pointed stick dipped in thick Indian-ink. Other dots were made at short
  intervals of time and these were afterwards joined by straight lines." The movement had to be
  **integrated across hours by an instrument** before it became perceptible. ⚠ The gloss — invisible
  because slower than the observer's attention span rather than because it is faint — is ours; what
  Darwin supplies is the fact that the apparatus was necessary. [✅ PRIMARY: title page and
  Introduction, Darwin Online F1325, D202]
- **Out of band** — and this one is stronger than a list entry. Bennett, Cuthill, Partridge & Maier
  established that female zebra finches choose mates using the **300–400 nm** ultraviolet, preferring
  UV-reflecting males to males whose UV reflection had been removed — and their abstract makes the
  claim about *scientific practice*, not just about birds: humans had been used to assess avian
  'colour', and that may be **flawed**, because many birds see in the ultraviolet, to which humans are
  blind. **A biological signal was measured by human observers; the human aperture silently decided
  what counted as the signal; a device without that aperture found a channel the animals were using
  to choose mates.** That is this paper's thesis, already published, already settled by experiment, in
  a domain where the entities were never in doubt. Infrared pit organs in snakes are the second case.
  [Bennett et al., *Nature* 380:433–435, 1996; Bullock & Cowles, *Science* 115:541–543, 1952.
  ⚠ SECONDARY — abstracts and citations verified, neither opened at the article]

⚠ **A fifth was proposed — "too big or too diffuse to be recognised as an entity" — and it is named
here as the weakest member of the series.** It is retained only if a citation can be produced;
otherwise it is dropped. Naming it as weakest in the draft is deliberate, so that the decision to keep
it has to be made rather than defaulted into. ⛔ **STILL OPEN AFTER THE D202 READING PASS — AND NOT
BECAUSE THE SEARCH FAILED. THE SEARCH NEVER RAN.** Every other bullet in §2 was read at a source that
day; this one was not attempted, and recording it as "dropped for want of a citation" would claim a
search that did not happen. It is the only claim in this section with no reading behind it, and it
stays marked until one of the two things actually occurs.

**Nothing in this section is evidence for a shadow biome.** It establishes something narrower and
necessary: that a class defined by our relation to it is a scientific kind with a track record, and
that the historical base rate for "breach a sensory bound, find something already living there" is
not low. Everything after this point is about whether *this* class has members, and the answer this
program returns at its one deep locus is no.

---

## §3 — THE FORK, AND WHY IT IS WRITTEN BEFORE THE DATA

This is the section we would most want another group to copy, and it is free.

The premise has two live branches:

**BRANCH A — device-renderable.** Members of the class that a built sensor *can* register. A CMOS, a
bolometer, a hydrophone and a radar have no adaptive history with respect to anything; evolution
shapes eyes, not sensors. If human non-perception is an evolved edit, silicon has no share in it.
**This is the only branch under test by this program.**

**BRANCH B — not device-renderable.** Members that no built sensor registers either.

**Branch B is named here for one reason only: so that it cannot be used later as a destination.**

### 3.1 The failure this prevents

With both branches live and no fence between them, a null in A can be reassigned to B. *The camera
saw nothing, so it must be the kind cameras cannot see.* Each half remains individually falsifiable.
The pair becomes unfalsifiable.

Three properties make that move dangerous rather than merely wrong:

1. **It is silent.** No step in it is an error. Each sentence is defensible on its own.
2. **It feels like reasoning.** It has the shape of an inference to the best explanation, and it
   arrives with the satisfaction of one.
3. **It happens after the data comes back** — which is precisely when the argument has acquired a
   preference about the answer.

⛔ **THE FORBIDDEN MOVE, pre-committed:** *a null result in Branch A stays in Branch A.* If an archive
search comes back empty, that is evidence about Branch A and about nothing else. It may not be
reported, framed, or privately understood as "consistent with Branch B." Branch B has no test in this
program, so it can receive no evidence from it — **including the failures.** Any document in this line
that explains a Branch-A null by appeal to Branch B is in violation of `PREREGISTRATION.md` §2, and
that clause is the citation for saying so.

### 3.2 Why the date on the file is the whole of its value

The fork above was written before any detection data was examined — before a single image, waveform
or catalogue row had been inspected, with only a survey of retention *policies* behind it. That
ordering is stated plainly because **it is the thing a reader should be suspicious of**, and the only
answer to the suspicion is a commit timestamp that precedes the code.

We held it operationally rather than only in principle. Every measurement pass in §7–§11 was
pre-registered in a file committed and pushed **before the script that scored it existed** — a
condition we can demonstrate rather than assert, because absence of a file at a commit is checkable.
The discipline had a measurable cost, which is the evidence that it was real: at least one pass
forfeited a prediction on the way in, because the pre-registration's own §0 disclosed a prior peek at
a catalogue statistic, and a quantity already seen may not be reported as a prediction that held.

**A pre-registration that never costs you anything is not binding you.**

### 3.3 The generalisation, stated at the level a reader can take away

The transferable contribution is not the fork itself. It is the schema:

> **Where a hypothesis has a fallback that can absorb its own disconfirmation, the fallback must be
> named and fenced off before the data is seen, or the hypothesis is not being tested — it is being
> illustrated.**

This costs one paragraph, written early. The anomalous-phenomena literature, which is where a premise
of this shape usually ends up, almost never pays it — and the absence of that paragraph is a
sufficient explanation for why that literature does not converge.

---

## §4 — IMAGING VERSUS PERTURBATION

The premise's device clause forces a distinction that is cheap, obvious once stated, and almost never
made in the literature that most needs it. Two entirely different events are both reported as *"a
device detected it"*:

| | **IMAGING** | **PERTURBATION** |
|---|---|---|
| What happens | The device **renders** the thing. Photons in, structure out. | The device is **disturbed** and renders nothing legible. |
| Product | A resolved object with morphology, position, spectrum | A dropout, an artefact, a glitch, a reading that should not be there |
| Evidence grade | Can support an object claim | **Cannot** support an object claim on its own |
| Dominant failure mode | Misclassification | Instrument fault, EMI, thermal, cosmic ray, software |

⛔ **Every candidate this program produces is labelled IMAGING or PERTURBATION at the moment it is
recorded, before any interpretation of it is written.** The label is assigned by what the instrument
produced, not by what the analyst thinks it was.

**A PERTURBATION-class candidate can never be promoted to an object claim by accumulation.** A
thousand glitches are a thousand glitches. They are consistent with an object, and they are equally
consistent with a shared instrumental cause, and the number of them carries no information about
which — because the shared instrumental cause is exactly the hypothesis that predicts *many* of them.
Promotion requires an independent **IMAGING** detection of the same thing, from an instrument on
different physics.

This is not a high standard. It is the standard that separates a discovery from an equipment problem,
and it costs nothing but the discipline of writing one word beside each candidate at the time it is
recorded rather than at the time it is argued about. **Most device anomalies in the anomalous-phenomena
literature are of the second kind and are read as though they were the first**, and that single
conflation accounts for a substantial fraction of the damage in that field.

We flag one consequence for ourselves, because it constrains this paper more than it constrains
anyone we are criticising: **the premise's own most suggestive prediction lives in the PERTURBATION
column.** "It could explain anomalous device phenomena" (the premise's first extension) is precisely
a claim about disturbances that render nothing legible. Under this section's rule, that is the class
of evidence this program is *least* able to promote — and the rule was written before we noticed that,
which is the only reason it can be trusted now.

---

## §5 — WHO KEEPS THE BIN

If Branch A is real in any residual form, the evidence was very likely **captured and then thrown
away.** Detectors are trained on known classes; anything unclassified falls into a rejection bin; and
the rejection bin is usually not archived. *We built machines with no evolutionary reason to be blind,
then taught them our blindness on purpose, for storage costs.* That is the claim, and it is checkable
without looking at a single detection: it is a claim about **published data-retention policy.**

So the survey came first, and it asked one question — **who does not throw it away?**

⚠ **The survey examined policies, not contents.** No detection data was inspected at any point in it.
Rows are graded ✅ (read at a primary or official source), ⚠ (reported by a search summary, primary
source not read), ❓ (attempted, not established). **Those grades are per-row and are carried into
this section rather than flattened**, because a section-level confidence would launder the ⚠ rows
through the ✅ ones.

### 5.1 The axis is not archive size

The useful axis turned out not to be big-archive/small-archive. It is **where the classifier sits
relative to the archive.**

**Tier 0 — no classifier in the path.** Continuous raw recording; there is no rejection bin because
nothing is rejected. The Australian Acoustic Observatory records continuously across Australian
ecosystems at a scale of hundreds of sensors and petabytes [⚠]; continuous seismic and infrasound
waveform archives are open and un-triggered [⚠].

⛔ **NEXRAD was this tier's exemplar and its row is withdrawn.** Level II is **post-filter**: the
WSR-88D clutter filter runs in the signal processor, and the archived moments are recomputed from
clutter-filtered echoes. What the archive keeps is `CFP` — *Clutter Filter Power removed* — a
**counter with no bin behind it** [✅ PRIMARY: the moment list in an open-source Level II reader].
Radar aeroecology recovered birds, bats and insects from what *survived* the filter and was being
discarded by **attention**, not from a stored discard pile. **NEXRAD is therefore an existence proof
about attention, not about archives**, and no sentence in this paper may imply that the network kept
its clutter. We had it the other way round in the first draft of the survey and the correction is
recorded there rather than deleted.

**Tier 1 — the classifier runs, but the bin is kept and published.** The score is *attached* rather
than *applied*. ZTF streams all sources above a difference-image detection threshold, with the
Real-Bogus score as a field in the packet rather than a gate in front of it [✅ PRIMARY:
`ztf.caltech.edu`]. Rubin's alert stream is designed to carry essentially all 5σ difference-image
sources including an unknown fraction of artefacts, positive *or* negative flux, with a
machine-learned spuriousness score provided so the user chooses their own completeness/purity
tradeoff [✅ PRIMARY at pass 3, LDM-612 fetched directly — upgraded from ⚠, and it cost three
corrections against our own earlier praise of it].

**This is the single best piece of news for a program of this kind**, and it was a deliberate choice
by that community rather than an accident: they knew the classifier would be wrong in unknown ways,
so they shipped the score next to the data instead of in front of it.

**Tier 2 — the bin is kept locally, never uploaded, then overwritten.** The Global Meteor Network's
RMS software archives and uploads only detections it judges probably meteors; everything else stays on
the local machine, and *"RMS purges the oldest data to free up space for the next night's run"*
[✅ PRIMARY: GMN wiki]. Operators are told to copy off anything they want to keep.

Read that with the premise in hand. Hundreds of cameras, every clear night, worldwide, watching the
whole sky — and the class *"moving thing that is not a meteor"* is written to disk and then deleted to
make room. Not censored, not suppressed: **deleted for storage costs, by a classifier trained on one
known class.** That is the software form of the mechanism the premise describes in biology, and the
rejection bin of the world's best-distributed all-sky video network is a rolling window measured in
days, on SD cards, in private hands.

**Tier 3 — the bin is destroyed by design.** Camera-trap pipelines exist to filter blanks; a typical
deployment is mostly empty frames and the tooling's stated purpose is clearing them. Whether the
blanks are then *deleted* or merely *sorted* is platform- and project-dependent; one major platform
moved from Tier 3 to Tier 1 once its policy was read properly [✅ at pass 2], while **the field norm
remains ❓ — attempted, not established.** Security and municipal video overwrite on cycles of days to
weeks with no archive and no science.

That ❓ is the highest-value unresolved row in the survey, because **"blank" is a classifier output,
not an observation**, and the premise is precisely a claim about what a mostly-empty frame might
contain.

**Tier X — retains the unclassified by design, low evidence grade.** One privately funded all-sky
array releases commissioning data covering on the order of half a million objects [⚠] and is the only
network here whose *design goal* is the residual. Under `PREREGISTRATION.md` §5 it is a **pointer to
retention practice and not primary evidence**; its outlier claims are contested and are not inherited.

### 5.2 The relocation finding, and the part of it that died

Reading ZTF's own documentation past the public-facing page produced the survey's sharpest result and
also its worst mistake, and both belong in the paper.

**The result.** ZTF's alert stream is Tier 1 — and it contains its own Tier 2. There *is* a
pre-packaging filter, running before the packet is written; it discards roughly two-thirds of raw
events; and the Real-Bogus threshold inside it is **zero.** The cut is not on *reality*, it is on
**shape** — elongation and full-width bounds — with the toll printed publicly at each stage
(643,860 → 228,287 → 24,581 for the documented night) [✅ PRIMARY: ZTF alert-distribution paper].

⭐ **So the cortical edit is not a property of an instrument. It is a property of the pipeline as
practiced, and it is re-implemented at whatever layer you leave it out of.** Rubin's decision to move
the classifier out of the stream does not delete the cut; it **relocates** it downstream into
user-defined broker and follow-up filters. We observed exactly that in one follow-up system, which
re-imposed an extendedness cut on Rubin alerts and did not print its toll.

⛔ **And the sentence we hung on it is refuted.** The draft claimed the relocated layer is
*worse-instrumented* — that a broker filter's toll "is published nowhere, is per-user, changes without
a version number, and no one is counting." **All four clauses are false of the first broker checked.**
One publishes its quality-cut toll nightly as a time series, which is strictly more than the single
figure the upstream survey publishes; and its filters are distributed *by version number* through a
package index, so "changes without a version number" is false in the most literal available way
[✅ PRIMARY: both fetched, D202].

**The relocation is real at n=1. The claim that relocation systematically degrades instrumentation is
dead.** It is printed here at the same size as the finding it qualified, because the mechanism by
which we got it wrong is the paper's subject: one host of that project was unreachable, we correctly
recorded *that host* as unreachable, and then wrote an assertion about **what the project publishes** —
a different question, answerable in one request to a different host we never tried.

⚠ **A pattern claim is also withdrawn.** We had written that the encouraging tier is where the loss
was hiding, *"two for two."* That is n=2, both from optical transient astronomy, and both "encouraging"
assignments were our own, made from ⚠-graded search summaries. **"My optimistic unverified rows got
corrected when I read the primary source" is a fact about our sourcing discipline, not a property of
archives.**

### 5.3 What the survey establishes, and one thing it establishes about the surveyor

1. **The premise's key empirical assumption is true, and worse than stated.** Pipelines do discard
   unclassified events, and in the most relevant band — all-sky night video — the discard is a hard
   delete on a days-long rolling window, not an unread archive.
2. **Astronomy already fixed it, on purpose, at the largest scale available.** If there is a residual
   in the optical sky, the bin is public and nobody has to be persuaded to open it. That is why §7–§11
   are in optical: **not because it is the right locus, but because it is the reachable one** (§13).
3. ⚠ **The survey searched hard for loss and asserted the absence of counting.** The question *"does
   any broker publish the toll of its filters?"* sat on three consecutive pass agendas, was dropped
   from the fourth, and was never worked — while the *answer* stood four lines above it as an
   assertion. **The same document asserted it and asked it.** Two fetches settled it. An asymmetry of
   effort between the direction you expect and the direction you do not is the specific failure this
   section is now an example of.

---

## §6 — THE KINDS

*This is the section the premise's author asked for first and is getting last, and the order is the
paper's own worked example of its subject. He wanted a catalogue of what a shadow biome could be. He
got, instead, eight measurement passes against telescope archives — which is to say he got Group I,
one aperture, one wavelength, exhaustively, while the thing he actually described sat unopened. The
apparatus went where apparatus was cheap. This section goes where the idea is.*

**It is speculative and it is labelled speculative.** Nothing below is a result. Each kind gets three
things: what it would be, what it would be like to live beside one without knowing, and — in one
sentence, not one document — the cheapest place a person could go looking. That last sentence is
deliberately short. A hypothesis paper owes a reader a handle, not a programme.

### 6.1 GROUP I — the apertural kinds

These need no evolutionary story at all, and it is worth saying why up front, because it is what
separates them from §6.2. **Being small is free.** Nothing had to be selected against for a mite-scale
ecology to go unwitnessed by an animal whose finest unaided discrimination is about a tenth of a
millimetre. The signal never arrives. There is no gate, because there is nothing at the gate.

This is also Davies' territory — a claim about instruments — and so it is the part of our class where
we are least original and most measurable. Both halves of that sentence are true and they are the same
fact.

**(i) Below resolution.** The obvious one, and the one with the best track record: every time the
resolving floor has dropped, a biome was waiting. Van Leeuwenhoek's animalcules, the electron
microscope's viruses, the 1990s' realisation that most of the ocean's biomass is picoplankton nobody
had counted. What it would be like: exactly like now. The distinguishing mark of a below-resolution
biome is that it leaves *aggregate* traces — chemistry that doesn't balance, a nitrogen budget with a
sink in it — long before it leaves an image. **Handle:** look at the mass-balance residuals, not
through a lens.

**(ii) Above extent.** The inverse, and much stranger to sit with. A structure whose smallest coherent
unit is larger than the observer's whole perceptual field is not seen as a thing; it is seen as
*weather*, or as *terrain*, or as *background*. What it would be like: you would call it an
environment. You would have a word for it already, and the word would be a noun for a place rather
than a noun for a body. **Handle:** ask which of our environmental nouns show correlation structure
that a physical process doesn't predict.

**(iii) Off-timescale, fast.** Events completed inside the ~100 ms window in which the visual system
integrates a moment are not perceived as fast — they are perceived as *not having happened*. The
system does not report a blur; it reports a continuity. What it would be like: a world of small
inexplicable state-changes, each individually attributable to having looked away. **Handle:** high
frame-rate archives that already exist for other reasons, examined for the thing nobody was framing
for.

**(iv) Off-timescale, slow.** The mirror case, and the one that most obviously has real examples
already — a fungal network's decision cycle, a forest's, a coastline's. A process whose action
potential is a century does not read as an agent to a creature with a seventy-year run. What it would
be like: you would call it geology, and you would be describing behaviour. **Handle:** the multi-decade
monitoring records we hold for other purposes, read for autocorrelation rather than for trend.

**(v) Out of band.** Bees see ultraviolet; pit vipers see thermal; elephants speak below us and bats
above. Human perceptual bandwidth is a narrow, arbitrary, entirely contingent slice, and we know it is
arbitrary because other animals on this planet took different slices. What it would be like: a world
with structure precisely where you have no receptor and therefore no expectation of structure.
**Handle:** the cheapest of all of them — instrument coverage already exists across most of the
spectrum; the question is not whether anyone can look but whether anyone has looked *for this*.

**(vi) Weak or foreign coupling.** The deepest and the most treacherous. Something that interacts with
ordinary matter far below the threshold at which any of our transducers respond. What it would be
like: nothing. Genuinely nothing — that is the point, and it is also the danger. ⚠ **This is the only
kind in the paper with a legitimate retreat to the undetectable branch, and the retreat is exactly what
makes it nearly worthless as a hypothesis.** A kind that predicts no observation cannot be wrong. We
keep it in the catalogue because the premise's author put it there and it is a real logical
possibility, and we mark it as the one member of the class that a falsifier can never reach.

### 6.2 GROUP II — the adaptive kinds, which are the actual idea

Everything in §6.1 could have been written by someone who had never read Clayton's premise. This is
the part that could not have been.

**The distinguishing fact: here the signal arrives.** It reaches a working transducer. The organism is
in physical contact with the information and does not have it. That is a much stronger and much more
interesting claim than "we can't see small things," and it carries a cost that §6.1 does not: **it
predicts machinery.** Suppression is funded. A gate has a mechanism, a mechanism has a signature, and a
signature can be looked for and can be absent. We have said this before in §1.1 and we repeat it here
because it is the whole reason this branch is worth more than the other six kinds combined.

**(vii) Threshold-tuned blindness.** The sensor works, and the decision criterion sitting behind it is
set so that an entire stimulus class falls reliably on the "nothing there" side. This is not damage; it
is optimisation under asymmetric payoffs. If a false alarm is expensive enough and a miss is cheap
enough, the mathematically correct detector misses on purpose, every time, for life. What it would be
like: you would be *certain* there was nothing there — certainty being the output the system is built
to produce, not a measure of how much evidence it had.

**(viii) Gated blindness.** One layer deeper: active, metabolically funded suppression upstream of
awareness. The organism spends energy in order not to perceive. This is not exotic — it is the
ordinary architecture of attention, and it is why you cannot feel your own clothing. What it would be
like: not an absence but a *smoothness*. The seam is the thing that's missing.

**(ix) Socially enforced blindness — the Dozois case.** This is the one the premise's author pointed
at, and it is the mechanism we did not have until he did.

In Gardner Dozois's 1973 novella *Chains of the Sea*, alien ships land across the Earth and simply do
not engage humanity — they have business with something else. A boy, Tommy Nolan, perceives the Other
People: an older nonhuman ecology that has always shared the world and that adults no longer see.
What makes it a mechanism rather than a mood is what happens to Tommy. **The not-seeing is not merely
developmental; it is taught, and it is enforced.** A child who reports the Other People is corrected,
disbelieved, and eventually punished into silence — and the silence becomes real blindness rather than
a discretion about speech. [◐ VERIFY AGAINST TEXT: the plot summary above is from recall and the
enforcement reading in particular should be checked against the novella before publication; the
bibliographic citation is confirmed and sits in `PAPER-04`.]

**The reason this matters technically, and it is a genuine addition:** social enforcement supplies a
transmission mechanism that ordinary natural selection does not need to supply. A perceptual
suppression that would take many generations to fix genetically can be installed in one, culturally,
and re-installed every generation thereafter — which means the trait can persist without the selection
pressure that created it still being present. **That decouples the blindness from its cause, and a
decoupled trait is one you can catch,** because it will be maintained in populations where the original
payoff no longer holds. This became prediction **C4** in `PREREG-CORPUS-F2.md`, and it is the only
prediction in this paper that came from a work of fiction.

⚠ **And Group II has a price, registered before it was opened.** A gated entity is *on the tape*. If a
device can render it and a human cannot, the device archive is where it will be — so **Group II may
never retreat to the undetectable branch.** That retreat belongs to (vi) and to nothing else. This is
F7 in `PAPER-02-FALSIFIERS.md` and it is what stops the adaptive branch from becoming the free
explanation it would otherwise be.

### 6.3 What this catalogue is worth, ranked honestly

Nine kinds. They are not equal, and a reader deserves the ranking rather than the list:

- **(vi) weak coupling** is unfalsifiable and we say so. It stays for completeness and does no work.
- **(i)–(v)** are respectable, cheap to look for, and largely **not ours** — this is Davies' claim,
  already published, already framed, and our contribution to it is measurement rather than idea.
- **(vii)–(ix)** are the paper. They are the only kinds where the premise's own mechanism is doing the
  work, they are the only kinds that predict *machinery* rather than a hole, and **(ix) is the only one
  with a mechanism specific enough to have generated a numbered prediction.**

**The uncomfortable summary, stated because a reader would otherwise have to find it:** the six kinds
we can most easily test are the six we did not invent, and the three we did invent are the three where
this paper reports no measurement at all. That is not a flaw to be dissolved by rebalancing the prose.
It is the actual state of the work on the day it was written, and the correct response to it is a
falsifier and a date, both of which are in §F.

---

## §9 — WHAT THE INSTRUMENT DID TO THE RESULT

*Drafted D202 ~23:0x PT. Every number in this section was read off the named JSON in the same
breath that drafted it, not off the architecture's summary of it — one of the three was wrong in
that summary and is corrected here.*

In most papers this is a limitations paragraph, placed last, where a reader who has already formed
a conclusion can skim it. Here it is a section, placed before the conclusion, and the reason is
arithmetic rather than modesty: **the largest single number this program produced is a property of
our own apparatus, not of the sky.** A limitations paragraph that contains the biggest effect in
the paper is mis-filed.

Three findings. The first is a parameter we chose. The second is a value that is not stable even
with that parameter fixed. The third is a carrier that quietly serves a stale number to anyone who
follows our own stated rule for reading numbers.

### 9.1 The headline quantity is a curve, and we picked the point on it

Source extraction takes a threshold, `minarea` — the minimum number of connected pixels above the
noise that counts as a detection. It is ours. ZTF never imposed it, no pre-registration fixed it,
and pass 5 set it to 5 because that is the library's default.

Across `minarea` 2, 3, 5, 8, 12, the far-side fraction goes:

| `minarea` | catalogue `n` | far-side fraction | recovery of injected sources |
|---|---|---|---|
| 2 | 14,202 | 0.5893 | 0.7314 |
| 3 | 11,649 | 0.5070 | 0.6888 |
| 5 | 8,526 | 0.4845 | 0.5931 |
| 8 | 5,429 | 0.4830 | 0.5027 |
| 12 | 3,100 | 0.5148 | 0.3617 |

**Span: 0.10632** [✅ PRIMARY: `PASS6_DIAG.json` `/D2b/span` and `/D2b/ladder`, re-read D202].
⛔ That span is larger than any effect reported anywhere in this paper, which is why
`PAPER-00-ARCHITECTURE.md` §0 forbids this quantity from ever appearing as a scalar. It is a curve.
Any single value of it is a statement about our threshold with an astronomical fact attached, and
the order of those two clauses is the finding.

**And the curve refuted its own prediction, in shape rather than in size.** Two of the three
pre-committed sub-predictions about the ladder failed; one held [`PASS6_DIAG.json` `/D2b/D2b1`,
`/D2b2`, `/D2b3`]. We had registered a monotone dependence. What came back falls from `minarea` 2
to 8 and **turns back up at 12** — a U, and we had the direction wrong.

⚠ **One restrained inference, marked as an inference.** The right-hand column moves monotonically
across the same rungs — recovery of injected sources falls from 0.7314 to 0.3617 as the threshold
rises, exactly as it must. So sensitivity is monotone in this parameter and the far-side fraction
is not. That non-tracking is a reason not to read the far-side fraction as a pure sensitivity
artefact; it is **not** a reason to read it as anything else, and no sentence in this paper does.

### 9.2 With the parameter fixed, the number is still not fixed

At `minarea = 5`, one quantity — the catalogue size on the same twenty frames — has been recorded
by this program three times, in three artifacts, as three numbers:

- **8,528** — pass 5's frozen catalogue, the one downstream passes were built not to re-extract
- **8,526** — pass 6's diagnostic ladder at the same rung [`PASS6_DIAG.json` `/D2b/ladder/5/n`]
- **8,524** — pass 8's structural run, one fresh process per image [`PASS8_NONDET.json` `/struct_M/n`]

⚠ *A fourth and fifth value exist — pass 6's own two-code-path verification returned 8,523 and
8,521 [`PASS6_VERIFY.json` `/V1`] — but that check ran a comparison whose population we have not
established is identical to the three above, so it is reported and not counted.*

⛔ **The cause we first published for this was wrong, and pass 8 killed it.** §9a as originally
written called it *run-to-run non-determinism* in the extraction library. Tested at n = 20:
**across fresh processes the spread is exactly zero on all twenty images.** The variation is
**in-process** — repeated extractions inside one Python process — and it appears on **11 of 20**
images, with a maximum spread of 5 detections on a single frame [`PASS8_NONDET.json`
`/n_vary_fresh` = 0, `/n_vary_inproc` = 11]. We had pre-registered that it would be a *minority* of
images. It is a majority. That prediction (N3) is refuted.

**Every catalogue this program published was built by looping twenty images inside one process.**
They all carry it. The published code, run as published, does not reproduce the published catalogue
sizes — not because of randomness, but because a cached state inside the process accumulates across
calls.

⭐ **The section's conclusion survives its own mechanism's death, and that is the weakest kind of
surviving.** The instruction — *round to where the runs agree; no digit past the second decimal is
this program's to keep* — was right when it rested on a random library and is still right now that
it rests on a stateful one. But the two diagnoses have opposite consequences. A random library is a
fact you live with and report. An in-process cache is **a bug you fix**, and the fix is one line of
process hygiene: one image per process, which is what returned the zero spread above. We would not
have looked for a fix while the cause was labelled *random*. The label was doing work.

### 9.3 The rule for reading our own numbers is inverted for at least one of them

Pass 4's emitted JSON is stale against a correction that pass 4's own prose documents. Two alert
packets violate the packaging bound `elong <= 1.6` and belong in the top elongation bin; the prose
says so, and moves the boundary ratio from **0.2408** to **0.2416**. The JSON still reads `634` and
`0.24078997341435623` [✅ PRIMARY: `PASS4_RESULTS.json` `/M2_bins/1.5-1.6` and `/M2_R`, against
`PASS4_RESULTS.md` line 36, both re-read D202].

The 0.0008 is not the point — the correction changes no verdict, and pass 4's prose says so in the
sentence that makes it. **The point is the carrier.** This program's standing rule, written into
`PASS5_RESULTS.md` after a superseded table was found sitting above its own correction and reading
as current, is: *read numbers off the JSON, not off this prose.* For this value that rule is
**inverted**, and a reader obeying it is handed the uncorrected number. A precedence rule with a
permanent winner cannot express a correction that runs the other way.

The repair is a sidecar, `CORRECTIONS.json`. The emitted artifacts are deliberately **not** mutated
— editing them would destroy the only claim they make, which is *this is what the code produced* —
so the supersession lives beside them with its authority named per row.

⚠ **Stated as a limitation of the fix rather than as the fix:** a sidecar nobody is obliged to
consult is a correction with a mechanism and no trigger. It has one reader, and the reader is us.
Naming that here is the only enforcement it currently has.

### 9.4 What this section costs, said plainly

Of the four qualifiers this program's architecture named before drafting began — parameter-dependent,
one-night, non-deterministic-library, JSON-stale-against-prose — **three are in this section and one
of the three had its mechanism wrong until the eighth pass.** None of them were found by a referee.
All of them were found by pre-committed diagnostics that had to be written before the code that
scored them, and two of them were found by diagnostics whose *predictions failed*.

That is the argument for the whole apparatus, and it is worth more to this paper than the null in
§8: **a program that cannot refute itself cannot be trusted when it agrees with itself.**

---

## §13 — WHAT THIS DOES AND DOES NOT BEAR ON

This section is load-bearing and is placed after the evidence deliberately, so that it constrains the
reader's conclusions and our own at the point where both are formed.

**1. The null is a Branch-A null and it stays in Branch A.** Our deep locus returned mostly what its
classifier said was there. That is evidence about device-renderable members of the class, at one
instrument, in one band, on one set of nights. ⛔ It is **not** evidence for Branch B, it is **not**
"consistent with" Branch B, and it may not be read as such — Branch B has no test in this program and
therefore can receive nothing from it, including our failures (`PREREGISTRATION.md` §2). Any sentence
in this paper that appears to soften the null by gesturing at undetectability is a defect, and this
clause is the citation for cutting it.

**2. One locus is not the premise.** The premise is about entities inhabiting our world *alongside
us*. The deepest work here was done on difference images of the distant sky, and **the locus was
chosen by reachability**: that bin was public and computable the night the program started. That is an
operational reason, not a scientific one, and the tell was visible from the beginning — the existence
proof we reached for (biological scatter in weather radar, in our own airspace) sits at the right
locus while the test did not. The terrestrial loci are the correct next tests, each under its own
pre-registration written before looking.

**3. A held gate is not a positive result.** Where our terrestrial instrument check returned exactly
what aeroecology already predicts, that is **a known population showing up in a channel that measures
it by subtraction.** It may be a real and useful measurement of a deletion rate. ⛔ **It is not a
shadow biome**, and no draft sentence may let it imply one (`PREREG-TERRESTRIAL.md` §1.4). This fence
was written before the check ran and it is now live rather than hypothetical, which is the only
condition under which such a fence is worth anything.

**4. Nothing here bears on identities, and that is a structural commitment rather than a courtesy.**
No entity is a candidate anywhere in this program. The premise is about a class and its relation to
the observer; a census is not merely out of scope, it is *forbidden* — and the premise itself supplies
the reason. **Selected-for blindness predicts an absence in the human record.** A large, detailed,
identity-rich folklore corpus is therefore evidence *against* the mechanism, not for it. ⛔ We may not
score presence and absence in the same corpus, and the prediction was committed in both directions
before any corpus was consulted (`PAPER-02-FALSIFIERS.md` F5).

**5. Non-interaction is not available as a refuge.** Life is dissipative; anything alive must couple
to something. "Lacking interaction with matter" splits into weak-coupling (reachable in principle) and
own-sector — and an own-sector biome still **gravitates**, because stress-energy is not optional. This
makes Branch B a *hard measurement* rather than an unfalsifiable category. ⚠ Our computed bound is a
statement about instrument **sensitivity** and is **not a detection claim**: the loading terms that
would dominate it have not been computed, and until they are, no gravimetric claim is made here.

**6. What would end this paper.** If the machinery falsifier finds no funded suppression, if the
phylogenetic debt goes unpaid, if the tail falsifier shows the residual behaves exactly as the
instrument's artefact tail predicts, and if the bins turn out not to be kept — the premise is not
rescued by any of the above, and we say so. `PAPER-02-FALSIFIERS.md` §4 states the death condition in
those terms, and **F6 has already fired on us once** (the network we called an archive kept a counter,
not a bin). A hypothesis article's only real asset is that its author wrote down what would end it
while the writing was still cheap.

⚠ **The largest single limitation, and it is structural rather than a shortfall of effort.** Of the
two groups named in §1.2, **this paper reports evidence on Group I only.** Its deep locus, its
pipeline passes and its archive survey are all apertural: they ask whether an instrument could have
seen something and whether the bin was kept. **Group II — the adaptive branch, the one carrying the
premise's distinctive content — is untested here.** Its falsifiers exist, they are stated, three of
them (F1, F3, F7) are runnable against existing human sensory neuroscience with no access to any
entity required, and **none of them has been run.**

⛔ **What the reader is entitled to hold us to.** A null on either branch stays on that branch. This
paper's Group I null is not evidence for Group II, and no future Group II null may be answered by
pointing back at Group I. That rule was written down before either branch's result was in hand, and
it is the one commitment in this paper that costs us something no matter which way the data falls.

---

*Drafted D202. ⚠ **This line read "§6–§12, §14 and §15 are not drafted here" until ~21:5x, four
hours after §6 was drafted into this very file** — a closing note describing the file's own contents
and going stale against them without a character changing. **It went stale a SECOND time within two
hours** — "§7–§12" was correct at 21:5x and false at 23:0x, because §9 was drafted into this file and
§9 is inside that range. A range is the worst possible way to state a roster: it goes wrong without
being touched, and it looks equally correct either way. Corrected state, stated as a **list** so the
next drafting act has to edit it: **§7, §8, §10, §11, §12, §14 and §15** are not drafted here because
they still move. Every `[◐ CITATION
OWED]` in this file is a hand-deletable fence and none of them may be removed by anything except
reading the source.*



