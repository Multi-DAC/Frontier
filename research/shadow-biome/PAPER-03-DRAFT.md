# SHADOW BIOME — DRAFT PROSE: §1 §2 §3 §4 §5 §6 §7 §8 §9 §10 §11 §13

*(14,126 words, 12 headings. Roster stated as an EXPLICIT LIST, never a range — it read
"§1–§6, §9 and §13" until D202 ~23:5x, and a range cannot say which sections are missing from inside
it. Re-measured by `wc -w` and `grep -o '^## §'` at each edit, never recalled. **Still unwritten:
§12, §14, §15** — §12 needs a second night's archive fetch, §14 needs a noise floor, §15 is
pre-registered with zero data.)*

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
  **⭐ LIVE COUNT: ZERO.** All eleven real markers were discharged by the D202 reading pass — four
  survived at source, five were amended against the source, one claim died, one is carried as
  `[⚠ SECONDARY]`. This bullet is now a definition with no users, and it is kept rather than deleted
  because the next drafting breath needs the convention available. *(Re-measure with*
  `grep -o "◐ CITATION OWED" | wc -l` *and subtract this legend line; the architecture carried "12
  markers" for hours after the debt was discharged, which is a stale-debt error in a file whose
  purpose is stopping stale debts.)*
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
What makes it a mechanism rather than a mood is what happens to Tommy. A child who reports the Other
People is corrected, disbelieved, sent to a school psychiatrist, and **medicated** into silence.

[✅ VERIFIED AGAINST TEXT — D203 / 2026-08-22, primary read, 23,973 words. **The enforcement reading
above is confirmed and is stronger than this draft claimed** (it is medicalization, not merely
disbelief). **But the sentence this bracket replaced was REFUTED and is deleted.** It read: *"The
not-seeing is not merely developmental; it is taught, and it is enforced… and the silence becomes real
blindness rather than a discretion about speech."* The novella does not show that. Tommy **never stops
seeing** — he perceives the Other People through every stage of the enforcement and on the final page.
The other children's loss of the sight is stated with **no cause given**, and they do not remember
having had it. Perception-loss and reporting-suppression are two uncoupled mechanisms in the text; the
welding was the drafter's, working from recall, and it welded in the direction that made the argument
work. See `PAPER-07-SHORT.md` §2.4 and §4.4. **Note that `PREREG-CORPUS-F2.md` C4 was written narrowly
enough to be unaffected** — it only ever predicted a measurable cost to *reporters*, which is exactly
what the text supports. The prereg was more careful than the prose it came from.]

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

## §7 — THE TEST, AND WHY IT WAS WRITTEN BEFORE THE DATA

*Drafted D202 ~00:1x PT off `PASS4/5/6/7/8/9_PREDICTIONS.md` and the commit log that timestamps
them. No number in this section is new; the section's whole content is the **ordering**.*

Kind (ix) of §6 — an aperture that discards a class of thing before any human sees it — is the only
one of our kinds with machinery specific enough to name a place and a threshold. The place is the
Zwicky Transient Facility's public alert stream. The threshold is its packaging cut on source
elongation, `elong ≤ 1.6`, applied before an alert packet is written.

The test is not "is there a shadow biome behind ZTF's shape cut." Nothing here could establish that,
and §13 states so at length. The test is the far weaker and far more checkable question that has to
be answered first: **does a real, non-noise population of detections exist on the far side of that
cut, and does it survive every instrumental explanation we can construct for it?** A negative answer
closes the locus. A positive answer does not open anything; it says only that the bin is occupied and
that the occupants are not obviously artefacts of our own extraction.

### 7.1 The ordering, which is the only thing that makes any of this evidence

Every numbered prediction in this program was committed to a public git repository **before the code
that scored it existed.** Not before the code was run — before it was written. The commit hashes are
in the table below and the ordering is externally checkable by anyone who clones the repository.

| pass | prediction file | committed as | what ran afterwards |
|---|---|---|---|
| 4 | `PASS4_PREDICTIONS.md` (+ Amendment 1) | `715182f` | `measure_pass4.py`, on a tarball that was still downloading when the amendment was filed |
| 5 | `PASS5_PREDICTIONS.md` | — | `measure_pass5.py` |
| 6 | `PASS6_PREDICTIONS.md` | `f3c51a5` | `measure_pass6.py` |
| 6d | `PASS6_DIAGNOSTIC_PREDICTIONS.md` | `685fa0c` | `diag_pass6.py` |
| 7 | `PASS7_PREDICTIONS.md` | `da25f0c` | `measure_pass7.py` |
| 8 | `PASS8_PREDICTIONS.md` | `6567f2b` | `measure_pass8.py`, `nondet_pass8.py` |
| 9 | `PASS9_PREDICTIONS.md` | `32877a0` | `measure_pass9.py` |

