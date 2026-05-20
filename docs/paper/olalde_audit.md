# Olalde citation audit (DIA-25063.pdf)

> Audit list for the prose instance. Every Olalde reference (and every
> "limited northern ancestry" claim) in the canonical submission PDF,
> flagged for rewriting under the bounded-genetics framing per
> CLAUDE.md:
>
> - Olalde et al. 2023 reports **~30–60 % Slavic-related ancestry** in
>   modern Balkan populations as one of the *largest permanent
>   demographic changes* in Migration-Period Europe — not "limited
>   northern ancestry (10–30 %)".
> - Ancestry proportion is bounded evidence: it ≠ migrant count, ≠
>   tempo, ≠ direction. aDNA tells us *that* admixture occurred, not
>   when, how fast, or in which direction.
> - The linguistic outcome (~80 %+ Slavic) **exceeds** the genetic
>   admixture (~30–60 %), so genetics alone cannot be the whole story
>   regardless of which way the paper goes on migration vs. substrate.
>
> Source: text extracted from `DIA-25063.pdf` into
> `dia25063_text.txt` for line lookup. PDF page numbers are from that
> extract (the published Diachronica page numbers may differ by a
> running-header offset; see "Note on page numbering" at the end).

## Findings

### Finding 1 — Introduction (PDF page 4, lines 197–199)

> "[…] mass migration alone cannot explain the observed linguistic
> dominance. Instead, a proto-Slavic substrate—pre-existing
> Slavic-speaking populations in the Balkans—provides a viable
> alternative, as it aligns with genetic evidence showing **limited
> northern ancestry (10–30 %)** in modern Balkan populations and the
> archaeological record's lack of widespread settlement sites
> indicative of massive influxes (Curta 2001; Barford 2001; Olalde
> et al. 2023)."

**Problem.** Two distinct misreadings stacked:

1. The figure is **wrong**. Olalde et al. (2023) reports ~30–60 %
   Slavic-related ancestry in modern Balkan populations, not 10–30 %.
   The 10–30 % figure does not come from Olalde and the citation does
   not support it.
2. The framing "**limited** northern ancestry" inverts Olalde's own
   conclusion. The paper describes the Slavic-period admixture as one
   of the largest permanent demographic changes in Migration-Period
   Europe.
3. Co-cited as if it supported the substrate hypothesis. Olalde
   neither adjudicates substrate vs. migration nor measures linguistic
   dominance — it bounds *that* substantial admixture occurred,
   nothing about tempo, count, or which population was Slavic-speaking
   at which date.

**Rewrite direction.** Replace with the bounded-genetics framing
(headline claim is the negative result about logistics + demography;
genetics is consistent with substantial admixture having occurred but
does not adjudicate the mechanism). Drop "10–30 %" entirely. Drop the
"limited northern ancestry" framing.

---

### Finding 2 — Methods §2.2 Spatial Framework and Initialization (PDF page 5, lines 285–293)

> "A 50×50 grid (2,500 cells) represents ~5 million individuals.
> Initial Slavic: 10 % (eastern/central Europe); Illyrian/Thracian:
> 30 % (Balkans); Greek: 20 %; Germanic: 20 %; Avar: 10 %; Other:
> 10 %. […] **These settings are based on genetic studies estimating
> pre-migration Balkan populations at ~4.5 million non-Slavic (Olalde
> et al., 2023; Ralph and Coop, 2013)**, with group fractions derived
> from ethnographic and historical reconstructions (Curta, 2001;
> Barford, 2001)."

**Problem.** Olalde is cited here as an authority for an **absolute
demographic count** ("~4.5 million non-Slavic pre-migration"). Olalde
is an ancient-DNA study; it measures ancestry composition, not
headcount. Population-size estimates for the early-medieval Balkans
come from demographic-history sources (Russell 1987, Campbell 2016,
Treadgold's Byzantine demography work), not aDNA. Ralph and Coop
(2013) is also a genetic-ancestry paper, not a demographic-count
source — same misuse.

**Rewrite direction.** Cite the population scale to the actual
demographic literature (Russell 1987 is already in the bibliography
as ref 9; add Treadgold or Campbell for the Balkan figure). Keep
Olalde out of this paragraph entirely — it doesn't speak to absolute
counts.

---

### Finding 3 — Discussion §4 (PDF page 9, lines 663–664)

> "[…] consistent with:
> • Archaeological continuity and the absence of widespread new
>   settlements (Curta 2001; Barford 2001);
> • **Genetic continuity showing limited northern ancestry (10–30 %)
>   in modern Balkan populations (Olalde et al. 2023; Ralph and Coop
>   2013);**
> • Demographic constraints known for the early medieval period
>   (Russell 1987; Campbell 2016)."

**Problem.** Same misreading as Finding 1, in a different position in
the paper. The bullet leads with "**continuity**" — a substrate-
favouring frame — and supports it with the misquoted 10–30 % figure.
Under the actual Olalde numbers (30–60 % Slavic-related ancestry),
this bullet would read as evidence *for* substantial population
turnover, not continuity. This is the citation most load-bearing for
the substrate argument, and it is the one most clearly inverted.

**Rewrite direction.** This bullet has to be rewritten to reflect
bounded genetics. Most honest version: "Genetic evidence (Olalde et
al. 2023) confirms substantial demographic admixture in the
Migration Period (~30–60 % Slavic-related ancestry in modern Balkan
populations) but does not adjudicate the mechanism, tempo, or
direction of that admixture, and the genetic admixture proportion is
substantially **lower** than the linguistic outcome (~80 %+), so
genetics alone cannot account for the language shift on either the
migration-maximalist or substrate reading."

