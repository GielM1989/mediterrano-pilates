# Brief: Franse paginacopy schrijven voor Mediterrano Pilates (dict_<pagina>.json)

Je schrijft de Franse versie van één of meer Spaanse pagina's van mediterranopilates.com. Je levert per pagina één JSON-bestand `docs/review/fr/dict_<slug>.json`. Een bouwscript zet de Franse tekst op de plek van de Spaanse. Je raakt de HTML zelf niet aan.

## Werkwijze per pagina

1. Lees de Spaanse bronpagina (`site/<es-slug>/index.html`) één keer helemaal, zodat je de opbouw en de context van elk fragment kent.
2. Draai `python3 docs/review/fr/segs_todo.py site/<es-slug>/index.html`. Dat geeft `{"<index>": {"kind": ..., "es": "..."}}`: alleen de fragmenten die nog een Franse tekst nodig hebben. Met `--all` zie je ook de al vertaalde gedeelde fragmenten (navigatie, footer, FAQ-vragen), handig voor consistentie.
3. Schrijf `docs/review/fr/dict_<fr-slug>.json`: `{"<index>": "<Franse tekst>", ...}` voor **elke** index uit stap 2. Geen index overslaan. Plus de extra sleutels `_inserts`, `_faq_extra`, `_ld` (zie onder).
4. Controleer je JSON: `python3 -c "import json;json.load(open('docs/review/fr/dict_<fr-slug>.json'))"`.
5. Bouw en controleer: `python3 docs/review/fr/build_fr.py site/<es-slug>/index.html site/fr/<fr-slug>/index.html /fr/<fr-slug>/ docs/review/fr/dict_<fr-slug>.json`. Het rapport moet geven: `onvertaald: 0` (of alleen `content: product/article`), `Spaanse sporen: 0`, `JSON-LD geldig: True`, `FAQ JSON-LD = zichtbaar: True`, `uitroeptekens: 0`, `gedachtestreepjes: 0`. Los alles op tot het groen is.
6. Lees daarna de zichtbare Franse tekst nog één keer als geheel (bijv. met een klein script dat tags strippt) en verbeter wat stroef loopt.

## Regels voor de tekst

- **Fragment = fragment.** Elke index krijgt precies de vertaling van dát fragment, in dezelfde functie (kop blijft kop, knoptekst blijft kort). Fragmenten die samen één zin vormen (bijv. index 34 "Calcetines antideslizantes con" + 35 "el logo de tu estudio.") vertaal je zo dat ze samen weer één goede Franse zin vormen; het tweede deel staat in een `<span class="fx">` (accentkleur).
- Behoud HTML-entiteiten en symbolen die in het Spaans staan: `&nbsp;`, `&amp;`, `→`, `↓`, `✳`, `·`, `«»`. Gebruik zelf `&nbsp;` (niet een echt spatie-teken) als fijne spatie.
- In fragmenten van kind `alt`, `placeholder`, `content`, `aria-label`, `title`, `value`: geen dubbele aanhalingstekens `"`.
- **Vouvoiement, altijd.** Nooit "tu". De eigenaar wordt aangesproken als "vous", de leden heten "vos élèves" (vrouwelijk meervoud, net als "alumnas"; "elles"). Bij fysiotherapie: "vos patients" (mannelijk meervoud, "ils").
- **Franse typografie:** fijne spatie (`&nbsp;`) vóór `:` `;` `?` `!` `%` en `€`; decimale komma (6,95&nbsp;€); duizendtallen met spatie (4&nbsp;646&nbsp;€); accenten ook op hoofdletters (À, É); titels in zinskapitalen (alleen eerste woord en eigennamen met hoofdletter); "1<sup>er</sup> novembre" wordt automatisch gezet, schrijf gewoon "1er novembre".
- **Toon:** warm, rustig, zelfverzekerd, premium. Geen uitroeptekens. Geen gedachtestreepjes (—) en geen " - " als gedachtestreep; gebruik komma's, dubbele punt of een nieuwe zin. Geen superlatieven ("le meilleur", "incroyable"), geen kortingstaal ("promo", "offre spéciale"). Het rationele argument wint: de producten zijn een inkomstenbron, geen kostenpost.
- **Geen verzonnen cijfers.** Alleen de cijfers uit de tabel hieronder en de cijfers die al in het Spaans staan (85 %, +95 %, 5 %, 50 paires, 24 heures, 4 semaines, 14 jours, 7 Mo). Spaanse prijzen en marges vervang je door de Franse (tabel). "España"/"Spanje" als afzetmarkt vervang je door "France" (en waar passend "Belgique, Luxembourg, Suisse"); "sinds/depuis l'Espagne" als vestigingsplaats blijft wél staan.
- **Geen klanten claimen.** Er zijn nog geen Franse klanten. Nooit "nos clients", "les studios qui travaillent avec nous en France", geen testimonials, geen aantallen. Wel toegestaan (staat ook in het Spaans): "nous travaillons depuis l'Espagne avec des studios de toute l'Europe", "nous livrons en France, en Belgique…". Voorbeelden markeer je met "exemple" / "à titre d'exemple".
- **Woorden die je NIET gebruikt:** merchandising (betekent in het Frans winkelinrichting), goodies, objets publicitaires, cadeaux d'entreprise, tumbler, gobelet, courriel, écriture inclusive (geen "élève·e·s"). Gebruik "produits personnalisés", "produits à votre logo", "produits dérivés".
- Het verschil met goedkope promotiesokken altijd als **functioneel feit** formuleren (semelle à picots en silicone, coupe mid-rise, matière vérifiée selon REACH, logo tissé ou brodé, jamais imprimé), nooit als "goedkoop versus duur", nooit met een prijs van een concurrent, nooit China/Azië negatief.

