#!/usr/bin/env python3
"""Static site generator for Jay Santoshi Watch.

Usage:  python3 src/build.py
Output: ./public  (deploy this folder to Vercel / Netlify / GitHub Pages / any host)
"""
import datetime
import html
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SITE_URL, BUSINESS as B, DAYS, REVIEW_THEMES, REVIEWS, SERVICES, BRANDS, SOLD_BRANDS, AREAS  # noqa: E402
from guides import GUIDES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "public")
TODAY = datetime.date.today().isoformat()
BIZ_ID = SITE_URL + "/#business"
HOURS = "daily, 10:30 AM – 9:00 PM"

SVC = {s["slug"]: s for s in SERVICES}
AREA = {a["slug"]: a for a in AREAS}
REPAIRS = [s for s in SERVICES if s["kind"] == "repair"]
SHOP = [s for s in SERVICES if s["kind"] == "shop"]
AREA_SERVICES = [s for s in SERVICES if s["in_areas"]]
TIER1 = [a for a in AREAS if a["tier"] == 1]


def has_combo(a):
    """Area+service pages exist for neighbouring areas (Chandkheda itself is covered by /services/)."""
    return a["tier"] == 1 and a["slug"] != B["locality"].lower()

PAGES = []  # (path, priority) for sitemap


def e(s):
    return html.escape(str(s), quote=True)


def full_address():
    return f"{B['street']}, {B['landmark']}, {B['locality']}, {B['city']}, {B['region']} {B['postal']}"


def wa_link(text="Hello Jay Santoshi Watch, I have a query about"):
    from urllib.parse import quote
    return f"https://wa.me/{B['whatsapp']}?text={quote(text)}"


# ---------------------------------------------------------------------------
# Icons (inline SVG, no external requests)
# ---------------------------------------------------------------------------
ICONS = {
    "watch": '<path d="M9 2h6l1 4H8zM8 18h8l-1 4H9z"/><circle cx="12" cy="12" r="6"/><path d="M12 9v3l2 1"/>',
    "battery": '<rect x="2" y="7" width="18" height="10" rx="2"/><path d="M22 11v2M6 10v4M10 10v4"/>',
    "strap": '<path d="M8 2h8v6H8zM8 16h8v6H8z"/><rect x="6" y="8" width="12" height="8" rx="2"/>',
    "glass": '<circle cx="12" cy="12" r="9"/><path d="M8 8l3 3M13 6l2 2"/>',
    "tool": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "gift": '<rect x="3" y="8" width="18" height="13" rx="1"/><path d="M3 12h18M12 8v13M12 8S10 3 7.5 4.5 9 8 12 8zm0 0s2-5 4.5-3.5S15 8 12 8z"/>',
    "tag": '<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "wa": '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M8.5 9.5c.5 2.5 3 5 5.5 5.5l1.2-1.2 2 1-.5 1.7c-4 .5-9.2-4.7-8.7-8.7l1.7-.5 1 2z"/>',
    "pin": '<path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
    "star": '<path d="M12 2l3 6.5 7 .8-5.2 4.8 1.4 7L12 17.6 5.8 21l1.4-7L2 9.3l7-.8z"/>',
}
SVC_ICON = {
    "watch-repair": "tool", "watch-battery-replacement": "battery", "watch-strap-replacement": "strap",
    "watch-glass-replacement": "glass", "watch-servicing": "watch", "wall-clock-repair": "clock",
    "wrist-watches": "watch", "wall-clocks": "clock", "watch-accessories": "tag", "gift-watches": "gift",
}


def icon(name, size=22):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


# ---------------------------------------------------------------------------
# Schema.org JSON-LD
# ---------------------------------------------------------------------------

def business_schema():
    return {
        "@type": ["Store", "LocalBusiness"],
        "@id": BIZ_ID,
        "name": B["name"],
        "alternateName": B["alt_names"],
        "description": f"{B['name']} is a watch store and watch & clock repair shop in {B['locality']}, {B['city']}. "
                       "Watch battery replacement, watch repair, strap and chain replacement, glass replacement, "
                       "wall clock repair, and wristwatches and wall clocks for sale.",
        "url": SITE_URL + "/",
        "logo": SITE_URL + "/icon-512.png",
        "image": SITE_URL + "/og-image.png",
        "telephone": B["phone"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{B['street']}, {B['landmark']}",
            "addressLocality": f"{B['locality']}, {B['city']}",
            "addressRegion": B["region"],
            "postalCode": B["postal"],
            "addressCountry": B["country"],
        },
        "hasMap": B["maps_url"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": DAYS,
            "opens": B["opens"],
            "closes": B["closes"],
        }],
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": B["phone"], "contactType": "customer service",
             "areaServed": "IN", "availableLanguage": ["en", "gu", "hi"]},
            {"@type": "ContactPoint", "telephone": B["phone2"], "contactType": "customer service",
             "areaServed": "IN", "availableLanguage": ["en", "gu", "hi"]},
        ],
        "priceRange": "₹",
        "currenciesAccepted": "INR",
        "areaServed": [
            {"@type": "City", "name": "Ahmedabad"},
            {"@type": "City", "name": "Gandhinagar"},
        ] + [{"@type": "Place", "name": f"{a['name']}, Ahmedabad"} for a in TIER1],
        "knowsAbout": ["Watch repair", "Watch battery replacement", "Watch strap replacement",
                       "Watch glass replacement", "Clock repair", "Wall clocks", "Wristwatches"],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Watch and clock services",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"],
                                                    "url": f"{SITE_URL}/services/{s['slug']}/"}}
                for s in SERVICES
            ],
        },
        "brand": [{"@type": "Brand", "name": n} for n in SOLD_BRANDS],
        "sameAs": B["same_as"],
    }


def website_schema():
    return {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": B["name"],
            "inLanguage": "en-IN", "publisher": {"@id": BIZ_ID}}


def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + p}
        for i, (n, p) in enumerate(crumbs)]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def service_schema(svc, area=None, path=None):
    served = ({"@type": "Place", "name": f"{area['name']}, {B['city']}"} if area
              else {"@type": "City", "name": B["city"]})
    name = f"{svc['name']} in {area['name']}" if area else f"{svc['name']} in {B['locality']}, {B['city']}"
    return {"@type": "Service", "name": name, "serviceType": svc["name"], "description": svc["short"],
            "provider": {"@id": BIZ_ID}, "areaServed": served, "url": SITE_URL + (path or "")}


# ---------------------------------------------------------------------------
# HTML building blocks
# ---------------------------------------------------------------------------
NAV = [("Home", "/"), ("Services", "/services/"), ("Areas", "/areas/"), ("Brands", "/brands/"),
       ("Guides", "/guides/"), ("About", "/about/"), ("Contact", "/contact/")]


