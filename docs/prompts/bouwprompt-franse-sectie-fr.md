# Bouwprompt: Franse sectie /fr/ voor Mediterrano Pilates

*Opgesteld 15 oktober 2026. Voor gebruik in deze sessie (repo `/home/claude/mediterrano-pilates`, project "Mediterrano — SEO & AEO (ES)").*

---

## 0. Opdracht in één alinea

Bouw een complete Franse sectie op `https://mediterranopilates.com/fr/`, gebaseerd op de Spaanse hoofdsite (de bron), maar geschreven voor Franse studio-eigenaren. De Franse pagina's moeten voldoen aan exact dezelfde merk-, feiten-, SEO- en AEO-eisen als de Spaanse, en daarnaast aan de Franse taal-, typografie- en juridische eisen. Doel van elke pagina: een gratis logo-mockup laten aanvragen. Doel van de sectie: zo snel mogelijk gevonden worden in Google (google.fr, .be, .lu, .ch) en genoemd worden in ChatGPT, Gemini, Perplexity, Le Chat en Google AI Overviews / AI Mode (in Frankrijk live sinds 22 juli 2026). Kwaliteit boven snelheid: geen enkele pagina gaat live die niet door alle controles in hoofdstuk 12 komt.

## 1. Eerst lezen (in deze volgorde)

1. Project: `merk-en-feiten` (merkregels, toon, verboden claims) en `claude/groeiplan-google-ai-landen-2026-10-14.md`.
2. Repo: `site/llms.txt`, sectie "Key facts". **Dit is de actuele feitenstand van de live site** (prijs 6,95 € per paar overal, gratis verzending in heel Europa, kwaliteitsgarantie, proefset). Waar `merk-en-feiten` iets anders zegt (bijv. "gratis wereldwijd", 7,50 €), volg je de live site en `llms.txt`, en zet je het verschil op de lijst voor Giel. Verzin nooit een nieuw feit.
3. Repo: alle Spaanse bronpagina's (tabel in hoofdstuk 3). De Spaanse site is door een native speaker gecorrigeerd en is de inhoudelijke bron. Gebruik voor structuur en techniek één op één dezelfde HTML-opbouw (inline CSS en JS per pagina, header, taalwisselaar, footer, formulier, cookiebanner, WhatsApp-knop, GA4 met Consent Mode, Meta Pixel).
4. Onderzoeksnotities: `research_notes/Franse sectie bouweisen/frans_terminologie_toon_aeo.md` en `frans_juridisch_cookies.md` (termen, slugs, toon, typografie, mentions légales, cookies, btw-teksten), plus `research_notes/Groeikansen Google AEO en landen/frankrijk_italie_kansen.md`.

## 2. Stap 0: beslissingen van Giel (één bericht, met voorstel)

Stel deze vijf vragen in één bericht, elk met het voorstel erbij, en bouw daarna door. Wacht alleen op antwoord bij vraag 3 en 4 als Giel afwijkt van het voorstel; de rest kan parallel.

1. **Prijs Frankrijk.** Voorstel: 6,95 € HT per paar (zoals overal), prix de vente conseillé 19,95 € TTC.
2. **Verzending.** Voorstel: "livraison offerte dans toute l'Europe", met een aparte FAQ voor Zwitserland (invoer-btw en douanekosten voor de ontvanger, DAP, tenzij de offerte anders zegt). Laat Giel dit door de gestor bevestigen.
3. **Adres in de mentions légales.** De andere talen tonen geen straatadres (merkregel). Het onderzoek zegt dat zowel Spaans als EU-recht een geografisch adres verwacht. Voorstel: Giel beslist; zonder akkoord volg je de huidige regel (land + CIF + e-mail + "adresse communiquée sur demande") en noteer je het risico.
4. **Cookies op /fr/.** De CNIL is strikt. Voorstel: op de Franse pagina's Consent Mode "basic": gtag.js en de Meta Pixel laden pas na "Tout accepter"; knoppen "Tout refuser" en "Tout accepter" even groot en even opvallend; een laag "Personnaliser"; een vaste link "Gestion des cookies" in de footer; keuze 6 maanden bewaard. Gevolg: minder GA4-data van Franse bezoekers die weigeren.
5. **Franstalige controle.** Voorstel: alle tekst via DeepL (zie hoofdstuk 4) plus jouw eigen controle; live na Giels akkoord op screenshots; een native Franse controle zodra Giel iemand heeft, als verbeterronde.