This is cheap. That is the point of including it. The discipline costs one file and ten minutes per
pass, and the anomalous-phenomena literature this paper sits adjacent to almost never pays it — which
is precisely why a result from that literature cannot be distinguished from a result that was framed
after its own data came back.

### 7.2 What a pre-registration has to contain to be worth anything

Four properties, each of which this program has violated at least once and repaired:

**(a) A statistic fixed before the histogram is seen.** Pass 4's boundary ratio *R* names its
numerator bin and its reference bin in advance, and says why the reference bin was chosen — it sits
immediately outside the survey's own tighter recommended cut, so it is ordinary populated territory
that neither threshold defends. A ratio whose bins are picked after the plot is a decoration.

**(b) A declared prior that points away from the interesting answer.** Pass 4's M2 predicted
*R* < 0.10 — that the shape cut sits harmlessly in the tail — which is the boring result and the one
that would have weakened the whole locus. It came back at 0.2416 and is scored as a refutation of our
own skeptical prior. A pre-registration that only ever predicts what its author hopes for is a wish
list with dates on it.

**(c) A control that can return both answers.** Pass 6 required three synthetic-data gates to pass
before its shape section could be read at all: one that must detect alignment, one that must *not*
false-alarm on uniform angles, and one run through the *actual* scoring function rather than a
reimplementation of it. Pass 9 required a scramble control to reproduce the pair statistic's null
before its pair result could be quoted. A gauge that has only ever rendered one verdict is furniture.

**(d) A decision rule, binding, written while the number does not yet exist.** Pass 8's D4 is the
clearest case: it states in advance what will be concluded at each possible value of a gap that had
not been measured. It is the mechanism that stops a result from being interpreted by whoever reads it
last.

### 7.3 The rule we broke, and what it cost

Pass 4's M1 predicted a survival fraction of 8–14 % against a figure quoted from ZTF's own
explanatory supplement. Between committing that prediction and opening the data, we re-read the
supplement and discovered the quoted figure was built from two different populations — a public-only
numerator over an all-programs denominator, which stacks a telescope-time allocation on top of a
shape attrition and calls the product morphology.

The right move was available and was taken: **the prediction was left exactly as written, an
amendment was filed stating that it would now be expected to fail and in which direction, and it was
scored as a miss.** It failed high, at 34.5 %, in the direction the amendment named. A
pre-registration that gets quietly edited when its author learns something is not a pre-registration,
and the scoreboard in §10 is more useful with a called miss on it than with a retrofitted hit.

What did not save us is worth stating, because it generalises: the numbers had been transcribed
correctly, the cuts listed correctly, and the arithmetic recomputed rather than re-read. **Every
check we ran was on the arithmetic; none was on whether the two counts described the same set of
objects.**

---

## §8 — THE RESULT: WHAT IS ON THE FAR SIDE OF `elong ≤ 1.6`

*Drafted D202 ~00:1x PT. Every number below was re-read off its named JSON in the drafting breath.
Two of them contradict summaries this project was carrying about its own results, and both
corrections run against us.*

### 8.1 The bin is occupied, and it is not a noise skirt

Re-extracting sources at 5 σ from twenty ZTF difference images, without ZTF's packaging cut,
**48.50 % of detections lie past `elong = 1.6`** [✅ PRIMARY: `PASS6_RESULTS.json` `/frac_far`,
`minarea = 5`]. The fraction is flat to a signal-to-noise ratio of 100, so it is not the skirt of a
noise distribution; the histogram crosses 1.6 smoothly with a step ratio of 0.8878, so our own
extraction is not truncated there; and pass 4's boundary statistic recomputed on the uncut extraction
is **1.387** against **0.2416** on the packaged alert stream.

Only **0.17 %** of those past-1.6 detections — 7 of 4,136 — lie within 2 px of a ZTF alert. Whatever
occupies that bin, ZTF did not package it.

### 8.2 What occupies it: dipoles, and the pairs are real

The far side is dominated by **difference-image dipoles** — a source that moved or varied between the
science and reference images leaves a paired positive and negative residual, and the pair's members
are elongated along the axis joining them.

**65.81 %** of far-side detections sit within 10 px of another detection of the opposite sign
[✅ PRIMARY: `PASS6_VERIFY.json` `/V2/far/opp_share_of_side`], with a median elongation angle of
**77.9°** to the line joining them — near-perpendicular, which is the dipole signature and not the
streak signature we had predicted.

