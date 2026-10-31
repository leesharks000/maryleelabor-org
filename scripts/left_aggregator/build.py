"""Render the Mary Lee Labor meta-aggregator on left politics and labor (left census schema 1.0): an index at /aggregators/ and one
page per resource, from data/left-census/census.json. Every quoted field shows its source, the date read and the hash of the saved copy.
Each record page carries two JSON-LD nodes: the record (ours) and the entity it describes (theirs). The census itself is published at
/aggregators/census.json. Run from the repository root: python3 scripts/left_aggregator/build.py"""
import html, json, pathlib, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import build_helpers as BH
D = json.load(open(ROOT / "data/left-census/census.json", encoding="utf-8")); ROWS = D["rows"]; BY = {r["slug"]: r for r in ROWS}
SITE = "https://www.maryleelabor.org"; BASE = SITE + "/aggregators/"
OUT = ROOT / "aggregators"
e = lambda s: html.escape(str(s if s is not None else ""), quote=True)
AREAS = D["areas"]
SHORT = {"texts-of-the-tradition": "Texts of the tradition", "movement-documents": "Movement documents", "archives-and-custody": "Archives and custody",
         "labor-action": "Labor action", "worker-power": "Worker power", "meta-aggregation": "Meta-aggregation"}
BASIS = {"operator": "the resource's own statement", "third_party": "a third-party account", "reading": "our reading"}
CSS = """<style>
.agg{max-width:960px;margin:0 auto;padding:24px 16px 48px}
.agg h1{font-family:'Playfair Display',Georgia,serif;margin:.2em 0}
.agg .q{font-size:1.15em;border-left:3px solid #C84B2E;padding:.4em .9em;margin:1em 0;background:rgba(200,75,46,.06)}
.agg .lede{color:#333}
.agg .fam{font-size:.8em;letter-spacing:.06em;text-transform:uppercase;color:#2D8B6F}
.agg .area{margin-top:2em}
.agg .area h2{font-size:1.1em;border-bottom:1px solid #ddd;padding-bottom:.3em}
.agg .card{border:1px solid #e3e0d8;border-radius:6px;padding:.8em 1em;margin:.7em 0;background:#fff}
.agg .card h3{margin:0 0 .2em;font-size:1.05em}
.agg .card .k{font-size:.85em;color:#555}
.agg .card .ls{font-size:.9em;margin-top:.4em}
.agg .chip{display:inline-block;font-size:.72em;border:1px solid #ccc;border-radius:9px;padding:0 .55em;margin:0 .3em .2em 0;color:#444}
.agg .chip.live{border-color:#2D8B6F;color:#2D8B6F}.agg .chip.dead{border-color:#999;color:#999}
.agg table{border-collapse:collapse;width:100%;font-size:.92em}.agg td,.agg th{border-top:1px solid #eee;padding:.45em .5em;vertical-align:top;text-align:left}
.agg th{width:28%;color:#555;font-weight:600}
.agg .ev{font-size:.85em}.agg .ev li{margin:.35em 0}.agg .ev q{font-style:italic}
.agg .src{color:#666;font-size:.85em;word-break:break-all}
.agg .neg li{color:#7a2a17}
.agg input[type=search]{width:100%;padding:.5em;border:1px solid #ccc;border-radius:4px;font:inherit;margin:.5em 0 1em}
.agg a{overflow-wrap:anywhere}
</style>"""


def lst(v):
    return e("; ".join(v)) if isinstance(v, list) else e(v)


def chips(r):
    st = (r.get("lifecycle") or {}).get("state", ""); c = {"active": "live", "ended": "dead"}.get(st, "")
    return "".join(f'<span class="chip">{e(SHORT.get(a, a))}</span>' for a in r["areas"]) + f'<span class="chip {c}">{e(st)}</span>'


def card(r):
    ls = (r.get("record") or {}).get("losing_side", "")
    return (f'<div class="card" data-s="{e((r["name"] + " " + " ".join(r.get("aka") or []) + " " + r["kind"]).lower())}">'
            f'<h3><a href="/aggregators/{e(r["slug"])}">{e(r["name"])}</a></h3><div class="k">{e(r["kind"])} · {e(r["operator"])}</div>'
            f'<div>{chips(r)}</div><div class="ls"><strong>The losing side:</strong> {e(ls)}</div></div>')


