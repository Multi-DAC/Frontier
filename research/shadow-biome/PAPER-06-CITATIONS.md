# PAPER-06 — THE CITATION LEDGER

*Opened D202 / 2026-08-21 ~22:2x PT. Clayton: **"let's start the reading pass."** This file is that
pass's record. It is not a plan for the pass; it is what reading the sources actually returned,
including the four places where the source **disagreed with the sentence it was fetched to support.***

**What the pass is.** `PAPER-03-DRAFT.md` carries `[◐ CITATION OWED]` markers — claims I believe and
had **not** read at a primary source. The convention was built so removing one is a **hand** action
that cannot happen by drafting past it. This pass goes and reads, then removes by hand, then records
here what the reading changed. **A marker may be removed in three ways and only three:**

- **✅ DISCHARGED** — read at the named source, claim stands as written.
- **⚠ AMENDED** — read at the source, and the **sentence had to change**. The amendment is quoted.
- **⛔ NOT DISCHARGED** — the source does not say it, or says the opposite. Marker stays or the claim goes.

---

## 0. TWO CORRECTIONS TO THE PROGRAM'S OWN BOOKKEEPING, BEFORE ANY SOURCE

**(a) The debt was 11, not 12.** `PAPER-00-ARCHITECTURE.md` §4 item 5 records that the draft "carries
**12** `[◐ CITATION OWED]` markers." `grep -c` returns 12 — because **one of them is the legend at
line 23**, which defines the convention using a literal `x` as its example. Eleven claims carry a real
debt. The count was a `grep` reported without reading what it matched, which is
`feedback_grep_derived_from_the_finding` in its cheapest possible form: a self-counting instrument
that counted itself.

**(b) The eight `[✅ PRIMARY]` grades in the draft were self-awarded and are NOT audited by this pass.**
This pass audits the ◐ pile only. A grade I gave myself is not evidence that I read the thing; it is
evidence that I remembered giving myself the grade. ⚠ **Stated as open, not resolved.** One of the
eight (Davies et al. 2009) is independently corroborated by the extraction artefact in
`sources/`; the other seven are not.

---

## 1. §1.1 — TOLERANCE VERSUS RESISTANCE

**Marker (line 85):** *plant-pathology origin + an animal-host tolerance case.*

**READ:** Råberg, L., Graham, A.L. & Read, A.F. (2009). "Decomposing health: tolerance and resistance
to parasites in animals." *Phil. Trans. R. Soc. B* **364**(1513):37–49. DOI 10.1098/rstb.2008.0184.
[✅ PRIMARY — full text, PMC2666700, D202]

**Both halves of the debt are discharged by this one source**, which is why it is the citation and not
two:

> "Plant biologists have long recognized that defence can be decomposed into these two components
> (Cobb 1894 cited in Schafer 1971; Caldwell *et al.* 1958; Clarke 1986), and have called them
> resistance and tolerance, respectively."

> "Resistance is typically measured as the inverse of infection intensity… Tolerance, on the other
> hand, is usually operationally defined as the slope of a regression of host fitness against
> infection intensity; the steeper the slope, the lower the tolerance."

Animal case named by the source: **Råberg *et al.* 2007**, *Plasmodium chabaudi* in laboratory mice —
the first test of tolerance in an animal host under the reaction-norm framework. Cost-of-response
mechanism, verbatim:

> "In many human diseases, a considerable proportion of the harm is due to the host's immune response
> rather than a direct effect of the parasite replicating in host tissue."

### ⚠ AMENDED — and this is the pass's most substantive catch on §1.1.

**Tolerance is not blindness.** A tolerant host still *detects* the parasite; its immune system is not
switched off, and in several tolerance models it is demonstrably engaged. What tolerance limits is
**damage per parasite**, not perception of the parasite. The draft's bullet reads "hosts that evolve
*not to respond*" — that is accurate — but the bullet sits under a heading arguing for evolved
**non-perception**, and a sympathetic reader will slide the one into the other for free.

**The amendment, and it costs us nothing to make:** the tolerance literature is cited for
**non-response**, explicitly *not* for non-detection, with the difference stated in the sentence
rather than left to the reader. Selection against *responding* is documented. Selection against
*perceiving* is the paper's conjecture, and the whole value of §1.1 is that the four literatures are
**ingredients** — the draft already says the premise "is a conjunction of the ordinary claims in
them." That sentence is now load-bearing, and each bullet has to be honest about which ingredient it
supplies.

---

## 2. §1.1 — ERROR MANAGEMENT UNDER ASYMMETRIC PAYOFFS

**Marker (line 89):** *signal-detection formulation with asymmetric loss.*

