"""Taalreview ronde 2 (DE), zichtbaar + JSON-LD + bronscripts. Idempotent."""
import glob
P = [
 ("Wir sitzen in Spanien und arbeiten mit Studios in ganz Europa.", "Wir sitzen in Spanien und liefern in ganz Europa."),
 ('Wir beliefern Studios in <span class="fx">ganz Europa.</span>', 'Wir liefern in <span class="fx">ganz Europa.</span>'),
 ('Wir beliefern Zentren in <span class="fx">ganz Europa.</span>', 'Wir liefern in <span class="fx">ganz Europa.</span>'),
 ("Mediterrano Pilates beliefert von Spanien aus Pilates- und Yogastudios in ganz Europa, und der Versand an jedes Studio in Europa ist kostenlos. Egal wo du bist, der Versand geht auf uns, ohne versteckte Kosten.",
  "Mediterrano Pilates versendet von Spanien aus an Pilates- und Yogastudios in ganz Europa, kostenlos und ohne versteckte Kosten."),
 ("Mediterrano Pilates beliefert von Spanien aus Pilates-, Yoga- und Barre-Studios sowie Physiotherapie-Praxen in ganz Europa, und der Versand ist kostenlos. Egal wo in Europa du bist, den Versand übernehmen wir, ohne versteckte Kosten.",
  "Mediterrano Pilates versendet von Spanien aus an Pilates-, Yoga- und Barre-Studios sowie Physiotherapie-Praxen in ganz Europa, kostenlos und ohne versteckte Kosten."),
 ("Mediterrano Pilates beliefert von Spanien aus", "Mediterrano Pilates versendet von Spanien aus an"),
 ("Das einfachste Produkt für den Start.", "Das Produkt für den Einstieg."),
 ("Die direkte Marge ist die sichtbarste, aber nicht die wichtigste.", "Die direkte Marge sieht man sofort. Sie ist aber nur ein Teil des Gewinns."),
 ("Mediterrano Pilates arbeitet mit einer Mindestbestellmenge von 50 Paar für Stoppersocken und mit einem individuellen Angebot für Trinkflaschen, Taschen und Pilates-Ringe.",
  "Bei Mediterrano Pilates liegt die Mindestbestellmenge bei 50 Paar Stoppersocken. Für Tumbler, Tote Bags und Pilates-Ringe gibt es keine feste Mindestmenge, die Menge legen wir im Angebot fest."),
 ("Bleibt der Preis und die Frage, ob etwas extra berechnet wird.", "Bleiben der Preis und die Frage, ob etwas extra berechnet wird."),
 ("für eine Schwester oder für sie selbst.", "für eine Schwester oder für sich selbst."),
 ("Dennoch kann deine Berufskammer das im Einzelfall anders einschätzen.", "Dennoch kann dein Berufsverband das im Einzelfall anders einschätzen."),
 ("deiner Berufskammer bzw. deinem Berufsverband", "deinem Berufsverband"),
 ("bei der Berufskammer registrierte", "bei den Berufskammern registrierte"),
 ("und der Versand ist kostenlos, ohne Ausnahmen. Bei Lieferungen", "und der Versand ist kostenlos. Bei Lieferungen"),
 ("damit Patientinnen und Patienten die verordneten Übungen zu Hause weiterführen", "damit Patientinnen und Patienten die Übungen aus der Therapie zu Hause weiterführen können"),
 ("So, wie wir es lesen und allgemein betrachtet, würde der Verkauf einer Stoppersocke, eines Tumblers oder einer Tote Bag mit dem Praxislogo nicht darunterfallen:",
  "Nach unserem Verständnis fällt der Verkauf einer Stoppersocke, eines Tumblers oder einer Tote Bag mit dem Praxislogo im Allgemeinen nicht darunter:"),
 ("Es wäre der Verkauf eines Alltagsprodukts", "Es ist der Verkauf eines Alltagsprodukts"),
 ("So wie wir es lesen: ganz allgemein ja.", "Nach unserem Verständnis: im Allgemeinen ja."),
 ("Der Patient braucht es für die Einheit, bezahlt dafür und nimmt es mit. Das ist weder Werbung für eine Behandlung noch ein Geschenk fürs Erscheinen zur Konsultation.",
  "Die Patientin oder der Patient braucht es für das Training, bezahlt dafür und nimmt es mit. Das ist weder Werbung für eine Behandlung noch ein Geschenk dafür, dass jemand zum Termin kommt."),
 ("eingeschränkt wird dabei vor allem, einem Produkt ohne Grundlage gesundheitliche Wirkungen zuzuschreiben oder Patienten mit Geschenken oder Werbeaktionen zu gewinnen",
  "eingeschränkt ist dabei vor allem zweierlei: einem Produkt ohne Grundlage gesundheitliche Wirkungen zuzuschreiben und Patientinnen und Patienten mit Geschenken oder Werbeaktionen anzuwerben"),
 ("mit dem Logo des jeweiligen Zentrums, damit es sie an seine Kundschaft verkauft", "mit dem Logo des jeweiligen Studios oder der jeweiligen Praxis, zum Weiterverkauf an die eigene Kundschaft"),
 ("Immer mehr Physiotherapie-Praxen arbeiten mit denselben Trainingsräumen, denselben Übungen und denselben Produkten.", "Immer mehr Physiotherapie-Praxen arbeiten mit ähnlichen Trainingsräumen, Übungen und Produkten wie Pilatesstudios."),
 ("wird ohnehin in Stoppersocken gearbeitet; deine Patientinnen und Patienten kaufen sie sowieso, die Frage ist nur, ob sie dabei eine x-beliebige Marke tragen oder deine.",
  "tragen Patientinnen und Patienten ohnehin Stoppersocken. Die Frage ist nur, ob sie eine x-beliebige Marke tragen oder deine."),
 ("zum Verkauf an deine Patientinnen und Patienten an der Rezeption.", "zum Verkauf an der Rezeption."),
 ("Ein Beispiel aus Spanien, wo Mediterrano Pilates seinen Sitz hat: Dort gibt es", "Ein Beispiel aus Spanien, dem Sitz von Mediterrano Pilates: Dort gibt es"),
 ("auf Matte, glattem Boden oder Reformer", "auf der Matte, auf glattem Boden oder am Reformer"),
 ("Sie verschenkt nichts, sondern verkauft, und präsentiert es als Kleidung, nicht als Behandlung.", "Die Praxis verschenkt nichts, sie verkauft, und sie präsentiert die Produkte als Kleidung, nicht als Behandlung."),
 ("Die Socke wird als Ausrüstung für das Training verkauft, ohne Versprechen zur Gesundheit.", "Die Socke wird als Trainingsausrüstung verkauft, ohne gesundheitsbezogene Versprechen."),
 ("Dort richtet sich Werbung für Gesundheitsprodukte nach den jeweils eigenen Vorschriften", "Dort richtet sich Werbung im Gesundheitsbereich nach eigenen Vorschriften"),
 ("Auf den Socken wird das Logo eingewebt oder aufgestickt", "Das Logo wird in die Socken eingewebt oder aufgestickt"),
 ("innerhalb und außerhalb der Behandlung", "in der Praxis und darüber hinaus"),
 ("Ein Paket, das sichtbar am Empfang liegt, mit einem klaren Preis, lässt sich in den Wochen vor Weihnachten einfach verkaufen,", "Ein Set, das mit klarem Preis sichtbar am Empfang liegt, lässt sich in den Wochen vor Weihnachten gut verkaufen,"),
 ("Wenn du es empfiehlst, vertrauen sie darauf.", "Deiner Empfehlung vertrauen sie."),
 ("Es ist eine echte Stoppersocke, gemacht für die Stunde:", "Es ist eine echte Stoppersocke, gemacht fürs Training:"),
 ("damit in der Wäsche nichts reißt oder abblättert", "damit in der Wäsche nichts rissig wird oder abblättert"),
 ("gegen eine kleine Gebühr, die bei deiner ersten Bestellung vollständig verrechnet wird, sodass die Muster kostenlos sind, wenn du bestellst.",
  "gegen eine kleine Gebühr, die wir dir bei deiner ersten Bestellung vollständig anrechnen. Wenn du bestellst, sind die Muster also kostenlos."),
 ("Etwaige Zölle oder Einfuhrabgaben im Bestimmungsland trägt der Kunde. Bei Lieferungen außerhalb der EU", "Bei Lieferungen außerhalb der EU"),
 ("nach Freigabe des Angebots", "nach Annahme des Angebots"),
 ("Das Material ist nach REACH geprüft.", "Das Material ist REACH-konform."),
 ("Material nach REACH geprüft", "Material REACH-konform"),
 ("Pilates-Ringe in Terrakotta mit cremefarbenen Griffen mit dem Logo deines Studios", "Pilates-Ringe in Terrakotta mit cremefarbenen Griffen, personalisiert mit dem Logo deines Studios,"),
 ("Wir personalisieren Tumbler mit 1,2 Liter Inhalt mit dem Logo", "Wir personalisieren 1,2-Liter-Tumbler mit dem Logo"),
 ("und der Versand in ganz Europa ist kostenlos, auch nach Deutschland", "und der Versand ist kostenlos, auch nach Deutschland"),
 ("Bei Lieferungen außerhalb der EU, etwa in die Schweiz", "Bei Lieferungen in Länder außerhalb der EU, etwa in die Schweiz"),
 ("Mediterrano Pilates ist der Merchandise-Partner für Pilates- und Yogastudios.", "Mediterrano Pilates ist Merchandise-Partner für Pilates- und Yogastudios."),
 ("Ein Tumbler mit deinem Logo im Wartebereich und an der Rezeption lässt sich einfach verkaufen.", "Ein Tumbler mit deinem Logo lässt sich gut im Wartebereich und an der Rezeption anbieten."),
 (" Dieselbe Verschiebung von der Behandlungsliege in den Trainingsraum ist auch in Praxen in Deutschland, Österreich und der Schweiz zu beobachten.", ""),
 ("ohne Kosten für Werbung", "ohne Kosten für Anzeigen"),
 ("Egal wo in Europa du bist,", "Egal, wo in Europa du bist,"),
 ("Egal wo du bist,", "Egal, wo du bist,"),
]
files = glob.glob("site/de/**/*.html", recursive=True) + ["docs/review/import_duties.py", "docs/review/dennl/content.py", "site/llms.txt"]
hits = {a: 0 for a, _ in P}
for f in files:
    s = open(f, encoding="utf-8").read(); o = s
    for a, b in P:
        if a in s and (b == "" or a not in b):
            hits[a] += s.count(a); s = s.replace(a, b)
    if s != o: open(f, "w", encoding="utf-8").write(s)
for a, n in hits.items():
    if not n: print("0x:", a[:80])