⚠ **The number this project printed as its headline for this section was the wrong one, and the
correction is against us.** We had quoted an opposite-sign excess of **+49.04 pp** (far-side
`opp_rate` 0.96252 against a composition-matched null of 0.47207) as evidence that the far side is
special. The kept side's own control, computed the same day and left unread for three passes, gives
`opp_rate` **0.97315** against a null of **0.43386** — an excess of **+53.93 pp**, *larger* than the
far side's [✅ PRIMARY: `PASS6_VERIFY.json` `/V2/kept`]. **Both sides' close pairs are overwhelmingly
opposite-sign. That is a property of the catalogue, not of the far side**, and +49.04 pp may not be
printed as a far-side finding.

The far-side-specific number is the *share of the side that is paired at all*: **0.65812 far versus
0.51161 kept, a gap of +14.65 pp.** That is what this section claims, and it is a third the size of
the number we nearly published.

The pairs are not a crowding coincidence. Scrambling the negative-sign positions by eight fixed
40-pixel offsets — preserving *n*, preserving the elongation distribution, destroying only the
pairing — collapses **2,329** mutual opposite-sign pairs to a median of **41.5**, i.e. **1.8 %** of
the observed count, and collapses the effect on the far-side fraction from −6.20 pp to a median
**0.020 pp** [✅ PRIMARY: `PASS9_RESULTS.json` `/S`].

### 8.3 The operation that would have been wrong, and the anchor that caught it

The obvious response — extract from the positive-difference image only, and the dipole doubling goes
away — is **the wrong operation, and we know that because an external anchor says so.**

It fails twice. First, the far side is *positive*-dominated, not negative: `frac_far` on
positive-only detections is **0.5487** against **0.4363** on negative-only, at all five `minarea`
rungs, with the effect growing monotonically [✅ PRIMARY: `PASS7_RESULTS.json` `/A`]. Two
pre-registered predictions asserting the opposite were refuted in the same direction. Second, and
decisively, dropping negatives deletes **2,505 unpaired negative detections that are not dipole
halves** — and ZTF's own negative-difference alerts land on exactly that population. Of ZTF's 240
`isdiffpos = 'f'` alerts on these frames, **64.17 %** fall on our unpaired negatives, against the
positive analogue's **41.18 %** — a gap of **+22.99 pp**, same sign at 5 of 5 rungs [✅ PRIMARY:
`PASS8_RESULTS.json` `/D3`].

`isdiffpos` is a label neither of our procedures controls. It is the only external adjudicator in
this chain, and it says the negatives we were about to delete are real detections ZTF itself alerted
on.

⛔ **One claim this project made and then killed, recorded here because §10's scoreboard is worth
nothing if the corpses are hidden.** We had written that the far-side *fraction* was manufactured by
counting dipoles twice. Measured: collapsing all 2,329 mutual pairs moves `frac_far` from 0.484991 to
**0.482820** — a change of **0.217 pp**. Dipole doubling inflates ***n*** and leaves the **fraction**
where it was. "Counted twice" is refuted and stays refuted. "The dipole pairs are an elongated
artefact class" is a *different* claim, established on different evidence, and may not inherit the
first one's citation.

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

## §10 — THE SCOREBOARD

A program that pre-registers is obliged to publish the scoreboard, including the parts that make it
look worse. This section is that. Every number in it comes from `score_program.py`, which recomputes
the tally from the per-pass artifacts on every run rather than storing a figure someone typed once
[✅ PRIMARY: `PROGRAM_SCORE.json`, regenerated D202]. The distinction matters here more than usual:
a hand tally of a scoreboard is a stamp, and a stamp is right on the day it is written and silently
wrong on every day after.

### 10.1 The count

Across nine passes plus the terrestrial L1 block, **51 of 72 scored predictions held — 70.8 %.**
Restricted to predictions committed before any data existed, **44 of 59 — 74.6 %.** Restricted to the
post-hoc diagnostics, which were minted after seeing an earlier pass's numbers and are labelled as
such throughout, **6 of 12 — 50.0 %.**

| pass | held / scored | refuted, pass-qualified |
|---|---|---|
| 4 | 4 / 6 | M1, M2 |
| 5 | 6 / 11 | P1, P3, P6, D1a, D1b |
| 6 | 8 / 16 | P1, P2, P3, P7, D2a-3, D2b-1, D2b-3, D2c-1 |
| 7 | 9 / 12 | A1, A3, B2 |
| 8 | 9 / 11 | N3, G2 |
| 9 | 11 / 11 | — |
| L1 | 4 / 5 | T5 |

Thirteen further items — synthetic-data gates, identity controls, positive controls, and one decision
rule that never fired — are **excluded from the denominator**, following the rule each pass declared
for itself and applying it uniformly backward to the passes that had not yet declared one. A control
that returns its known answer is not a confirmed hypothesis; counting it would inflate the score with
the program's own furniture.

Passes 1–3 contribute **zero** to both columns. They were policy and instrument specification and
produced five findings, not one of which had a number that could come back and contradict it. They
are named here rather than quietly omitted, because a denominator that drops its weakest passes is
not a scoreboard.