def header(path):
    links = "".join(
        f'<li><a href="{p}"{" aria-current=page" if (p == path or (p != "/" and path.startswith(p))) else ""}>{n}</a></li>'
        for n, p in NAV)
    nav = f'<nav class="nav" aria-label="Main"><ul>{links}<li><a class="cta" href="tel:{B["phone"]}">Call now</a></li></ul></nav>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="top"><div class="wrap"><span>{icon("pin", 14)} {e(B["street"])}, {e(B["locality"])}, {e(B["city"])}</span>
<span>{e(B["hours_display"])} · <a href="tel:{B["phone"]}">{e(B["phone_display"])}</a></span></div></div>
<header class="hdr"><div class="wrap">
<a class="logo" href="/" aria-label="{e(B["name"])} home"><img src="/favicon.svg" width="36" height="36" alt="">
<span>{e(B["name"])}<small>Watch shop &amp; repair · Chandkheda</small></span></a>
{nav}
<details class="menu"><summary aria-label="Open menu">☰ Menu</summary>{nav}</details>
</div></header>"""


def footer():
    svc_links = "".join(f'<li><a href="/services/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SERVICES[:7])
    area_links = "".join(f'<li><a href="/areas/{a["slug"]}/">Watch shop in {e(a["name"])}</a></li>' for a in AREAS[:9])
    more = "".join(f'<li><a href="{p}">{n}</a></li>' for n, p in [
        ("All areas we serve", "/areas/"), ("Brands we service", "/brands/"), ("Watch care guides", "/guides/"),
        ("FAQ", "/faq/"), ("About us", "/about/"), ("Contact & directions", "/contact/")])
    return f"""<footer class="ftr"><div class="wrap"><div class="cols">
<div><h2>{e(B["name"])}</h2>
<p>{e(B["street"])},<br>{e(B["landmark"])},<br>{e(B["locality"])}, {e(B["city"])}, {e(B["region"])} {e(B["postal"])}</p>
<p><a href="tel:{B["phone"]}">{e(B["phone_display"])}</a><br><a href="tel:{B["phone2"]}">{e(B["phone2_display"])}</a><br><a href="{e(wa_link())}" rel="noopener" target="_blank">WhatsApp {e(B["phone2_display"])}</a></p>
<p>{e(B["hours_display"])}</p>
<p><a href="{e(B["maps_url"])}" rel="noopener" target="_blank">★ {B["rating"]} on Google ({B["review_count"]}+ reviews)</a></p></div>
<div><h3>Services</h3><ul>{svc_links}</ul></div>
<div><h3>Areas</h3><ul>{area_links}</ul></div>
<div><h3>More</h3><ul>{more}</ul></div>
</div>
<p class="legal">© {datetime.date.today().year} {e(B["name"])}, Chandkheda, Ahmedabad. {e(B["name"])} is an independent watch shop and repair service. It is not an authorised service centre of any brand; brand names are used only to describe the watches we work on.</p>
</div></footer>
<nav class="bar" aria-label="Quick contact">
<a href="tel:{B["phone"]}">{icon("phone")}Call</a>
<a class="wa" href="{e(wa_link())}" rel="noopener" target="_blank">{icon("wa")}WhatsApp</a>
<a href="{e(B["maps_url"])}" rel="noopener" target="_blank">{icon("pin")}Directions</a>
</nav>"""


def breadcrumbs_html(crumbs):
    items = []
    for i, (n, p) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{e(n)}</li>')
        else:
            items.append(f'<li><a href="{p}">{e(n)}</a></li>')
    return f'<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def faq_html(faqs, heading="Frequently asked questions"):
    items = "".join(f"<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in faqs)
    return f'<section class="faq"><div class="wrap"><h2>{e(heading)}</h2>{items}</div></section>'


def cta_block(title="Visit or contact us", text=None):
    text = text or (f"Walk in at {full_address()}. We're open {HOURS}. "
                    "Call or WhatsApp to check if a part or strap is in stock.")
    return f"""<section class="alt"><div class="wrap two">
<div><h2 style="margin-top:0">{e(title)}</h2><p>{e(text)}</p>
<div class="btns"><a class="btn btn-dark" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link())}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp</a>
<a class="btn btn-gold" href="{e(B["maps_url"])}" rel="noopener" target="_blank">{icon("pin", 18)} Get directions</a></div></div>
{nap_card()}
</div></section>"""


def nap_card():
    return f"""<div class="nap"><dl>
<dt>Shop</dt><dd><strong>{e(B["name"])}</strong></dd>
<dt>Address</dt><dd>{e(full_address())}</dd>
<dt>Phone</dt><dd><a href="tel:{B["phone"]}">{e(B["phone_display"])}</a> · <a href="tel:{B["phone2"]}">{e(B["phone2_display"])}</a></dd>
<dt>WhatsApp</dt><dd><a href="{e(wa_link())}" rel="noopener" target="_blank">{e(B["phone2_display"])}</a></dd>
<dt>Hours</dt><dd>{e(B["hours_display"])}</dd>
<dt>Rating</dt><dd><span class="stars">★★★★★</span> {B["rating"]}/5 · {B["review_count"]}+ Google reviews</dd>
</dl></div>"""


def map_embed():
    return (f'<iframe class="map" src="{e(B["maps_embed"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'title="Map showing {e(B["name"])}, {e(B["locality"])}, {e(B["city"])}" allowfullscreen></iframe>')


def answer_box(text, label="Quick answer"):
    return f'<div class="answer"><strong>{e(label)}</strong><p>{e(text)}</p></div>'


REVIEW_FOR = {"watch-battery-replacement": 0, "watch-repair": 0, "wall-clock-repair": 1, "wall-clocks": 1,
              "watch-strap-replacement": 2, "watch-accessories": 2, "wrist-watches": 3, "gift-watches": 3,
              "seiko": 0, "ajanta-orpat": 1}


def review_card(r):
    return (f'<figure class="review"><div class="stars" aria-label="{r["stars"]} out of 5 stars">{"★" * r["stars"]}</div>'
            f'<blockquote><p>{e(r["text"])}</p></blockquote>'
            f'<figcaption><strong>{e(r["author"])}</strong> · {e(r["topic"])} · Google review, {e(r["when"])}</figcaption></figure>')


def reviews_section(idxs, heading="What our customers say", alt=False):
    cards = "".join(review_card(REVIEWS[i]) for i in idxs)
    return (f'<section{" class=alt" if alt else ""}><div class="wrap"><h2 style="margin-top:0">{e(heading)}</h2>'
            f'<div class="reviews">{cards}</div>'
            f'<p style="margin-top:16px"><a href="{e(B["review_url"])}" rel="noopener" target="_blank">Read all {B["review_count"]}+ reviews on Google →</a></p></div></section>')


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def service_cards(svcs, area=None):
    out = []
    for s in svcs:
        if area and s["in_areas"] and has_combo(area):
            href = f"/areas/{area['slug']}/{s['slug']}/"
            title = f"{s['name']} in {area['name']}"
        else:
            href, title = f"/services/{s['slug']}/", s["name"]
        out.append(f'<div class="card"><div class="ico">{icon(SVC_ICON[s["slug"]])}</div>'
                   f'<h3><a href="{href}">{e(title)}</a></h3><p>{e(s["short"])}</p></div>')
    return '<div class="grid">' + "".join(out) + "</div>"


def area_pills(areas, service=None):
    out = []
    for a in areas:
        if service and has_combo(a):
            out.append(f'<li><a href="/areas/{a["slug"]}/{service["slug"]}/">{e(service["name"])} in {e(a["name"])}</a></li>')
        else:
            out.append(f'<li><a href="/areas/{a["slug"]}/">{e(a["name"])}</a></li>')
    return '<ul class="pills">' + "".join(out) + "</ul>"


def page(path, title, description, body, schema=None, crumbs=None, og_type="website", priority="0.6"):
    canonical = SITE_URL + path
    graph = [business_schema()]
    if path == "/":
        graph.append(website_schema())
    graph.append({"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": title,
                  "description": description, "inLanguage": "en-IN", "isPartOf": {"@id": SITE_URL + "/#website"},
                  "about": {"@id": BIZ_ID}, "dateModified": TODAY})
    if crumbs:
        graph.append(crumbs_schema(crumbs))
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    crumbs_html = breadcrumbs_html(crumbs) if crumbs else ""
    doc = f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="geo.region" content="{B["region_code"]}">
<meta name="geo.placename" content="{e(B["locality"])}, {e(B["city"])}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{e(B["name"])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14213d">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(path)}
{crumbs_html}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
"""
    write(path, doc)
    PAGES.append((path, priority))


