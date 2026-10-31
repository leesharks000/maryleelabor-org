"""The left-politics-and-labor census, first batch (2026-10-31). Writes census.json.

Operator, 2026-10-31: maryleelabor needs a meta-aggregator, "probably as a separate page, on specifically left politics and labor,
distinct from the focus of labor vector, more in line with the present focus"; "perhaps labor vector itself could be one of the
aggregator sources"; "lets also include one or two of the large marxist writing archives online". The present focus is the research
report Ils ne sont pas marxistes (#1725, AXN:0B50): the left's capacity to hold internal critique, and what keeps a defeated position
in the record. Organizing question, taken from #1725's conclusion: whose record does the resource keep, who holds it, and does it keep
the losing side (minority positions, splits, expulsions, dissent) in a form that could be taken up later?

Each row is written in rows/<slug>.py from the saved sources only (sources/, dated and hashed in sources/manifest.json). Every quoted
value is checked verbatim (whitespace-normalised) against the saved text of its source. A resource's own terms are kept as its own;
where it meets #1725's question is stated separately, in ml_reading, as the archive's reading.
"""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
MAN = json.load(open(HERE / "sources/manifest.json"))

AREAS = {
    "texts-of-the-tradition": "Texts of the tradition: primary writings of Marx, Engels and the socialist movements, in editions and translations",
    "movement-documents": "Movement and party documents: programmes, polemics, internal bulletins, periodicals, the record of splits",
    "archives-and-custody": "Archives and custody: collections of papers and records of labor and the left, held for later readers",
    "labor-action": "Labor action: strikes, stoppages and protest events, counted and described",
    "worker-power": "Worker power measured: membership, coverage, rights, and the organizing that builds it",
    "meta-aggregation": "Meta-aggregation: a resource that itself gathers and reads other resources",
}
EVIDENCE_KINDS = ["primary text", "scholarly edition", "movement document", "periodical run", "archival collection", "event dataset",
                  "official statistics", "rating against standards", "survey estimate", "case record", "organizing resource", "census of resources"]


def Q(src, quote, basis="operator"):
    return {"src": src, "basis": basis, "quote": quote}


ROWS = []
def row(**r): ROWS.append(r)


ORDER = ["marxists-internet-archive", "mega-digital", "bannedthought", "erol", "banmarchive", "libcom-library", "irish-left-archive",
         "iish", "reuther-library", "cornell-labor-action-tracker", "crowd-counting-consortium", "unionstats", "gnad", "labor-notes",
         "labor-vector"]
for slug in ORDER:
    p = HERE / "rows" / f"{slug}.py"
    if p.exists():
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), {"row": row, "Q": Q})

def norm(s): return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()
problems = []
REQ = ["slug", "name", "url", "operator", "areas", "evidence_kind", "kind", "unit", "record_object", "record", "method",
       "holdings", "stated_limits", "answers", "does_not_answer", "ml_reading", "lifecycle", "version_and_time", "negative_tags", "evidence"]
for r in ROWS:
    miss = [k for k in REQ if k not in r]
    if miss: problems.append((r.get("slug"), "missing fields", miss))
    for i in r.get("areas") or []:
        if i not in AREAS: problems.append((r["slug"], "unknown area", i))
    for k in r.get("evidence_kind") or []:
        if k not in EVIDENCE_KINDS: problems.append((r["slug"], "unknown evidence kind", k))
    rec = r.get("record") or {}
    for k in ("keeps", "holder", "losing_side"):
        if k not in rec: problems.append((r.get("slug"), "record missing", k))
    srcs = {}
    for f, ev in (r.get("evidence") or {}).items():
        sid = ev["src"]
        if sid not in MAN:
            problems.append((r["slug"], f, "source not saved", sid)); continue
        srcs[sid] = {"url": MAN[sid]["url"], "read": MAN[sid]["fetched"][:10], "sha256": MAN[sid]["sha256"], "http": MAN[sid]["http"]}
        if ev.get("quote"):
            txt = norm((HERE / "sources" / f"{sid}.txt").read_text(encoding="utf-8"))
            if norm(ev["quote"]) not in txt:
                problems.append((r["slug"], f, sid, ev["quote"][:80]))
    r["sources"] = srcs
    r.setdefault("observed", {"on": "2026-10-31", "fetch": "read"})
unread = {k: {"url": v["url"], "http": v["http"], "fetched": v["fetched"]} for k, v in MAN.items() if v["http"] != "200" or v["text_chars"] < 100}
out = {"name": "Mary Lee Labor meta-aggregator census: left politics and labor", "compiled": "2026-10-31", "schema_version": "1.0", "editor": "Lee Sharks",
       "family": "Meta-Aggregators of the Crimson Hexagon",
       "schema_note": ("The MMRS, provenance and Labor Vector census core (slug, name, aka, url, operator, kind, unit, count, lifecycle, version_and_time, "
                       "negative_tags, evidence, relations, unchecked, sources) extended for left politics and labor: areas (one or more of six), "
                       "evidence_kind, record_object (what it records), record (keeps: whose record; holder: who holds it and on what terms; losing_side: "
                       "whether and how it keeps minority positions, splits, expulsions and dissent, as the resource itself shows, or 'not recorded'), "
                       "method, coverage, holdings, stated_limits, answers and does_not_answer, and ml_reading (where it meets the question of #1725: "
                       "the archive's reading, kept apart from the resource's own terms). Every quote is verbatim from a saved source."),
       "organizing_question": "Whose record does it keep, who holds it, and does it keep the losing side in a form that could be taken up later?",
       "anchor": {"deposit": 1725, "axn": "AXN:0B50", "title": "Ils ne sont pas marxistes: r/LeftistsForAI, Marx's Legacy, and the Left's Lost Capacity for Internal Critique",
                  "url": "https://www.alexanarch.org/s/records/1725/"},
       "areas": AREAS, "evidence_kinds": EVIDENCE_KINDS, "unread_sources": unread,
       "pending": ["bls-work-stoppages", "ituc-global-rights-index", "tdu", "strike-map-uk", "tamiment-library"],
       "rows": ROWS}
json.dump(out, open(HERE / "census.json", "w"), ensure_ascii=False, indent=1)
print(len(ROWS), "rows;", sum(len(r.get("evidence") or {}) for r in ROWS), "evidence items;", len(problems), "problems")
for p in problems: print("  ", p)
