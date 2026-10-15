# Brief: Franse pagina's schrijven voor Mediterrano Pilates (fase B)

Je schrijft de Franse versie van één of meer Spaanse pagina's van mediterranopilates.com. Je levert per pagina één JSON-bestand `docs/review/fr/dict_<pagina>.json`. Het bouwscript zet jouw Franse tekst op de plaats van de Spaanse segmenten; jij raakt geen HTML aan.

## Lees eerst (in deze volgorde)
1. `docs/prompts/bouwprompt-franse-sectie-fr.md`, hoofdstukken 5 (taal en toon), 6 (merk), 7 (cijfers), 9 (AEO).
2. `research_notes/Franse sectie bouweisen/frans_terminologie_toon_aeo.md` en `termencheck_1_webshops.md`, `termencheck_2_pilateswereld.md` (vastgestelde termen).
3. `docs/review/fr/dict_common.json` (gedeelde vertalingen: navigatie, footer, formulier, FAQ-vragen die op meerdere pagina's staan) en `docs/review/fr/dict_socks.json` (voorbeeld van een afgeronde pagina, inclusief `_inserts`, `_faq_extra`, `_ld`).
4. Het todo-bestand van je pagina: `docs/review/fr/todo_<pagina>.json`. Daarin: `_todo` (index → Spaanse tekst die vertaald moet worden), `_ld_strings` (strings uit de JSON-LD die vertaald moeten worden), `_numeric_segments` (cijfers die het script overslaat; zie `_replace`).
5. De Spaanse bronpagina zelf (`site/<pagina>/index.html`), om de context van elk segment te zien (koppen, tabellen, knoppen).

## Wat je oplevert: `dict_<pagina>.json`
```json
{
  "0": "Franse tekst voor segment 0",
  "35": "…",
  "_ld_map": { "Spaanse JSON-LD-string (exact)": "Franse versie" },
  "_replace": [ ["7,88&nbsp;€", "9,68&nbsp;€"], ["53%", "58&nbsp;%"] ],
  "_inserts": [ { "after": "<unieke HTML-marker uit de bron>\n", "html": "…" } ],
  "_faq_extra": [ { "q": "Vraag&nbsp;?", "a": "Antwoord." } ],
  "_ld": { "Product": { "name": "…", "description": "…" } }
}
```
- Elke sleutel uit `_todo` krijgt een Franse waarde. Laat de prefix `content: ` / `alt: ` / `placeholder: ` / `aria-label: ` weg in je waarde; vertaal alleen de tekst. Behoud leidende/afsluitende spaties niet (het script doet dat). Behoud HTML-entiteiten zoals `&nbsp;` en `&amp;` en schrijf zelf `&nbsp;` vóór `: ; ? ! % €` in de Franse typografie. Geen `"` in waarden van attributen (gebruik « »).
- Segmenten zijn soms halve zinnen (een `<span class="fx">`-deel van een kop). Vertaal ze zo dat de twee helften samen één Franse zin vormen; kijk in de bron welke segmenten bij elkaar horen.
- `_ld_map`: elke string uit `_ld_strings` krijgt een Franse versie (behalve typenamen zoals "BreadcrumbList"; die mag je weglaten). FAQ-strings in JSON-LD moeten woordelijk gelijk zijn aan je zichtbare FAQ-tekst (gebruik dezelfde tekst, zonder `&nbsp;`: het script normaliseert).
- `_replace`: voor cijfers die in `_numeric_segments` staan en in Frankrijk anders zijn (prijzen, marges, btw-percentages). Gebruik de exacte tekst zoals die in de HTML staat (met `&nbsp;` als het er staat). Controleer in de bron.
- `_inserts`: alleen voor product- en nichepagina's: een "En bref"-feitenblok (4 tot 6 korte, zelfstandige zinnen met de merknaam erin) bovenaan, direct na de hero. Kopieer de opmaak uit `dict_socks.json`. Kies een marker die exact één keer in de bron voorkomt (bijvoorbeeld de eerste `<div class="wrap" …>` na `</header>`).
- `_faq_extra`: voeg toe als de pagina minder dan 6 FAQ-vragen heeft, of als de vaste vragen ontbreken (zie hieronder). Maximaal 10 vragen in totaal.
- Vertaal niet: merknamen, "Mediterrano Pilates", "Ecomtierra Group SL", e-mailadres, "Pantone", "REACH", "Instagram", "WhatsApp", "Reformer", "tote bag".

## Taal (hard)
- Frans voor Frankrijk, vouvoiement overal, warm, zelfverzekerd, premium, rustig. Geen uitroeptekens, geen gedachtestreepjes (—), geen kortingstaal, geen superlatieven ("le meilleur", "incroyable"). Komma's of een dubbele punt in plaats van streepjes.
- Typografie: fijne spatie (`&nbsp;`) vóór `: ; ? ! %` en `€`; decimale komma (6,95 €); "6,95 € HT", "19,95 € TTC"; accenten ook op hoofdletters (À, É); titels in zinskapitaal (alleen eerste letter hoofdletter); « guillemets » met `&nbsp;` erbinnen.
- Doelgroep aanspreken als "vos élèves" (vrouwelijk, net als "alumnas" in het Spaans: "elles"); de eigenaar is "vous". Waar het Spaans "tu" zegt, zeg jij "vous".

## Vaste termen (niet afwijken)
| Spaans | Frans |
|---|---|
| boceto / mockup | maquette (gratuite, en 24 h); "le visuel" als synoniem in lopende tekst |
| presupuesto | devis |
| calcetines antideslizantes | chaussettes antidérapantes (synoniem: chaussettes de Pilates) |
| suela de agarre de silicona | semelle à picots en silicone / picots en silicone |
| tejido o bordado, nunca estampado | tissé (jacquard) ou brodé, jamais imprimé |
| vaso térmico / tumbler | gourde isotherme (1,2 L); nooit "tumbler", "gobelet", "mug" |
| tote bag | tote bag (mannelijk: un tote bag, personnalisé) |
| aro de pilates | anneau de Pilates (synoniemen: cercle de Pilates, Magic Circle) |
| merchandising | produits personnalisés / produits à votre logo / produits dérivés. Nooit "merchandising" (betekent winkelinrichting), nooit "goodies", nooit "objets publicitaires" |
| estudio de pilates | studio de Pilates (hoofdletter P) |
| alumnas | élèves (ook: pratiquantes, clientes) |
| pedido mínimo / desde 50 pares | minimum de commande / dès 50 paires |
| envío gratis | livraison gratuite (of "livraison offerte") dans toute l'Europe |
| sin IVA / IVA incluido | HT / TTC; "après TVA" |
| margen | marge; "chiffre d'affaires", "source de revenus" |
| fidelizar | fidéliser |
| pack de bienvenida | kit de bienvenue |
| regalos de Navidad | cadeaux de Noël |
| España (als land van vestiging) | Espagne ("Basés en Espagne", "depuis l'Espagne") |
| fisioterapia / clínica | kinésithérapie / cabinet de kinésithérapie (voor Zwitserland ook "physiothérapie" noemen) |
| entiteitszin | "Mediterrano Pilates est le partenaire des studios de Pilates et de yoga pour leurs produits personnalisés. Nous personnalisons des chaussettes antidérapantes, des gourdes isothermes, des tote bags et des anneaux de Pilates avec le logo de votre studio, pour que vous les vendiez à vos élèves." |
| positionering | "Ce n'est pas un article promotionnel. C'est une vraie chaussette antidérapante." |

## Cijfers voor Frankrijk (TVA 20 %; marge = TTC / 1,20 − HT). Gebruik uitsluitend deze.
| Product | Inkoop HT | Verkoop conseillé TTC | Marge na TVA |
|---|---|---|---|
| Chaussettes antidérapantes | 6,95 € | 19,95 € | 9,68 € (58 %) |
| Gourde isotherme 1,2 L | 11 € | 24 € | 9,00 € (45 %) |
| Tote bag | 6,50 € | 15 € | 6,00 € (48 %) |
| Anneau de Pilates | 7 € | 16,50 € | 6,75 € (49 %) |
- Bereik: "entre 45 et 58 % de marge après TVA, selon le produit". 50 paires = 347,50 € HT.
- Spaanse cijfers die je dus vervangt: 17,95 € → 19,95 €; 7,88 € → 9,68 €; 53 % → 58 %; 21 % → 20 %; 8,83 € → 9,00 €; 5,90 € → 6,00 €; 6,64 € → 6,75 €; "45–53 %" → "45–58 %".
- "PVP recomendado en España" → "prix de vente conseillé en France". Schrijf nooit dat studio's in Frankrijk al bij ons kopen of iets "de media" verkopen: er zijn nog geen Franse klanten. Formuleer als advies of voorbeeld ("exemple").
- Vast: minimum 50 paar sokken (overige producten op devis); maquette gratuite sous 24 h; commande uniquement après validation; production et livraison environ 4 semaines; échantillons (chaussette, gourde, tote bag) pour un petit montant, intégralement déduit de la première commande; garantie: couleur non conforme au design validé ou défaut de fabrication signalé sous 14 jours = refabrication sans frais.
- Btw voor bedrijven: "entreprise de l'UE avec numéro de TVA intracommunautaire valide: livraison intracommunautaire exonérée, TVA due par l'acquéreur (autoliquidation); sans numéro de TVA: TVA espagnole facturée; Suisse: hors TVA, TVA à l'importation (8,1 %) et frais de dédouanement à la charge du destinataire, sauf mention contraire dans le devis". Zet "à confirmer par votre comptable" er niet bij op de site; wel "selon votre situation".
- Landen: zeg nooit dat we alleen in Frankrijk of Spanje leveren. Standaardzin: "livraison gratuite dans toute l'Europe, y compris la France, la Belgique, le Luxembourg et la Suisse" en "nous travaillons depuis l'Espagne avec des studios de toute l'Europe".
- Geen testimonials, geen klantenaantallen, geen casestudy's. Voorbeelden markeren als "exemple".
- Statistieken alleen deze twee, letterlijk: "85 % des personnes se souviennent de la marque d'un produit qu'elles ont porté (ASI Global Advertising Impressions Study, 2026)" en "augmenter la fidélisation de seulement 5 % peut représenter jusqu'à 95 % de bénéfice en plus (Bain & Company / Harvard Business Review)". Verzin geen andere cijfers, ook niet over de Franse markt.

## SEO/AEO per pagina
- Segment 0 is de `<title>`: maximaal 60 tekens, hoofdterm vooraan. Meta description (segment met `content:` dat op de Spaanse description lijkt): maximaal 155 tekens.
- De H1 bevat de hoofdterm van de pagina (zie tabel in bouwprompt hoofdstuk 3; let op: de nichepagina's heten `/fr/produits-personnalises-studios-yoga/`, `/fr/produits-personnalises-studios-barre/`, `/fr/produits-personnalises-cabinets-kinesitherapie/`).
- FAQ-antwoorden: 1 tot 3 zinnen, zelfstandig citeerbaar (de merknaam of het product mag erin).
- Vaste vragen die op product- en nichepagina's moeten voorkomen (voeg toe via `_faq_extra` als ze ontbreken): "Quel est le minimum de commande&nbsp;?", "Livrez-vous en France, en Belgique, au Luxembourg et en Suisse&nbsp;?" (antwoord met de Zwitserland-zin), en op de prijzenpagina en FAQ-pagina de btw-vraag "Comment fonctionne la TVA pour un studio français&nbsp;?".
- Blogtitels en interne linkteksten staan al in `dict_common.json`; gebruik dezelfde formuleringen.

## Werkwijze
1. Lees de bron en het todo-bestand. Schrijf per segment Frans dat natuurlijk klinkt voor een Franse studio-eigenaar; vertaal de bedoeling, niet woord voor woord. Houd de lengte vergelijkbaar (lay-out).
2. Schrijf het dict-bestand. Valideer dat het geldige JSON is (`python3 -c "import json;json.load(open(...))"`).
3. Bouw de pagina en lees het rapport: `python3 docs/review/fr/build_fr.py site/<es-pad>/index.html site/fr/<fr-slug>/index.html /fr/<fr-slug>/ docs/review/fr/dict_<pagina>.json`. Het rapport moet geven: `onvertaald: 0`, `Spaanse sporen: 0`, `JSON-LD geldig: True`, `FAQ JSON-LD = zichtbaar: True`, `gedachtestreepjes: 0`, `uitroeptekens: 0`. Los alles op wat niet klopt (ook `WAARSCHUWING: _replace niet gevonden`).
4. Controleer daarna in `site/fr/<fr-slug>/index.html` met een grep dat er geen Spaanse cijfers meer staan: `17,95`, `7,88`, `53%`, `21%`, `8,83`, `5,90`, `6,64`, en geen woorden "merchandising", "tumbler", "goodies", "España", "IVA".
5. Meld in je eindbericht: welke pagina's, aantal woorden, de gekozen title en description per pagina, twijfelgevallen in terminologie, en wat je in `_replace`/`_faq_extra`/`_inserts` hebt gezet. Commit niets.