def write(path, content):
    target = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Area-specific copy helpers
# ---------------------------------------------------------------------------

def area_reach(a):
    lm = ", ".join(a["landmarks"][:2])
    if a["tier"] == 1:
        return (f"{a['name']} is right next to our shop. Customers from around {lm} usually reach us in a few minutes. "
                f"Come along the Visat–Sabarmati Highway to Swapna Shilp Complex in Nigam Nagar, near ONGC, Chandkheda.")
    if a["tier"] == 2:
        return (f"From {a['name']} ({lm}), we're a short drive away in Chandkheda. Head towards the Visat–Sabarmati "
                f"Highway and look for Swapna Shilp Complex in Nigam Nagar, near ONGC. Use the Directions button for live "
                f"Google Maps directions from where you are.")
    return (f"{a['name']} is across the city from Chandkheda, but many customers make the trip for honest advice and fair "
            f"prices. Call or WhatsApp us before you come, so we can confirm a part or strap is in stock and your visit "
            f"isn't wasted.")


INTROS = [
    "Looking for a trusted watch shop or watch repair near {name}? {biz} in Chandkheda is rated {r}★ on Google by {n}+ customers. We replace watch batteries, repair watches and wall clocks, fit new straps and chains, and sell wristwatches and wall clocks.",
    "Customers from {name} come to {biz} for quick watch battery replacement, honest watch and clock repairs, and a good choice of watches and wall clocks. We're rated {r}★ from {n}+ Google reviews, and we explain the problem and the price before starting any work.",
    "If you live or work in {name}, {biz} is your local watch expert in North Ahmedabad. We fix stopped watches, change batteries, replace glass and straps, repair wall clocks, and help you choose a new watch. {n}+ Google reviews give us an average of {r}★.",
    "Need a watch battery, a new strap, or a stopped wall clock fixed near {name}? {biz} at Nigam Nagar, Chandkheda handles everyday watch and clock repairs quickly and at fair prices, and our {r}★ rating comes from {n}+ Google reviews.",
]


def area_intro(a, i):
    return INTROS[i % len(INTROS)].format(name=a["name"], biz=B["name"], r=B["rating"], n=B["review_count"])