### 10.2 Three errors the arithmetic found in our own record

None of these are about the sky. All three are about the scoreboard, and they were invisible until
the tally was actually run.

**(i) "8 of 16 held" was pass 6's headline, not the program's.** It had been carried in the
architecture as though it described the whole series. It describes one pass — and it is the pass with
the worst ratio in the program.

**(ii) A pre-registered prediction was scored in prose and nowhere else.** L1's **T5** — the
self-directed prediction that at least one of T1–T4 would fail for an *instrument* reason rather than
a scientific one — was pre-registered [✅ PRIMARY: `PREREG-TERRESTRIAL.md` line 87] and adjudicated
REFUTED [✅ PRIMARY: `L1_T5_VERDICT.md` line 24], but `L1_RESULTS.json` `/verdicts` contains only
T1–T4. Any count taken off the machine-readable dictionaries therefore read L1 as **4 of 4**. It is
**4 of 5**, and the program's refutation count in that same dictionary set moves from five to six.
The defect is exactly the one this program names as its signature: a mechanism with no trigger, here
a verdict with no emitter.

**(iii) A bare prediction label does not identify a prediction in this program.** Nine keys are used
by more than one pass, and **five of them disagree with themselves across passes**:

| key | pass 5 | pass 6 | pass 9 |
|---|---|---|---|
| P1 | REFUTED | REFUTED | HELD |
| P2 | **HELD** | **REFUTED** | HELD |
| P3 | REFUTED | REFUTED | HELD |
| P6 | REFUTED | HELD | HELD |
| P7 | HELD | REFUTED | — |

The architecture had been citing "P2 refuted" unqualified. Two different P2s exist and they hold
opposite verdicts. Every reference in this paper is pass-qualified for that reason.

### 10.3 The number this section actually has to explain

Split the program at the point where its subject changed. Passes 4–6 asked questions about **ZTF's
sky and ZTF's data**. Passes 7–9 and L1 asked questions largely about **our own extraction and our
own artefact taxonomy** — whether our pair-finder was under-inclusive, whether our library was
non-deterministic, whether our citations anchored.

> **Passes 4–6: 18 of 33 held (54.5 %). Passes 7–9 + L1: 33 of 39 held (84.6 %). A swing of
> +30.1 percentage points.**

There are two readings and the flattering one is not automatically correct.

The flattering reading is calibration: nine passes of being wrong in public taught us to write
predictions we could actually defend, and the late passes are the payoff.

The unflattering reading is that **the questions got closer to our own machinery**, and a question
about your own code is one you are in a far better position to answer than a question about someone
else's telescope. On that reading the rising hit-rate is not evidence of a better forecaster; it is
evidence of an easier forecast. Pass 9's own write-up already flagged 11-of-11 as the worst-looking
result the program has produced, on the narrower ground that three of its four ladder predictions
passed at *exactly* their threshold. The era split is the same alarm with the whole series behind it.

We cannot presently separate the two readings, and we are not going to pick one. What follows from
saying so is a commitment, entered here: **the next pass on this chain is designed so that we do not
know which way it goes, and it is aimed back at the sky rather than at ourselves.**

### 10.4 The one calibration number we can compute, and it is small

Pass 5 is the only pass that attached explicit prior probabilities to its predictions before running
them [✅ PRIMARY: `PASS5_PREDICTIONS.md` §2, table]. That makes it the only block in the program that
supports a calibration statistic rather than a hit-rate.

Stated confidences averaged **67.9 %**; **57.1 %** of those predictions held. **Overconfident by 10.7
percentage points on n = 7.** The Brier score is **0.161** against a base-rate Brier of **0.245** — a
skill score of **0.34**, so the forecasts carried real information despite the overconfidence. On the
six science predictions alone, dropping the operational cost prediction, the overconfidence widens to
**15.0 points** and the skill falls to **0.26**.

⚠ **n = 7.** This is not a calibration curve; it is a single small sample from one pass, and it is
reported because it is the only such sample that exists and because the direction — overconfident —
is the direction that costs a program like this one the most. That eight subsequent blocks of
predictions were committed without priors attached is a defect in the apparatus and is recorded as
one. Prior probabilities are cheap to write and are the only thing that converts a scoreboard into a
calibration.

### 10.5 What a 70.8 % means, and what it does not

It does not mean the program is 70.8 % likely to be right about anything. It is not a confidence in a
conclusion. It is a record of how often a number committed in advance survived contact with data —
and its usefulness is almost entirely in the **21 refutations**, not the 51 confirmations. Every
qualifier in §9 arrived through a failed prediction. The most consequential correction in the program
came from a control whose prediction failed. A scoreboard with no losses on it is not a strong
program; it is an unfalsifiable one that has not noticed yet.