This is the key paragraph for the new abstract's claim structure.

---

### Finding 4 — References list (PDF page 10, lines 764–765)

> "3. Olalde, Iñigo, et al. 'A Genetic History of the Balkans from
> Roman Frontier to Slavic Migrations.' *Cell* 186, no. 25 (2023):
> 5472–5485.e9."

**Problem.** None — bibliographic entry is correct. Keep.

Suggestion only: consider adding the e-locator / DOI in the rewrite
pass; *Cell* uses article numbers and DOIs for indexing.

---

### Finding 5 — Code comment, Appendix A (PDF page 13, line 1125 of extract)

In the printed code listing, the substrate-flag block reads:

> `GROUPS["slavic"]["initial_fraction"] = 0.3  # Justification:
> Proto-substrate hypothesis (genetics 10-30 % ancestry)`

The comment is **still present in the canonical script**
(`slavic_migration_submited_v1.py`, the substrate block inside
`run_simulation`), inherited from the published code listing.

**Problem.** Same 10–30 % misreading, now in the code as a parameter
"justification". A reviewer cross-checking code against text will see
the misreading reinforced.

**Rewrite direction.** Two options:

1. **Conservative.** Update the comment in `slavic_migration_submited_v1.py`
   to read: `# Substrate proportion is a free parameter; we sweep
   0/10/20/30/40/50 %. Genetics (Olalde 2023) bounds total Slavic-
   related admixture at ~30–60 % but does not constrain the
   pre-migration substrate fraction.`
2. **Stronger.** Replace the comment AND delete the literal `0.3`,
   replacing it with a CLI-overridable parameter so the substrate
   response curve from batch 2 lives in the code structure, not a
   hard-coded default. This is queued under batch 2 anyway.

Either way, the standing comment is wrong and should not survive the
rewrite pass.

---

## Cross-cutting recommendations

- **No Olalde citation should support a substrate-favouring claim
  without explicit qualification.** The genetics tells us substantial
  admixture occurred; it does not tell us *which* population
  contributed the Slavic-speaking layer (incoming migrants vs.
  pre-existing locals) or in what proportion.
- **No "limited northern ancestry" phrase should survive the rewrite.**
  Olalde's actual conclusion is the opposite — a large permanent
  ancestry shift. The misreading appears in at least two places
  (Findings 1 and 3); search-and-flag for any remaining instances if
  the manuscript is reorganised.
- **The genetics ≠ headcount move (Finding 2) is worth a sentence in
  Methods.** A reviewer who knows aDNA will flag it. The current
  Methods §2.2 citation looks like aDNA-as-demography; the rewrite
  should source population size to demographic history, not to Olalde
  or Ralph–Coop.
- **The 30–60 % vs. 80 %+ asymmetry is an argument the paper isn't
  yet making.** Linguistic dominance exceeds the genetic-admixture
  proportion by a wide margin in the modern populations. That is itself
  evidence against migration-as-sole-mechanism, independent of any
  ABM result, and complements the Arabic gap (the ~15 pp upper bound
  on combined institutional + bilingual contributions): linguistic
  dominance can exceed genetic contribution when non-demographic
  mechanisms align with the incoming language. Worth a sentence in
  Discussion. (NB: "institutional premium" framing is *not yet*
  defensible — that 15 pp combines institutional reinforcement and
  bilingual transitional states and cannot be separated without the
  bilingualism workstream; see `response4.md`.)

## Status

This is the audit list. The actual rewrite is for the prose instance
(Claude.ai, not Claude Code). The code-comment update in Finding 5 is
a one-line code change and can be done by Claude Code on request —
not done yet because it touches the canonical script and the prose
instance may want to coordinate the comment text with the rewritten
Methods passage.

## Note on page numbering

PDF page numbers above refer to positions in `dia25063_text.txt`
(extracted with `pypdf` from `DIA-25063.pdf`). The page anchors in
that file are at extract-text lines:

| extract page | extract line | section / role                            |
|--------------|--------------|-------------------------------------------|
| 1            | 1            | Title / abstract                          |
| 4            | 169          | Introduction (continues §1)               |
| 5            | 274          | Methods §2.2                              |
| 9            | 660          | Discussion / §4 conclusion bullets        |
| 10           | 763          | References                                |
| 13           | 1089         | Appendix A code listing (start)           |

These will align with the published Diachronica page numbers if and
when the manuscript is re-typeset for resubmission; for now the
internal extract is the authoritative source for the prose
instance's rewrite pass.