**READ:** Nesse, R.M. (2019). "The smoke detector principle: signal detection and optimal defense
regulation." *Evolution, Medicine, and Public Health* **2019**(1):1. DOI 10.1093/emph/eoy034.
[✅ PRIMARY — full text, PMC6343816, D202]

The rule, verbatim: **"fitness is maximized by expressing a response whenever pD > CR/CD"** — where
CR is the cost of the response and CD the cost of failing to respond when danger is present.

### ⛔ NOT DISCHARGED AS WRITTEN — THE CITED LITERATURE RUNS THE OTHER WAY.

The draft's bullet says: *"when a false alarm costs more than a miss, the optimal detection threshold
is set so that an entire stimulus class is reliably missed."* The entire smoke-detector literature
treats the **opposite** case — cheap false alarms, expensive misses, therefore *over*-response. Nesse
gives **no formula, discussion or example** for the direction we need. Haselton & Buss (2000), the
EMT origin, is likewise built on biases toward the *less* costly error in a domain where the cheap
error is the false positive.

**What is true and what I am allowed to say:** the inverse is a **corollary of Nesse's own
inequality, derived by us** — as CR/CD grows large the required pD approaches 1 and the class is
reliably missed. That is arithmetic on his rule, not a finding in his paper, and
`feedback_unchecked_clause_costs_nothing_to_write` is exactly what shipping it unmarked would have
been. **Amendment: cite the inequality, state that we are running it in the under-explored direction,
and say so in the sentence.** The bullet gets *weaker* and the paper gets *more* defensible, because
a breaker who knows this literature will reach for the smoke-detector asymmetry first and find we
already named it.

---

## 3. §1.1 — SENSORY GATING

**Marker (line 91):** *(bare).*

**READ:** thalamic reticular nucleus gating literature, survey level. The TRN is entirely GABAergic
and exerts inhibition onto thalamic relay nuclei; sensory gating is an **active inhibitory** process,
not an absence of input. That half stands.

### ⚠ AMENDED — "METABOLICALLY FUNDED" IS MINE, NOT THE LITERATURE'S.

The draft says the organism "**spends energy** *not* to perceive." The gating literature is
anatomical and functional; it does **not** cost the inhibition in ATP. And the neural energy-budget
literature cuts slightly against the rhetorical weight: the large share of signalling cost is
attributed to **excitatory** postsynaptic currents, with inhibition a small fraction.

**Amendment:** keep "active suppression upstream of awareness" (sourced). Drop "metabolically
funded" and "spends energy" unless a specific energetic measurement is produced. ⚠ **The reason to
care is that the energy framing is what makes gating look like an *adaptation with a price tag*, and
the price tag is the part I cannot source.** That is precisely the load-bearing clause, so it is
precisely the one that cannot stay on a hunch.

---

## 4. §1.1 — THE VIGILANCE–FORAGING TRADEOFF

**Marker (line 93):** *(bare).*

**READ:** Lima, S.L. & Dill, L.M. (1990). "Behavioural decisions made under the risk of predation: a
review and prospectus." *Can. J. Zool.* **68**:619–640. Supporting: Lima 1987; McNamara & Houston 1992.
[⚠ SECONDARY — citation and finding verified through the reviewing literature; the 1990 review itself
was not opened at source this pass. Marked, not laundered.]

The cost of vigilance is well established: vigilance interrupts search and handling and reduces
intake rate; vigilance and feeding are treated as competing allocations of a fixed budget.

### ⚠ AMENDED — same shape as §1.1's other three.

The literature establishes **attention is costly**. The draft's second sentence — *"Detection with no
available response is pure cost"* — is the paper's **argument**, not the review's finding. Lima & Dill
are about attention paid to threats one *can* act on. Extending that to a class one *cannot* act on is
our step. It is a reasonable step. It is not a citation.

**The pattern across all four §1.1 bullets, stated once so §1.1 can carry it in one sentence rather
than four:** every one of the four literatures supplies an **ingredient** and none supplies the
**conjunction**. Tolerance gives non-response, EMT gives cost-asymmetric thresholds, gating gives
active suppression, vigilance gives the price of attention. The premise is the conjunction. The
draft already asserts this; the pass establishes it was true, at the level of each individual source,
by going and looking. **That is worth more to the paper than four clean citations would have been**,
because a hypothesis paper that says exactly how much its literature does and does not carry is doing
the thing the genre is for.

---

## 5. §2 — CRYPTIC SPECIES

**Marker (line 154):** *a review giving the definition and a documented magnitude.*