def area_faqs(a):
    near = "one of the closest" if a["tier"] == 1 else ("a short drive away and a popular choice" if a["tier"] == 2 else "a well-rated option")
    return [
        (f"Where is the nearest watch repair shop to {a['name']}?",
         f"{B['name']} at {full_address()} is {near} for watch and clock repair for people in {a['name']}. Call {B['phone_display']} for directions."),
        (f"Can I get my watch battery replaced near {a['name']}?",
         f"Yes. {B['name']} in Chandkheda replaces watch batteries for customers from {a['name']}. It usually takes a few minutes while you wait."),
        (f"Do you repair wall clocks for customers from {a['name']}?",
         "Yes. We repair quartz wall, table and alarm clocks, including movement (machine) replacement. For very old mechanical clocks, call first."),
        (f"What are {B['name']}'s timings?",
         f"We are open {HOURS}. Timings can change on festivals, so call {B['phone_display']} before a special trip."),
    ]


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def build_home():
    services = service_cards(REPAIRS) + "<h3 style='margin-top:24px'>Shop watches &amp; clocks</h3>" + service_cards(SHOP)
    themes = "".join(f'<div class="card"><div class="ico">{icon("star")}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in REVIEW_THEMES)
    guides = "".join(f'<div class="card"><h3><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></h3><p>{e(g["description"])}</p></div>' for g in GUIDES[:6])
    sold = '<ul class="pills">' + "".join(f'<li><a href="/brands/{b["slug"]}/">{e(b["name"])}</a></li>' for b in BRANDS if b["sold"]) + "</ul>"
    brands = '<ul class="pills">' + "".join(f'<li><a href="/brands/{b["slug"]}/">{e(b["name"])}</a></li>' for b in BRANDS if not b["sold"]) + "</ul"
    faqs = [
        ("Where is Jay Santoshi Watch located?", f"{B['name']} is at {full_address()}."),
        ("What are the shop timings?", f"{B['hours_display']}. Call {B['phone_display']} to confirm on festival days."),
        ("How long does watch battery replacement take?", "Usually just a few minutes. Most customers wait while it's done."),
        ("Do you repair wall clocks?", "Yes. We repair quartz wall, table and alarm clocks and replace clock movements. For very old mechanical clocks, please call first."),
        ("Do you repair all watch brands?", "We repair most everyday brands, including Titan, Sonata, Fastrack, Casio, Timex, Maxima and HMT. We're an independent shop, not an authorised service centre for any brand."),
        ("Which watch brands do you sell?", f"We sell {', '.join(SOLD_BRANDS[:-1])} and {SOLD_BRANDS[-1]} watches for men, women and kids, plus wall clocks, straps and watch accessories."),
        ("Which areas do you serve?", "Customers come to us from Chandkheda, Motera, Sabarmati, Visat, Zundal, Tragad, Ranip, Gota, Gandhinagar and all over Ahmedabad."),
    ]
    summary = (f"{B['name']} is a watch shop and watch & clock repair service at Swapna Shilp Complex, Nigam Nagar, "
               f"Chandkheda, Ahmedabad (near ONGC, Visat–Sabarmati Highway). It's rated {B['rating']}/5 from "
               f"{B['review_count']}+ Google reviews and is open daily from 10:30 AM to 9:00 PM. Services include watch battery "
               "replacement, watch repair, strap and chain replacement, glass replacement and wall clock repair, along with "
               f"{', '.join(SOLD_BRANDS[:-1])} and {SOLD_BRANDS[-1]} wristwatches and wall clocks for sale.")
    body = f"""<section class="hero"><div class="wrap">
<h1>Watch Shop &amp; Watch Repair in Chandkheda, Ahmedabad</h1>
<p class="lead">{e(B["name"])}: quick watch battery replacement, honest watch and wall clock repairs, new straps and chains, and Titan, Sonata, Timex, Maxima &amp; Lamex watches at fair prices. In Nigam Nagar, near ONGC.</p>
<div class="meta"><span class="chip"><span class="stars">★★★★★</span> {B["rating"]}/5 · {B["review_count"]}+ Google reviews</span>
<span class="chip">{icon("clock", 16)} {e(B["hours_display"])}</span><span class="chip">{icon("pin", 16)} Nigam Nagar, Chandkheda</span></div>
<div class="btns"><a class="btn btn-gold" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link())}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp us</a>
<a class="btn btn-line" href="{e(B["maps_url"])}" rel="noopener" target="_blank">{icon("pin", 18)} Directions</a></div>
</div></section>
<section><div class="wrap">{answer_box(summary, "About us in one paragraph")}
<p class="local">ચાંદખેડામાં ઘડિયાળની દુકાન અને ઘડિયાળ રિપેર · चांदखेड़ा में घड़ी की दुकान और घड़ी रिपेयर</p></div></section>
<section><div class="wrap"><h2 style="margin-top:0">Watch &amp; clock repair services</h2>{services}</div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Why customers rate us {B["rating"]}★</h2>
<p>From {B["review_count"]}+ Google reviews, these are the things customers mention most:</p><div class="grid">{themes}</div>
</div></section>
{reviews_section(range(len(REVIEWS)), "Real reviews from our customers")}
<section><div class="wrap"><h2 style="margin-top:0">Watch shop near you, across Ahmedabad</h2>
<p>We're in Chandkheda, North Ahmedabad, close to Motera, Sabarmati, Visat, Zundal, Tragad and Gandhinagar. Customers also come to us from across the city. Find your area:</p>
{area_pills(AREAS)}</div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Watch brands we sell</h2>
<p>New watches for men, women and kids from:</p>{sold}
<h2>Brands we also service</h2>
<p>Battery, strap, glass and repair work for everyday watches from these and many other brands:</p>{brands}</div></section>
<section><div class="wrap"><h2 style="margin-top:0">Watch care guides</h2><div class="grid">{guides}</div></div></section>
{faq_html(faqs)}
<section><div class="wrap two"><div>{map_embed()}</div>{nap_card()}</div></section>"""
    page("/", f"{B['name']} | Watch Shop & Watch Repair in Chandkheda, Ahmedabad",
         f"Watch shop & repair in Chandkheda, Ahmedabad: battery replacement, watch & clock repair, straps, glass. "
         f"Rated {B['rating']}★ ({B['review_count']}+ reviews). Call {B['phone_display']}.",
         body, schema=[faq_schema(faqs)], priority="1.0")


def build_services_index():
    crumbs = [("Home", "/"), ("Services", "/services/")]
    body = f"""<div class="wrap page-head"><h1>Watch &amp; Clock Services in Chandkheda, Ahmedabad</h1>
<p class="lead">Everything we do at {e(B["name"])}, from a quick battery change to wall clock repairs and new watches.</p></div>
<section><div class="wrap"><h2 style="margin-top:0">Repairs</h2>{service_cards(REPAIRS)}
<h2>Shop</h2>{service_cards(SHOP)}</div></section>{cta_block()}"""
    page("/services/", f"Watch Repair, Battery & Clock Repair Services | {B['name']} Ahmedabad",
         "Watch repair, battery, strap, chain & glass replacement, servicing, wall clock repair, and watches & clocks for sale in Chandkheda, Ahmedabad.",
         body, crumbs=crumbs, priority="0.9")


STEPS_REPAIR = [
    ("Bring it in", "Walk in with your watch or clock. No appointment needed."),
    ("Free check & price", "We check it in front of you and tell you the problem and the cost."),
    ("Repair", "We do the work only after you agree. Small jobs are often done while you wait."),
    ("Test & hand over", "We test it before handing it back and give you simple care tips."),
]


def build_service(s):
    path = f"/services/{s['slug']}/"
    crumbs = [("Home", "/"), ("Services", "/services/"), (s["name"], path)]
    intro = "".join(f"<p>{e(p)}</p>" for p in s["intro"])
    steps = ""
    if s["kind"] == "repair":
        steps = '<h2>How it works</h2><ol class="steps">' + "".join(f"<li><strong>{e(t)}</strong><br>{e(d)}</li>" for t, d in STEPS_REPAIR) + "</ol>"
    related_guides = [g for g in GUIDES if s["slug"] in g["related"]]
    guides = ""
    if related_guides:
        guides = "<h2>Helpful guides</h2><ul>" + "".join(f'<li><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></li>' for g in related_guides) + "</ul>"
    others = service_cards([x for x in SERVICES if x["slug"] != s["slug"]][:6])
    faqs = s["faqs"]
    title_kw = f"{s['name']} in Chandkheda, Ahmedabad"
    body = f"""<div class="wrap page-head"><h1>{e(title_kw)}</h1>
<p class="lead">{e(s["short"])}</p>
<div class="btns"><a class="btn btn-dark" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link("Hello, I want to ask about " + s["name"]))}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp</a></div></div>
<section><div class="wrap prose">{answer_box(f"{B['name']} offers {s['name'].lower()} at {full_address()}. {s['short']} Open {HOURS}.")}
{intro}<p class="local">{e(s["local"])}</p></div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">What's included</h2>{ticks(s["includes"])}{steps}</div></section>
{reviews_section([REVIEW_FOR[s["slug"]]], "From our Google reviews") if s["slug"] in REVIEW_FOR else ""}
{faq_html(faqs)}
<section><div class="wrap"><h2 style="margin-top:0">{e(s["name"])} near you</h2>
<p>We serve customers from all over Ahmedabad and Gandhinagar. Pick your area:</p>{area_pills(AREAS, s if s["in_areas"] else None)}
<div class="prose">{guides}</div></div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Other services</h2>{others}</div></section>
{cta_block()}"""
    page(path, f"{s['name']} in Chandkheda, Ahmedabad | {B['name']}",
         f"{s['name']} at {B['name']}, Nigam Nagar, Chandkheda, Ahmedabad. Rated {B['rating']}★ by {B['review_count']}+ customers. Open daily. Call {B['phone_display']}.",
         body, schema=[service_schema(s, path=path), faq_schema(faqs)], crumbs=crumbs, priority="0.9")


def build_areas_index():
    crumbs = [("Home", "/"), ("Areas we serve", "/areas/")]
    groups = [(1, "Chandkheda & nearby (closest to our shop)"), (2, "A short drive away"), (3, "Across Ahmedabad")]
    sections = "".join(f'<h2>{e(t)}</h2>{area_pills([a for a in AREAS if a["tier"] == tier])}' for tier, t in groups)
    body = f"""<div class="wrap page-head"><h1>Watch Shop &amp; Watch Repair Near You in Ahmedabad</h1>
<p class="lead">{e(B["name"])} is in Chandkheda, North Ahmedabad. These are the areas our customers come from. Pick yours for directions, services and local FAQs.</p></div>
<section><div class="wrap">{sections}</div></section>
<section><div class="wrap two"><div>{map_embed()}</div>{nap_card()}</div></section>"""
    page("/areas/", f"Areas We Serve: Watch Repair Near You in Ahmedabad | {B['name']}",
         f"Watch shop and watch repair for Chandkheda, Motera, Sabarmati, Visat, Ranip, Gota, Gandhinagar and all of Ahmedabad. {B['name']}, rated {B['rating']}★.",
         body, crumbs=crumbs, priority="0.9")


def build_area(a, i):
    path = f"/areas/{a['slug']}/"
    crumbs = [("Home", "/"), ("Areas", "/areas/"), (a["name"], path)]
    near = [AREA[s] for s in a["near"] if s in AREA]
    faqs = area_faqs(a)
    lms = ", ".join(a["landmarks"])
    body = f"""<div class="wrap page-head"><h1>Watch Shop &amp; Watch Repair in {e(a["name"])}, Ahmedabad</h1>
<p class="lead">{e(area_intro(a, i))}</p>
<div class="btns"><a class="btn btn-dark" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link("Hello, I am from " + a["name"] + ". I have a query about"))}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp</a>
<a class="btn btn-gold" href="{e(B["maps_url"])}" rel="noopener" target="_blank">{icon("pin", 18)} Directions</a></div></div>
<section><div class="wrap prose">{answer_box(f"The nearest {B['name']} shop for {a['name']} customers is at {full_address()}. Open {HOURS}. Phone {B['phone_display']}.")}
<h2>Getting here from {e(a["name"])}</h2><p>{e(area_reach(a))}</p>
<p>Landmarks around {e(a["name"])}: {e(lms)} ({e(a["zone"])}).</p>
<p class="local">{e(a["name"])} નજીક ઘડિયાળ રિપેર અને બેટરી · {e(a["name"])} के पास घड़ी रिपेयर और बैटरी</p></div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Services for {e(a["name"])} customers</h2>{service_cards(SERVICES, a)}</div></section>
<section><div class="wrap"><h2 style="margin-top:0">Why people from {e(a["name"])} choose us</h2>{ticks([t + ": " + d for t, d in REVIEW_THEMES])}</div></section>
{reviews_section([i % len(REVIEWS)], "What our customers say", alt=True)}
{faq_html(faqs, f"Questions from {a['name']} customers")}
<section><div class="wrap"><h2 style="margin-top:0">Nearby areas</h2>{area_pills(near)}</div></section>
<section><div class="wrap two"><div>{map_embed()}</div>{nap_card()}</div></section>"""
    page(path, f"Watch Shop & Watch Repair in {a['name']}, Ahmedabad | {B['name']}",
         f"Watch repair, battery replacement, straps and wall clock repair for {a['name']}, Ahmedabad. {B['name']}, Chandkheda: rated {B['rating']}★. Call {B['phone_display']}.",
         body, schema=[faq_schema(faqs)], crumbs=crumbs, priority="0.8" if a["tier"] < 3 else "0.7")


def build_area_service(a, s):
    path = f"/areas/{a['slug']}/{s['slug']}/"
    crumbs = [("Home", "/"), ("Areas", "/areas/"), (a["name"], f"/areas/{a['slug']}/"), (s["name"], path)]
    near = [AREA[x] for x in a["near"] if x in AREA]
    faqs = [(f"Where can I get {s['keyword']} near {a['name']}?",
             f"{B['name']} at {full_address()} offers {s['keyword']} for customers from {a['name']}. Call {B['phone_display']}.")] + s["faqs"]
    intro = "".join(f"<p>{e(p)}</p>" for p in s["intro"])
    other = [x for x in AREA_SERVICES if x["slug"] != s["slug"]]
    other_links = '<ul class="pills">' + "".join(f'<li><a href="/areas/{a["slug"]}/{x["slug"]}/">{e(x["name"])} in {e(a["name"])}</a></li>' for x in other) + "</ul>"
    body = f"""<div class="wrap page-head"><h1>{e(s["name"])} in {e(a["name"])}, Ahmedabad</h1>
<p class="lead">{e(s["short"])} For customers in {e(a["name"])}, from {e(B["name"])} in nearby Chandkheda: rated {B["rating"]}★ by {B["review_count"]}+ Google reviewers.</p>
<div class="btns"><a class="btn btn-dark" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link("Hello, I am from " + a["name"] + ". I want " + s["keyword"]))}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp</a></div></div>
<section><div class="wrap prose">{answer_box(f"For {s['keyword']} near {a['name']}, visit {B['name']} at {full_address()}. Open {HOURS}. Call {B['phone_display']}.")}
{intro}<h2>Coming from {e(a["name"])}</h2><p>{e(area_reach(a))}</p><p class="local">{e(s["local"])}</p></div></section>
<section class="alt"><div class="wrap"><h2 style="margin-top:0">What's included</h2>{ticks(s["includes"])}
<h2>How it works</h2><ol class="steps">{"".join(f"<li><strong>{e(t)}</strong><br>{e(d)}</li>" for t, d in STEPS_REPAIR)}</ol></div></section>
{reviews_section([REVIEW_FOR[s["slug"]]], "From our Google reviews") if s["slug"] in REVIEW_FOR else ""}
{faq_html(faqs)}
<section><div class="wrap"><h2 style="margin-top:0">More services in {e(a["name"])}</h2>{other_links}
<h2>{e(s["name"])} in nearby areas</h2>{area_pills(near, s)}
<p style="margin-top:16px"><a href="/services/{s["slug"]}/">Read more about our {e(s["name"].lower())} service →</a></p></div></section>
{cta_block()}"""
    page(path, f"{s['name']} in {a['name']}, Ahmedabad | {B['name']}",
         f"{s['name']} near {a['name']}, Ahmedabad at {B['name']}, Chandkheda. Rated {B['rating']}★ ({B['review_count']}+ reviews). Call {B['phone_display']}.",
         body, schema=[service_schema(s, a, path), faq_schema(faqs)], crumbs=crumbs, priority="0.7")


def build_brands_index():
    crumbs = [("Home", "/"), ("Brands", "/brands/")]
    def cards(bs, label):
        return '<div class="grid">' + "".join(f'<div class="card"><h3><a href="/brands/{b["slug"]}/">{e(b["name"])}{label}</a></h3><p>{e(b["note"])}</p></div>' for b in bs) + "</div>"
    body = f"""<div class="wrap page-head"><h1>Watch Brands We Sell &amp; Repair in Ahmedabad</h1>
<p class="lead">New Titan, Sonata, Timex, Maxima and Lamex watches, plus battery replacement, straps, glass and everyday repairs for most popular watch and clock brands, at our Chandkheda shop.</p></div>
<section><div class="wrap"><h2 style="margin-top:0">Brands we sell</h2>{cards([b for b in BRANDS if b["sold"]], " watches")}
<h2>Brands we service</h2>{cards([b for b in BRANDS if not b["sold"]], " repair")}
<p class="note">{e(B["name"])} is an independent watch shop. It is not an authorised service centre for any of these brands, and brand names are used only to describe the watches we work on. For warranty repairs, please contact the brand's authorised service centre.</p></div></section>{cta_block()}"""
    page("/brands/", f"Watch Brands We Sell & Repair: Titan, Sonata, Timex, Maxima, Lamex | {B['name']}",
         "Buy Titan, Sonata, Timex, Maxima & Lamex watches in Chandkheda. Battery, strap & repair for Seiko, Casio, Fastrack, HMT, Fossil, Citizen and more.",
         body, crumbs=crumbs, priority="0.8")


def build_brand(b):
    path = f"/brands/{b['slug']}/"
    is_clock = "Clock" in b["name"]
    noun = b["name"] if is_clock else f"{b['name']} watch"
    crumbs = [("Home", "/"), ("Brands", "/brands/"), (b["name"], path)]
    items = (["Wall clock movement (machine) replacement", "Clock hands replacement", "Battery and contact cleaning", "General check-up"]
             if is_clock else
             [f"{b['name']} watch battery replacement", f"{b['name']} strap and metal chain replacement / resizing",
              f"{b['name']} watch glass replacement", "Crown, button and hand repairs", "Cleaning and general check-up"])
    faqs = [
        (f"Where can I repair my {noun} in Ahmedabad?",
         f"{B['name']} at {full_address()} handles everyday {noun} repairs. Call {B['phone_display']} to check your model."),
        (f"Are you an authorised {b['name']} service centre?",
         f"No. {B['name']} is an independent watch shop. For warranty claims, contact {b['name']}'s authorised service centre. For out-of-warranty jobs like batteries, straps and glass, we can usually help."),
    ]
    if not is_clock:
        faqs.insert(1, (f"How long does {b['name']} watch battery replacement take?",
                        "Usually a few minutes while you wait, for most models."))
    svc_links = service_cards([SVC[x] for x in (["wall-clock-repair", "wall-clocks"] if is_clock else
                                                ["watch-battery-replacement", "watch-repair", "watch-strap-replacement", "watch-glass-replacement"])])
    if is_clock:
        title = f"{b['name']} Repair in Ahmedabad"
    elif b["sold"]:
        title = f"{b['name']} Watches: Buy & Repair in Chandkheda, Ahmedabad"
        items = [f"New {b['name']} watches for men, women and kids", "Free strap / chain sizing when you buy"] + items
        faqs.insert(0, (f"Where can I buy {b['name']} watches in Chandkheda?",
                        f"{B['name']} at {full_address()} sells {b['name']} watches. Call {B['phone_display']} or WhatsApp {B['phone2_display']} to ask about models in stock."))
    else:
        title = f"{b['name']} Watch Repair & Battery Replacement in Ahmedabad"
    body = f"""<div class="wrap page-head"><h1>{e(title)}</h1><p class="lead">{e(b["note"])}</p></div>
<section><div class="wrap prose">{answer_box(f"Bring your {noun} to {B['name']}, {full_address()}. We handle everyday jobs like {'movement replacement' if is_clock else 'batteries, straps, glass'} and repairs. Open {HOURS}.")}
<h2>{e(noun)} services</h2>{ticks(items)}
<p class="note">{e(B["name"])} is an independent shop{" and is not an authorised " + e(b["name"]) + " service centre" if b["sold"] else " and is not affiliated with or authorised by " + e(b["name"])}. Brand names are used only to describe the watches and clocks we sell and work on.</p></div></section>
{reviews_section([REVIEW_FOR[b["slug"]]], "From our Google reviews", alt=True) if b["slug"] in REVIEW_FOR else ""}
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Related services</h2>{svc_links}</div></section>
{faq_html(faqs)}{cta_block()}"""
    page(path, f"{title} | {B['name']}",
         f"{noun} repair, battery & straps in Chandkheda, Ahmedabad at {B['name']}. Rated {B['rating']}★. Independent shop. Call {B['phone_display']}.",
         body, schema=[faq_schema(faqs)], crumbs=crumbs, priority="0.6")


def render_section(blocks):
    out = []
    for blk in blocks:
        if isinstance(blk, tuple) and blk[0] == "ul":
            out.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in blk[1]) + "</ul>")
        else:
            out.append(f"<p>{e(blk)}</p>")
    return "".join(out)