## 3. Wat er gebouwd wordt: 21 pagina's

Spaanse bron → Franse URL. Slugs zonder accenten, met koppeltekens. Titels maximaal 60 tekens, descriptions maximaal 155 (tellen na het omzetten van HTML-entiteiten).

| Spaanse bron | Franse URL | Hoofdterm (H1 en title) |
|---|---|---|
| `/` | `/fr/` | merchandising et chaussettes antidérapantes à votre logo pour studios de Pilates |
| `/calcetines-antideslizantes-personalizados/` | `/fr/chaussettes-antiderapantes-personnalisees/` | chaussettes antidérapantes personnalisées (synoniem in H2/tekst: chaussettes de Pilates à votre logo) |
| `/botellas-personalizadas-estudios-pilates/` | `/fr/gourde-isotherme-personnalisee/` | gourde isotherme personnalisée 1,2 L ("tumbler" in de tekst) |
| `/tote-bags-personalizadas-estudios-yoga/` | `/fr/tote-bag-personnalise/` | tote bag personnalisé |
| `/aro-de-pilates-personalizado/` | `/fr/anneau-de-pilates-personnalise/` | anneau de Pilates personnalisé (ook "cercle de Pilates", "magic circle") |
| `/precios-y-margenes/` | `/fr/prix-et-marges/` | prix et marges |
| `/preguntas-frecuentes/` | `/fr/faq/` | questions fréquentes |
| `/como-funciona/` | `/fr/comment-ca-marche/` | comment ça marche |
| `/mockup-gratis/` | `/fr/maquette-gratuite/` | maquette gratuite en 24 h ("mockup" mag in de tekst) |
| `/sobre-mediterrano-pilates/` | `/fr/a-propos-de-mediterrano-pilates/` | à propos de Mediterrano Pilates |
| `/merchandising-estudios-yoga/` | `/fr/merchandising-studios-yoga/` | merchandising pour studios de yoga |
| `/merchandising-estudios-barre/` | `/fr/merchandising-studios-barre/` | merchandising pour studios de barre |
| `/merchandising-clinicas-fisioterapia/` | `/fr/merchandising-cabinets-kinesitherapie/` | merchandising pour cabinets de kinésithérapie (in de tekst ook "physiothérapie" voor Zwitserland) |
| `/blog/` | `/fr/blog/` | blog |
| `/blog/aumentar-ingresos-estudio-pilates-sin-stock/` | `/fr/blog/augmenter-chiffre-affaires-studio-pilates-sans-stock/` | augmenter le chiffre d'affaires de votre studio sans stock |
| `/blog/fidelizar-alumnas-pilates-productos-marca/` | `/fr/blog/fideliser-eleves-pilates-produits-a-votre-logo/` | fidéliser vos élèves avec des produits à votre logo |
| `/blog/como-elegir-proveedor-calcetines-personalizados/` | `/fr/blog/choisir-fournisseur-chaussettes-antiderapantes-personnalisees/` | choisir un fournisseur de chaussettes antidérapantes personnalisées |
| `/blog/cuanto-cuesta-personalizar-calcetines-antideslizantes/` | `/fr/blog/prix-chaussettes-antiderapantes-personnalisees/` | combien coûtent des chaussettes antidérapantes personnalisées |
| `/blog/regalos-de-navidad-alumnas-pilates/` | `/fr/blog/cadeaux-de-noel-eleves-pilates/` | cadeaux de Noël pour vos élèves de Pilates |
| `/blog/pack-de-bienvenida-alumnas-nuevas-pilates/` | `/fr/blog/kit-de-bienvenue-nouveaux-eleves-pilates/` | kit de bienvenue pour vos nouveaux élèves |
| `/legal.html` | `/fr/legal.html` | Mentions légales, CGV, confidentialité et cookies |