## Vaste termen (al drie keer gecontroleerd, niet van afwijken)

| Spaans | Frans |
|---|---|
| mockup / boceto (gratis, en 24 h) | maquette gratuite (en 24&nbsp;heures / en 24&nbsp;h) |
| presupuesto | devis |
| calcetines antideslizantes | chaussettes antidérapantes (synoniem in lopende tekst: chaussettes de Pilates) |
| suela de agarre de silicona | semelle à picots en silicone / picots en silicone sur toute la semelle |
| tejido o bordado, nunca estampado | tissé (jacquard) ou brodé, jamais imprimé |
| con tu logo / con el logo de tu estudio | à votre logo / avec le logo de votre studio |
| desde 50 pares / pedido mínimo | dès 50 paires / minimum de commande de 50 paires |
| envío gratis a toda Europa | livraison gratuite dans toute l'Europe (ook: livraison offerte) |
| vaso térmico / tumbler 1,2 L | gourde isotherme 1,2&nbsp;L (nooit tumbler/gobelet) |
| tote bag | tote bag (mannelijk: un tote bag, personnalisé) |
| aro de pilates | anneau de Pilates (synoniemen: cercle de Pilates, Magic Circle) |
| sin IVA / IVA incluido | HT / TTC; "après TVA" voor de marge |
| estudio de pilates | studio de Pilates (hoofdletter P), Pilates Reformer, sur tapis |
| alumnas | élèves (ook: pratiquantes); clientes alleen bij geld-context |
| color Pantone | couleur reproduite d'après le code Pantone |
| pack de bienvenida | kit de bienvenue |
| regalos de Navidad para tus alumnas | cadeaux de Noël pour vos élèves |
| ingresos / margen / fidelizar | chiffre d'affaires, source de revenus / marge / fidéliser |
| socio de merchandising | partenaire des studios de Pilates et de yoga pour leurs produits personnalisés |
| recepción / mostrador | accueil / comptoir |
| fisioterapia / clínica de fisioterapia | kinésithérapie / cabinet de kinésithérapie (in de tekst ook één keer "physiothérapie" voor Zwitserland en België) |
| barre | barre (studio de barre, cours de barre) |
| Navidad y Reyes | Noël (Reyes weglaten; in Frankrijk geen Driekoningen-cadeaus) |