def build_guides_index():
    crumbs = [("Home", "/"), ("Guides", "/guides/")]
    cards = "".join(f'<div class="card"><h3><a href="/guides/{g["slug"]}/">{e(g["title"])}</a></h3><p>{e(g["description"])}</p></div>' for g in GUIDES)
    body = f"""<div class="wrap page-head"><h1>Watch &amp; Clock Care Guides</h1>
<p class="lead">Simple, honest answers to the questions customers ask us every day at our Chandkheda shop.</p></div>
<section><div class="wrap"><div class="grid">{cards}</div></div></section>{cta_block()}"""
    page("/guides/", f"Watch Care Guides & Tips | {B['name']} Ahmedabad",
         "Guides on watch battery life, a stopped watch, strap sizes, water resistance, quartz vs automatic, wall clocks and watch gifts.",
         body, crumbs=crumbs, priority="0.7")


def build_guide(g):
    path = f"/guides/{g['slug']}/"
    crumbs = [("Home", "/"), ("Guides", "/guides/"), (g["title"], path)]
    sections = "".join(f"<h2>{e(h)}</h2>{render_section(blocks)}" for h, blocks in g["sections"])
    rel = service_cards([SVC[x] for x in g["related"]])
    article = {"@type": "Article", "headline": g["title"], "description": g["description"],
               "author": {"@id": BIZ_ID}, "publisher": {"@id": BIZ_ID}, "datePublished": "2026-10-27",
               "dateModified": TODAY, "mainEntityOfPage": SITE_URL + path, "image": SITE_URL + "/og-image.png",
               "inLanguage": "en-IN"}
    body = f"""<div class="wrap page-head"><h1>{e(g["title"])}</h1><p class="lead">{e(g["description"])}</p>
<p class="note">By {e(B["name"])}, Chandkheda, Ahmedabad · Updated {TODAY}</p></div>
<section><article class="wrap prose">{answer_box(g["answer"], "Short answer")}{sections}</article></section>
{faq_html(g["faqs"])}
<section class="alt"><div class="wrap"><h2 style="margin-top:0">Need help with your watch?</h2>{rel}</div></section>{cta_block()}"""
    page(path, f"{g['title']} | {B['name']}", g["description"], body,
         schema=[article, faq_schema(g["faqs"])], crumbs=crumbs, og_type="article", priority="0.6")


