#!/usr/bin/env python3
"""Nederlandse pagina's op Franse pariteit: ontbrekende FAQ-vragen (zichtbaar + FAQPage-JSON-LD)
en enkele herschreven antwoorden. Idempotent (bestaande vragen worden overgeslagen).
Gebruik: python3 docs/review/nl_parity.py  (vanuit de repo-root)"""
import sys
sys.path.insert(0, "docs/review/dennl")
from aeo_upgrade import add_faqs, set_answer

STD = ("Bij leveringen buiten de EU, zoals naar Zwitserland, het Verenigd Koninkrijk of Noorwegen, "
       "zijn invoer-btw, invoerrechten en inklaringskosten altijd voor rekening van de ontvanger.")
BTW_Q = "Hoe werkt de btw voor een studio in Nederland of België?"
BTW_A = ("Mediterrano Pilates factureert vanuit Spanje. Heeft je bedrijf een geldig btw-identificatienummer in de EU, "
         "dan is de factuur een vrijgestelde intracommunautaire levering en geef je de btw zelf aan in je eigen land "
         "(btw verlegd). Zonder geldig btw-nummer rekenen we Spaanse btw. " + STD)
MIN_A = ("Voor antislipsokken 50 paar. Voor tumblers, tote bags en pilatesringen is er geen vast minimum: "
         "we maken een offerte op maat voor het aantal dat je in gedachten hebt.")
SAMPLES = ("Ja. We sturen je een set proefexemplaren (sok, tumbler en tote bag) voor een klein bedrag, dat volledig wordt "
           "verrekend met je eerste bestelling. Bestel je, dan zijn de proefexemplaren dus gratis.")
SHIP_BLOG = ("Ja, gratis, net als in de rest van Europa. We verzenden vanuit Spanje, en op aanvraag ook buiten Europa. " + STD)
SHIP_Q = "Leveren jullie ook in Nederland en België?"