Vaste zinnen:
- Entiteitszin: "Mediterrano Pilates est le partenaire des studios de Pilates et de yoga pour leurs produits personnalisés. Nous personnalisons des chaussettes antidérapantes, des gourdes isothermes, des tote bags et des anneaux de Pilates avec le logo de votre studio, pour que vous les vendiez à vos élèves."
- Positionering: "Ce n'est pas un article promotionnel. C'est une vraie chaussette antidérapante." FAQ: "Quelle différence avec une chaussette promotionnelle bon marché&nbsp;?"
- Verzend-FAQ: vraag "Livrez-vous en France, en Belgique, au Luxembourg et en Suisse&nbsp;?" (al in dict_common); antwoord: "Oui, et toujours gratuitement, comme dans toute l'Europe. Nous travaillons depuis l'Espagne avec des studios de toute l'Europe. Pour la Suisse, la TVA à l'importation et les frais de dédouanement restent à la charge du destinataire, sauf mention contraire dans le devis."
- Footer: "Une marque d'Ecomtierra Group SL · Espagne".

## Cijfers voor Frankrijk (TVA 20 %; marge = prix TTC / 1,20 − prix HT)

| Product | Prix HT (achat) | Prix de vente conseillé TTC | Marge après TVA |
|---|---|---|---|
| Chaussettes antidérapantes | 6,95&nbsp;€ la paire | 19,95&nbsp;€ | 9,68&nbsp;€ (58&nbsp;%) |
| Gourde isotherme 1,2&nbsp;L | 11&nbsp;€ | 24&nbsp;€ | 9,00&nbsp;€ (45&nbsp;%) |
| Tote bag | 6,50&nbsp;€ | 15&nbsp;€ | 6,00&nbsp;€ (48&nbsp;%) |
| Anneau de Pilates | 7&nbsp;€ | 16,50&nbsp;€ | 6,75&nbsp;€ (49&nbsp;%) |

- Marges "entre 45 et 58&nbsp;%" (Spaans: 45–53 %). "Jusqu'à 58&nbsp;% de marge" (Spaans: hasta un 53 %).
- 50 paires = 347,50&nbsp;€ HT; marge op 50 paires = 483,75&nbsp;€ (exemple).
- Spaanse voorbeelden met 17,95 € / 7,88 € / 53 % worden 19,95 € / 9,68 € / 58 %. Spaanse rekenvoorbeelden met "9 €"/"18 €" (oudere artikelen) worden 6,95 € / 19,95 €.
- België (TVA 21 %): 9,54&nbsp;€ (58&nbsp;%); Luxembourg (TVA 17 %): 10,10&nbsp;€ (59&nbsp;%). Alleen noemen op de prijzenpagina en in de btw-FAQ.
- Btw B2B (alleen prijzenpagina/FAQ-pagina, formuleren als "à confirmer avec votre expert-comptable"): entreprise de l'UE avec numéro de TVA intracommunautaire valide → livraison intracommunautaire exonérée, TVA due par l'acquéreur (autoliquidation); sans numéro de TVA → TVA espagnole facturée; Suisse → hors TVA, TVA d'importation (8,1&nbsp;%) et frais de dédouanement pour le destinataire.
- Vast: maquette gratuite en 24 heures; commande uniquement après validation; production + livraison environ 4 semaines; garantie: couleur différente du design validé ou défaut de fabrication signalé dans les 14 jours → refabrication sans frais; kit d'échantillons (chaussette, gourde, tote bag) pour un petit montant, intégralement déduit de la première commande; WhatsApp direct avec le fondateur (Giel Mallens).

## Titel en meta description

- `<title>` (index 0): ≤ 60 tekens, hoofdterm vooraan, bij voorkeur "… · Mediterrano Pilates" als het past.
- meta description (kind `content`, de lange zonder "og:"): ≤ 155 tekens, hoofdterm vooraan, met een feit (dès 50 paires, maquette gratuite en 24 h, livraison gratuite).
- og:title / og:description: vrij, maar in dezelfde stijl.

