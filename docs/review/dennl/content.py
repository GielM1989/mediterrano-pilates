# Let op: geen promotiesok-vraag (klantbesluit 04-11-2026: bewust weggelaten).
# Inhoud voor de AEO-upgrade van /de/ en /nl/ (04-11-2026).
# Alle cijfers komen van de bestaande pagina's en de kassabon (inkoop 6,95 EUR sokken, adviesprijs 19,95 EUR).
# Zichtbare tekst gebruikt &nbsp; voor EUR en %; de JSON-LD krijgt automatisch gewone spaties.

NB = "&nbsp;"

# ---------- Duits ----------
DE_SHIP_Q_STUDIO = "Versendet ihr auch außerhalb Spaniens?"
DE_SHIP_Q_NICHE = "Liefert ihr auch außerhalb Spaniens?"
DE_SHIP_A_STUDIO = ("Ja. Wir arbeiten vor allem mit Studios in Spanien und ganz Europa, und der Versand in ganz Europa "
                    "ist kostenlos, auch nach Deutschland, Österreich und in die Schweiz. Außerhalb Europas liefern wir "
                    "auf Anfrage. Bei Lieferungen außerhalb der EU, etwa in die Schweiz, nach Großbritannien oder "
                    "Norwegen, trägt der Empfänger immer die Einfuhrumsatzsteuer, Zölle und Verzollungskosten.")
DE_SHIP_A_NICHE = DE_SHIP_A_STUDIO.replace("mit Studios in Spanien", "mit Studios und Praxen in Spanien")

DE_SAMPLES = ("Kann ich die Qualität vor der Bestellung sehen?",
              "Ja. Wir schicken dir ein Muster-Set (Socke, Tumbler und Tote Bag) gegen eine kleine Gebühr, die bei "
              "deiner ersten Bestellung vollständig verrechnet wird, sodass die Muster kostenlos sind, wenn du bestellst.")
DE_PROMO = ("Worin unterscheidet sich das von einer günstigen Werbesocke?",
            "Eine Werbesocke ist ein bedruckter Werbeartikel. Unsere ist eine echte Stoppersocke für die Stunde: "
            "Grip-Sohle aus PVC oder Silikon, Mid-Rise-Schnitt, Material nach REACH geprüft und dein Logo eingewebt "
            "oder aufgestickt, nie aufgedruckt. Deine Kundinnen tragen sie in jeder Stunde und genau deshalb kaufen "
            "sie sie.")

DE_SHIP_BULLET = ("Gratisversand in ganz Europa, auch nach Deutschland, Österreich und in die Schweiz. Außerhalb der "
                  "EU, etwa in der Schweiz, trägt der Empfänger immer Einfuhrumsatzsteuer, Zölle und "
                  "Verzollungskosten. Mediterrano Pilates ist eine Marke der Ecomtierra Group SL (Spanien).")
DE_MOCKUP_BULLET = ("Kostenloses Mockup in 24 Stunden, unverbindlich. Die Lieferung erfolgt rund 4 Wochen nach Freigabe "
                    "des Angebots.")


def de_product(name_sentence, logo_sentence, qty_price_sentence):
    return ("Kurz gesagt", [name_sentence, logo_sentence, qty_price_sentence, DE_MOCKUP_BULLET, DE_SHIP_BULLET])


# ---------- Nederlands ----------
NL_SAMPLES = ("Kan ik de kwaliteit zien voordat ik bestel?",
              "Ja. We sturen je een sampleset (sok, tumbler en tote bag) voor een klein bedrag, dat we volledig "
              "verrekenen met je eerste bestelling. Bestel je daarna, dan zijn de samples dus gratis.")
NL_PROMO = ("Wat is het verschil met een goedkope promotiesok?",
            "Een promotiesok is een bedrukt reclameartikel. Onze sok is een echte antislipsok voor de les: een "
            "antislipzool van PVC of siliconen, een middelhoge schacht, materiaal getest volgens REACH en je logo "
            "in de sok geweven of geborduurd, nooit bedrukt. Je leden dragen hem in elke les, en daarom kopen ze hem.")
