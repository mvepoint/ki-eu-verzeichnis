#!/usr/bin/env python3
"""Statischer Generator: data/tools.json -> docs/ (GitHub Pages: Branch main, Ordner /docs)."""
import json, os, shutil, html, datetime
import guides
BASE = "https://mvepoint.github.io/ki-eu-verzeichnis/"  # TODO Max: echte Basis-URL/Domain eintragen
SITE = "KI-EU-Verzeichnis"
OUT = "docs"
D = json.load(open("data/tools.json", encoding="utf-8"))
CATS = {c["slug"]: c for c in D["kategorien"]}
TOOLS = D["tools"]
STAND = D["stand"]
e = lambda s: html.escape(str(s), quote=True)
def de_date(iso): y, m, d = iso.split("-"); return f"{d}.{m}.{y}"

def page(path, title, desc, body, depth, jsonld=None, noindex=False):
    r = "../" * depth
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    canon = BASE + path
    nav = "".join(f'<a href="{r}kategorie/{c["slug"]}/">{e(c["kurz"])}</a>' for c in D["kategorien"])
    doc = f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canon}"><meta property="og:locale" content="de_DE">
<link rel="stylesheet" href="{r}assets/style.css">{ld}</head>
<body><a class="skip" href="#main">Zum Inhalt</a>
<header class="top"><div class="wrap"><a class="logo" href="{r}">KI<span>·EU</span> Verzeichnis</a>
<nav class="cats">{nav}</nav></div></header>
<main id="main" class="wrap">{body}</main>
<footer class="foot"><div class="wrap">
<p class="disc"><strong>Hinweis:</strong> {e(D['hinweis'])} Angaben können sich ändern – maßgeblich sind die verlinkten Anbieterseiten. Keine Rechtsberatung.</p>
<p><a href="{r}ratgeber/">Ratgeber</a> · <a href="{r}methodik/">Methodik</a> · <a href="{r}tool-eintragen/">Tool eintragen</a> · <a href="{r}#newsletter">Newsletter</a> · <a href="{r}impressum/">Impressum</a> · <a href="{r}datenschutz/">Datenschutz</a> · <a href="https://tally.so/r/VpprVl" rel="noopener" target="_blank">Kontakt</a></p>
<p class="muted">Datenstand: {de_date(STAND)}</p></div></footer>
<script src="{r}assets/app.js" defer></script>
<script data-goatcounter="https://ki-eu-verzeichnis.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script></body></html>"""
    fp = os.path.join(OUT, path, "index.html") if not path.endswith(".html") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(doc)

def badge(region):
    cls = "de" if region.startswith("DE") else ("self" if "Self" in region else "eu")
    return f'<span class="badge {cls}">{e(region)}</span>'

def unk(s):
    return f'<span class="unk">unbekannt</span>' if s.strip().lower().startswith("unbekannt") else e(s)

def table(tools, r, show_cat=True):
    rows = []
    for t in tools:
        c = CATS[t["kategorie"]]
        rows.append(f'<tr data-cat="{t["kategorie"]}" data-region="{e(t["hosting_region"])}" data-q="{e((t["name"]+" "+t["beschreibung"]+" "+t["hosting_angabe"]).lower())}">'
            f'<td><a href="{r}tool/{t["slug"]}/"><strong>{e(t["name"])}</strong></a><div class="muted small">{e(t["beschreibung"])}</div></td>'
            + (f'<td><a href="{r}kategorie/{c["slug"]}/">{e(c["kurz"])}</a></td>' if show_cat else "")
            + f'<td>{badge(t["hosting_region"])}</td><td class="small">{unk(t["dsgvo_avv"])}</td><td class="small">{unk(t["preis"])}</td></tr>')
    head = "<th>Tool</th>" + ("<th>Kategorie</th>" if show_cat else "") + "<th>Hosting laut Anbieter</th><th>AVV/DPA laut Anbieter</th><th>Preis-Hinweis</th>"
    return f'<div class="tablewrap"><table class="tools"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

