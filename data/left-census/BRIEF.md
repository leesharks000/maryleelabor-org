# Brief: write left-politics-and-labor census rows from saved sources (Mary Lee Labor meta-aggregator, 2026-10-31)

Repository /home/claude/fleet/maryleelabor-org. Do not run git. Do not fetch anything: every source has already been fetched once and saved verbatim. Write only your rows, as new files data/left-census/rows/<slug>.py, one per entity you are given.

## Read first
1. data/left-census/census_src.py: the driver. It defines row(), Q(), the six areas and the evidence kinds, the required fields, and the verbatim check. Read its docstring: the organizing question comes from the research report Ils ne sont pas marxistes (#1725), text at /home/claude/alexanarch/data/texts/AXN-0B50-text.md; read its Conclusion and its section 'What held critique' before writing.
2. The exemplar census this follows: /home/claude/fleet/laborvector/data/labor-census/ (census_src.py and rows/). Read three rows whole (turkopticon, data-workers-inquiry, fairwork-cloudwork) for register: short field values, quotes carried in evidence, untested or unrecorded things said plainly, negative tags that keep the resource apart from what it is mistaken for.
3. Your entities' saved sources: data/left-census/sources/<slug>--<id>.txt (the text) with sources/manifest.json (url, http, sha256). source-list.json says which ids belong to which entity. A source with http 403 or almost no text is unread; say so in unchecked, and never quote it.

## Each row (a single row(...) call in rows/<slug>.py)
- slug (given), name (the resource's own name), aka, url (its own canonical page), operator (who runs it, as its sources say), kind (what it is in its own words: archive, library, digital edition, database, tracker, publication, organisation...).
- areas: one or more keys of AREAS, primary first, only where its sources make it bear on that area.
- evidence_kind: one or more of EVIDENCE_KINDS, for the kind of record it actually holds.
- unit: its own unit of record (a text, a document, a collection, a strike event, a membership estimate, a case...).
- record_object: what it records, as its sources say (whose writings, which movements, which actions, which period).
- record: {"keeps": whose record it keeps, "holder": who holds it and on what terms (ownership, license, access, volunteer or institution), "losing_side": whether and how it keeps minority positions, splits, expulsions, dissent, rival tendencies and defeated programmes, AS ITS OWN SOURCES SHOW (e.g. a section of anti-revisionist splinter groups, a faction's bulletin, a "deviations" index), or "not recorded"}. This is the census's organizing question; do not supply what the sources do not show.
- method (how it gathers: volunteer transcription, scholarly edition, deposit of papers, news-derived event coding, survey microdata...), coverage {"geography", "period"}, count {"value", "as_of"} where stated.
- holdings: its holdings or headline content as it states them, short, each figure backed by an evidence item. stated_limits: its own stated limits (quote them).
- answers / does_not_answer: two short lists of questions its record can and cannot settle, exact to its method.
- ml_reading: one or two sentences, the archive's reading, on where the resource meets #1725's question (an organ that keeps a defeated critique stated; a holder independent of the body criticized; a route by which a position could be taken up later), or "none stated". Keep the resource's own terms intact.
- data_access, license (as stated), lifecycle {"state": active | historical | paused | ended, "detail"}, founded where stated, version_and_time {"...": date, "read": "2026-10-31"}.
- negative_tags: "NOT ..." lines that keep it apart from what it is mistaken for or a stronger claim than it makes.
- evidence: {field_key: Q("<slug>--<id>", "<verbatim quote>")}. Every figure, date, limit and self-description is backed here; quotes verbatim from the saved .txt. basis "third_party" for a source not the resource's own.
- relations: [{"rel": "neighbour" | "part_of" | "has_part" | "uses" | "used_by", "target": "<another slug in ORDER>", "note"}] only where the sources support it (EROL is part of the Marxists Internet Archive, for example, if its pages say so).
- unchecked: what you could not read.

## Prose
Plain declarative English. Do not write "not X but Y", "X, not Y", "rather than" or "instead of" outside quotations; state the thing directly. No gendered generics. No hard line breaks inside values.

## Check
Run `cd data/left-census && python3.12 census_src.py`. It prints problems for every row present; fix yours (missing fields, unknown keys, a quote not found) until your rows show none. Other readers' rows may appear; ignore their problems.

Final message: your rows, each with its intersections, evidence kinds and lifecycle; sources you could not use; anything a row could not record; and any resource whose sources make it look misplaced in this census.
