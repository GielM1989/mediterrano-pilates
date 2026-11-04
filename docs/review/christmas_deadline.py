"""Kerstdeadline bijgewerkt (04-11-2026): '1 november aanvragen' is verstreken; de echte grens is
mockup goedkeuren uiterlijk 15 november (mockup komt binnen 24 uur). Zichtbaar + JSON-LD + FR-dicts. Idempotent."""
import glob
P=[
 # NL
 ("vraag je gratis mockup aan vóór 1 november","keur je gratis mockup goed vóór 15 november"),
 ("Vraag je mockup aan vóór 1 november.","Keur je mockup goed vóór 15 november."),
 ("vraag je mockup dan aan vóór 1 november en keur hem uiterlijk half november goed.","keur je mockup dan uiterlijk 15 november goed."),
 ("dus vraag je mockup aan vóór 1 november.","dus keur je mockup uiterlijk 15 november goed."),
 ("Vraag je mockup daarom aan vóór 1 november, dan heb je de producten ruim op tijd in de studio.","Keur je mockup daarom uiterlijk 15 november goed, dan heb je de producten half december in de studio."),
 ("Wil je speling houden, vraag je gratis mockup dan aan vóór 1 november: je hebt hem binnen 24 uur, en hoe eerder je goedkeurt, hoe meer ruimte je overhoudt.","Je gratis mockup heb je binnen 24 uur, en hoe eerder je goedkeurt, hoe meer ruimte je overhoudt."),
 # EN
 ("request your free mockup before 1 November","approve your free mockup by 15 November"),
 ("Request your mockup before 1 November.","Approve your mockup by 15 November."),
 ("request your mockup before 1 November and approve it by mid-November at the latest","approve your mockup by 15 November at the latest"),
 ("The free mockup arrives within 24 hours, so request it before 1 November: the earlier you approve it, the more breathing room you have.","The free mockup arrives within 24 hours, and the earlier you approve it, the more breathing room you have."),
 # ES
 ("pide tu boceto gratis antes del 1 de noviembre","aprueba tu boceto gratis antes del 15 de noviembre"),
 ("Pide tu boceto antes del 1 de noviembre.","Aprueba tu boceto antes del 15 de noviembre."),
 ("Sí, si pides tu boceto antes del 1 de noviembre y lo apruebas como muy tarde el 15 de noviembre.","Sí, si apruebas tu boceto como muy tarde el 15 de noviembre."),
 ("El boceto llega en 24 horas; si lo pides antes del 1 de noviembre, tienes dos semanas para elegir y aprobar con calma.","El boceto llega en 24 horas, así que tienes tiempo para elegir y aprobar con calma."),
 # FR
 ("demandez votre maquette gratuite avant le 1er novembre","validez votre maquette gratuite avant le 15 novembre"),
 ("Demandez votre maquette avant le 1er novembre.","Validez votre maquette avant le 15 novembre."),
 ("Oui, si vous demandez votre maquette avant le 1er novembre et que vous la validez au plus tard le 15 novembre.","Oui, si vous validez votre maquette au plus tard le 15 novembre."),
 ("La maquette arrive en 24 heures ; si vous la demandez avant le 1er novembre, vous avez deux semaines pour choisir et valider sans précipitation.","La maquette arrive en 24 heures, ce qui vous laisse le temps de choisir et de valider sans précipitation."),
 ("La maquette arrive en 24 heures&nbsp;; si vous la demandez avant le 1er novembre, vous avez deux semaines pour choisir et valider sans précipitation.","La maquette arrive en 24 heures, ce qui vous laisse le temps de choisir et de valider sans précipitation."),
 ("La maquette arrive en 24 heures ; si vous la demandez avant le 1er novembre, vous avez deux semaines pour choisir et valider sans précipitation.","La maquette arrive en 24 heures, ce qui vous laisse le temps de choisir et de valider sans précipitation."),
]
n=0
for f in glob.glob('site/**/*.html',recursive=True)+glob.glob('docs/review/fr/*.json')+glob.glob('docs/review/fr/*.py'):
    s=open(f,encoding='utf-8').read();o=s
    for a,b in P: s=s.replace(a,b)
    if s!=o: open(f,'w',encoding='utf-8').write(s); n+=1
print('bestanden:',n)
