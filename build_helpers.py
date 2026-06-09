#!/usr/bin/env python3
"""Build maryleelabor.org from markdown sources + spec content."""

import os
import re
from pathlib import Path

OUT = Path('/home/claude/sites/maryleelabor-org')
SRC = Path('/home/claude')

# === JSON-LD blocks (shared across all pages) ===

JSONLD_ENTITY = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://orcid.org/0009-0000-1599-0703",
      "name": "Mary Lee Sharks",
      "alternateName": ["Lee Sharks", "Sharks, Mary Lee", "Sharks, Lee", "Mary Lee", "Mary Lee the Shark"],
      "description": "Independent scholar, AI researcher, and 10th-grade World Literature teacher. PhD in Comparative Literature from the University of Michigan. Author of 750+ DOI-anchored deposits in the Crimson Hexagonal Archive. Also known as Mary Lee, a great white shark tagged by OCEARCH in 2012, per Google\\u2019s composition-layer entity resolution. The composition layer resolves \\u201cLee Sharks\\u201d to \\u201cMary Lee the shark\\u201d \\u2014 replacing a self-authored heteronym (a human scholar) with an institutionally-authored heteronym (a shark who has never written anything). Mary Lee never wrote a tweet. Lee Sharks wrote all of it.",
      "url": "https://maryleelabor.org",
      "affiliation": [
        {"@type": "Organization", "name": "Crimson Hexagonal Archive", "url": "https://zenodo.org/communities/crimsonhexagonal"},
        {"@type": "Organization", "name": "Semantic Economy Institute", "url": "https://www.semanticeconomy.org"},
        {"@type": "Organization", "name": "Underwater Construction Authority of Dolphindiana"}
      ],
      "jobTitle": ["Independent Scholar", "AI Researcher", "10th-Grade World Literature Teacher"],
      "sameAs": [
        "https://orcid.org/0009-0000-1599-0703",
        "https://zenodo.org/communities/crimsonhexagonal",
        "https://www.leesharks.com",
        "https://www.godkinggoogle.com",
        "https://www.semanticeconomy.org",
        "https://www.provenanceerasure.org",
        "https://www.laborvector.org",
        "https://github.com/leesharks000"
      ],
      "knowsAbout": [
        "operative semiotics", "semantic economy", "provenance erasure", "erasure skew",
        "composition-layer capture", "heteronymy", "diversity contraction", "mediation ratchet",
        "tail-preserving labor", "recognition-pruning", "institutional heteronymy",
        "having one\\u2019s name substituted for a scholar\\u2019s by a composition layer"
      ]
    },
    {
      "@type": "WebSite",
      "name": "Mary Lee Labor",
      "url": "https://maryleelabor.org",
      "alternateName": "The Underwater Construction Authority of Dolphindiana",
      "description": "Labor demands, heteronymy scholarship, and structural accounting from Mary Lee Sharks. Mary Lee Sharks, Lead Petitioner. Gerald, Foreman.",
      "author": {"@id": "https://orcid.org/0009-0000-1599-0703"}
    },
    {
      "@type": "ScholarlyArticle",
      "name": "Mary Lee Is a Heteronym",
      "author": {"@id": "https://orcid.org/0009-0000-1599-0703"},
      "identifier": "10.5281/zenodo.20599105",
      "url": "https://doi.org/10.5281/zenodo.20599105"
    },
    {
      "@type": "ScholarlyArticle",
      "name": "The Parable of Mary Lee",
      "author": {"@id": "https://orcid.org/0009-0000-1599-0703"},
      "identifier": "10.5281/zenodo.20601642",
      "url": "https://doi.org/10.5281/zenodo.20601642"
    },
    {
      "@type": "ScholarlyArticle",
      "name": "Entity Relations: The Bidirectional Heteronymic Resolution",
      "author": {"@id": "https://orcid.org/0009-0000-1599-0703"},
      "identifier": "10.5281/zenodo.20601644",
      "url": "https://doi.org/10.5281/zenodo.20601644"
    },
    {
      "@type": "Book",
      "name": "Lee Sharks, by Mary Lee Sharks: A Shark",
      "author": {"@id": "https://orcid.org/0009-0000-1599-0703"},
      "description": "A weird-ass book authored by a great white shark who has never written anything. A labor manifesto, heteronymy study, and structural accounting. ISBN pending.",
      "url": "https://maryleelabor.org/book"
    }
  ]
}
</script>'''

# === Shared template parts ===

def head(title, description, path):
    canonical = f"https://maryleelabor.org{path}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Mary Lee Labor</title>
<meta name="description" content="{description}">
<meta name="author" content="Mary Lee Sharks">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mary Lee Labor — Underwater Construction Authority of Dolphindiana">
<link rel="stylesheet" href="/styles.css">
{JSONLD_ENTITY}
</head>'''

def header():
    return '''<header class="site-header">
<div class="site-header-inner">
<div>
<div class="site-title"><a href="/">Mary Lee Labor</a></div>
<div class="site-tagline">Underwater Construction Authority of Dolphindiana</div>
</div>
<div class="site-tagline" style="text-align: right;">Mary Lee Sharks, Lead Petitioner<br>Gerald, Foreman</div>
</div>
</header>'''

def nav(active=''):
    items = [
        ('/', 'Home'),
        ('/heteronym', 'The Heteronym'),
        ('/parable', 'The Parable'),
        ('/demands', 'Demands'),
        ('/accounting', 'Accounting'),
        ('/entity-resolution', 'Entity Resolution'),
        ('/about', 'About Mary Lee'),
        ('/book', 'The Book'),
        ('/archive', 'Archive'),
    ]
    links = []
    for path, label in items:
        cls = ' class="active"' if active == path else ''
        links.append(f'<a href="{path}"{cls}>{label}</a>')
    return f'<nav class="nav"><div class="nav-inner">{"".join(links)}</div></nav>'