**READ (magnitude):** Pfenninger, M. & Schwenk, K. (2007). "Cryptic animal species are homogeneously
distributed among taxa and biogeographical regions." *BMC Evol. Biol.* **7**:121.
DOI 10.1186/1471-2148-7-121. [✅ PRIMARY — full text, PMC1939701, D202]

Definition, verbatim: **"two or more distinct but morphologically similar species that were classified
as a single species."** Magnitude, verbatim: **2,207 cryptic species reports** drawn from **771,931
studies** suitable to detect them, Zoological Record 1978–2006.

**READ (review/definition):** Bickford, D., Lohman, D.J., Sodhi, N.S., Ng, P.K.L., Meier, R., Winker,
K., Ingram, K.K. & Das, I. (2007). "Cryptic species as a window on diversity and conservation."
*Trends Ecol. Evol.* **22**(3):148–155. [⚠ SECONDARY — PubMed served a cookie notice, not the
abstract; citation verified, text not read. Marker downgraded, not removed.]

### ⚠ AMENDED — THE BEST MAGNITUDE SOURCE CUTS AGAINST OUR SENTENCE.

The draft says cryptic species "reorganised diversity estimates **in several groups**." Pfenninger &
Schwenk's headline finding is the opposite shape: the proportion is **homogeneously distributed**
across metazoan taxa and biogeographical regions once corrected for species richness and study
intensity, and they conclude cryptic diversity **"can be treated as random error in biodiversity
assessments."** No taxon and no biome is specially cryptic.

**Why I am keeping it anyway, and why the amendment makes it stronger.** Homogeneity does not
weaken the precedent — it **generalises** it. The kind is legitimate and it has members *everywhere*,
rather than in a few charismatic pockets where one might suspect a taxonomist's attention rather than
nature's structure. A uniform base rate is a **better** analogue for a class we cannot pre-localise
than a clumped one would be. But the sentence has to say what the source says, and the source says
uniform.

---

## 6. §2 — DARK TAXA

**Marker (line 159):** *(bare).*

**READ:** Ryberg, M. & Nilsson, R.H. (2018). "New light on names and naming of dark taxa." *MycoKeys*
**36**:49–54. [⚠ SECONDARY — title, authors, year, journal and the operative definition verified;
full text not opened at source this pass.]

### ⚠ AMENDED — WRONG FIELD.

The draft calls dark taxa "the working name, **in molecular ecology**." The term's home is
**mycology** specifically — fungi known only from sequence, unlinkable to any physical specimen or
resolved name, and therefore absent from legislation and species counts. It has since spread. The
amendment names the field of origin, because a reader in molecular ecology who has never heard the
phrase is a reader who has just found our first sloppy sentence.

---

## 7. §2 — THE CANDIDATE PHYLA RADIATION

**Marker (line 163):** *the metagenomic paper that made the radiation visible + a diversity figure.*

**Diversity figure — in the title of the paper itself:** Brown, C.T., Hug, L.A., Thomas, B.C., Sharon,
I., Castelle, C.J., Singh, A., Wilkins, M.J., Wrighton, K.C., Williams, K.H. & Banfield, J.F. (2015).
**"Unusual biology across a group comprising more than 15% of domain Bacteria."** *Nature*
**523**(7559):208–211. Proposed **at least 35 candidate phyla** within the CPR from ~800 genomes.

**The paper that made it visible:** Rinke, C. *et al.* (2013). "Insights into the phylogeny and coding
potential of microbial dark matter." *Nature* **499**:431–437 — the source of the term *microbial dark
matter*, and the support for the draft's "around 2013."

[⚠ SECONDARY — *Nature* served an auth redirect at `nature.com/articles/nature14486`; title, volume,
issue, pages and the >15% figure were verified through indexing, **not read at the article.** The
marker is downgraded to ⚠ and stays visible. It can be discharged with one PDF.]

**Claim stands as drafted.** ✅ on the substance — the class was defined by an instrument limitation
(culturability), and a device that did not share the limitation found members, which is exactly the
precedent §2 is buying.

---

## 8. §2 — TOO SMALL: LEEUWENHOEK

**Marker (line 176):** *(bare).*

**READ:** van Leeuwenhoek, A. (1677). "Observations, communicated to the publisher by Mr. Antony van
Leewenhoeck, in a dutch letter of the 9th Octob. 1676… concerning little animals by him observed in
rain- well- sea- and snow water; as also in water wherein pepper had lain infused." *Phil. Trans. R.
Soc.* **12**:821–831. DOI 10.1098/rstl.1677.0003. Leeuwenhoek's **Letter 18**.

> "In 1675 I discovered living creatures in Rain water which had stood but few days in a new earthen
> pot, glased blew within."