def page(path, title, desc, body, ld):
    return (BH.head(e(title), e(desc), path).replace("</head>", f'<script type="application/ld+json">{ld}</script>{CSS}</head>')
            + "<body>" + BH.header() + BH.nav("/aggregators").replace('<a href="/archive">Archive</a></div>', '<a href="/archive">Archive</a><a class="active" href="/aggregators">Left &amp; Labor</a></div>') + f'<main class="agg">{body}</main>' + BH.footer())


def index():
    groups = []
    seen = set()
    for a in AREAS:
        rs = [r for r in ROWS if r["areas"] and r["areas"][0] == a]
        if not rs: continue
        seen.update(r["slug"] for r in rs)
        groups.append(f'<section class="area"><h2>{e(AREAS[a])}</h2>' + "".join(card(r) for r in rs) + "</section>")
    an = D["anchor"]
    pend = ", ".join(e(p) for p in D.get("pending", []))
    body = (f'<div class="fam">{e(D["family"])}</div><h1>Left politics and labor: a meta-aggregator</h1>'
            f'<p class="lede">A census of the archives, editions, trackers and organizing records of left politics and labor, read one resource at a time from its own pages. '
            f'Every field is quoted from a saved copy of the resource\'s own pages, with the date read and a hash of the copy. Compiled {e(D["compiled"])}; editor Lee Sharks.</p>'
            f'<div class="q"><strong>The census asks of each resource:</strong> {e(D["organizing_question"])}</div>'
            f'<p>The question comes from <a href="{e(an["url"])}"><em>{e(an["title"])}</em></a> ({e(an["axn"])}, #{an["deposit"]}). Its finding: a defeated critique survives where it keeps an organ in which it can go on being stated, a holder with standing independent of the body it criticized, and a route by which it could later be taken up. An archive or a periodical can be that organ. This census records which resources show it.</p>'
            f'<p>Its sibling census, on the intersections of labor and AI, is <a href="https://www.laborvector.org/aggregators/">Labor Vector</a>, which also appears below as one of the resources read.</p>'
            f'<input type="search" id="q" placeholder="Search {len(ROWS)} resources" aria-label="Search the resources">'
            + "".join(groups)
            + f'<section class="area"><h2>Pending</h2><p>Sources that could not be read on {e(D["compiled"])} and are held for the next batch: {pend}.</p>'
            f'<p>The census as data: <a href="/aggregators/census.json">census.json</a> (schema {e(D["schema_version"])}). {e(D["schema_note"])}</p></section>'
            "<script>(function(){var q=document.getElementById('q'),C=[].slice.call(document.querySelectorAll('.card'));q.addEventListener('input',function(){var t=q.value.toLowerCase();C.forEach(function(c){c.style.display=(!t||c.getAttribute('data-s').indexOf(t)>-1)?'':'none'})})})();</script>")
    ld = {"@context": "https://schema.org", "@type": "Dataset", "@id": BASE + "#census", "name": D["name"], "description": D["organizing_question"],
          "url": BASE, "dateModified": D["compiled"], "license": "https://creativecommons.org/licenses/by/4.0/",
          "creator": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
          "isBasedOn": {"@type": "CreativeWork", "name": an["title"], "url": an["url"], "identifier": an["axn"]},
          "distribution": {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": BASE + "census.json"},
          "hasPart": [{"@type": "WebPage", "@id": BASE + r["slug"], "name": r["name"], "url": BASE + r["slug"]} for r in ROWS]}
    return page("/aggregators/", "Left politics and labor: a meta-aggregator", D["organizing_question"], body, json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))


