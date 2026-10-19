# Franse sectie /fr/ gebouwd (19 oktober 2026)

Status: gebouwd en gecontroleerd op branch `fr` (laatste commit 27a923d). Niets live: merge naar `main` pas na akkoord van Giel.

## Wat er staat
- 21 Franse pagina's in `site/fr/`: home, chaussettes, gourde, tote bag, anneau, prix et marges, comment ça marche, FAQ, à propos, maquette gratuite, 3 nichepagina's (yoga, barre, kinésithérapie), blogindex + 6 artikelen (kerst eerst), `legal.html` (noindex).
- Besluiten: prijs 6,95 € HT / 19,95 € TTC; gratis levering in Europa, Zwitserse invoer-btw voor de ontvanger; geen straatadres; CNIL-cookiebanner (GA en Meta laden pas na "Tout accepter", gelijke knoppen, keuze 6 maanden); teksten DeepL-gecontroleerd, native review later.
- Cijfers: TVA 20 %, marge = TTC/1,20 − HT. Sokken 9,68 € (58 %), gourde 9,00 € (45 %), tote 6,00 € (48 %), anneau 6,75 € (49 %). BE 9,54 €, LU 10,10 €. Alleen externe cijfers: ASI 85 %, Bain/HBR 5 % → 95 %.
- Buiten /fr/ (alleen toevoegingen): hreflang fr + "FR" in taalwisselaar op 81 bestaande pagina's, sitemap (+20 FR-URL's en fr in bestaande clusters), `llms.txt` (Français-sectie, entiteitsalinea, Frankrijk-marge), Franse optie in de taalsuggestie-banner op de ES-home.
- Tooling: `docs/review/fr/` (build_fr.py, rebuild_all.sh, build_legal_fr.py, add_fr_links.py, update_sitemap_fr.py) en `docs/review/check_fr.py` (0 harde fouten).

## Open punten voor Giel
1. Laat `/fr/legal.html` juridisch nakijken. Zelf toegevoegd: verwijlrente volgens Spaanse wet 3/2004 plus 40 € incassokosten; btw-regeling (art. 4); Spaanse versie prevaleert bij verschil; CISG niet besproken; geen directeur de la publication; geen bewaartermijn GA.
2. Kerstdeadline overal: maquette vragen vóór 1 november, valideren uiterlijk 15 november.
3. Native review van de Franse teksten (vooral blog en nichepagina's).
4. Merge naar `main` na akkoord.

## Na livegang
Search Console en Bing Webmaster (sitemap), IndexNow, LinkedIn/Wikidata in het Frans, bsport, Europages, FPMP, Deciplus/Resamania, Team France Export (lead BRSE20260622007, sluit 8 dec 2026), 5 Franse test-prompts voor AI-zichtbaarheid.

## Aanvulling op merk-en-feiten (Frankrijk, nog niet in dat bestand verwerkt)
- Frankrijk heeft een eigen prijsstandaard: inkoop sokken 6,95 € HT, verkoop 19,95 € TTC, TVA 20 %, marge 9,68 € (58 %); gourde 11 → 24 (9,00 €, 45 %), tote 6,50 → 15 (6,00 €, 48 %), anneau 7 → 16,50 (6,75 €, 49 %). België (21 %) 9,54 €, Luxemburg (17 %) 10,10 €. 50 paar = 347,50 € HT, marge 483,75 €. Weergave in het Frans als HT en TTC.
- Verzending: in de Franse sectie "livraison gratuite dans toute l'Europe"; Zwitserse invoer-btw (8,1 %) en dedouanering voor de ontvanger, tenzij anders in de offerte.
- Franse termen: maquette gratuite en 24 h, devis, chaussettes antidérapantes, picots en silicone, tissé (jacquard) of brodé jamais imprimé, gourde isotherme 1,2 L, anneau de Pilates, élèves, vouvoiement. Nooit: merchandising, tumbler, goodies, courriel.
- Cookies op /fr/: CNIL-stijl, GA en Meta pas na "Tout accepter", knoppen gelijkwaardig, keuze 6 maanden.
- Rechtspagina /fr/legal.html is een concept en moet juridisch worden nagekeken (zie hierboven).