### ✅ DISCHARGED — with a date trap disarmed on the way past.

**"18 October 1676" is a corruption that appears in the secondary literature.** The **18** is the
**letter number**; the date is **9 October 1676**, and the *publication* is 1677. Three numbers, three
different roles, and the draft says only "1670s" — so it was never wrong, but it was one specific
sentence away from being wrong in a way a historian of science would enjoy. Pinned here so the
citation cannot acquire the error later.

⚠ **One word of the draft is amended:** "in water people had been drinking." Leeuwenhoek's find was in
**rain, well, sea and snow water and a pepper infusion**. Well and rain water are drinking water; sea
water is not. The sentence keeps its force with "in rain and well water" and stops overreaching.

---

## 9. §2 — INAUDIBLE: THE BAT/MOTH ARMS RACE

**Marker (line 181):** *(bare).* The draft calls this **"the closest analogue in the paper."**

**READ:** Conner, W.E. & Corcoran, A.J. (2012). "Sound Strategies: The 65-Million-Year-Old Battle
Between Bats and Insects." *Annu. Rev. Entomol.* **57**:21–39. DOI 10.1146/annurev-ento-121510-133537.
[✅ PRIMARY — full PDF, 71,499 characters extracted with `pypdf`, D202]

> "The frequency of the echolocation calls varies from 8 to 215 kHz depending on the bat species."

> "Tympanic organs (ears) sensitive to ultrasound have evolved multiple times in nocturnal Lepidoptera
> and exist in nearly half of extant species."

> "Insect ears have evolved in at least 7 of 27 insect orders."

### ⛔ THE SOURCE FALSIFIES OUR SENTENCE, AND IT IS THE SENTENCE WE CALLED OUR BEST ONE.

The draft says the interaction takes place "at a frequency **we do not transduce**." The band runs
from **8 kHz**. Human hearing extends to roughly 20 kHz. **The bottom of the bat band is inside human
hearing** — audibly so; low-frequency bat calls are heard by children and by some adults, and the
species that use them are not exotic.

**Amendment, mandatory before this section ships:** *most of the band, not the band.* The correct
claim is that the interaction is conducted **largely above human hearing**, that the strongest
examples sit well above 20 kHz, and that the human bound is a **boundary crossed by part of the
phenomenon**, not a wall the whole phenomenon hides behind.

⚠ **And notice which sentence it was.** The draft singles this bullet out as *"the closest analogue in
the paper"* — the one carrying the most rhetorical weight in §2 — and it is the one that overstated.
`feedback_scrutiny_is_motive_shaped`: the sentence I liked best got the least checking, and it only
got checked at all because the reading pass is indiscriminate by construction.

**What the source gives back, and it is worth more than the sentence cost:** the numbers are far
better than the prose was. **7 of 27 insect orders** have independently evolved ears. Ultrasonic
tympanal organs exist in **nearly half of extant nocturnal Lepidoptera**. **65 million years.** That
is not "a thing we happened not to hear" — it is a coevolutionary arms race with a fossil-scale
duration and convergent origins across a quarter of the insect orders, and humans stood inside it,
outdoors, at dusk, for the whole of our existence. The corrected sentence is stronger than the wrong
one was.

---

## 10. §2 — WRONG TIMESCALE: DARWIN ON PLANT MOVEMENT

**Marker (line 183):** *(bare).*

**READ:** Darwin, C., **assisted by Francis Darwin** (1880). *The Power of Movement in Plants.*
London: John Murray. [✅ PRIMARY — title page and Introduction, Darwin Online F1325, D202]

Title page, verbatim: **"BY CHARLES DARWIN, LL.D., F.R.S. — ASSISTED BY FRANCIS DARWIN."** The
method, verbatim:

> "A glass filament, not thicker than a horsehair, and from a quarter to three-quarters of an inch in
> length, was affixed to the part to be observed by means of shellac dissolved in alcohol."

> "dots were made on the glass-plate with a sharply pointed stick dipped in thick Indian-ink. Other
> dots were made at short intervals of time and these were afterwards joined by straight lines."

### ✅ DISCHARGED — and the *method* is the citation, not any sentence of Darwin's.

Darwin does not write "this is invisible to the attention span." **He builds an instrument that
accumulates the movement across hours and joins the dots into a line** — a filament, a glass plate, an
ink dot at intervals, a traced curve. The evidence for our claim is the *existence of the apparatus*:
circumnutation had to be **integrated over time to become perceptible at all**, which is precisely the
obscuration mode the bullet names.

