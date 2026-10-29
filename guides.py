"""Ratgeber-/Vergleichsseiten. Alle Fakten kommen aus data/tools.json (Anbieterangaben mit Quelle).
Redaktioneller Text: nur neutrale Prüfpunkte, keine Rechtsbewertung."""

GUIDES = [
    {"slug": "chatgpt-alternativen-eu-hosting", "kat": "ki-chatbots",
     "h1": "ChatGPT-Alternativen mit EU-Hosting für Unternehmen",
     "title": "ChatGPT-Alternativen mit EU-Hosting: {n} Tools im Vergleich (DSGVO-Prüfpunkte)",
     "desc": "{n} ChatGPT-Alternativen, deren Anbieter Hosting in Deutschland oder der EU angeben – mit AVV-Hinweis, Preis und Quelle. Vergleich für KMU, Stand {stand}.",
     "kurz": "ChatGPT-Alternativen mit EU-Hosting",
     "lead": "Sie suchen eine ChatGPT-Alternative, bei der die Daten in Deutschland oder der EU bleiben? Hier stehen {n} Unternehmens-KI-Plattformen nebeneinander – mit den Angaben der Anbieter zu Serverstandort, AVV und Preis.",
     "checks": [
        "Wo werden Eingaben und Chatverläufe gespeichert, und wo laufen die Sprachmodelle? Manche Anbieter hosten die Anwendung in der EU, nutzen aber einzelne Modelle anderswo.",
        "Gibt es einen Auftragsverarbeitungsvertrag (AVV/DPA) nach Art. 28 DSGVO – öffentlich, als Self-Service oder auf Anfrage?",
        "Werden Ihre Eingaben zum Training von Modellen verwendet? Das steht meist in den Datenschutz- oder Sicherheitsseiten der Anbieter.",
        "Welche Unterauftragsverarbeiter (z. B. Cloud-Anbieter) setzt der Anbieter ein, und gehört einer davon zu einem Konzern außerhalb der EU?",
        "Preismodell: pro Nutzer, pro Unternehmen oder nach Verbrauch (Credits/Token)?"]},
    {"slug": "ki-transkription-dsgvo-vergleich", "kat": "transkription-dsgvo",
     "h1": "KI-Transkription & Meeting-Protokolle mit Datenspeicherung in DE/EU",
     "title": "KI-Transkription DSGVO: {n} Tools mit Hosting in Deutschland/EU im Vergleich",
     "desc": "{n} Transkriptions- und Meeting-Tools mit Speicherung in Deutschland oder der EU laut Anbieter: Serverstandort, AVV, Preise und Quellen im Vergleich. Stand {stand}.",
     "kurz": "KI-Transkription mit EU-Hosting",
     "lead": "Meetings, Interviews oder Diktate automatisch transkribieren, ohne dass die Aufnahmen in die USA gehen? Diese {n} Tools geben laut Anbieter Speicherung bzw. Verarbeitung in Deutschland oder der EU an.",
     "checks": [
        "Wo wird die Spracherkennung ausgeführt, und wo werden Audio und Transkript gespeichert? Das kann sich unterscheiden.",
        "Wird die Audiodatei nach der Verarbeitung gelöscht oder dauerhaft gespeichert?",
        "Bei Meeting-Bots: Werden alle Teilnehmenden über die Aufzeichnung informiert, und wer muss zustimmen? Das klären Sie am besten mit Ihrem Datenschutzbeauftragten.",
        "Gibt es einen AVV/DPA – und ist er in Ihrem Tarif enthalten?",
        "Abrechnung nach Minuten/Stunden oder pauschal pro Nutzer?"]},
    {"slug": "llm-api-eu-hosting", "kat": "ki-infrastruktur",
     "h1": "Sprachmodelle per API mit Hosting in Europa (OpenAI-API-Alternativen)",
     "title": "LLM-API mit EU-Hosting: {n} europäische Alternativen zur OpenAI-API",
     "desc": "{n} Anbieter, die Sprachmodelle per API aus europäischen Rechenzentren anbieten oder Self-Hosting ermöglichen – Region, AVV, Token-Preise und Quellen. Stand {stand}.",
     "kurz": "LLM-APIs mit EU-Hosting",
     "lead": "Für eigene KI-Anwendungen brauchen Sie ein Sprachmodell per API – aber aus einem europäischen Rechenzentrum? Diese {n} Optionen geben laut Anbieter Hosting in der EU bzw. Deutschland an oder lassen sich selbst betreiben.",
     "checks": [
        "In welcher Region läuft die Inferenz, und lässt sie sich fest auf die EU einstellen?",
        "Welche Modelle sind verfügbar (Open-Source-Modelle wie Llama, Mistral, Qwen, GPT-oss)?",
        "Gibt es ein Data Processing Agreement, und werden API-Eingaben gespeichert oder protokolliert?",
        "Preis pro Million Token für Input und Output – und gibt es ein Gratis-Kontingent zum Testen?",
        "Alternative Self-Hosting: Dann liegt der Standort bei Ihnen, aber auch Betrieb und Sicherheit."]},
]