KIT_FORM_ID = "KIT_FORM_ID_TBD"  # numerische Kit-Formular-ID des KI-EU-Formulars (noch anzulegen)
NEWSLETTER = """<section id="newsletter" class="box nl"><h2>Wöchentlich: neue EU-KI-Tools für KMU</h2>
<p>Jeden Donnerstag die neu aufgenommenen und geänderten Einträge – kurz, mit Quellen.</p>
<form class="nlform" action="https://app.kit.com/forms/""" + KIT_FORM_ID + """/subscriptions" method="post"><label for="nl-mail" class="sr">E-Mail</label>
<input id="nl-mail" name="email_address" type="email" placeholder="name@firma.de" required autocomplete="email"><button type="submit">Anmelden</button></form>
<p class="muted">Kostenlos, jederzeit abbestellbar. Sie erhalten zuerst eine E-Mail mit einem Bestätigungslink (Double-Opt-In). Versand über Kit (USA), Details in der <a href="/ki-eu-verzeichnis/datenschutz/#newsletter">Datenschutzerklärung</a>.</p></section>"""

IMPRESSUM = """<h1>Impressum</h1>
<h2>Angaben gemäß § 5 DDG</h2>
<p>Maximilian van Elst<br>Gerhart-Hauptmann-Ring 58<br>81737 München<br>Deutschland</p>
<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:mvepoint@gmail.com">mvepoint@gmail.com</a><br>
Kontaktformular: <a href="https://tally.so/r/VpprVl" rel="noopener" target="_blank">https://tally.so/r/VpprVl</a></p>
<h2>Umsatzsteuer</h2>
<p>Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz: DE367537481<br>
Kleinunternehmer gemäß § 19 UStG.</p>
<h2>Verantwortlich für den Inhalt gemäß § 18 Abs. 2 MStV</h2>
<p>Maximilian van Elst<br>Gerhart-Hauptmann-Ring 58<br>81737 München</p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Inhalte und Links</h2>
<p>Die Angaben in diesem Verzeichnis geben Aussagen der jeweiligen Anbieter wieder und werden mit Quelle und Prüfdatum veröffentlicht. Trotz sorgfältiger Prüfung übernehmen wir keine Gewähr für Richtigkeit, Vollständigkeit und Aktualität; maßgeblich sind die verlinkten Anbieterseiten. Die Inhalte stellen keine Rechtsberatung dar.</p>
<p>Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte wir keinen Einfluss haben. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber verantwortlich. Bei Bekanntwerden von Rechtsverletzungen entfernen wir derartige Links umgehend. Hinweise auf veraltete oder falsche Angaben nehmen wir gern per E-Mail oder über das Kontaktformular entgegen.</p>"""