def build_about():
    crumbs = [("Home", "/"), ("About", "/about/")]
    body = f"""<div class="wrap page-head"><h1>About {e(B["name"])}</h1>
<p class="lead">A local watch shop and watch &amp; clock repair service in Nigam Nagar, Chandkheda, Ahmedabad, trusted by {B["review_count"]}+ Google reviewers ({B["rating"]}★).</p></div>
<section><div class="wrap prose">
<p>{e(B["name"])} (also known as {e(", ".join(B["alt_names"]))}) is a neighbourhood watch store and repair shop at {e(full_address())}.</p>
<p>We help people in Chandkheda and across Ahmedabad keep their watches and clocks running. We change batteries, repair watches and wall clocks, fit new straps, chains and glass, and sell wristwatches and wall clocks for daily use and gifting.</p>
<h2>How we work</h2>{ticks(["We check your watch in front of you", "We explain the problem in simple words", "We tell you the price before starting", "We test everything before handing it back", "We tell you honestly if a job needs a specialist or brand service centre"])}
<h2>What customers say</h2>{ticks([t + ": " + d for t, d in REVIEW_THEMES])}
</div></section>{reviews_section(range(len(REVIEWS)), "Reviews from our customers", alt=True)}{cta_block()}"""
    page("/about/", f"About {B['name']} | Watch Shop in Chandkheda, Ahmedabad",
         f"About {B['name']}: a trusted local watch shop and watch & clock repair service in Nigam Nagar, Chandkheda, Ahmedabad. Rated {B['rating']}★ by {B['review_count']}+ customers.",
         body, crumbs=crumbs, priority="0.6")