def build_guides(page, TOOLS, CATS, D, e, badge, unk, de_date, BASE, crumbs):
    STAND = de_date(D["stand"])
    urls = []
    for g in GUIDES:
        ts = [t for t in TOOLS if t["kategorie"] == g["kat"]]
        n = len(ts)
        reg = {}
        for t in ts: reg.setdefault(t["hosting_region"], []).append(t)
        avv_known = [t for t in ts if not t["dsgvo_avv"].strip().lower().startswith("unbekannt")]
        price_known = [t for t in ts if not t["preis"].strip().lower().startswith("unbekannt")]
        rows = "".join(
            f'<tr><td><a href="../../tool/{t["slug"]}/"><strong>{e(t["name"])}</strong></a>{"" if t["anbieter"].lower().startswith("unbekannt") else '<div class="muted small">'+e(t["anbieter"])+'</div>'}</td>'
            f'<td>{badge(t["hosting_region"])}<div class="small">{unk(t["hosting_angabe"])}</div></td>'
            f'<td class="small">{unk(t["dsgvo_avv"])}</td><td class="small">{unk(t["preis"])}</td></tr>' for t in ts)
        table = ('<div class="tablewrap"><table class="tools"><thead><tr><th>Tool</th><th>Hosting laut Anbieter</th><th>AVV/DPA laut Anbieter</th><th>Preis-Hinweis</th></tr></thead>'
                 f'<tbody>{rows}</tbody></table></div>')
        regsum = " · ".join(f'{e(r)}: {", ".join(e(t["name"]) for t in v)}' for r, v in sorted(reg.items()))
        de_only = [t["name"] for t in ts if t["hosting_region"].startswith("DE")]
        faq = [
            (f"Welche dieser Tools geben einen Serverstandort in Deutschland an?",
             (", ".join(de_only) + " geben laut eigener Website Hosting bzw. Verarbeitung in Deutschland an (teils zusätzlich EU).") if de_only else "Keines der hier gelisteten Tools nennt ausschließlich Deutschland; alle geben die EU bzw. Europa an."),
            ("Bei welchen Tools ist ein AVV bzw. DPA öffentlich erwähnt?",
             f"Bei {len(avv_known)} von {n}: " + ", ".join(t["name"] for t in avv_known) + ". Bei den übrigen haben wir auf den Anbieterseiten keine eindeutige Angabe gefunden (Stand {STAND})."),
            ("Sind diese Tools damit automatisch DSGVO-konform?",
             "Nein, das lässt sich nicht pauschal sagen. Das Verzeichnis gibt nur Angaben der Anbieter wieder. Ob ein Tool für Ihren Einsatz zulässig ist, hängt u. a. von AVV, Unterauftragsverarbeitern und Ihren Daten ab – klären Sie das mit Ihrem Datenschutzbeauftragten."),
        ]
        faqh = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faq)
        checks = "".join(f"<li>{e(c)}</li>" for c in g["checks"])
        others = " · ".join(f'<a href="../{o["slug"]}/">{e(o["kurz"])}</a>' for o in GUIDES if o["slug"] != g["slug"])
        c = CATS[g["kat"]]
        body = f"""<nav class="bc"><a href="../../">Start</a> › <a href="../">Ratgeber</a> › {e(g['kurz'])}</nav>
<h1>{e(g['h1'])}</h1><p class="lead">{e(g['lead'].format(n=n))}</p>
<p class="muted">{n} Tools · {len(avv_known)} mit AVV-/DPA-Angabe · {len(price_known)} mit öffentlichem Preis-Hinweis · Stand: {STAND}. {e(D['hinweis'])}</p>
<h2>Vergleich: Hosting, AVV und Preise laut Anbieter</h2>{table}
<p class="small">Hosting-Regionen laut Anbieter – {regsum}</p>
<h2>Worauf Sie bei der Auswahl achten sollten</h2><ul>{checks}</ul>
<p class="disc">Diese Liste ist eine Orientierung, keine Rechtsberatung.</p>
<h2>Häufige Fragen</h2>{faqh}
<p class="small">Alle Einträge der Kategorie: <a href="../../kategorie/{c['slug']}/">{e(c['name'])}</a> · Weitere Ratgeber: {others} · <a href="../../methodik/">So prüfen wir</a></p>"""
        p = f"ratgeber/{g['slug']}/"; urls.append(p)
        ld = [crumbs([("Start", ""), ("Ratgeber", "ratgeber/"), (g["kurz"], p)]),
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                  {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
              {"@context": "https://schema.org", "@type": "ItemList", "name": g["h1"], "numberOfItems": n,
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + f"tool/{t['slug']}/", "name": t["name"]} for i, t in enumerate(ts)]}]
        page(p, g["title"].format(n=n), g["desc"].format(n=n, stand=STAND), body, 2, ld)
    # Übersicht
    tiles = "".join(f'<a class="tile" href="{g["slug"]}/"><h3>{e(g["h1"])}</h3><p>{e(g["desc"].format(n=sum(t["kategorie"]==g["kat"] for t in TOOLS), stand=STAND))}</p></a>' for g in GUIDES)
    body = f"""<nav class="bc"><a href="../">Start</a> › Ratgeber</nav><h1>Ratgeber: KI mit EU-Hosting auswählen</h1>
<p class="lead">Vergleiche nach Anwendungsfall – mit den Angaben der Anbieter zu Serverstandort, AVV und Preis.</p><div class="tiles">{tiles}</div>"""
    page("ratgeber/", "Ratgeber: KI-Tools mit EU-Hosting vergleichen – KI-EU-Verzeichnis", "Vergleiche von KI-Tools mit Hosting in Deutschland/EU nach Anwendungsfall: ChatGPT-Alternativen, Transkription, LLM-APIs.", body, 1)
    urls.append("ratgeber/")
    return urls

def home_section(TOOLS):
    links = "".join(f'<a class="tile" href="ratgeber/{g["slug"]}/"><h3>{g["h1"]}</h3><p>{sum(t["kategorie"]==g["kat"] for t in TOOLS)} Tools im Vergleich</p></a>' for g in GUIDES)
    return f'<section><h2>Ratgeber & Vergleiche</h2><div class="tiles">{links}</div></section>'