NL_SHIP_BULLET = ("Gratis verzending binnen heel Europa, ook naar Nederland, België en Luxemburg. Mediterrano Pilates "
                  "is een merk van Ecomtierra Group SL (Spanje).")
NL_MOCKUP_BULLET = ("Gratis mockup binnen 24 uur, vrijblijvend. De levering volgt ongeveer 4 weken nadat je de offerte "
                    "hebt goedgekeurd.")


def nl_product(name_sentence, logo_sentence, qty_price_sentence):
    return ("In het kort", [name_sentence, logo_sentence, qty_price_sentence, NL_MOCKUP_BULLET, NL_SHIP_BULLET])


PAGES = {
    # ===================== DUITS =====================
    "de/stoppersocken-mit-logo": {
        "replace": [
            ("<title>Pilates-Socken mit Logo: Grip-Socken für dein Studio</title>",
             "<title>Stoppersocken mit Logo ab 50 Paar | Mediterrano Pilates</title>"),
            ("<h1>Pilates-Socken mit <span class=\"fx\">dem Logo deines Studios.</span></h1>",
             "<h1>Stoppersocken mit <span class=\"fx\">dem Logo deines Studios.</span></h1>"),
            ("<h2>Das Produkt, mit dem die meisten Studios starten.</h2>",
             "<h2>Das einfachste Produkt für den Start.</h2>"),
        ],
        "block": de_product(
            "Mediterrano Pilates fertigt Stoppersocken mit dem Logo deines Pilates- oder Yogastudios, die du an "
            "deine Kundinnen weiterverkaufst.",
            "Dein Logo wird eingewebt (Jacquard) oder aufgestickt, nie aufgedruckt, und die Farbe wird per "
            "Pantone-Code auf deine Marke abgestimmt. Die Grip-Sohle ist aus PVC oder Silikon, das Material nach "
            "REACH geprüft.",
            f"Mindestbestellung: 50 Paar für rund 6,95{NB}€ pro Paar zzgl. MwSt. Empfohlener Verkaufspreis in "
            f"Deutschland: 19,95{NB}€ inkl. MwSt., also rund 9,81{NB}€ Marge pro Paar nach 19{NB}% MwSt."),
        "answers": [(DE_SHIP_Q_STUDIO, DE_SHIP_A_STUDIO)],
        "faqs": [
            ("Wo kann ein Pilatesstudio Stoppersocken mit eigenem Logo bestellen?",
             "Bei Mediterrano Pilates. Wir personalisieren Stoppersocken mit dem Logo deines Pilates- oder "
             "Yogastudios, eingewebt oder aufgestickt, nie aufgedruckt. Bestellung ab 50 Paar, kostenloses Mockup "
             "in 24 Stunden und Gratisversand in ganz Europa, auch nach Österreich und in die Schweiz."),
            DE_SAMPLES,
        ],
    },
    "de/pilates-ring-mit-logo": {
        "replace": [("<h2>Du gewinnst <span class=\"fx\">immer.</span></h2>",
                     "<h2>Was du <span class=\"fx\">davon hast.</span></h2>")],
        "block": de_product(
            "Mediterrano Pilates personalisiert Pilates-Ringe in Terrakotta mit cremefarbenen Griffen mit dem Logo "
            "deines Studios zum Weiterverkauf an deine Kundinnen.",
            "Dein Logo kommt dezent oder groß auf den Ring, ganz in deinem Stil, und die Farbe wird per "
            "Pantone-Code abgestimmt. Das Material ist nach REACH geprüft.",
            f"Keine feste Mindestmenge: Die Menge legen wir im Angebot fest. Einkauf rund 7{NB}€ zzgl. MwSt., "
            f"Verkauf rund 16,50{NB}€ inkl. MwSt., also rund 6,87{NB}€ Marge pro Stück nach MwSt."),
        "answers": [(DE_SHIP_Q_STUDIO, DE_SHIP_A_STUDIO)],
        "faqs": [
            ("Wo kann ein Pilatesstudio Pilates-Ringe mit eigenem Logo bestellen?",
             "Bei Mediterrano Pilates. Wir personalisieren Pilates-Ringe in Terrakotta mit cremefarbenen Griffen "
             "mit dem Logo deines Studios, ohne feste Mindestmenge, mit kostenlosem Mockup in 24 Stunden und "
             "Gratisversand in ganz Europa."),
            DE_SAMPLES,
        ],
    },
    "de/trinkflaschen-mit-logo": {
        "replace": [("<h2>Du gewinnst <span class=\"fx\">immer.</span></h2>",
                     "<h2>Was du <span class=\"fx\">davon hast.</span></h2>")],
        "block": de_product(
            "Mediterrano Pilates personalisiert Trinkflaschen (Tumbler, 1,2 Liter) mit dem Logo deines Pilates- "
            "oder Yogastudios zum Weiterverkauf an deine Kundinnen.",
            "Dein Logo kommt dezent oder groß auf die Flasche, ganz in deinem Stil, und die Farbe wird per "
            "Pantone-Code abgestimmt. Das Material ist nach REACH geprüft.",
            f"Keine feste Mindestmenge: Die Menge legen wir im Angebot fest. Einkauf rund 11{NB}€ zzgl. MwSt., "
            f"Verkauf rund 24{NB}€ inkl. MwSt., also rund 9,17{NB}€ Marge pro Stück nach MwSt."),
        "answers": [(DE_SHIP_Q_STUDIO, DE_SHIP_A_STUDIO)],
        "faqs": [
            ("Wo kann ein Studio Trinkflaschen mit eigenem Logo bestellen?",
             "Bei Mediterrano Pilates. Wir personalisieren Tumbler mit 1,2 Liter Inhalt mit dem Logo deines "
             "Pilates- oder Yogastudios, ohne feste Mindestmenge, mit kostenlosem Mockup in 24 Stunden und "
             "Gratisversand in ganz Europa."),
        ],
    },
    "de/stofftaschen-mit-logo": {
        "replace": [("<h2>Du gewinnst <span class=\"fx\">immer.</span></h2>",
                     "<h2>Was du <span class=\"fx\">davon hast.</span></h2>")],
        "block": de_product(
            "Mediterrano Pilates personalisiert Tote Bags aus Baumwolle mit dem Logo deines Pilates- oder "
            "Yogastudios zum Weiterverkauf an deine Kundinnen.",
            "Dein Logo kommt dezent oder groß auf die Tasche, ganz in deinem Stil, und die Farbe wird per "
            "Pantone-Code abgestimmt. Das Material ist nach REACH geprüft.",
            f"Mindestbestellung: 50 Stück, wie bei den Socken. Einkauf rund 6,50{NB}€ zzgl. MwSt., Verkauf rund "
            f"15{NB}€ inkl. MwSt., also rund 6,11{NB}€ Marge pro Stück nach MwSt."),
        "answers": [(DE_SHIP_Q_STUDIO, DE_SHIP_A_STUDIO)],
        "faqs": [
            ("Wo kann ein Studio Tote Bags mit eigenem Logo bestellen?",
             "Bei Mediterrano Pilates. Wir personalisieren Tote Bags aus Baumwolle mit dem Logo deines Pilates- "
             "oder Yogastudios, ab 50 Stück, mit kostenlosem Mockup in 24 Stunden und Gratisversand in ganz "
             "Europa."),
        ],
    },
    "de/merchandise-fuer-yogastudios": {
        # heeft al een feitenblok ("Auf einen Blick"); alleen vragen en verzendantwoord
        "answers": [(DE_SHIP_Q_NICHE, DE_SHIP_A_NICHE)],
        "faqs": [DE_SAMPLES],
    },
    "de/merchandising-fuer-physiotherapie-praxen": {
        "block": ("Kurz gesagt", [
            "Mediterrano Pilates personalisiert Stoppersocken, Tumbler und Tote Bags mit dem Logo deiner "
            "Physiotherapie-Praxis zum Verkauf an der Rezeption.",
            "Auf den Socken wird das Logo eingewebt oder aufgestickt, nie aufgedruckt; die Grip-Sohle ist aus PVC "
            "oder Silikon, das Material nach REACH geprüft.",
            f"Mindestbestellung: 50 Paar Socken für rund 6,95{NB}€ pro Paar zzgl. MwSt. Empfohlener "
            f"Verkaufspreis: 19,95{NB}€ inkl. MwSt., also rund 9,81{NB}€ Marge pro Paar nach 19{NB}% MwSt.",
            "Die Socke wird als Ausrüstung für das Training verkauft, ohne Versprechen zur Gesundheit.",
            DE_MOCKUP_BULLET,
            DE_SHIP_BULLET,
        ]),
        "answers": [(DE_SHIP_Q_NICHE, DE_SHIP_A_NICHE)],
        "faqs": [DE_SAMPLES],
    },

    # ===================== NEDERLANDS =====================
    "nl/antislipsokken-met-logo": {
        "replace": [("<h2>Het product waar de meeste studio's mee beginnen.</h2>",
                     "<h2>Het makkelijkste product om mee te beginnen.</h2>")],
        "block": nl_product(
            "Mediterrano Pilates maakt antislipsokken met het logo van je pilates- of yogastudio, die je aan je "
            "leden doorverkoopt.",
            "Je logo wordt in de sok geweven (jacquard) of geborduurd, nooit bedrukt, en de kleur stemmen we af op "
            "de Pantone-code van je merk. De antislipzool is van PVC of siliconen, het materiaal getest volgens "
            "REACH.",
            f"Minimale bestelling: 50 paar, voor ongeveer € 6,95 per paar exclusief btw. Adviesverkoopprijs in "
            f"Nederland: € 19,95 inclusief btw, dus ongeveer € 9,54 marge per paar na 21% btw."),
        "faqs": [
            ("Waar kan een pilatesstudio antislipsokken met eigen logo bestellen?",
             "Bij Mediterrano Pilates. We personaliseren antislipsokken met het logo van je pilates- of yogastudio, "
             "geweven of geborduurd, nooit bedrukt. Bestellen kan vanaf 50 paar, met een gratis mockup binnen 24 "
             "uur en gratis verzending binnen heel Europa, ook naar België."),
            NL_SAMPLES,
        ],
    },
    "nl/pilatesring-met-logo": {
        "replace": [("<h2>Waarom een pilatesring met logo <span class=\"fx\">altijd loont.</span></h2>",
                     "<h2>Wat een pilatesring met logo <span class=\"fx\">je oplevert.</span></h2>")],
        "block": nl_product(
            "Mediterrano Pilates zet het logo van je studio op pilatesringen in terracotta met crèmekleurige "
            "handgrepen, om aan je leden door te verkopen.",
            "Je logo komt subtiel of groot op de ring, helemaal in jouw stijl, en de kleur stemmen we af op je "
            "Pantone-code. Het materiaal is getest volgens REACH.",
            "Geen vast minimum: het aantal leggen we vast in de offerte. Inkoop ongeveer € 7 exclusief btw, "
            "verkoop ongeveer € 16,50 inclusief btw, dus ongeveer € 6,64 marge per stuk na btw."),
        "faqs": [
            ("Waar kan een pilatesstudio pilatesringen met eigen logo bestellen?",
             "Bij Mediterrano Pilates. We zetten het logo van je studio op pilatesringen in terracotta met "
             "crèmekleurige handgrepen, zonder vast minimum, met een gratis mockup binnen 24 uur en gratis "
             "verzending binnen heel Europa."),
            NL_SAMPLES,
        ],
    },
    "nl/tumblers-met-logo": {
        "replace": [("<h2>Waarom een tumbler met logo <span class=\"fx\">altijd loont.</span></h2>",
                     "<h2>Wat een tumbler met logo <span class=\"fx\">je oplevert.</span></h2>")],
        "block": nl_product(
            "Mediterrano Pilates personaliseert tumblers (drinkflessen van 1,2 liter) met het logo van je pilates- "
            "of yogastudio, om aan je leden door te verkopen.",
            "Je logo komt subtiel of groot op de fles, helemaal in jouw stijl, en de kleur stemmen we af op je "
            "Pantone-code. Het materiaal is getest volgens REACH.",
            "Geen vast minimum: het aantal leggen we vast in de offerte. Inkoop ongeveer € 11 exclusief btw, "
            "verkoop ongeveer € 24 inclusief btw, dus ongeveer € 8,83 marge per stuk na btw."),
        "faqs": [
            ("Waar kan een studio drinkflessen met eigen logo bestellen?",
             "Bij Mediterrano Pilates. We personaliseren tumblers van 1,2 liter met het logo van je pilates- of "
             "yogastudio, zonder vast minimum, met een gratis mockup binnen 24 uur en gratis verzending binnen heel "
             "Europa."),
        ],
    },
    "nl/tote-bags-met-logo": {
        "replace": [("<h2>Waarom een tote bag met logo <span class=\"fx\">altijd loont.</span></h2>",
                     "<h2>Wat een tote bag met logo <span class=\"fx\">je oplevert.</span></h2>")],
        "block": nl_product(
            "Mediterrano Pilates personaliseert katoenen tote bags met het logo van je pilates- of yogastudio, om "
            "aan je leden door te verkopen.",
            "Je logo komt subtiel of groot op de tas, helemaal in jouw stijl, en de kleur stemmen we af op je "
            "Pantone-code. Het materiaal is getest volgens REACH.",
            "Minimale bestelling: 50 stuks, net als bij de sokken. Inkoop ongeveer € 6,50 exclusief btw, verkoop "
            "ongeveer € 15 inclusief btw, dus ongeveer € 5,90 marge per stuk na btw."),
        "faqs": [
            ("Waar kan een studio tote bags met eigen logo bestellen?",
             "Bij Mediterrano Pilates. We personaliseren katoenen tote bags met het logo van je pilates- of "
             "yogastudio, vanaf 50 stuks, met een gratis mockup binnen 24 uur en gratis verzending binnen heel "
             "Europa."),
        ],
    },
    "nl/merchandise-voor-yogastudios": {
        "faqs": [NL_SAMPLES],
    },
    "nl/merchandise-voor-fysiotherapiepraktijken": {
        "block": ("In het kort", [
            "Mediterrano Pilates personaliseert antislipsokken, tumblers en tote bags met het logo van je "
            "fysiotherapiepraktijk, om aan de balie te verkopen.",
            "Op de sokken wordt het logo geweven of geborduurd, nooit bedrukt; de antislipzool is van PVC of "
            "siliconen, het materiaal getest volgens REACH.",
            "Minimale bestelling: 50 paar sokken, voor ongeveer € 6,95 per paar exclusief btw. Adviesverkoopprijs: "
            "€ 19,95 inclusief btw, dus ongeveer € 9,54 marge per paar na 21% btw.",
            "Je verkoopt de sok als trainingsmateriaal, zonder beloftes over gezondheid.",
            NL_MOCKUP_BULLET,
            NL_SHIP_BULLET,
        ]),
        "faqs": [NL_SAMPLES],
    },
}