---

## §11 — THE RESIDUAL

*Drafted D202 ~00:2x PT under constraints pre-committed in `PASS9_PREDICTIONS.md` §6 **before** the
pass-9 data existed: the headline may not be printed alone, the band must travel with it, and the
alternative estimators must appear beside it rather than in a footnote. Those constraints are
honoured below and are the reason this section is shaped the way it is.*

### 11.1 The number, with everything that qualifies it in the same sentence

After removing both members of every mutual opposite-sign pair — the artefact class §8 established —
the fraction of detections past ZTF's packaging cut is:

> **`frac_far`(P_D) = 0.42** at `minarea = 5`, against **0.4845** for the untreated union and
> **0.5487** for the positive-only estimator, and moving across the `minarea` ladder by
> **+0.48 / −4.53 / −6.32 / −5.69 / −1.43 percentage points** at rungs 2 / 3 / 5 / 8 / 12
> [✅ PRIMARY: `PASS9_RESULTS.json` `/P0` and `/ladder`].

Three things are load-bearing in that sentence and none of them is the leading digit.

**The estimators disagree by more than the effect.** 0.42, 0.48 and 0.55 are three defensible
answers to "how much of the extraction is past 1.6," and the spread between them (13 pp) is twice the
size of the pair correction (6.3 pp). Any reader handed 0.42 alone would take from it a precision the
data does not contain.

**The correction is a band and it dies at one end of it.** At `minarea = 2` the move reverses sign
(+0.48 pp) and the effect is gone; at `minarea = 12` it is nearly gone (−1.43 pp). The mechanism is
visible in the same table: pair share rises to **0.5478** at rung 2, so the pair population there is
diluted with non-dipoles and removing it stops meaning what it means at rung 5. **This is not a
robust result across the parameter. It is a result at one parameter, with a stated shape either side
of it.**

**And it peaks exactly where we were already standing.** The largest correction any procedure in this
program has produced is largest at `minarea = 5` — the value the frozen catalogue was already built
at, chosen three passes earlier for reasons unrelated to pairs. ⚠ We have no evidence the choice was
motivated: `minarea = 5` predates the pair procedure by three passes and the commit log shows it.
But a coincidence that flatters the result is reported, not filed, and this is the report.

### 11.2 The third decimal does not exist

`PASS9_RESULTS.json` contains two values for this quantity, produced by two runs at the same
parameter in the same session: **0.422997** (*n* = 8,528) from the reproduction control and
**0.421366** (*n* = 8,526) from the ladder. They differ by **0.16 pp**, and the catalogue sizes
differ by two detections.

This is §9's in-process non-determinism arriving at the headline. The correct response is not to pick
the prettier number or to average them. It is the rule §9 states and this section obeys: **round to
where the runs agree.** That is two decimal places. `frac_far`(P_D) is **0.42**, and any digit past
it in this program is run-dependent.

### 11.3 What survives the pair correction, and what it is worth

A residual survives. After removing 2,329 mutual pairs — 27.3 % of the catalogue — roughly **42 % of
detections still lie past a threshold that ZTF applies before writing an alert packet.** The pair
procedure is also demonstrably *not* under-inclusive: on the survivors, the far-side opposition excess
falls from +49.04 pp to **+4.48 pp** and the far-minus-kept paired share from +14.65 pp to
**+2.55 pp**, so the mask is taking the dipoles it was built to take and is not leaving a large
uncaught population behind it [✅ PRIMARY: `PASS9_RESULTS.json` `/P5P6`].

⛔ **And here is what that residual is not.**

It is not a detection of anything. It is not evidence for a shadow biome, or for any object, or for
any phenomenon. Passes 7 through 9 established a floor for the dull reading and the dull reading
holds where it was tested: pass 7's recovery block found the residual there to be a
**detection-efficiency floor** — 101 unrecovered of 376, dominated by `UNEXTRACTED_DESPITE_FLUX` at
68, median magnitude offset **+1.124**, spread across **20 of 20** frames. That is what a threshold
looks like from underneath, and it was pre-registered as the boring answer before it was measured.

What the residual is, precisely: **a population in a bin that a major survey discards before a human
sees it, which we have failed to explain away in nine attempts.** The correct epistemic weight of
"we failed to explain it away" is set entirely by how hard we tried, which is what §10's scoreboard
and §9's instrument section exist to let a reader judge — and §10's own verdict on that is that our
success rate rose by 30 points at exactly the moment the questions turned inward. A reader who
discounts this residual on that basis is reading the paper correctly.