PAGES = {
 "pilatesring-met-logo": {"faqs": [
  ("Waarom een pilatesring en niet een ander product met mijn logo?",
   "Omdat het een trainingsaccessoire is dat je leden echt gebruiken, in de studio en thuis. Elke training met de ring "
   "brengt je merk in herinnering, en elke ring die je aan de balie verkoopt, levert je studio marge op.")]},
 "tumblers-met-logo": {"faqs": [
  ("Hoe komt het logo op de tumbler?",
   "Op de manier die het best bij het product past, in jouw stijl, subtiel of groot, en in de kleur van je merk, "
   "afgestemd op de Pantone-code. Je ziet het resultaat op de gratis mockup voordat je iets beslist.")]},
 "tote-bags-met-logo": {"faqs": [
  ("Waarom een tote bag met je logo aanbieden?",
   "Omdat hij gemaakt is om te gebruiken: stevig katoen, een logo in jouw stijl en de kleur van je merk, afgestemd op "
   "de Pantone-code. Je leden nemen hem mee naar de les, naar hun werk of naar de supermarkt. Daarom kopen ze hem, "
   "en zo gaat je merk overal met ze mee.")]},
 "prijzen-en-marges": {
  "answers": [("Zijn de prijzen inclusief btw?",
   "De inkoopprijzen zijn groothandelsprijzen exclusief btw. De verkoopprijzen zijn wat je leden betalen, dus "
   "inclusief btw. De marges op deze pagina zijn berekend na aftrek van 21% btw; afhankelijk van je land en situatie "
   "kan het tarief verschillen.")],
  "faqs": [
  ("Wat kost een eerste bestelling van 50 paar?",
   "Een voorbeeld: 50 paar antislipsokken met je logo kosten € 347,50 exclusief btw, en de verzending is gratis. "
   "Verkoop je ze voor € 19,95 inclusief btw per paar, dan houd je na aftrek van 21% btw ongeveer € 9,54 marge per "
   "paar over. De exacte offerte voor jouw aantal krijg je samen met je gratis mockup."),
  (BTW_Q, BTW_A)]},
 "zo-werkt-het": {"faqs": [
  ("Wat gebeurt er als de kleur of de kwaliteit niet klopt?",
   "Wijkt de geleverde kleur af van het goedgekeurde ontwerp, of meld je binnen 14 dagen na ontvangst een "
   "productiefout, dan maakt Mediterrano Pilates de bestelling kosteloos opnieuw. De goedgekeurde mockup is daarbij "
   "het uitgangspunt."),
  ("Met wie heb ik contact tijdens de bestelling?",
   "Rechtstreeks met de oprichter, Giel Mallens, per e-mail of WhatsApp, van de mockup tot de levering. Je krijgt de "
   "mockup binnen 24 uur, daarna de offerte, en we volgen de zending tot die in je studio is.")]},
 "veelgestelde-vragen": {
  "answers": [("Is dit niet gewoon een leuk extraatje?",
   "Het is meer dan dat: er zitten drie soorten marge achter. De marge bij doorverkoop is het meest zichtbaar, maar "
   "niet het belangrijkst. 85% van de mensen onthoudt het merk van een product dat ze hebben gedragen (ASI Global "
   "Advertising Impressions Study, 2026), dus elk lid dat jouw logo draagt, maakt je studio zichtbaar zonder "
   "advertentiekosten. Daarnaast kan 5% meer klantbehoud de winst met maximaal 95% laten stijgen (Bain &amp; Company / "
   "Harvard Business Review), en een consistent merk kan helpen om leden langer te binden.")],
  "faqs": [
  ("Werken jullie ook voor barrestudio's?",
   "Ja. Bij barre train je op antislipsokken, dus het product is hetzelfde als bij pilates: logo geweven of "
   "geborduurd, vanaf 50 paar, gratis mockup binnen 24 uur en gratis verzending binnen heel Europa. We hebben een "
   "aparte pagina voor <a href=\"/nl/merchandise-voor-barrestudios/\">barrestudio's</a>."),
  ("Is er een leverancier van antislipsokken met logo bij mij in de buurt?",
   "Een leverancier om de hoek heb je niet nodig: het hele proces verloopt online en de verzending is gratis, in "
   "Nederland en België net als in de rest van Europa. Je krijgt de mockup binnen 24 uur per e-mail, keurt het "
   "ontwerp en de offerte goed, en na ongeveer vier weken is de bestelling in je studio. Mediterrano Pilates is een "
   "merk van Ecomtierra Group SL, gevestigd in Spanje."),
  ("Maken jullie ook antislipsokken met logo voor yogastudio's?",
   "Ja. Het product is hetzelfde als voor pilates: logo geweven of geborduurd, de kleur zo dicht mogelijk bij je "
   "Pantone-code, vanaf 50 paar en een gratis mockup binnen 24 uur. We hebben een aparte pagina voor "
   "<a href=\"/nl/merchandise-voor-yogastudios/\">yogastudio's</a>."),
  ("Maken jullie antislipsokken met logo voor bedrijven?",
   "Ja, als het gaat om een pilates-, yoga- of barrestudio of om een fysiotherapiepraktijk: voor die bedrijven maken "
   "we onze producten. We personaliseren de sokken met je logo vanaf 50 paar, voor ongeveer € 6,95 per paar "
   "exclusief btw."),
  ("Komen ze op tijd binnen om ze met kerst aan mijn leden te geven?",
   "Ja, als je je mockup uiterlijk 15 november goedkeurt. Productie en levering duren ongeveer vier weken na "
   "goedkeuring, dus de bestelling kan half december in je studio zijn. De mockup heb je binnen 24 uur. Op de blog vind je "
   "de opties, de termijnen en het budget voor <a href=\"/nl/blog/kerstcadeaus-voor-pilatesleden/\">kerstcadeaus</a>."),
  (BTW_Q, BTW_A)]},
 "gratis-mockup": {"faqs": [
  ("Hoe ziet de mockup eruit?",
   "Het is een digitale afbeelding van je logo op het product dat je kiest, een antislipsok, tumbler, tote bag of "
   "pilatesring, in de kleur van je merk. Kleur, formaat en positie kun je laten aanpassen voordat je goedkeurt. Na "
   "goedkeuring geldt de mockup als drukproef voor de productie, en je krijgt de offerte erbij."),
  ("Hoeveel tijd zit er tussen de mockup en de levering?",
   "De mockup heb je binnen 24 uur. Na je akkoord op de offerte en je betaling duren productie en levering "
   "ongeveer 4 weken, tot de bestelling in je studio is. De verzending is gratis binnen heel Europa."),
  ("Wie beantwoordt mijn aanvraag?",
   "De oprichter van Mediterrano Pilates, Giel Mallens. Hij behandelt elke aanvraag persoonlijk en blijft je vaste "
   "aanspreekpunt, per e-mail of WhatsApp, van de mockup tot de levering.")]},
 "over-mediterrano-pilates": {"faqs": [
  ("Welke producten personaliseert Mediterrano Pilates?",
   "Vier producten met het logo van je studio: antislipsokken (logo geweven of geborduurd, nooit bedrukt), tumblers "
   "van 1,2 liter, tote bags en pilatesringen. Elk project begint met een gratis mockup binnen 24 uur, zonder "
   "verplichtingen."),
  ("Wat is de minimale bestelling?", MIN_A),
  ("Levert Mediterrano Pilates ook buiten Europa?",
   "Ja, op aanvraag. Binnen heel Europa is de verzending gratis; voor de rest van de wereld staan de kosten en de "
   "levertijd in de offerte die je bij je mockup krijgt. " + STD)]},
 "merchandise-voor-fysiotherapiepraktijken": {"faqs": [
  ("Hoe goed is de kwaliteit van jullie antislipsokken?",
   "Het is een echte antislipsok, gemaakt voor de training: antislipnopjes van PVC of siliconen over de hele zool, "
   "een halfhoge schacht, materiaal getest volgens REACH en je logo in de sok geweven of geborduurd, nooit "
   "bedrukt, zodat het logo de was goed doorstaat. Je patiënten dragen hem bij elke sessie, en daarom kopen ze hem "
   "graag.")]},
 "blog/meer-omzet-pilatesstudio-zonder-voorraad": {"faqs": [
  ("Wat is de minimale bestelling?", MIN_A), (SHIP_Q, SHIP_BLOG)]},
 "blog/leverancier-antislipsokken-met-logo-kiezen": {"faqs": [(SHIP_Q, SHIP_BLOG)]},
 "blog/klantbinding-pilatesstudio-met-merkproducten": {"faqs": [
  ("Wat is de minimale bestelling?", MIN_A), (SHIP_Q, SHIP_BLOG)]},
}

if __name__ == "__main__":
    for path, spec in PAGES.items():
        f = f"site/nl/{path}/index.html"
        s = open(f, encoding="utf-8").read(); o = s
        for q, a in spec.get("answers", []):
            s, ok = set_answer(s, q, a)
            if not ok and a not in s:
                print("  vraag niet gevonden:", path, q)
        s, n = add_faqs(s, spec.get("faqs", []))
        if s != o:
            open(f, "w", encoding="utf-8").write(s)
        print(f"{path}: +{n}")