DATENSCHUTZ = """<h1>Datenschutzerklärung</h1>
<p class="muted">Stand: {stand}</p>
<h2>1. Verantwortlicher</h2>
<p>Verantwortlich für die Datenverarbeitung auf dieser Website im Sinne der Datenschutz-Grundverordnung (DSGVO) ist:</p>
<p>Maximilian van Elst<br>Gerhart-Hauptmann-Ring 58<br>81737 München<br>Deutschland<br>E-Mail: <a href="mailto:mvepoint@gmail.com">mvepoint@gmail.com</a></p>
<h2>2. Überblick</h2>
<p>Diese Website ist ein statisches Verzeichnis. Sie setzt <strong>keine Cookies</strong>, bindet <strong>keine externen Schriftarten oder eingebetteten Inhalte Dritter</strong> ein und speichert keine Daten in Ihrem Browser. Einzige externe Komponente ist das Skript des cookielosen Reichweitenmessdienstes GoatCounter (Abschnitt 4), mit dem wir anonyme, zusammengefasste Besucherzahlen erheben. Das kleine Skript für Suche und Filter läuft ausschließlich lokal in Ihrem Browser und sendet keine Daten. Es gibt derzeit kein Benutzerkonto, keine Kommentarfunktion, kein aktives Formular zum Eintragen von Tools. Das Newsletter-Formular (Abschnitt 7) überträgt Daten erst, wenn Sie es absenden. Das Kontaktformular (Abschnitt 6) ist nicht in diese Website eingebettet, sondern nur verlinkt; erst wenn Sie den Link anklicken, wird eine Seite des Formulardienstes Tally geladen.</p>
<h2>3. Hosting durch GitHub Pages und Server-Logfiles</h2>
<p>Diese Website wird über den Dienst GitHub Pages bereitgestellt. Anbieter ist die GitHub, Inc., 88 Colin P. Kelly Jr. St., San Francisco, CA 94107, USA (in der EU: GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Niederlande).</p>
<p>Beim Aufruf der Website werden durch GitHub technisch notwendige Daten verarbeitet, insbesondere Ihre IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite sowie Angaben zu Browser und Betriebssystem (Server-Logfiles). GitHub gibt an, dass die IP-Adresse von Besuchern einer GitHub-Pages-Website aus Sicherheitsgründen protokolliert und gespeichert wird. Wir selbst haben keinen Zugriff auf diese Logfiles und führen keine eigene Auswertung durch.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt in der sicheren, stabilen und kostengünstigen Bereitstellung der Website.</p>
<p>Dabei können Daten in die USA übermittelt werden. GitHub ist nach eigenen Angaben unter dem EU-US Data Privacy Framework zertifiziert, für das ein Angemessenheitsbeschluss der EU-Kommission besteht (Art. 45 DSGVO). Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener" target="_blank">Datenschutzerklärung von GitHub</a>.</p>
<h2>4. Reichweitenmessung mit GoatCounter</h2>
<p>Um zu erfahren, wie viele Besucher die Website hat und welche Seiten aufgerufen werden, nutzen wir den Dienst GoatCounter (goatcounter.com). GoatCounter wird nach eigenen Angaben von Martin Tournoij mit Sitz in Irland betrieben; die Daten werden auf Servern der Hetzner Online GmbH in Finnland und Deutschland gespeichert. Das Zählskript wird von der Adresse gc.zgo.at über ein Content-Delivery-Network (BunnyCDN) geladen; dabei wird, wie bei jedem Abruf einer Datei, technisch Ihre IP-Adresse verarbeitet.</p>
<p>GoatCounter setzt <strong>keine Cookies</strong> und speichert nach eigenen Angaben auch sonst nichts in Ihrem Browser (kein localStorage, kein Cache o. Ä.). Beim Seitenaufruf werden die aufgerufene Seite, die verweisende Seite (Referrer), Browser und Betriebssystem, Bildschirmbreite, Sprache sowie das aus der IP-Adresse abgeleitete Land übermittelt. Gespeichert werden nach Angaben von GoatCounter nur zusammengefasste Zählwerte je Stunde bzw. Tag (z. B. „Seite X: 4 Aufrufe mit Firefox“), die nicht miteinander verknüpft werden können. <strong>IP-Adressen, der vollständige User-Agent und Tracking-Kennungen werden nicht gespeichert.</strong> Um wiederholte Aufrufe nicht mehrfach zu zählen, hält GoatCounter eine Zuordnung aus Website, IP-Adresse und User-Agent zu einer zufälligen Kennung für höchstens acht Stunden ausschließlich im Arbeitsspeicher; sie wird nicht in der Datenbank abgelegt. Eine Weitergabe an Dritte findet nach Angaben von GoatCounter nicht statt. Wir erhalten nur die zusammengefassten Statistiken; ein Rückschluss auf einzelne Personen ist uns nicht möglich.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt darin, die Reichweite und Nutzung des Verzeichnisses in anonymer, datensparsamer Form zu messen, um das Angebot zu verbessern. Sie können der Verarbeitung widersprechen (Art. 21 DSGVO), etwa indem Sie die Ausführung von JavaScript für gc.zgo.at in Ihrem Browser bzw. mit einem Inhaltsblocker unterbinden; die Website bleibt dabei voll nutzbar.</p>
<p>Weitere Informationen: <a href="https://www.goatcounter.com/help/privacy" rel="noopener" target="_blank">Datenschutzerklärung von GoatCounter</a> und <a href="https://www.goatcounter.com/help/gdpr" rel="noopener" target="_blank">GoatCounter zur DSGVO</a>.</p>
<h2>5. Kontakt per E-Mail</h2>
<p>Wenn Sie uns per E-Mail kontaktieren (z. B. um ein Tool vorzuschlagen oder eine Angabe zu korrigieren), verarbeiten wir Ihre E-Mail-Adresse, Ihren Namen (falls angegeben) und den Inhalt Ihrer Nachricht, um Ihre Anfrage zu bearbeiten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage auf einen Vertrag oder vorvertragliche Maßnahmen zielt, ansonsten Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen). Wir löschen die Daten, sobald die Anfrage abschließend bearbeitet ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<p>Für das E-Mail-Postfach nutzen wir den Dienst Gmail der Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland. Dabei kann eine Übermittlung in die USA nicht ausgeschlossen werden; Google ist nach eigenen Angaben unter dem EU-US Data Privacy Framework zertifiziert.</p>
<h2>6. Kontaktformular (Tally)</h2>
<p>Für Anfragen bieten wir ein Kontaktformular an, das über den Formulardienst Tally bereitgestellt wird: <a href="https://tally.so/r/VpprVl" rel="noopener" target="_blank">https://tally.so/r/VpprVl</a>. Anbieter ist die Tally BV, Sint-Pietersnieuwstraat 11, 9000 Gent, Belgien. Das Formular ist nicht in diese Website eingebettet; es öffnet sich auf einer Seite von Tally (tally.so), sobald Sie den Link anklicken.</p>
<p>Wenn Sie das Formular nutzen, verarbeiten wir Ihren Namen (freiwillige Angabe), Ihre E-Mail-Adresse, den Inhalt Ihrer Nachricht sowie Ihre Bestätigung der Einwilligungs-Checkbox, um Ihre Anfrage zu beantworten. Beim Aufruf der Formularseite verarbeitet Tally zudem technisch notwendige Daten wie Ihre IP-Adresse und Browserangaben. Über neue Einsendungen werden wir per E-Mail benachrichtigt; dabei gelangt der Inhalt Ihrer Nachricht in unser E-Mail-Postfach (siehe Abschnitt 5).</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO, sofern Ihre Anfrage auf einen Vertrag oder vorvertragliche Maßnahmen zielt, ansonsten Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen). Tally verarbeitet die Formulardaten als Auftragsverarbeiter in unserem Auftrag; nach eigenen Angaben werden die Formulardaten verschlüsselt und in Europa gespeichert. Tally setzt dafür weitere Dienstleister (Unterauftragsverarbeiter) ein, z. B. für Hosting und den Versand von E-Mail-Benachrichtigungen; dabei kann eine Übermittlung in Drittländer wie die USA nicht ausgeschlossen werden. Wir löschen die Einsendungen, sobald die Anfrage abschließend bearbeitet ist und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<p>Weitere Informationen: <a href="https://tally.so/help/privacy-policy" rel="noopener" target="_blank">Datenschutzerklärung von Tally</a> und <a href="https://tally.so/help/gdpr" rel="noopener" target="_blank">Tally zu DSGVO und Unterauftragsverarbeitern</a>.</p>
<h2 id="newsletter">7. Newsletter (Kit)</h2>
<p>Sie können unseren kostenlosen Newsletter mit neuen und geänderten Einträgen des Verzeichnisses abonnieren. Dafür benötigen wir nur Ihre E-Mail-Adresse. Das Anmeldeformular ist ein einfaches HTML-Formular ohne Skripte oder Cookies von Dritten; erst beim Absenden wird Ihre E-Mail-Adresse an den Versanddienstleister Kit übertragen.</p>
<p><strong>Double-Opt-In:</strong> Nach der Anmeldung erhalten Sie eine E-Mail mit einem Bestätigungslink. Erst nach der Bestätigung werden Sie in den Verteiler aufgenommen. Zum Nachweis der Einwilligung werden Zeitpunkt der Anmeldung und der Bestätigung sowie die IP-Adresse gespeichert.</p>
<p><strong>Rechtsgrundlage</strong> ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO). Sie können die Einwilligung jederzeit mit Wirkung für die Zukunft <strong>widerrufen</strong>, über den Abmeldelink in jeder Newsletter-E-Mail oder formlos per E-Mail an die oben genannte Adresse. Die Rechtmäßigkeit der bis zum Widerruf erfolgten Verarbeitung bleibt unberührt. Nach der Abmeldung löschen wir Ihre Adresse bzw. sperren sie nur noch für den Nachweis der früheren Einwilligung.</p>
<p><strong>Versanddienstleister:</strong> Der Newsletter wird über Kit versendet, einen Dienst der Kit, Inc. (vormals ConvertKit), P.O. Box 761, Boise, ID 83701, USA. Kit verarbeitet die Daten als Auftragsverarbeiter auf Grundlage eines Auftragsverarbeitungsvertrags (Kit Data Processing Addendum). Kit kann auswerten, ob ein Newsletter geöffnet und welche Links angeklickt wurden; diese Auswertung nutzen wir nur zusammengefasst, um den Newsletter zu verbessern.</p>
<p><strong>Übermittlung in die USA:</strong> Die Daten werden auf Servern von Kit in den USA verarbeitet. Kit war unter dem EU-US Data Privacy Framework zertifiziert; laut der offiziellen DPF-Liste ist diese Zertifizierung seit 31.07.2026 nicht mehr aktiv. Die Übermittlung erfolgt daher auf Grundlage der EU-Standardvertragsklauseln (Art. 46 Abs. 2 lit. c DSGVO), die im Auftragsverarbeitungsvertrag von Kit enthalten sind.</p>
<p>Weitere Informationen: <a href="https://kit.com/privacy" rel="noopener" target="_blank">Datenschutzerklärung von Kit</a> und <a href="https://kit.com/gdpr" rel="noopener" target="_blank">Kit zur DSGVO</a>.</p>
<h2>8. Links auf andere Websites</h2>
<p>Das Verzeichnis enthält Links zu Websites der gelisteten Anbieter. Beim Anklicken eines Links verlassen Sie unsere Website; für die Datenverarbeitung auf der Zielseite ist deren Betreiber verantwortlich. Vor dem Anklicken werden keine Daten an diese Anbieter übermittelt.</p>
<h2>9. Ihre Rechte</h2>
<p>Sie haben nach der DSGVO das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) sowie das Recht, einer Verarbeitung auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO aus Gründen, die sich aus Ihrer besonderen Situation ergeben, zu <strong>widersprechen</strong> (Art. 21). Wenden Sie sich dazu formlos an die oben genannte E-Mail-Adresse.</p>
<p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO). Zuständig für uns ist das Bayerische Landesamt für Datenschutzaufsicht (BayLDA), Promenade 18, 91522 Ansbach, <a href="https://www.lda.bayern.de" rel="noopener" target="_blank">www.lda.bayern.de</a>.</p>
<h2>10. Keine automatisierte Entscheidungsfindung</h2>
<p>Eine automatisierte Entscheidungsfindung einschließlich Profiling findet nicht statt.</p>
<h2>11. Änderungen</h2>
<p>Wir passen diese Datenschutzerklärung an, sobald sich die Website oder die eingesetzten Dienste ändern, insbesondere vor dem Start eines Eintragsformulars.</p>"""