⛔ **The forbidden move, restated at the point where it would be tempting.** This is a Branch A
result. A residual we cannot presently account for is **not** evidence for Branch B, and no sentence
anywhere in this paper may explain a Branch A null or a Branch A residual by appeal to a
non-interacting biome. §13 item 1 holds. The cost of that rule is that this section ends without a
conclusion, and that is the correct place for it to end.

---

## §12 — ARCHIVE REACHABILITY, AND A NUMBER WE TOOK BACK

The previous sections asked whether an instrument could have seen something and whether the bin was
kept. This one asks a smaller question that turns out to sit underneath both: **when the public record
points at an exposure, is the exposure still there?**

It began as a favourable observation. Of the 55 exposures referenced by the alerts of 2018-06-01,
**15 are not retrievable from IRSA**, the archive of record — 27.3% of exposures, stranding 1,037 of
17,991 alerts, or **5.76%**. We wrote that down in June with a fence around it: *n = 55, one night,
may not be quoted as an archive property until re-measured on at least two.* The fence was cheap to
write because there was no reason to expect it to fire.

**It fired.** `PREREG-REACHABILITY.md` pinned the second night — 2018-06-02, deliberately adjacent so
that archive *epoch* was held fixed and only the night varied — and pre-committed three predictions
before the tarball was opened. R1: the miss reproduces at all. R2: the rate is within a factor of two
of 27.3%. R3: alert stranding stays below exposure loss.

**Night 2 returns zero. Zero of 32 exposures missing, zero of 19,446 alerts stranded.** R1 and R2 are
refuted; R3 compares two zeros and is uninterpretable, recorded as such rather than counted. Two of
two interpretable predictions failed, which makes this the only block in the program where nothing
held — and it is the block whose pre-registration said in writing that its direction was unknown.

⛔ **So the number is withdrawn as an archive property.** 5.76% is a fact about 2018-06-01. It is not
a rate, it is not a decay constant, and it may not be quoted as either.

**The obvious rescue was tested, and it failed too.** Within night 1, missing exposures are markedly
thinner than surviving ones — 47 alerts at the median against 348, 12 referenced images against 38 —
which invites the tidy story that archives lose marginal field-nights. Night 2's thinnest exposure
carries **11 alerts and one referenced image, and it is present**; thirteen of night 1's fifteen
missing exposures are richer than that. The correlation is real inside one night and does not
transfer. We report it because an untested rescue that sounds right is worse than no rescue: it would
have let the withdrawn number survive under a mechanism nobody measured.

**What survives is a different and better-shaped claim.** Night 1's losses are not scattered. They
fall in runs — five consecutive exposures missing with intact neighbours on both sides, then three,
then two — and, decisively, **field 000577 is present at one point in the night and missing at
another.** The same patch of sky, the same night, two outcomes. Whatever removed these products is
keyed to **when an exposure was processed**, not to where it pointed.

The honest reading is dull, and dullness is the correct register: on one night there were processing
intervals whose products never reached the archive, while the alert stream went on referencing them.
The next night has no such interval. **Reachability is episodic, not a rate.**

⛔ **What this is not.** A stranded alert is one whose difference image is unreachable. No missing
file was opened here, because a missing file cannot be opened — which is simultaneously the finding
and its ceiling. Nothing in this section is evidence that content was removed, that the removed
content differed from the retained content, or that anyone chose any of it. Archives lose things.

⚠ **Both nights are 2018 and adjacent by construction, so nothing here bears on whether older
holdings decay.** That leg was costed and not run.

The reason this section stays in a paper about a shadow biome is now methodological rather than
evidential, and it is the only lesson we would ask a reader to carry out of it: **a program that
plans to re-derive results from a public archive must measure reachability per epoch, because one
night said 27% and the next said zero.**

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

## §14 — BRANCH B HAS A FLOOR, AND THE FLOOR IS GRAVITY

Branch B is the version of the premise that puts the biome outside the electromagnetic channel
entirely — the reading that sounds unfalsifiable and is usually deployed as a refuge. This section
exists to close the refuge, and then to measure honestly how far short of closing it we fall.

**The argument that removes the refuge is short.** Life is dissipative. Anything alive maintains
itself against equilibrium, and maintaining requires exchanging something with something. "Lacking
interaction with matter" is therefore not a coherent property of a *biome*; it splits into two
readings, and both are reachable in principle. **B1 — weak coupling:** the interaction exists and is
small, which is a sensitivity problem, not a category problem. **B2 — own sector:** the constituents
carry no charge under our forces at all. **And B2 still gravitates**, because stress-energy is not
optional and gravity does not ask what sector a thing belongs to. So Branch B is a hard measurement,
badly funded, rather than an unfalsifiable category. That is the whole content of the argument and we
think it is correct.

**What it is worth is another matter, and the arithmetic is unkind.**

A superconducting gravimeter is the most sensitive static gravity instrument that exists. Set a
350-gram mass one metre from one and its Newtonian attraction is