def build_contact():
    crumbs = [("Home", "/"), ("Contact", "/contact/")]
    rows = "".join(f"<tr><td>{d}</td><td>10:30 AM – 9:00 PM</td></tr>" for d in DAYS)
    body = f"""<div class="wrap page-head"><h1>Contact &amp; Directions: {e(B["name"])}, Chandkheda</h1>
<p class="lead">Walk in, call or WhatsApp. We're in Swapna Shilp Complex, Nigam Nagar, near ONGC on the Visat–Sabarmati Highway.</p>
<div class="btns"><a class="btn btn-dark" href="tel:{B["phone"]}">{icon("phone", 18)} Call {e(B["phone_display"])}</a>
<a class="btn btn-wa" href="{e(wa_link())}" rel="noopener" target="_blank">{icon("wa", 18)} WhatsApp</a>
<a class="btn btn-gold" href="{e(B["maps_url"])}" rel="noopener" target="_blank">{icon("pin", 18)} Open in Google Maps</a></div></div>
<section><div class="wrap two"><div>{map_embed()}</div><div>{nap_card()}
<h2>Opening hours</h2><table class="hours"><tbody>{rows}</tbody></table>
<p class="note">Hours may change on festivals and public holidays. Please call before a special trip.</p></div></div></section>"""
    page("/contact/", f"Contact & Directions | {B['name']}, Chandkheda, Ahmedabad",
         f"{B['name']}, Swapna Shilp Complex, Nigam Nagar, Chandkheda, Ahmedabad 382424. Call {B['phone_display']}. Open daily 10:30 AM–9 PM.",
         body, crumbs=crumbs, priority="0.8")