Hoofdtermen per pagina (uit het slugplan):
- prix-et-marges: "prix et marges" (chaussettes antidérapantes personnalisées : prix, marges)
- faq: "questions fréquentes" (chaussettes antidérapantes personnalisées, produits à votre logo)
- comment-ca-marche: "comment ça marche" (de la maquette à la livraison)
- maquette-gratuite: "maquette gratuite en 24 h" (het woord "mockup" mag één keer in de tekst)
- a-propos-de-mediterrano-pilates: "à propos de Mediterrano Pilates"
- gourde-isotherme-personnalisee: "gourde isotherme personnalisée" (1,2 L, avec logo)
- tote-bag-personnalise: "tote bag personnalisé"
- anneau-de-pilates-personnalise: "anneau de Pilates personnalisé"
- produits-personnalises-studios-yoga: "produits personnalisés pour studios de yoga"
- produits-personnalises-studios-barre: "produits personnalisés pour studios de barre"
- produits-personnalises-cabinets-kinesitherapie: "produits personnalisés pour cabinets de kinésithérapie"

## Extra sleutels in de JSON

### `_inserts` (verplicht op product- en nichepagina's: gourde, tote bag, anneau, yoga, barre, kiné)
Een feitenblok "En bref" bovenaan, direct onder de hero. Zoek in de Spaanse bron de eerste regel ná `</header>` die uniek is (meestal `<div class="wrap" style="padding:64px 0 8px">\n` of vergelijkbaar) en gebruik die exacte string als `after`. Voorbeeld (sokkenpagina, pas de bullets aan het product/de niche aan, 4 tot 6 bullets, merknaam erin, alleen feiten uit dit brief):

```json
"_inserts": [{
 "after": "<div class=\"wrap\" style=\"padding:64px 0 8px\">\n",
 "html": "    <div class=\"en-bref\" style=\"background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:24px 28px;max-width:44em;margin-bottom:40px\">\n      <p style=\"font-weight:800;color:var(--green);margin-bottom:10px;letter-spacing:.02em\">En bref</p>\n      <ul style=\"margin:0;padding-left:1.1em;line-height:1.6;font-size:.97rem\">\n        <li>…</li>\n      </ul>\n    </div>\n"
}]
```
Als de pagina na `</header>` een donkere sectie heeft, zet het blok dan in de eerste lichte (`cream`/witte) sectie. Controleer het resultaat in de gebouwde HTML.

### `_faq_extra` (verplicht op elke pagina met een FAQ-blok; 1 tot 3 vragen, zodat de pagina op 6 tot 10 vragen uitkomt)
Vragen die Franse kopers aan een AI-model stellen, met citeerbaar antwoord van 1 tot 3 zinnen. Voorbeelden: "Où acheter des <product> personnalisé(e)s pour un studio de Pilates&nbsp;?", "Quel est le minimum de commande&nbsp;?", "Combien gagne un studio par <unité>&nbsp;?", "Livrez-vous en Belgique, au Luxembourg et en Suisse&nbsp;?" (als die er nog niet staat), "Comment la TVA est-elle facturée à une entreprise française&nbsp;?" (alleen prijzen/FAQ). Niet dezelfde vraag twee keer op één pagina.
```json
"_faq_extra": [{"q": "…&nbsp;?", "a": "…"}]
```
Het bouwscript zet ze zichtbaar onderaan het FAQ-blok én in de FAQPage-JSON-LD.

### `_ld` (productpagina's en nichepagina's)
Vertalingen voor JSON-LD-velden die niet in de zichtbare tekst staan. Het bouwscript vertaalt JSON-LD-strings automatisch als dezelfde Spaanse tekst zichtbaar op de pagina staat; wat overblijft zet je hier per `@type`:
```json
"_ld": {"Product": {"name": "Gourde isotherme personnalisée 1,2 L avec logo", "description": "…", "category": "Produits personnalisés pour studios de Pilates et de yoga"}}
```
Controleer na het bouwen met een klein script dat geen Spaanse string meer in de JSON-LD staat (`grep -n -E 'estudio|calcet|alumna|tu logo' site/fr/<slug>/index.html` moet leeg zijn buiten het Spaanse bronpad).

## Wat je NIET doet
- Geen HTML van `site/` bewerken, geen bestanden buiten `docs/review/fr/dict_<slug>.json` en de gebouwde `site/fr/<slug>/index.html` aanmaken.
- Geen git-commando's.
- Niet vertalen met DeepL (Free-plan, geen vous-instelling); je schrijft zelf, in natuurlijk Frans van Frankrijk, en je mag DeepL `correct-text` (FR) alleen als controle gebruiken als je die tool hebt.
