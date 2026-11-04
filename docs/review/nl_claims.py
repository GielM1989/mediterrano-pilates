"""NL (en DE-koppen) naar het Franse claimniveau; FR-dubbeling 'sans frais d'annonce' herstellen."""
import glob,re
NL=[
 ("is reclame die vanzelf rondloopt, zonder dat je een euro aan advertenties uitgeeft","zorgt voor zichtbaarheid, zonder advertentiekosten"),
 ("is reclame die vanzelf rondgaat, zonder dat je er een cent aan uitgeeft","zorgt voor zichtbaarheid, zonder advertentiekosten"),
 ("is reclame die vanzelf rondgaat, zonder dat je een euro aan advertenties uitgeeft","zorgt voor zichtbaarheid, zonder advertentiekosten"),
 ("reclame die vanzelf rondgaat, zonder dat het je een cent kost","zichtbaarheid zonder advertentiekosten"),
 ("is een wandelende aanbeveling, zonder dat je een euro aan advertenties uitgeeft","maakt je studio bekend, zonder advertentiekosten"),
 ("is een aanbeveling die vanzelf rondloopt, zonder dat je een cent aan advertenties uitgeeft.","maakt je merk bekend zonder advertentiekosten. Dit cijfer gaat over producten met logo in het algemeen, niet specifiek over fysiotherapie."),
 ("In de fysiotherapie houdt juist de patiënt die na de behandeling naar de oefenruimte blijft komen, de praktijk draaiende. Een consistent merk, binnen en buiten de behandelkamer, is een van de redenen waarom mensen blijven.",
  "Een consistent merk, binnen en buiten de behandelkamer, wekt vertrouwen, zonder de kwaliteit van de zorg te vervangen."),
 ("Een goed geleide praktijk, met goede apparatuur en goede zorg, en dan een anonieme supermarktsok in de oefenruimte: dat komt niet over als “bijna perfect”, maar als slordig. Zo onevenredig zwaar weegt één zwak detail.",
  "Een verzorgde praktijk, met goede apparatuur en goede zorg, kan tekortgedaan worden door een anonieme sok in de oefenruimte: één zwak detail weegt vaak zwaarder dan je denkt."),
 ("maar als slordig. Zo onevenredig zwaar weegt één zwak detail.","maar loopt het risico slordig over te komen. Eén zwak detail kan onevenredig zwaar wegen."),
 ("Die wordt gezien als slordig. Zo onevenredig zwaar weegt één zwak detail.","Die loopt het risico als slordig gezien te worden. Eén zwak detail kan onevenredig zwaar wegen."),
 ("Het komt slordig over. Zo onevenredig zwaar weegt één zwak detail.","Het loopt het risico slordig over te komen. Eén zwak detail kan onevenredig zwaar wegen."),
 ("Die komt over als slordig. Daarom beginnen we","Die loopt het risico slordig over te komen. Daarom beginnen we"),
 ("<h3>Brengt je nieuwe leden</h3>","<h3>Kan je nieuwe leden opleveren</h3>"),
 ("<h3>Het levert je nieuwe leden op</h3>","<h3>Kan je nieuwe leden opleveren</h3>"),
 ("<h3>Zorgt dat ze terugkomen</h3>","<h3>Kan helpen om leden te binden</h3>"),
 ("<h3>Zorgt dat ze blijven</h3>","<h3>Kan helpen om leden te binden</h3>"),
 ("<h3>Het zorgt dat ze terugkomen</h3>","<h3>Kan helpen om leden te binden</h3>"),
 ("<h3>Laat ze terugkomen</h3>","<h3>Kan helpen om leden te binden</h3>"),
 ("We werken met studio's in heel Europa.","We leveren aan studio's in heel Europa."),
]
DE=[
 ("<h3>Bringt dir neue Kundinnen</h3>","<h3>Kann dir neue Kundinnen bringen</h3>"),
 ("<h3>Sorgt dafür, dass sie bleiben</h3>","<h3>Kann helfen, Kundinnen zu binden</h3>"),
 ("<h3>Sorgt dafür, dass sie wiederkommen</h3>","<h3>Kann helfen, Kundinnen zu binden</h3>"),
]
FR=[("une visibilité sans frais d'annonce, sans frais d'annonce.","une visibilité sans frais d'annonce."),
    ("est une visibilité sans frais d'annonce, sans frais d'annonce.","est une visibilité sans frais d'annonce.")]
def run(pattern,pairs):
    for f in glob.glob(pattern,recursive=True):
        s=open(f,encoding='utf-8').read(); o=s
        for a,b in pairs: s=s.replace(a,b)
        if s!=o: open(f,'w',encoding='utf-8').write(s); print('bijgewerkt',f)
run('site/nl/**/*.html',NL); run('site/de/**/*.html',DE); run('site/fr/**/*.html',FR); run('docs/review/fr/dict_*.json',FR)
