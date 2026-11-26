# -*- coding: utf-8 -*-
"""Nieuwe kwaliteitstekst (klantbesluit 26-11-2026) in alle 6 talen.
Marketingtekst: foto's van elke productiestap, grote fout = uitzondering, dan gratis opnieuw.
Verkoopvoorwaarden: de meldprocedure (14 dagen, met foto's) blijft; er komt een zin over de foto's bij."""
import os
SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'site'))

R = {
 'index.html': [("Si el color no coincide con el diseño aprobado o hay un defecto de fabricación, avísanos en los 14 días siguientes a la entrega y lo volvemos a fabricar sin coste.",
   "Recibes fotos claras de cada fase de la producción, así que ves con tus propios ojos cómo se fabrica tu pedido antes de que salga hacia tu estudio. En nuestro caso, un fallo grave es una excepción. Si aun así ocurre, lo volvemos a fabricar gratis.")],
 'en/index.html': [("If the colour doesn't match your approved design, or there's a manufacturing fault, tell us within 14 days of delivery and we'll remake it free of charge.",
   "You get clear photos of every stage of production, so you can see for yourself how your order is made before it's dispatched. A major fault is the exception with us. If one does happen, we'll remake it free of charge.")],
 'de/index.html': [("Weicht die Farbe vom freigegebenen Design ab oder gibt es einen Produktionsfehler? Melde es innerhalb von 14 Tagen nach Lieferung, und wir fertigen kostenlos neu.",
   "Du bekommst von jedem Produktionsschritt klare Fotos und siehst so selbst, wie deine Bestellung gefertigt wird, noch bevor sie verschickt wird. Ein grober Fehler ist bei uns die Ausnahme. Passiert es trotzdem, fertigen wir kostenlos neu.")],
 'nl/index.html': [("Wijkt de kleur af van je goedgekeurde ontwerp, of zit er een productiefout in? Meld het binnen 14 dagen na levering en we maken het kosteloos opnieuw.",
   "Je krijgt van elke productiestap duidelijke foto's, dus je ziet zelf hoe je bestelling gemaakt wordt, nog voordat die verstuurd wordt. Een grote fout is bij ons een uitzondering. Gebeurt het toch, dan maken we het gratis opnieuw.")],
 'fr/index.html': [("Si la couleur ne correspond pas au design validé ou en cas de défaut de fabrication, prévenez-nous dans les 14 jours suivant la livraison et nous refabriquons sans frais.",
   "Vous recevez des photos claires de chaque étape de fabrication&nbsp;: vous voyez ainsi par vous-même comment votre commande est fabriquée, avant même son expédition. Chez nous, un défaut important reste une exception. Si cela arrive malgré tout, nous refabriquons gratuitement.")],
 'it/index.html': [("Se il colore non corrisponde al design approvato o in caso di difetto di fabbricazione, avvisaci entro 14 giorni dalla consegna e rifacciamo i prodotti senza costi.",
   "Ricevi foto chiare di ogni fase della produzione, così vedi con i tuoi occhi come viene realizzato il tuo ordine, prima ancora che parta. Da noi, un errore grave è un'eccezione. Se succede comunque, lo rifacciamo gratis.")],
 'merchandising-estudios-yoga/index.html': [("Si el color no coincide con el diseño aprobado o hay un defecto de fabricación, nos avisas en 14 días y lo rehacemos gratis.",
   "Recibes fotos claras de cada fase de la producción. Un fallo grave es una excepción; si aun así ocurre, lo volvemos a fabricar gratis.")],
 'en/custom-merchandise-for-yoga-studios/index.html': [("If the colour doesn't match the approved design or there's a manufacturing fault, tell us within 14 days and we'll remake it free of charge.",
   "You get clear photos of every stage of production. A major fault is the exception; if one does happen, we'll remake it free of charge.")],
 'de/merchandise-fuer-yogastudios/index.html': [("Stimmt die Farbe nicht mit dem freigegebenen Design überein oder gibt es einen Produktionsfehler, meldest du es innerhalb von 14 Tagen, und wir fertigen kostenlos neu.",
   "Du bekommst von jedem Produktionsschritt klare Fotos. Ein grober Fehler ist die Ausnahme; passiert er trotzdem, fertigen wir kostenlos neu.")],
 'nl/merchandise-voor-yogastudios/index.html': [("Klopt de kleur niet met het goedgekeurde ontwerp of is er een productiefout, meld het binnen 14 dagen en we maken het gratis opnieuw.",
   "Je krijgt van elke productiestap duidelijke foto's. Een grote fout is een uitzondering; gebeurt het toch, dan maken we het gratis opnieuw.")],
 'fr/produits-personnalises-studios-yoga/index.html': [("Si la couleur ne correspond pas au design validé ou en cas de défaut de fabrication, signalez-le-nous sous 14 jours, photos à l'appui&nbsp;; nous proposons un remplacement, une nouvelle livraison ou une compensation.",
   "Vous recevez des photos claires de chaque étape de fabrication. Un défaut important reste une exception&nbsp;; si cela arrive malgré tout, nous refabriquons gratuitement.")],
 'it/prodotti-personalizzati-studi-yoga/index.html': [("Se il colore non corrisponde al design approvato o in caso di difetto di fabbricazione, segnalacelo entro 14 giorni dalla consegna, con foto: rifacciamo l'ordine senza costi.",
   "Ricevi foto chiare di ogni fase della produzione. Un errore grave è un'eccezione; se succede comunque, rifacciamo l'ordine gratis.")],
 'fr/comment-ca-marche/index.html': [("Si la couleur livrée diffère du design validé, ou si un défaut de fabrication est signalé dans les 14 jours suivant la réception, Mediterrano Pilates refabrique la commande sans frais. La maquette validée sert de référence.",
   "Vous recevez des photos claires de chaque étape de fabrication : vous voyez ainsi par vous-même comment votre commande est fabriquée, avant même son expédition. Chez nous, un défaut important reste une exception. Si cela arrive malgré tout, Mediterrano Pilates refabrique la commande gratuitement. La maquette validée sert de référence.")],
 'it/come-funziona/index.html': [("Se il colore consegnato è diverso dal design approvato, o se segnali un difetto di fabbricazione entro 14 giorni dalla consegna, Mediterrano Pilates rifà i prodotti interessati senza costi. Il mockup approvato fa da riferimento.",
   "Ricevi foto chiare di ogni fase della produzione, così vedi con i tuoi occhi come viene realizzato il tuo ordine, prima ancora che parta. Da noi, un errore grave è un'eccezione. Se succede comunque, Mediterrano Pilates rifà i prodotti interessati gratis. Il mockup approvato fa da riferimento.")],
 'nl/zo-werkt-het/index.html': [("Wijkt de geleverde kleur af van het goedgekeurde ontwerp of is er een productiefout, en meld je dat binnen 14 dagen na ontvangst, dan maakt Mediterrano Pilates de bestelling kosteloos opnieuw. De goedgekeurde mockup is daarbij het uitgangspunt.",
   "Je krijgt van elke productiestap duidelijke foto's, zodat je zelf ziet hoe je bestelling gemaakt wordt, nog voordat die verstuurd wordt. Een grote fout is bij ons een uitzondering. Gebeurt het toch, dan maakt Mediterrano Pilates de bestelling gratis opnieuw. De goedgekeurde mockup is daarbij het uitgangspunt.")],
}