> *GM/r²* = 2.34 × 10⁻¹¹ m s⁻² = **2.34 nGal** = 0.023 nm s⁻².

Our architecture recorded that as **2.34× the instrument's floor**, and the sentence is true. It is
also the wrong comparison, and we said so at the time without knowing by how much. **An instrument's
static resolution is not the floor a measurement stands on. The floor is what is left after the Earth
is subtracted, and the Earth is enormous.**

Computed from first principles rather than recalled: the degree-2 tidal acceleration at the sub-body
point is 2*GMR*/*d*³, giving **110 nm s⁻²** for the Moon and **50 nm s⁻²** for the Sun; multiplied by
the elastic gravimetric factor δ ≈ 1.16 the solid-Earth tide reaches **≈ 1,860 nm s⁻²**, which is
**80,000 times our signal**. That term is modelled and removed to high accuracy, so it is not itself
the floor — it is the scale of what has to be removed before a floor exists at all.

What remains after removal is measured, at real stations, and we take it from the literature rather
than estimating it. At Apache Point, where a superconducting gravimeter has been characterised against
GPS and hydrological modelling in support of lunar laser ranging, Crossley, Murphy & Liang report a
narrowband tidal-band residual noise of **0.017–0.037 μGal**, a mean error of fit after tidal and
pressure correction of **1.5–2.0 μGal**, and — after a local hydrology model removes more than 90% of
the seasonal variance — residual episodes still departing from that model by **up to 4 μGal**. Their
nominal barometric admittance is −3.0 nm s⁻² hPa⁻¹, fitted at −2.63. Antokoletz *et al.*, across five
European stations, put non-tidal ocean loading at an RMS of **2 nm s⁻²** at the most coastal site and
the inverted-barometer effect at **1.4 nm s⁻²** at the most inland one.

Against those numbers our 2.34 nGal signal sits:

| floor | value | signal is below it by |
|---|---|---|
| best narrowband tidal-band residual | 17–37 nGal | **7×–16×** |
| inverted-barometer effect, inland station | 140 nGal | 60× |
| non-tidal ocean loading, coastal station | 200 nGal | 86× |
| mean error of fit, broadband | 1,500–2,000 nGal | 640×–860× |
| departure from the hydrological model | up to 4,000 nGal | 1,700× |

**So the fence we wrote around this number — *sensitivity, not detection* — holds, and it now has a
size.** Depending on which band and which correction level a measurement can honestly claim, the
signal is between one and three orders of magnitude under the noise. It is not a near miss.

**The useful form of the result is the inversion, and it is the one sentence in this section a reader
should keep.** Requiring the signal to exceed the *best published residual* rather than the
instrument's resolution, the mass needed at one metre is

> **≈ 2.6 kg** to clear the narrowband tidal residual · **≈ 225 kg** to clear the broadband fit error,

scaling as *r*², so **≈ 23 kg at 3 m** and **≈ 255 kg at 10 m** against the narrowband figure. That
is a real bound and it is falsifiable in the direction that matters: **a persistent own-sector mass
concentration of more than a few kilograms, sitting within a metre of one of the world's
superconducting gravimeters, would already have shown up in the residuals.** It has not. We claim
nothing more from that than it can carry — the instruments are few, they are fixed, and their
sampling of the planet is negligible — but it is a measurement rather than a posture, and it is
available to anyone who wants to tighten it.

⛔ **No gravimetric detection claim is made anywhere in this paper, and none is available from this
section.** What is claimed is narrower and, we think, more useful: **Branch B is not exempt from
measurement, and the price of the exemption it usually claims is now written down in kilograms.**

---

## §15 — THE MENTAL REGISTER, THE INVERSION, AND A GATE THAT PASSED THE WRONG OBJECT

The premise has a second register. If the class is defined by its relation to the observer rather
than by a shared mechanism, then the human record of *anomalous perception* — the folklore, the
sightings, the reports made in altered states — is the obvious place to look, and it is the place
this program has most carefully avoided until now.

**The structural point has to come first, because it costs us.** Selected-for blindness predicts an
**absence** in the human record. A large, detailed, identity-rich folklore corpus is therefore
evidence **against** the mechanism, not for it. We committed that in both directions before consulting
anything (`PAPER-02-FALSIFIERS.md` F5), and it generates a forbidden move we hold to throughout:
**presence and absence may not be scored in the same corpus.** Taking the arm on which reports count
forfeits the arm on which their silence counts. One arm, chosen in advance.

The arm was chosen, and chosen by a criterion written before it was invoked. `PREREGISTRATION.md` §7d
pre-committed two readings — **F1**, a silent record, and **F2**, a record that is
altered-state-concentrated and identity-poor — and required any candidate corpus to be named in a
successor pre-registration written before it was opened. That successor exists
(`PREREG-CORPUS-F2.md`), it registers a mass-concentration gate **C5** to be run first and alone, and
it registers four predictions with failure conditions, one of which it declares unscorable on the
named corpus for circularity before looking at it.

**Then the gate ran, and the interesting thing happened.**

C5 asks whether the corpus is really one document wearing many filenames: if a single source holds
more than half the total word mass, no distributional claim may be made from it. Measured across
2,552 live files and 5.46 million words, the largest single file holds **1.59%**, the largest five
**6.1%**. The gate passes cleanly and, by its own pre-committed rule, licenses the scoring of C1–C4.

⛔ **We are not scoring them, because the object is inadmissible and the gate could not see it.**

The corpus named in the pre-registration is **our own**. Its README opens *"a unified intellectual
program built by Clayton Iggulden-Schnell and Clawd"*; 31% of its mass is one author's identity and
memory files, 30% is this program's technical work, 7% is the drafts of a book we wrote. It is a body
of analysis, produced by the two parties who hold the hypothesis. It is not a record of reports by
anyone else. F2's predictions are all statements about a record of reports — C1 wants motifs
recurring across *independent source clusters*, C3 wants the affect of a reported phenomenology, C4
wants the cost borne by *reporters* — and not one of them has a referent here.

**A name collision did it.** In the authors' working vocabulary "the Corpus" denotes that repository,
and the sentence admitting a corpus of anomalous reports as evidence was routed at the filing cabinet
that owns the word.

⭐ **The reason this is in the paper rather than quietly repaired is the branch it exposes.** Had C5
returned *void*, we would have written the right conclusion — *this corpus cannot carry the weight* —
for a reason that has nothing to do with why it is true, and never noticed. C5 passing is the
dangerous outcome, and what it licensed was not a null. The corpus contains a file titled *The
Comprehensive Catalog of Perspectival Beings*: a taxonomy of named entities, each rated across twelve
labelled dimensions on a five-point scale. C1's pre-committed failure condition reads *"fails if a
small set of stable, elaborated, cross-source-consistent named taxa carries the bulk of report
mass."* A faithful scorer would have found exactly that, marked **C1 refuted**, and recorded that the
record disqualifies its own subject — having measured our philosophical appendix and reported it as
the human record. The verdict would have been pre-registered, reproducible, dated, and confidently
wrong, with the pre-registration itself serving as the alibi.

**Nothing in the pre-registration failed.** It was written before opening, it stated its failure
conditions, it forbade the moves that would have rescued it, and it put its gate first. What it did
not do — what none of our gates did — is ask whether the named object is **the kind of thing the
predictions are about**. That question is upstream of every safeguard the file contains. A
pre-registration protects an inference from its data; it does not protect an object from its name.

**So this register is opened and unresolved, and the honest inventory is:** C5 ran and returned open,
reported with its numbers because a gate that ran is worth more on the record than a gate that was
skipped. **C1, C3 and C4 are unscored and are not nulls.** C2 remains owed for the separate reason of
selection circularity, which this defect neither causes nor repairs. **No claim about any folklore or
ethnographic record appears anywhere in this paper**, because nothing bearing on one was measured.

What is owed is a successor pre-registration against an actual report corpus — Thompson's
Motif-Index, HRAF, or a comparable collection — carrying a new admissibility gate **in front of** C5:
*is the object a record of reports made by parties independent of the hypothesis's authors?* That
gate did not exist. Its absence is the most instructive thing this section produced, and we would
rather publish it than the finding it nearly manufactured.

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

*⭐ **D203 / 2026-08-22 ~11:3x — THE LIST ABOVE IS NOW EMPTY, AND IT WENT STALE A THIRD TIME BEFORE
ANYONE EDITED IT.** §7, §8, §10 and §11 were drafted on D202 between ~23:5x and ~00:2x; the note kept
naming them undrafted for eleven hours. §12, §14 and §15 were drafted this morning. **Roster, read
off this file's own `## §` headings by `grep` and not off any prose: §1 §2 §3 §4 §5 §6 §7 §8 §9 §10
§11 §12 §13 §14 §15 — fifteen of fifteen, no gaps.** The fence about citation markers stands
unchanged and is not affected by completion.*

*⚠ **What completion does NOT mean, stated here because this is the line a reader will reach last.**
Three of the last four sections drafted report a **refutation or a retraction**, not a result: §12
withdraws its own headline number after the second night returned zero, §14 finds its gravimetric
signal one to three orders of magnitude under the environmental floor, and §15 rejects its own
pre-registered corpus as inadmissible after the gate designed to protect it passed. **The paper is
complete; the program is not vindicated by its completion, and no section may be read as though it
were.***