Het kerstartikel krijgt de actuele deadline (maquette goedgekeurd uiterlijk vrijdag 13 november voor levering rond half december, levertijd ongeveer 4 weken).

## 4. Vertaalmethode: DeepL eerst, dan aanpassen

1. **Elke vertaling gaat via DeepL** (`mcp__DeepL__translate-text`), niet uit je hoofd. Vertaal tekstblokken, niet hele HTML-bestanden: haal per pagina de zichtbare teksten, alt-teksten, meta-teksten en JSON-LD-teksten eruit, vertaal ze in batches en zet ze terug in de HTML.
   - `sourceLang: "ES"`, `targetLangs: ["FR"]`, `formality: "more"` (vouvoiement).
   - `context`: "B2B website for pilates and yoga studio owners in France. Custom grip socks and merchandise with the studio's logo, resold to members."
   - `customInstructions`, bijvoorbeeld: "Use 'vous'." · "calcetines antideslizantes = chaussettes antidérapantes" · "alumnas = élèves" · "estudio = studio de Pilates" · "IVA = TVA" · "tejido = tissé (jacquard), bordado = brodé, estampado = imprimé" · "No exclamation marks."
   - Controleer eerst `list-glossaries`. Stel een glossarium ES→FR voor met de termen uit hoofdstuk 5, en maak het pas aan na akkoord van Giel.
2. **Daarna aanpassen voor Frankrijk (transcreatie).** Zet "tú" om naar "vous", vervang Spaanse voorbeelden, prijzen en btw door de Franse cijfers (hoofdstuk 7), en verwijder alles wat alleen voor Spanje geldt.
3. **Daarna corrigeren** met `mcp__DeepL__correct-text` (`targetLang: "FR"`) op alle eindteksten, en waar zinnen stijf zijn `rephrase-text` met `writingStyle: "business"`.
4. Controleer daarna zelf of de feiten nog kloppen: DeepL mag nooit een getal, claim of merknaam veranderen.

## 5. Taal en toon in het Frans

- **Vouvoiement overal.** Geen "tu", "ton", "ta", "tes", "toi" (bsport en Resamania spreken studio-eigenaren ook met "vous" aan).
- **Toon:** warm, zelfverzekerd, premium, rustig. Geen uitroeptekens, geen kortingstaal ("promo", "offre spéciale", "-20 %"), geen overtreffende trap ("le meilleur", "n°1"). Het rationele argument wint: le merchandising est un revenu, pas une dépense.
- **Termen (verplicht):**
  - chaussettes antidérapantes (hoofdterm), chaussettes de Pilates (synoniem); "grip" alleen als het merkwoord in een productnaam staat
  - personnalisées, à votre logo, sur mesure
  - logo tissé (jacquard) ou brodé, jamais imprimé
  - semelle antidérapante en silicone, coupe mi-mollet (mid-rise)
  - gourde isotherme 1,2 L (niet "gobelet")
  - tote bag en toile (mannelijk: un tote bag personnalisé)
  - anneau de Pilates (ook cercle de Pilates)
  - studio de Pilates (Pilates met hoofdletter), Pilates Reformer / Pilates sur machine, barre, yoga
  - élèves (bij binding en cadeaus), clients (bij omzet), adhérents (bij abonnementen)
  - maquette (mockup), devis, TVA, HT, TTC, accueil (de balie), merchandising, produits à votre logo