def rec_page(r):
    rec = r.get("record") or {}
    rows = [("Kind", r["kind"]), ("Operator", r["operator"]), ("Unit of record", r["unit"]), ("What it records", r["record_object"]),
            ("Whose record it keeps", rec.get("keeps")), ("Who holds it", rec.get("holder")), ("The losing side", rec.get("losing_side")),
            ("Method", r.get("method")), ("Coverage", "; ".join(f"{k}: {v}" for k, v in (r.get("coverage") or {}).items())),
            ("Count", "; ".join(f"{k}: {v}" for k, v in (r.get("count") or {}).items())), ("Holdings", lst(r.get("holdings")) and "; ".join(r.get("holdings") or [])),
            ("Stated limits", "; ".join(r.get("stated_limits") or [])), ("Data access", r.get("data_access")), ("Licence", r.get("license")),
            ("Lifecycle", "; ".join(f"{k}: {v}" for k, v in (r.get("lifecycle") or {}).items())), ("Founded", r.get("founded"))]
    tbl = "<table>" + "".join(f"<tr><th>{e(k)}</th><td>{e(v)}</td></tr>" for k, v in rows if v) + "</table>"
    ans = (f'<h2>What its record can settle</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in r.get("answers") or []) + "</ul>"
           f'<h2>What it cannot settle</h2><ul>' + "".join(f"<li>{e(x)}</li>" for x in r.get("does_not_answer") or []) + "</ul>")
    neg = '<h2>Kept apart</h2><ul class="neg">' + "".join(f"<li>{e(x)}</li>" for x in r.get("negative_tags") or []) + "</ul>"
    ev = '<h2 id="evidence">Evidence</h2><ul class="ev">'
    for f, v in (r.get("evidence") or {}).items():
        s = r["sources"].get(v["src"], {})
        ev += (f'<li><strong>{e(f)}</strong> ({e(BASIS.get(v.get("basis"), v.get("basis")))}): <q>{e(v.get("quote"))}</q>'
               f'<div class="src"><a href="{e(s.get("url"))}">{e(s.get("url"))}</a> · read {e(s.get("read"))} · http {e(s.get("http"))} · sha256 {e((s.get("sha256") or "")[:16])}…</div></li>')
    ev += "</ul>"
    rel = ""
    if r.get("relations"):
        rel = "<h2>Relations</h2><ul>" + "".join(f'<li>{e(x["rel"])}: ' + (f'<a href="/aggregators/{e(x["target"])}">{e(BY[x["target"]]["name"])}</a>' if x.get("target") in BY else e(x.get("target") or x.get("label") or "")) + (f' — {e(x["note"])}' if x.get("note") else "") + "</li>" for x in r["relations"]) + "</ul>"
    unc = ("<h2>Unchecked</h2><p>" + lst(r.get("unchecked")) + "</p>") if r.get("unchecked") else ""
    body = (f'<p class="fam"><a href="/aggregators/">Left politics and labor</a> / {e(r["name"])}</p><h1>{e(r["name"])}</h1>'
            f'<p><a href="{e(r["url"])}">{e(r["url"])}</a></p><div>{chips(r)}</div>'
            f'<div class="q"><strong>The archive\'s reading.</strong> {e(r["ml_reading"])}</div>' + tbl + ans + neg + rel + ev + unc
            + f'<p class="src">Cite: Lee Sharks, ed. "{e(r["name"])}." Mary Lee Labor meta-aggregator: left politics and labor, maryleelabor.org, compiled {e(D["compiled"])}. {BASE}{e(r["slug"])}</p>')
    ent = {"@id": BASE + r["slug"] + "#entity", "@type": "CreativeWork", "name": r["name"], "alternateName": r.get("aka", []), "url": r["url"],
           "creator": {"@type": "Organization", "name": r["operator"]}}
    recd = {"@id": BASE + r["slug"], "@type": "WebPage", "name": f'{r["name"]} — Mary Lee Labor meta-aggregator record', "about": {"@id": ent["@id"]},
            "mainEntity": {"@id": ent["@id"]}, "dateModified": D["compiled"], "isPartOf": {"@id": BASE + "#census"},
            "editor": {"@type": "Person", "name": "Lee Sharks", "identifier": "https://orcid.org/0009-0000-1599-0703"},
            "citation": [s["url"] for s in r["sources"].values()], "license": "https://creativecommons.org/licenses/by/4.0/"}
    ld = json.dumps({"@context": "https://schema.org", "@graph": [recd, ent]}, ensure_ascii=False).replace("</", "<\\/")
    return page(f"/aggregators/{r['slug']}", r["name"], r["ml_reading"][:200], body, ld)


OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(index(), encoding="utf-8")
for r in ROWS:
    d = OUT / r["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(rec_page(r), encoding="utf-8")
shutil.copy(ROOT / "data/left-census/census.json", OUT / "census.json")
print(f"aggregators: index + {len(ROWS)} record pages + census.json")