# Verkoopvoorwaarden: zin over de foto's vóór de bestaande meldprocedure (die blijft staan)
LEGAL = {
 'legal.html': ('¿Recibes productos con un defecto de fabricación', 'Durante la producción recibes fotos claras de cada fase, así que ves con tus propios ojos cómo se fabrica tu pedido antes de que se envíe. '),
 'en/legal.html': ('If you receive products with a manufacturing fault', "During production you receive clear photos of every stage, so you can see for yourself how your order is made before it is dispatched. "),
 'de/legal.html': ('Hast du Produkte mit einem Produktionsfehler erhalten', 'Während der Produktion bekommst du von jedem Produktionsschritt klare Fotos und siehst so selbst, wie deine Bestellung gefertigt wird, bevor sie verschickt wird. '),
 'nl/legal.html': ('Heb je producten met een productiefout ontvangen', "Tijdens de productie ontvang je van elke productiestap duidelijke foto&#39;s, zodat je zelf ziet hoe je bestelling gemaakt wordt voordat die verstuurd wordt. "),
 'fr/legal.html': ('Vous recevez un produit présentant un défaut de fabrication', 'Pendant la fabrication, vous recevez des photos claires de chaque étape&nbsp;: vous voyez ainsi par vous-même comment votre commande est fabriquée avant son expédition. '),
 'it/legal.html': ('Ricevi un prodotto con un difetto di fabbricazione', 'Durante la produzione ricevi foto chiare di ogni fase, così vedi con i tuoi occhi come viene realizzato il tuo ordine prima che venga spedito. '),
}


def run():
    for f, reps in R.items():
        p = os.path.join(SITE, f); t = open(p, encoding='utf-8').read(); n = 0
        for a, b in reps:
            if b in t:
                continue
            assert a in t, (f, a[:60])
            n += t.count(a); t = t.replace(a, b)
        open(p, 'w', encoding='utf-8').write(t); print(f, n)
    for f, (anchor, sent) in LEGAL.items():
        p = os.path.join(SITE, f); t = open(p, encoding='utf-8').read()
        if sent.strip()[:40] in t:
            print(f, 'al gedaan'); continue
        assert t.count(anchor) == 1, (f, t.count(anchor))
        t = t.replace(anchor, sent + anchor)
        open(p, 'w', encoding='utf-8').write(t); print(f, 1)


if __name__ == '__main__':
    run()