- **Verboden of af te raden:** goodies, objets publicitaires (klinkt als gratis weggeefartikelen), chaussettes de préhension, étudiantes, propriétaire de studio als aanspreekvorm, courriel (Québec; gebruik e-mail), inclusieve punt (élève·s).
- **Typografie (Frans uit Frankrijk):**
  - Vaste spatie (`&nbsp;`, of `&#8239;` als smalle spatie) vóór `:` `;` `?` `!` `%` en vóór `€`, en binnen « guillemets ».
  - Decimale komma, spatie als duizendtalscheiding: `6,95 € HT`, `19,95 € TTC`, `1 200 studios`, `1,2 L`, `24 h`.
  - Hoofdletters met accent: À, É.
  - Titels in zinsvorm, geen hoofdletter per woord.
- **Huisregels die ook in het Frans gelden:**
  - Geen gedachtestreepjes (—) en geen en-dash als gedachtestreepje; het middelpuntje (·) mag.
  - Geen testimonials, geen klantenaantallen.
  - Voorbeelden markeer je als "exemple".
  - Nooit prijzen van concurrenten.
  - China/Azië nooit negatief als productieland neerzetten.

## 6. Merk en propositie (zelfde als Spanje, in het Frans)

- **Vaste omschrijving van de entiteit, letterlijk in de Organization-gegevens en op home/over ons, eerst door DeepL en dan vastzetten:** "Mediterrano Pilates est le partenaire merchandising des studios de Pilates et de yoga. Nous personnalisons des chaussettes antidérapantes, des gourdes isothermes, des tote bags et des anneaux de Pilates avec le logo de votre studio, pour que vous les vendiez à vos élèves." Plus: "Une marque d'Ecomtierra Group SL (Espagne)."
- **Bereik, altijd in FAQ en over ons:** werkt vooral met studio's in Spanje en Europa, levering in heel Europa (volgens de keuze uit stap 0). Sluit geen land uit. Noem Frankrijk, België, Luxemburg en Zwitserland expliciet in de FAQ.
- **De drie marges** (verplicht op conversiepagina's en in artikelen), met dezelfde bronnen, letterlijk vertaald via DeepL:
  - 85 % (ASI Global Advertising Impressions Study, 2026)
  - +95 % (Bain & Company / Harvard Business Review)
  - "tout ou rien" (Rozin & Royzman, 2001)
- **Positionering:** "Ce n'est pas un article promotionnel. C'est une vraie chaussette antidérapante." Plus de vaste FAQ "Quelle différence avec une chaussette promotionnelle bon marché ?".

## 7. Feiten en cijfers voor Frankrijk

Uitgangspunt: de keuze uit stap 0. Hieronder het voorstel. **Rekenregel: marge = verkoop TTC / (1 + TVA) − inkoop HT.** Deze rekenregel geldt ook in de JavaScript-rekentool: deel door **1,20**, niet door 1,21. In Duitsland stond eerder per ongeluk het Spaanse tarief in de rekentool.

| Product | Inkoop HT | Conseillé TTC | Marge na TVA 20 % |
|---|---|---|---|
| Chaussettes antidérapantes | 6,95 € | 19,95 € | 9,68 € (58 %) |
| Gourde isotherme 1,2 L | 11 € | 24 € | 9,00 € (45 %) |
| Tote bag | 6,50 € | 15 € | 6,00 € (48 %) |
| Anneau de Pilates | 7 € | 16,50 € | 6,75 € (49 %) |

- 50 paar: 347,50 € HT inkoop, marge 483,75 € (exemple).
- België (TVA 21 %): sokmarge 9,54 € (58 %). Luxemburg (TVA 17 %): 10,10 € (59 %). Zwitserland: geen marge-berekening, alleen de FAQ over invoer-btw.
- Vast:
  - minimum 50 paar sokken; tumbler, tote en ring op offerte
  - maquette gratis binnen 24 uur
  - bestelling pas na goedkeuring
  - productie en levering samen ongeveer 4 weken ("environ 4 semaines"); tijdlijn "Livraison : semaine 4 (env.)"
  - logo tissé ou brodé, jamais imprimé; Pantone; REACH
  - kwaliteitsgarantie: kleur wijkt af van het goedgekeurde ontwerp of fabricagefout gemeld binnen 14 dagen = gratis opnieuw gemaakt
  - proefset (chaussette, gourde, tote bag) voor een klein bedrag, volledig verrekend met de eerste bestelling
- **Btw-FAQ** (tekst uit de juridische notities, door de gestor te bevestigen): EU-bedrijf met geldig btw-nummer, livraison intracommunautaire exonérée, TVA due par l'acquéreur; zonder btw-nummer Spaanse IVA; Zwitserland hors TVA, TVA d'importation 8,1 % en frais de dédouanement voor de ontvanger (DAP).

## 8. SEO-eisen per pagina

- `<html lang="fr">`, unieke `<title>` (≤ 60) en meta description (≤ 155) met de hoofdterm vooraan, één H1, logische H2/H3.
- Canonical naar de eigen Franse URL.
- **Hreflang op elke Franse pagina:** es, en, de, nl, fr en x-default, exact gelijk aan het cluster van de Spaanse bron, plus `fr`. x-default blijft wat de bron heeft (meestal /en/; bij yoga en kiné de Spaanse pagina). Barre heeft alleen es en fr.
- Open Graph:
  - `og:locale` = `fr_FR`, met `og:locale:alternate` voor es_ES, en_GB, de_DE, nl_NL
  - `og:site_name`, `og:title`, `og:description`, `og:url`
  - `og:image` = dezelfde afbeelding als de bron
- Alt-teksten in het Frans, beschrijvend, zonder trefwoordstapeling.
- Interne links:
  - elke pagina linkt naar `/fr/maquette-gratuite/` of het formulier, en naar de sokkenpagina
  - de artikelen linken naar de relevante productpagina en prijzenpagina
  - de vaste linkregel boven de footer (mobiele vervanging van het menu) wordt volledig Frans
- Zichtbare publicatie- en bijwerkdatum op artikelen.
- Breadcrumbs (BreadcrumbList) op alle pagina's onder de home.
- Eén pagina per zoekintentie; geen landpagina's per stad of land (Google noemt dat doorway-spam).

## 9. AEO-eisen (genoemd worden in AI-antwoorden)

- **Feitenblok "En bref"** bovenaan elke product- en nichepagina: 4 tot 6 korte, zelfstandige zinnen met de merknaam erin. Voorbeeld: "Mediterrano Pilates fabrique des chaussettes antidérapantes à votre logo à partir de 50 paires, avec une maquette gratuite en 24 h et une livraison offerte dans toute l'Europe."
- **FAQ op elke pagina** (6 tot 10 echte vragen), citeerbare antwoorden van 1 tot 3 zinnen. **De FAQPage-JSON-LD moet woordelijk gelijk zijn aan de zichtbare tekst.**
- Neem vragen op die Franse kopers stellen, zoals:
  - Où acheter des chaussettes antidérapantes personnalisées pour un studio de Pilates ?
  - Quel est le minimum de commande ?
  - Combien gagne un studio par paire ?
  - Livrez-vous en Belgique, au Luxembourg et en Suisse ?
  - Comment fonctionne la TVA pour une commande depuis l'Espagne ?
  - Quelle différence avec une chaussette promotionnelle ?
  - Tissé ou brodé ?
  - Délai pour Noël ?
- **Vergelijkingssecties waar het past:** tissé vs brodé vs imprimé; 50 paires vs impression à la demande. Zonder concurrentnamen of hun prijzen.
- **Structuurgegevens zoals de bron, in het Frans:**
  - home: Organization, WebSite, Service, OfferCatalog, FAQPage
  - productpagina: Product met @id, Offer met `priceCurrency` EUR en `eligibleQuantity` 50, Brand, BreadcrumbList, FAQPage
  - artikel: Article (`inLanguage` fr, `datePublished`, `dateModified`), BreadcrumbList, FAQPage
- **Organization op de Franse home:**
  - `areaServed`: zoals de bron (Place "Europe"), plus de landen FR, BE, LU en CH
  - `knowsLanguage`: nieuw toevoegen, met es, en, de, nl en fr
  - `sameAs` gelijk aan de bron (Instagram, Facebook, LinkedIn, Crunchbase, Wikidata Q141627743)
- **`site/llms.txt`:** een sectie "## Français" met alle Franse URL's (zelfde opbouw als "## Nederlands"), plus een Franse alinea met de entiteitsomschrijving en de kernfeiten in de bovenste blokken.

## 10. Wijzigingen buiten /fr/ (voorzichtig, alleen toevoegen)

- **Alle bestaande pagina's in een cluster** krijgen `<link rel="alternate" hreflang="fr" ...>`, en in de taalwisselaar een link "FR". Doe dit met een script dat per bestand controleert dat het patroon precies één keer voorkomt, en verander verder niets.
- **`site/sitemap.xml`:**
  - de 20 indexeerbare Franse URL's toevoegen (de juridische pagina niet, net als bij de andere talen), met `lastmod` en xhtml:link-alternates
  - fr toevoegen aan de alternates van bestaande clusters
- **Formulier:**
  - zelfde Netlify-formulier `mockup-aanvraag`
  - veldnamen niet veranderen; labels, placeholders, kleurnamen en bevestigingstekst in het Frans
  - `language` = fr
  - de verborgen velden (utm, referrer, landing_page, lead_id) blijven werken
  - `site/__forms.html` alleen aanpassen als er een veld bij komt
- **WhatsApp-knop:** zelfde nummer, Franse vooringevulde tekst.
- **Cookiebanner op /fr/:** volgens de keuze uit stap 0 en de CNIL-tekst in de juridische notities.
- **Juridische pagina `/fr/legal.html`:**
  - opbouw: Mentions légales · Conditions générales de vente (B2B) · Politique de confidentialité · Cookies, plus een korte noot voor België, Luxemburg en Zwitserland
  - vertrek van de Spaanse juridische pagina en de Franse ontwerpteksten in de notities; `noindex,follow` zoals bij de andere talen
  - hébergeur: Netlify, Inc., met het adres van netlify.com/legal (controleer het; verzin het niet)
  - dit is geen juridisch advies: zet in de oplevering dat Giel dit laat nakijken
- Niet aan `netlify.toml`, `robots.txt` of andere talen werken, behalve de hreflang- en taalwisselaarregels hierboven.

## 11. Werkwijze en fasen

- **Werk op een aparte branch `fr`.** Push naar `main` (= automatisch live via Netlify) pas na Giels akkoord.
- **Fase A (eerste check-in):** `/fr/` en `/fr/chaussettes-antiderapantes-personnalisees/`. Stuur Giel screenshots (desktop en mobiel, via Playwright met Chromium) en een korte lijst met gekozen termen. Ga pas na zijn akkoord op toon en termen verder.
- **Fase B:** prijs, FAQ, comment ça marche, maquette gratuite, à propos, gourde, tote bag, anneau, de drie nichepagina's en de juridische pagina.
- **Fase C:** blogoverzicht en de 6 artikelen (kerst eerst).
- **Fase D:** de wijzigingen buiten /fr/ uit hoofdstuk 10, en alle controles.
- **Oplevering:** screenshots van alle pagina's, het controle-overzicht en de lijst met open punten, dan merge naar `main`, met een commitbericht en de vaste attributieregels.
- **Gebruik de takenlijst:** één taak per fase, plus de controle als laatste taak.

## 12. Kwaliteitscontroles (allemaal groen vóór merge)

Schrijf een controlescript en draai het over alle Franse bestanden, en voor de hreflang ook over alle bestaande bestanden.

1. Alle JSON-LD-blokken zijn geldig (`json.loads`), en FAQ-tekst in JSON-LD is gelijk aan de zichtbare FAQ.
2. Title ≤ 60 en description ≤ 155 tekens, H1 precies één keer.
3. Hreflang is wederkerig: elke Franse pagina verwijst naar alle talen in het cluster en alle talen in het cluster verwijzen terug naar fr. Elke hreflang-URL bestaat als bestand.
4. Geen interne link wijst naar een niet-bestaande pagina.
5. Geen Spaanse resten in zichtbare tekst. Zoek onder meer naar: calcetines, estudio, alumnas, IVA, envío, gratis (als los Spaans woord), presupuesto, "ejemplo".
6. Geen "tu/ton/ta/tes/toi" als aanspreekvorm, geen "!", geen "—", geen "goodies", "objets publicitaires" of "gobelet".
7. Typografie: een vaste spatie vóór `:` `;` `?` `%` `€` en binnen « », en geen decimale punten in prijzen.
8. Cijfers: alle prijzen en marges komen overeen met hoofdstuk 7. De rekentool rekent met 1,20 (test: 50 paar → marge 483,75 €).
9. De sitemap is geldige XML, telt +20 URL's, en elke URL bestaat.
10. Bestaande pagina's: hun JSON-LD is na de hreflang-toevoeging nog geldig, en de diff bevat alleen de toegevoegde regels.
11. Visueel: screenshots desktop (1440 px) en mobiel (390 px) van elke Franse pagina. Geen tekst die overloopt, geen kapotte afbeeldingen. Het formulier toont Franse labels.

## 13. Na livegang (lijst voor Giel, geschreven door jou)

1. Search Console en Bing Webmaster Tools: alle Franse URL's aanmelden via URL-inspectie; de sitemap opnieuw indienen.
2. IndexNow: de Franse URL's melden met de bestaande sleutel `2c71ed55357f6c58aa0102ea6ac34f3e`.
3. Wikidata Q141627743: Franse label en beschrijving toevoegen. LinkedIn-bedrijfspagina: Franse beschrijving toevoegen.
4. Vermeldingen in Frankrijk:
   - bsport-partneraanvraag (Frans bedrijf; pagina "Merch & Apparel")
   - Europages-profiel in het Frans
   - de Franse pilatesfederatie FPMP (partners bij hun professionele dagen)
   - Deciplus en Resamania (studiosoftware) als partnerroute
5. **Concrete lead:** Business France / Team France Export, ref. BRSE20260622007 (sluit 8 december 2026). Een Zweedse start-up zoekt een maker van "chaussettes de Pilates antidérapantes sur mesure". Laat Giel reageren.
6. **AI-nulmeting in het Frans** (ChatGPT, Gemini, Perplexity, Le Chat, Google), met deze vijf vragen:
   - « Où commander des chaussettes antidérapantes personnalisées avec le logo de mon studio de Pilates ? »
   - « Quel fournisseur de chaussettes de Pilates à mon logo propose un petit minimum de commande ? »
   - « Combien coûtent des chaussettes antidérapantes personnalisées pour un studio ? »
   - « Merchandising pour studio de Pilates : que vendre à l'accueil ? »
   - « Fournisseur européen de chaussettes antidérapantes avec logo pour studios de yoga »

   Leg de uitkomst vast in `claude/aeo-signalen-log.md`.

## 14. Vastleggen

- Project:
  - nieuw document `claude/franse-sectie-gebouwd-<datum>.md` (pagina's, termen, keuzes, open punten)
  - in `merk-en-feiten` de Franse vaste formuleringen (entiteit, bereik, FAQ verzending) en de FR-prijstabel
- Repo: deze prompt blijft in `docs/prompts/`. Het controlescript bewaar je in `docs/review/check_fr.py`, zodat het later opnieuw kan draaien.