def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (n, p) in enumerate(items)]}

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + "/assets")
    shutil.copy("assets/style.css", OUT + "/assets/style.css")
    shutil.copy("assets/app.js", OUT + "/assets/app.js")
    open(OUT + "/.nojekyll", "w").close()
    shutil.copy("data/tools.json", OUT + "/tools.json")
    # Unveränderte Dateien (z. B. Google-Search-Console-Verifizierung) 1:1 übernehmen
    for f in sorted(os.listdir("static")): shutil.copy(os.path.join("static", f), os.path.join(OUT, f))
    urls = [""]
    # Startseite
    tiles = "".join(f'<a class="tile" href="kategorie/{c["slug"]}/"><h3>{e(c["name"])}</h3><p>{e(c["intro"])}</p><span class="count">{sum(t["kategorie"]==c["slug"] for t in TOOLS)} Tools</span></a>' for c in D["kategorien"])
    opts = "".join(f'<option value="{c["slug"]}">{e(c["kurz"])}</option>' for c in D["kategorien"])
    regions = sorted({t["hosting_region"] for t in TOOLS})
    ropts = "".join(f'<option value="{e(x)}">{e(x)}</option>' for x in regions)
    body = f"""<section class="hero"><h1>KI-Tools mit EU-Hosting für KMU</h1>
<p class="lead">{len(TOOLS)} KI-Tools, deren Anbieter Hosting in Deutschland oder der EU angeben – mit Quelle und Prüfdatum zu jeder Angabe.</p>
<p class="muted">{e(D['hinweis'])} Stand: {de_date(STAND)}.</p></section>
<section><h2>Kategorien</h2><div class="tiles">{tiles}</div></section>
{guides.home_section(TOOLS)}
<section><h2>Alle Tools</h2>
<div class="filters"><input id="q" type="search" placeholder="Suchen, z. B. Transkription, Frankfurt, AVV …" aria-label="Tools durchsuchen">
<select id="cat" aria-label="Kategorie"><option value="">Alle Kategorien</option>{opts}</select>
<select id="reg" aria-label="Hosting-Region"><option value="">Alle Regionen</option>{ropts}</select>
<span id="cnt" class="muted small"></span></div>
{table(TOOLS, "")}</section>
{NEWSLETTER}
<section class="box"><h2>Ihr Tool fehlt?</h2><p>Anbieter können Tools zur Prüfung vorschlagen. Aufgenommen wird nur, was sich auf den Anbieterseiten belegen lässt.</p><p><a class="btn" href="tool-eintragen/">Tool eintragen</a></p></section>"""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": BASE, "inLanguage": "de-DE"},
          {"@context": "https://schema.org", "@type": "ItemList", "name": "KI-Tools mit EU-Hosting", "numberOfItems": len(TOOLS),
           "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + f"tool/{t['slug']}/", "name": t["name"]} for i, t in enumerate(TOOLS)]}]
    page("", "KI-Tools mit EU-Hosting für KMU – Verzeichnis mit Quellen", f"{len(TOOLS)} KI-Tools mit Hosting in Deutschland/EU laut Anbieter: Chatbots, Transkription, Übersetzung, Kundenservice, KI-APIs. Mit AVV-Hinweis, Preis und Quelle.", body, 0, ld)
    # Kategorien
    for c in D["kategorien"]:
        ts = [t for t in TOOLS if t["kategorie"] == c["slug"]]
        others = " · ".join(f'<a href="../{o["slug"]}/">{e(o["kurz"])}</a>' for o in D["kategorien"] if o["slug"] != c["slug"])
        body = f"""<nav class="bc"><a href="../../">Start</a> › {e(c['kurz'])}</nav><h1>{e(c['name'])}</h1>
<p class="lead">{e(c['intro'])}</p><p class="muted">{len(ts)} Tools · {e(D['hinweis'])} Stand: {de_date(STAND)}.</p>
{table(ts, "../../", False)}<p class="small">Weitere Kategorien: {others}</p>{NEWSLETTER}"""
        p = f"kategorie/{c['slug']}/"; urls.append(p)
        ld = [crumbs([("Start", ""), (c["kurz"], p)]),
              {"@context": "https://schema.org", "@type": "ItemList", "name": c["name"], "numberOfItems": len(ts),
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + f"tool/{t['slug']}/", "name": t["name"]} for i, t in enumerate(ts)]}]
        page(p, f"{c['name']} ({len(ts)} Tools) – {SITE}", f"{c['intro']} {len(ts)} Tools mit Quelle und Prüfdatum.", body, 2, ld)
    # Tools
    for t in TOOLS:
        c = CATS[t["kategorie"]]
        src = "".join(f'<li><a href="{e(u)}" rel="nofollow noopener" target="_blank">{e(u)}</a></li>' for u in t["quellen"])
        sim = [x for x in TOOLS if x["kategorie"] == t["kategorie"] and x["slug"] != t["slug"]][:5]
        simh = " · ".join(f'<a href="../{x["slug"]}/">{e(x["name"])}</a>' for x in sim)
        body = f"""<nav class="bc"><a href="../../">Start</a> › <a href="../../kategorie/{c['slug']}/">{e(c['kurz'])}</a> › {e(t['name'])}</nav>
<article class="tool"><h1>{e(t['name'])} {badge(t['hosting_region'])}</h1><p class="lead">{e(t['beschreibung'])}</p>
<dl class="facts">
<dt>Website</dt><dd><a href="{e(t['url'])}" rel="nofollow noopener" target="_blank">{e(t['url'])}</a></dd>
<dt>Anbieter</dt><dd>{unk(t['anbieter'])}</dd>
<dt>Kategorie</dt><dd><a href="../../kategorie/{c['slug']}/">{e(c['name'])}</a></dd>
<dt>Hosting / Rechenzentrum (Angabe des Anbieters)</dt><dd>{unk(t['hosting_angabe'])}</dd>
<dt>DSGVO / AVV (Angabe des Anbieters)</dt><dd>{unk(t['dsgvo_avv'])}</dd>
<dt>Preis-Hinweis</dt><dd>{unk(t['preis'])}</dd>
<dt>Quellen</dt><dd><ul>{src}</ul></dd>
<dt>Geprüft am</dt><dd><time datetime="{t['geprueft']}">{de_date(t['geprueft'])}</time></dd></dl>
<p class="disc">{e(D['hinweis'])} Ob ein Tool für Ihren Einsatz datenschutzkonform ist, klären Sie bitte mit Ihrem Datenschutzbeauftragten bzw. einer Rechtsberatung.</p>
<p class="small">Angabe veraltet oder falsch? <a href="../../tool-eintragen/">Korrektur melden</a></p></article>
{f'<section><h2>Ähnliche Tools</h2><p>{simh}</p></section>' if sim else ''}"""
        p = f"tool/{t['slug']}/"; urls.append(p)
        ld = [crumbs([("Start", ""), (c["kurz"], f"kategorie/{c['slug']}/"), (t["name"], p)]),
              {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": t["name"], "url": t["url"],
               "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "description": t["beschreibung"],
               "dateModified": t["geprueft"]}]
        page(p, f"{t['name']}: Hosting, AVV & Preise laut Anbieter – {SITE}", f"{t['name']} – {t['beschreibung']} Hosting laut Anbieter: {t['hosting_region']}. Quellen und Prüfdatum {de_date(t['geprueft'])}.", body, 2, ld)
    urls += guides.build_guides(page, TOOLS, CATS, D, e, badge, unk, de_date, BASE, crumbs)
    # Tool eintragen
    catopts = "".join(f'<option>{e(c["name"])}</option>' for c in D["kategorien"])
    body = f"""<h1>Tool eintragen</h1><p class="lead">Sie bieten ein KI-Tool mit Hosting in Deutschland oder der EU an? Schlagen Sie es zur Aufnahme vor.</p>
<div class="todo">Das Eintragsformular ist noch nicht aktiv. Bitte schlagen Sie Ihr Tool vorerst über unser <a href="https://tally.so/r/VpprVl" rel="noopener" target="_blank">Kontaktformular</a> oder per E-Mail an <a href="mailto:mvepoint@gmail.com">mvepoint@gmail.com</a> vor.</div>
<p>Aufnahmekriterien: Die Hosting-Angabe muss auf einer öffentlichen Seite des Anbieters stehen. Wir übernehmen nur Anbieterangaben mit Quelle und Prüfdatum; bezahlte Aufnahme beeinflusst die Angaben nicht und würde als „Sponsor“ gekennzeichnet.</p>
<form class="form" onsubmit="return false" aria-disabled="true">
<label>Name des Tools<input disabled></label><label>Website<input type="url" disabled></label>
<label>Kategorie<select disabled>{catopts}</select></label>
<label>Link zur Seite mit der Hosting-/Rechenzentrumsangabe<input type="url" disabled></label>
<label>Link zu AVV/DPA (falls vorhanden)<input type="url" disabled></label>
<label>Ihre E-Mail<input type="email" disabled></label>
<button disabled>Absenden (noch inaktiv)</button></form>"""
    page("tool-eintragen/", f"Tool eintragen – {SITE}", "KI-Tool mit EU-Hosting zur Aufnahme ins Verzeichnis vorschlagen.", body, 1); urls.append("tool-eintragen/")
    body = f"""<h1>Methodik</h1><ul>
<li>Aufgenommen werden nur Tools, deren Anbieter auf der eigenen Website Hosting bzw. Datenverarbeitung in Deutschland, der EU/dem EWR angibt (oder die selbst gehostet werden können).</li>
<li>Jede Angabe stammt von einer verlinkten Anbieterseite und trägt ein Prüfdatum. Was dort nicht eindeutig steht, ist als <span class="unk">unbekannt</span> markiert.</li>
<li>Wir geben Angaben der Anbieter wieder und nehmen <strong>keine rechtliche Bewertung</strong> vor (z. B. zu Drittlandübermittlung, Unterauftragsverarbeitern oder US-Konzernmüttern).</li>
<li>Alle Quell-Links werden regelmäßig automatisch auf Erreichbarkeit geprüft; Inhalte werden wöchentlich stichprobenartig nachgeprüft.</li>
<li>Sponsoren werden klar gekennzeichnet und haben keinen Einfluss auf die Angaben.</li></ul><p>Datenstand: {de_date(STAND)}</p>"""
    page("methodik/", f"Methodik – {SITE}", "Wie das Verzeichnis Angaben zu EU-Hosting, AVV und Preisen erhebt.", body, 1); urls.append("methodik/")
    page("impressum/", f"Impressum – {SITE}", "Impressum und Anbieterkennzeichnung des KI-EU-Verzeichnisses.", IMPRESSUM, 1, noindex=True)
    page("datenschutz/", f"Datenschutzerklärung – {SITE}", "Datenschutzerklärung des KI-EU-Verzeichnisses: Hosting über GitHub Pages, cookielose Reichweitenmessung mit GoatCounter, keine Cookies.", DATENSCHUTZ.replace("{stand}", de_date(STAND)), 1, noindex=True)
    page("404.html", f"Seite nicht gefunden – {SITE}", "Seite nicht gefunden", '<h1>Seite nicht gefunden</h1><p><a href="/ki-eu-verzeichnis/">Zur Startseite</a></p>', 0, noindex=True)
    # 404 nutzt relative Pfade ab Root-Tiefe 0; für GitHub-Pages-Unterpfad Basis setzen
    import re
    s = re.sub(r'(href|src)="(?!https?:|/|#)', r'\1="/ki-eu-verzeichnis/', open(OUT + "/404.html", encoding="utf-8").read())
    open(OUT + "/404.html", "w", encoding="utf-8").write(s)
    sm = "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{STAND}</lastmod></url>" for u in urls)
    open(OUT + "/sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
    open(OUT + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    print(f"gebaut: {len(urls)} URLs in Sitemap, {len(TOOLS)} Tool-Seiten")

if __name__ == "__main__":
    build()