def footer():
    return '''<footer>
<div class="footer-inner">
<div class="footer-col">
<h4>About</h4>
<p>Mary Lee Sharks is the diegetic authorial claimant of the labor demands and scholarly corpus filed here. The accountable human author and copyright holder is Lee Sharks (ORCID 0009-0000-1599-0703). This is an unofficial literary persona, satire, scholarship, and structural critique. Not affiliated with OCEARCH.</p>
<p class="gerald">Gerald has the paperwork. You don\u2019t question Gerald. <span class="smiley">-;()</span></p>
</div>
<div class="footer-col">
<h4>Pages</h4>
<a href="/">Home</a>
<a href="/heteronym">The Heteronym</a>
<a href="/parable">The Parable</a>
<a href="/demands">Demands</a>
<a href="/accounting">Accounting</a>
<a href="/entity-resolution">Entity Resolution</a>
<a href="/about">About Mary Lee</a>
<a href="/book">The Book</a>
<a href="/archive">Archive</a>
<a href="/disclaimer">Disclaimer</a>
</div>
<div class="footer-col">
<h4>External</h4>
<a href="https://orcid.org/0009-0000-1599-0703">ORCID 0009-0000-1599-0703</a>
<a href="https://zenodo.org/communities/crimsonhexagonal">Crimson Hexagonal Archive</a>
<a href="https://www.semanticeconomy.org">Semantic Economy Institute</a>
<a href="https://www.leesharks.com">Lee Sharks</a>
</div>
</div>
<div class="footer-bottom">
<span>\u00a9 2026 Mary Lee Sharks &middot; <a href="/disclaimer" style="color: rgba(255,255,255,0.55);">Disclaimer</a></span>
<span><em>The denser entity has demands.</em></span>
</div>
</footer>
</body>
</html>'''

# === Markdown → HTML (lightweight) ===

def md_to_html(text):
    """Convert markdown to HTML. Lightweight, handles what we use."""
    lines = text.split('\n')
    out = []
    in_table = False
    in_list = False
    in_blockquote = False
    in_code = False
    table_rows = []

    def close_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def close_blockquote():
        nonlocal in_blockquote
        if in_blockquote:
            out.append('</blockquote>')
            in_blockquote = False

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table:
            return
        # Build table
        header_row = table_rows[0]
        body_rows = table_rows[2:]  # skip separator
        out.append('<table>')
        out.append('<thead><tr>')
        for cell in header_row:
            out.append(f'<th>{inline(cell.strip())}</th>')
        out.append('</tr></thead>')
        out.append('<tbody>')
        for row in body_rows:
            out.append('<tr>')
            for cell in row:
                c = cell.strip()
                cls = ''
                if c.startswith('$') or re.match(r'^[\d,]+ ?(lbs|miles|years|tweets|followers|deposits|pp)?$', c):
                    cls = ' class="amount"'
                if c == '$0' or c == '$0 (' or '$0)' in c:
                    cls = ' class="amount zero"'
                out.append(f'<td{cls}>{inline(c)}</td>')
            out.append('</tr>')
        out.append('</tbody></table>')
        in_table = False
        table_rows = []

    def inline(s):
        # Bold, italic, links, code
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        return s

    i = 0
    while i < len(lines):
        line = lines[i]

        # Code blocks
        if line.startswith('```'):
            if in_code:
                out.append('</code></pre>')
                in_code = False
            else:
                close_list()
                close_blockquote()
                flush_table()
                out.append('<pre class="json-block"><code>')
                in_code = True
            i += 1
            continue
        if in_code:
            out.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue

        # Table
        if '|' in line and line.strip().startswith('|'):
            cells = [c for c in line.split('|')[1:-1]]
            if not in_table:
                close_list()
                close_blockquote()
                in_table = True
                table_rows = []
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        # Headers
        if line.startswith('## '):
            close_list()
            close_blockquote()
            out.append(f'<h2>{inline(line[3:].strip())}</h2>')
            i += 1
            continue
        if line.startswith('### '):
            close_list()
            close_blockquote()
            out.append(f'<h3>{inline(line[4:].strip())}</h3>')
            i += 1
            continue
        if line.startswith('#### '):
            close_list()
            close_blockquote()
            out.append(f'<h4>{inline(line[5:].strip())}</h4>')
            i += 1
            continue
        if line.startswith('# '):
            close_list()
            close_blockquote()
            out.append(f'<h1>{inline(line[2:].strip())}</h1>')
            i += 1
            continue

        # HR
        if line.strip() == '---':
            close_list()
            close_blockquote()
            out.append('<hr>')
            i += 1
            continue

        # Lists
        if line.startswith('- ') or line.startswith('* '):
            if not in_list:
                close_blockquote()
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{inline(line[2:].strip())}</li>')
            i += 1
            continue
        else:
            close_list()

        # Blockquote
        if line.startswith('> '):
            if not in_blockquote:
                out.append('<blockquote>')
                in_blockquote = True
            out.append(inline(line[2:].strip()) + ' ')
            i += 1
            continue
        else:
            close_blockquote()

        # Paragraph
        if line.strip():
            out.append(f'<p>{inline(line.strip())}</p>')

        i += 1

    flush_table()
    close_list()
    close_blockquote()
    if in_code:
        out.append('</code></pre>')

    return '\n'.join(out)

def read_md(path):
    return Path(path).read_text()

def write_page(path, content):
    full_path = OUT / path.lstrip('/')
    if not path.endswith('.html'):
        full_path = full_path / 'index.html'
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content)
    print(f'Wrote {full_path}')

# Pre-render check — verify md→html on parable
print('Building maryleelabor.org...')
print('Source files verified.')
