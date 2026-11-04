"""DE/NL fysio-pagina's naar het claimniveau van de Franse kiné-pagina; geen gedachtestreepjes."""
F_DE='site/de/merchandising-fuer-physiotherapie-praxen/index.html'
F_NL='site/nl/merchandise-voor-fysiotherapiepraktijken/index.html'
DE=[
 ("<h3>Bringt dir neue Patientinnen und Patienten</h3>","<h3>Deine Marke außerhalb der Praxis</h3>"),
 ("Wenn jemand im eigenen Fitnessstudio oder Verein mit den Socken deiner Praxis trainiert, ist das eine Empfehlung, die von allein läuft – ohne einen einzigen Euro für Anzeigen.",
  "Wenn jemand im Fitnessstudio oder Verein mit den Socken deiner Praxis trainiert, macht das deine Marke bekannt, ohne Kosten für Anzeigen. Diese Zahl gilt für Produkte mit Logo im Allgemeinen, nicht speziell für die Physiotherapie."),
 ("<h3>Kann helfen, Kundinnen zu binden</h3>\n        <p>Schon 5&nbsp;% mehr Kundenbindung","<h3>Ein stimmiges Markenbild</h3>\n        <p>Schon 5&nbsp;% mehr Kundenbindung"),
 ("In der Physiotherapie ist es der Patient, der nach Abschluss der Behandlung weiter in den Trainingsraum kommt, der die Praxis trägt. Ein stimmiges Markenbild, innerhalb und außerhalb der Behandlung, ist mit ein Grund, warum Menschen bleiben.",
  "Ein stimmiges Markenbild, innerhalb und außerhalb der Behandlung, schafft Vertrauen, ersetzt aber nicht die Qualität der Behandlung. Hinweis: allgemeine Zahlen, nicht speziell für die Physiotherapie."),
 ("Eine gepflegte Praxis mit guter Ausstattung und freundlichem Umgang, in der im Trainingsraum aber eine x-beliebige Supermarktsocke liegt, wirkt nicht „fast perfekt“. Sie wirkt nachlässig. So unverhältnismäßig schwer wiegt ein einziges schwaches Detail.",
  "Eine gepflegte Praxis mit guter Ausstattung und freundlichem Umgang kann durch eine x-beliebige Socke im Trainingsraum an Wirkung verlieren: Ein schwaches Detail wiegt oft schwerer, als man denkt."),
 ("verkauft sich von allein.","lässt sich einfach verkaufen."),
 ("mit dem Logo deiner Praxis – zum Verkauf","mit dem Logo deiner Praxis, zum Verkauf"),
 ("denselben Produkten – deshalb gibt es diese Seite.","denselben Produkten. Deshalb gibt es diese Seite."),
 ("glattem Boden oder Reformer – und eine normale Socke rutscht.","glattem Boden oder Reformer, und eine normale Socke rutscht."),
 ("mit deinem Logo verkaufen – damit Patientinnen","mit deinem Logo verkaufen, damit Patientinnen"),
 ("So wie wir es lesen – und allgemein betrachtet – würde","So wie wir es lesen, und allgemein betrachtet, würde"),
 ("Heilmittelwerbegesetz (HWG) – kläre das am besten","Heilmittelwerbegesetz (HWG). Kläre das am besten"),
 ("sondern verkauft – und präsentiert es","sondern verkauft, und präsentiert es"),
 ("in Deutschland, Österreich oder der Schweiz – dort greifen eigene Vorschriften","in Deutschland, Österreich oder der Schweiz; dort greifen eigene Vorschriften"),
]
NL=[
 ("<h3>Het levert je nieuwe patiënten op</h3>","<h3>Je merk buiten de praktijk</h3>"),
 ("<h3>Kan helpen om leden te binden</h3>\n        <p>Wie het klantbehoud met slechts 5% verhoogt","<h3>Een consistent merk</h3>\n        <p>Wie het klantbehoud met slechts 5% verhoogt"),
 ("wekt vertrouwen, zonder de kwaliteit van de zorg te vervangen.</p>","wekt vertrouwen, zonder de kwaliteit van de zorg te vervangen. Let op: algemene cijfers, niet specifiek voor fysiotherapie.</p>"),
 ("bij de balie verkoopt zichzelf.","bij de balie is eenvoudig te verkopen."),
]
for f,pairs in ((F_DE,DE),(F_NL,NL)):
    s=open(f,encoding='utf-8').read()
    for a,b in pairs:
        if b in s: continue
        n=s.count(a)
        if not n: print('NIET:',a[:60]); continue
        s=s.replace(a,b)
    open(f,'w',encoding='utf-8').write(s)
    import re
    print(f, 'resterende –:', len(re.findall(r'[^\d]–[^\d]', re.sub(r'<title>.*?</title>','',s))))