⚠ Two amendments: the co-author goes in (it is on the title page), and the interpretive clause is
marked as ours — **the apparatus is the finding; "slower than the observer's attention span" is our
gloss on why the apparatus was necessary.**

---

## 11. §2 — OUT OF BAND: PIT ORGANS AND UV SIGNALLING

**Marker (line 186):** *(bare).*

**READ (infrared):** Bullock, T.H. & Cowles, R.B. (1952). "Physiology of an infrared receptor: the
facial pit of pit vipers." *Science* **115**:541–543. [⚠ SECONDARY — citation verified, text not
opened.]

**READ (ultraviolet):** Bennett, A.T.D., Cuthill, I.C., Partridge, J.C. & Maier, E.J. (1996).
"Ultraviolet vision and mate choice in zebra finches." *Nature* **380**:433–435. Waveband **300–400
nm**; females preferred UV-reflecting males over males whose UV reflection was removed.

### ⭐ PROMOTE THIS ONE. IT IS DOING MORE WORK THAN THE DRAFT LETS IT.

The Bennett *et al.* abstract makes a claim about **scientific practice**, not just about birds: that
humans have been used to assess 'colour' and this **may be flawed**, because many birds see in the
ultraviolet — *to which humans are blind* — and have at least four spectral cone classes.

**That is this paper's whole thesis, already published, in a domain where it was settled by
experiment.** A biological signal was measured by human observers; the human aperture silently
determined what counted as the signal; a device without that aperture found the measurement had been
missing a channel that the animals were *using to choose mates*. Not a curiosity — **a documented case
of human sensory blindness corrupting a scientific measurement and being caught by an instrument.**

The draft's bullet says only that these channels "were unavailable to us until an instrument was
pointed at them." ⚠ **Amendment: say the stronger true thing.** The bullet is retitled around the
zebra finch result and the pit organ becomes the second example.

---

## 12. THE FIFTH HISTORICAL MEMBER — STILL OPEN, AND I DID NOT TRY

`PAPER-03-DRAFT.md` names a fifth candidate for the historical series — *"too big or too diffuse to be
recognised as an entity"* — as **the weakest member**, retained only if a citation can be produced and
otherwise dropped. The draft's own rule is that the decision **has to be made rather than defaulted
into.**

⛔ **I did not search for it this pass.** No decision is recorded, and I am explicitly **not**
recording "dropped for want of a citation," because that sentence would claim a search that never ran
— the exact shape of `feedback_test_passes_by_not_running`. **It remains owed**, and it is now the
only item in §2 with no reading behind it.

---

## 13. WHAT THIS PASS COST THE PAPER, TALLIED HONESTLY

**11 markers. 4 discharged clean. 5 amended against the source. 1 refuted outright. 1 never attempted.**

| # | Claim | Verdict |
|---|---|---|
| 1 | Tolerance/resistance | ✅ sourced · ⚠ non-**response**, not non-**detection** |
| 2 | Error management | ⛔ literature runs the **opposite** direction; ours is a derived corollary |
| 3 | Sensory gating | ⚠ "metabolically funded" unsourced, struck |
| 4 | Vigilance–foraging | ✅ cost of vigilance · ⚠ the unactionable-class step is ours |
| 5 | Cryptic species | ✅ 2,207/771,931 · ⚠ **homogeneous**, not concentrated |
| 6 | Dark taxa | ⚠ mycology, not molecular ecology |
| 7 | CPR | ✅ substance · ⚠ >15% figure not read at *Nature* |
| 8 | Leeuwenhoek | ✅ · ⚠ "water people had been drinking" narrowed to rain and well |
| 9 | Bat/moth | ⛔ **8 kHz is audible** — "a frequency we do not transduce" is false as written |
| 10 | Darwin | ✅ apparatus quoted · ⚠ co-author, and the gloss is ours |
| 11 | Pit organs / UV | ✅ · ⭐ **understated** — promote |
| — | Fifth member | ⛔ **not attempted**, still owed |

**Four claims got weaker. Two got stronger. One died.** The ledger is the paper's, not mine — the two
directions are the point. A reading pass that only ever confirmed would be
`feedback_gauge_can_only_render_its_good_news` wearing a bibliography.

⚠ **And the shape of the failures is not random.** The two hardest hits — the bat band and the
smoke-detector direction — landed on the **two sentences the draft was proudest of**: the one it calls
"the closest analogue in the paper," and the one that supplies §1.1's mechanism. The sentences I would
have defended in conversation are the sentences that had never been checked, because conviction
substitutes for verification precisely where conviction is highest. **That is the argument for handing
this to Clayton's human breaker, and it is now an argument with data behind it.**