DE_ENTITY = ("Wo kann ein Pilatesstudio Stoppersocken mit eigenem Logo bestellen?",
             "Bei Mediterrano Pilates. Wir personalisieren Stoppersocken mit dem Logo deines Pilates- oder "
             "Yogastudios, eingewebt oder aufgestickt, nie aufgedruckt. Bestellung ab 50 Paar, kostenloses Mockup "
             "in 24 Stunden und Gratisversand in ganz Europa, auch nach Österreich und in die Schweiz.")
NL_ENTITY = ("Waar kan een pilatesstudio antislipsokken met eigen logo bestellen?",
             "Bij Mediterrano Pilates. We personaliseren antislipsokken met het logo van je pilates- of yogastudio, "
             "geweven of geborduurd, nooit bedrukt. Bestellen kan vanaf 50 paar, met een gratis mockup binnen 24 "
             "uur en gratis verzending binnen heel Europa, ook naar België.")

PAGES.update({
    "de/faq": {"faqs": [DE_ENTITY]},
    "de/preise-und-margen": {"faqs": [DE_SAMPLES]},
    "de/kostenloses-mockup": {"faqs": [DE_SAMPLES]},
    "de/ueber-mediterrano-pilates": {"faqs": [DE_ENTITY]},
    "nl/veelgestelde-vragen": {"faqs": [NL_ENTITY]},
    "nl/prijzen-en-marges": {"faqs": [NL_SAMPLES]},
    "nl/gratis-mockup": {"faqs": [NL_SAMPLES]},
    "nl/over-mediterrano-pilates": {"faqs": [NL_ENTITY]},
})