def build_faq():
    crumbs = [("Home", "/"), ("FAQ", "/faq/")]
    general = [
        ("Where is Jay Santoshi Watch?", f"{full_address()}."),
        ("What are your opening hours?", f"{B['hours_display']}. Hours may change on festivals."),
        ("What is your phone number?", f"Call {B['phone_display']} or {B['phone2_display']}. WhatsApp us on {B['phone2_display']}."),
        ("Are you an authorised service centre for any brand?", "No. We are an independent watch shop and repair service."),
        ("Do I need an appointment?", "No. Just walk in during shop hours."),
    ]
    seen, svc_faqs = set(), []
    for s in SERVICES:
        for q, a in s["faqs"]:
            if q not in seen:
                seen.add(q)
                svc_faqs.append((q, a))
    allfaqs = general + svc_faqs
    items = "".join(f"<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in svc_faqs)
    gen = "".join(f"<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in general)
    body = f"""<div class="wrap page-head"><h1>Frequently Asked Questions</h1>
<p class="lead">Answers about watch repair, battery replacement, straps, clocks and visiting {e(B["name"])} in Chandkheda, Ahmedabad.</p></div>
<section class="faq"><div class="wrap"><h2 style="margin-top:0">Visiting the shop</h2>{gen}<h2>Repairs, batteries, straps &amp; clocks</h2>{items}</div></section>{cta_block()}"""
    page("/faq/", f"FAQ: Watch Repair, Battery & Clock Questions | {B['name']}",
         "Answers to common questions about watch battery replacement, watch and clock repair, straps, timings and location of Jay Santoshi Watch, Chandkheda.",
         body, schema=[faq_schema(allfaqs)], crumbs=crumbs, priority="0.7")


def build_404():
    body = f"""<div class="wrap page-head" style="padding:48px 16px"><h1>Page not found</h1>
<p class="lead">Sorry, that page doesn't exist. Try one of these:</p>
<ul class="pills"><li><a href="/">Home</a></li><li><a href="/services/">Services</a></li><li><a href="/areas/">Areas</a></li><li><a href="/contact/">Contact</a></li></ul></div>"""
    doc_path = "/404.html"
    canonical_backup = list(PAGES)
    page(doc_path, f"Page not found | {B['name']}", "Page not found.", body)
    PAGES[:] = canonical_backup  # keep 404 out of the sitemap
    # 404 must not be indexed
    target = os.path.join(OUT, "404.html")
    with open(target, encoding="utf-8") as f:
        txt = f.read().replace("index,follow,max-image-preview:large,max-snippet:-1", "noindex,follow")
    with open(target, "w", encoding="utf-8") as f:
        f.write(txt)


# ---------------------------------------------------------------------------
# Non-HTML files
# ---------------------------------------------------------------------------

def build_sitemap():
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')


def build_robots():
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot",
            "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "DuckDuckBot"]
    rules = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    write("/robots.txt", f"# Search engines and AI assistants are welcome.\n{rules}User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")


def build_llms():
    svc = "\n".join(f"- [{s['name']}]({SITE_URL}/services/{s['slug']}/): {s['short']}" for s in SERVICES)
    areas = ", ".join(a["name"] for a in AREAS)
    guides = "\n".join(f"- [{g['title']}]({SITE_URL}/guides/{g['slug']}/): {g['answer']}" for g in GUIDES)
    brands = ", ".join(b["name"] for b in BRANDS)
    reviews = "\n".join(f'- "{r["text"]}" — {r["author"]} ({r["topic"]})' for r in REVIEWS)
    txt = f"""# {B['name']}

> {B['name']} is a watch store and watch & clock repair shop in {B['locality']}, {B['city']}, {B['region']}, India. Rated {B['rating']}/5 on Google from {B['review_count']}+ reviews.

## Key facts
- Name: {B['name']} (also: {', '.join(B['alt_names'])})
- Category: Watch store, watch repair shop, clock repair service
- Address: {full_address()}, India
- Landmark: {B['landmark']}
- Phone: {B['phone_display']} / {B['phone2_display']} (WhatsApp: {B['phone2_display']})
- Hours: {B['hours_display']} (may change on festivals)
- Google Maps: {B['maps_url']}
- Independent shop, not an authorised service centre of any brand.
- Languages: Gujarati, Hindi, English

## Services
{svc}

## Brands sold
{', '.join(SOLD_BRANDS)}

## Brands serviced
{brands}

## Customer reviews (Google, 5★)
{reviews}

## Areas served
Customers come from: {areas}, and the rest of Ahmedabad and Gandhinagar.

## Guides (short answers)
{guides}

## Pages
- [Home]({SITE_URL}/)
- [All services]({SITE_URL}/services/)
- [Areas served]({SITE_URL}/areas/)
- [Brands]({SITE_URL}/brands/)
- [FAQ]({SITE_URL}/faq/)
- [Contact & directions]({SITE_URL}/contact/)
"""
    write("/llms.txt", txt)


def build_static():
    for name in os.listdir(os.path.join(SRC, "static")):  # style.css, Google verification file, etc.
        shutil.copy(os.path.join(SRC, "static", name), os.path.join(OUT, name))
    write("/favicon.svg", """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14213d"/><rect x="24" y="6" width="16" height="10" rx="2" fill="#c8962b"/><rect x="24" y="48" width="16" height="10" rx="2" fill="#c8962b"/><circle cx="32" cy="32" r="17" fill="#fff" stroke="#c8962b" stroke-width="4"/><path d="M32 22v10l7 4" stroke="#14213d" stroke-width="4" stroke-linecap="round" fill="none"/></svg>""")
    manifest = {"name": B["name"], "short_name": "Jay Santoshi", "start_url": "/", "display": "standalone",
                "background_color": "#ffffff", "theme_color": "#14213d",
                "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    write("/site.webmanifest", json.dumps(manifest, indent=2))
    try:
        make_images()
    except ImportError:
        print("Pillow not installed: skipped PNG icons / og-image (existing ones kept)")


def make_images():
    from PIL import Image, ImageDraw, ImageFont
    fonts = "/usr/share/fonts/truetype/dejavu/"

    def font(name, size):
        try:
            return ImageFont.truetype(fonts + name, size)
        except OSError:
            return ImageFont.load_default()

    def logo(size):
        s = size / 64
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(14 * s), fill="#14213d")
        d.rounded_rectangle([24 * s, 6 * s, 40 * s, 16 * s], radius=int(2 * s), fill="#c8962b")
        d.rounded_rectangle([24 * s, 48 * s, 40 * s, 58 * s], radius=int(2 * s), fill="#c8962b")
        d.ellipse([15 * s, 15 * s, 49 * s, 49 * s], fill="#ffffff", outline="#c8962b", width=max(1, int(4 * s)))
        d.line([(32 * s, 22 * s), (32 * s, 32 * s), (39 * s, 36 * s)], fill="#14213d", width=max(1, int(4 * s)), joint="curve")
        return im

    for sz, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        logo(sz).save(os.path.join(OUT, name))

    og = Image.new("RGB", (1200, 630), "#14213d")
    d = ImageDraw.Draw(og)
    d.rectangle([0, 590, 1200, 630], fill="#c8962b")
    og.paste(logo(220), (900, 190), logo(220))
    d.text((80, 120), B["name"], font=font("DejaVuSans-Bold.ttf", 76), fill="#ffffff")
    d.text((80, 225), "Watch Shop & Watch Repair", font=font("DejaVuSans-Bold.ttf", 46), fill="#c8962b")
    d.text((80, 290), "Battery • Straps • Glass • Clock Repair", font=font("DejaVuSans.ttf", 34), fill="#dfe5f3")
    d.text((80, 380), f"★ {B['rating']}/5 · {B['review_count']}+ Google reviews", font=font("DejaVuSans-Bold.ttf", 36), fill="#ffc94a")
    d.text((80, 450), "Nigam Nagar, Chandkheda, Ahmedabad", font=font("DejaVuSans.ttf", 34), fill="#ffffff")
    d.text((80, 505), f"Call {B['phone_display']} · Open daily 10:30 AM–9 PM", font=font("DejaVuSans.ttf", 30), fill="#dfe5f3")
    og.save(os.path.join(OUT, "og-image.png"), optimize=True)


def main():
    if os.path.isdir(OUT):
        for name in os.listdir(OUT):
            p = os.path.join(OUT, name)
            if name.endswith(".png"):
                continue  # keep images if Pillow is missing on this machine
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)

    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_areas_index()
    for i, a in enumerate(AREAS):
        build_area(a, i)
        if has_combo(a):
            for s in AREA_SERVICES:
                build_area_service(a, s)
    build_brands_index()
    for b in BRANDS:
        build_brand(b)
    build_guides_index()
    for g in GUIDES:
        build_guide(g)
    build_about()
    build_contact()
    build_faq()
    build_404()
    build_static()
    build_sitemap()
    build_robots()
    build_llms()
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
