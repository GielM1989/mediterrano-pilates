#!/usr/bin/env python3
"""Bouwt site/fr/legal.html: kop en CSS uit site/legal.html, Franse body met vijf ankers
(#mentions-legales, #confidentialite, #cgv, #contenu, #cookies)."""
import re, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
src = (root / "site/legal.html").read_text(encoding="utf-8")
css = re.search(r"<style>\n@font-face.*?</style>\n<style>.*?</style>", src, re.S).group(0)
css = css.replace("url('fonts/", "url('/fonts/")
css = css.replace("section ul{", "section table{width:100%;border-collapse:collapse;margin:0 0 14px;font-size:.92rem}\nsection th,section td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top;color:#3d453e}\nsection th{font-weight:700;color:var(--green)}\nsection ul{", 1)
css = css.replace("@media (max-width:640px){section{padding:26px 20px}}", "@media (max-width:640px){section{padding:26px 20px}section table{display:block;overflow-x:auto}}")

BASE = "https://mediterranopilates.com"
head = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mentions légales, confidentialité et CGV · Mediterrano</title>
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/images/favicon.svg">
<meta name="robots" content="noindex,follow">
<meta name="description" content="Mentions légales, politique de confidentialité, cookies et conditions générales de vente de Mediterrano Pilates, marque d'Ecomtierra Group SL (Espagne).">
<link rel="canonical" href="{BASE}/fr/legal.html">
<link rel="alternate" hreflang="es" href="{BASE}/legal.html">
<link rel="alternate" hreflang="en" href="{BASE}/en/legal.html">
<link rel="alternate" hreflang="de" href="{BASE}/de/legal.html">
<link rel="alternate" hreflang="nl" href="{BASE}/nl/legal.html">
<link rel="alternate" hreflang="fr" href="{BASE}/fr/legal.html">
<link rel="alternate" hreflang="x-default" href="{BASE}/en/legal.html">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="Mentions légales, confidentialité et CGV · Mediterrano">
<meta property="og:description" content="Mentions légales, politique de confidentialité, cookies et conditions générales de vente de Mediterrano Pilates.">
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
{css}
</head>
"""

M = "hola@mediterranopilates.com"
body = f"""<body>

<div class="topbar">
  <div class="wrap bar-row">
    <a class="brand" href="/fr/" aria-label="Mediterrano Pilates"><img src="/images/logo-mediterrano-light.svg" alt="Mediterrano Pilates" width="1000" height="377"></a>
    <a class="back" href="/fr/">← Retour au site</a>
  </div>
</div>

<div class="page">
  <div class="wrap">
    <h1>Informations légales</h1>
    <p class="lede">La transparence compte autant pour nous que la qualité de nos produits. Vous trouverez ici qui nous sommes, comment nous traitons vos données et dans quelles conditions nous travaillons.</p>

    <div class="toc">
      <a href="#mentions-legales">Mentions légales</a>
      <a href="#confidentialite">Politique de confidentialité</a>
      <a href="#cookies">Cookies</a>
      <a href="#cgv">Conditions générales de vente</a>
    </div>

    <!-- ================= MENTIONS LÉGALES ================= -->
    <section id="mentions-legales">
      <h2>Mentions légales</h2>
      <p class="sub">Informations fournies en application de l'article&nbsp;10 de la loi espagnole 34/2002 (LSSI-CE) et de l'article&nbsp;6 de la loi française pour la confiance dans l'économie numérique (LCEN)</p>
      <p>Ce site, <b>mediterranopilates.com</b>, est édité par&nbsp;:</p>
      <ul>
        <li><b>Raison sociale&nbsp;:</b> Ecomtierra Group SL (société à responsabilité limitée de droit espagnol, «&nbsp;S.L.&nbsp;»)</li>
        <li><b>Siège social&nbsp;:</b> Espagne</li>
        <li><b>Numéro d'identification fiscale (NIF)&nbsp;:</b> B24923328</li>
        <li><b>E-mail&nbsp;:</b> {M}</li>
      </ul>
      <p>Mediterrano Pilates est une marque d'Ecomtierra Group SL. Nous travaillons depuis l'Espagne et fournissons des produits personnalisés à des clients professionnels (studios de Pilates, de yoga, de barre et cabinets de kinésithérapie) en France, en Belgique, au Luxembourg, en Suisse et dans le reste de l'Europe.</p>
      <h3>Hébergement</h3>
      <p>Le site est hébergé par Netlify, Inc., 101 2nd Street, San Francisco, CA 94105, États-Unis (netlify.com).</p>
      <h3>Propriété intellectuelle</h3>
      <p>L'ensemble du contenu de ce site (textes, images, nom commercial, logos) appartient à Ecomtierra Group SL ou est utilisé avec l'autorisation de ses titulaires. Il ne peut être reproduit sans accord écrit préalable.</p>
    </section>

    <!-- ================= CONFIDENTIALITÉ ================= -->
    <section id="confidentialite">
      <h2>Politique de confidentialité</h2>
      <p class="sub">Conformément au Règlement général sur la protection des données (RGPD, UE 2016/679) et à la loi espagnole LOPDGDD</p>

      <h3>Qui est responsable du traitement&nbsp;?</h3>
      <p>Ecomtierra Group SL (Mediterrano Pilates), joignable à l'adresse {M}.</p>

      <h3>Quelles données collectons-nous, et pourquoi&nbsp;?</h3>
      <p>Via notre formulaire de demande, nous collectons votre nom, votre adresse e-mail, le nom de votre studio, les produits qui vous intéressent, votre message, le logo que vous téléversez et, si vous le souhaitez, votre compte Instagram et votre numéro de téléphone. Nous utilisons ces données uniquement pour&nbsp;:</p>
      <ul>
        <li>répondre à votre demande et vous envoyer une maquette et un devis&nbsp;;</li>
        <li>rester en contact avec vous au sujet d'une éventuelle collaboration&nbsp;;</li>
        <li>établir les devis, les commandes et les factures, et respecter nos obligations comptables et fiscales si une commande est passée.</li>
      </ul>
      <p>Les bases juridiques sont les mesures précontractuelles prises à votre demande (art.&nbsp;6.1.b du RGPD), l'exécution du contrat et nos obligations légales (art.&nbsp;6.1.b et 6.1.c), ainsi que notre intérêt légitime à répondre à des demandes professionnelles (art.&nbsp;6.1.f). La mesure d'audience et la mesure publicitaire reposent uniquement sur votre consentement (art.&nbsp;6.1.a). Nous n'envoyons pas de lettre d'information sans votre accord et nous ne vendons jamais vos données.</p>

      <h3>Combien de temps conservons-nous vos données&nbsp;?</h3>
      <p>Le temps nécessaire pour traiter votre demande. Si une collaboration s'engage, nous les conservons pendant la durée de la relation commerciale, puis pendant les délais légaux de conservation comptable et fiscale applicables en Espagne.</p>

      <h3>Quels prestataires interviennent dans le traitement&nbsp;?</h3>
      <p>Notre site et son formulaire sont hébergés par Netlify, Inc. (hébergement et réception des formulaires, États-Unis). Si vous acceptez les cookies, nous utilisons en outre le pixel Meta (Meta Platforms Ireland Ltd.) pour mesurer les résultats de nos annonces sur Facebook et Instagram, et Google Analytics 4 (Google Ireland Ltd.) pour comprendre, de façon agrégée, comment le site est utilisé. Meta et Google peuvent traiter des données telles que votre adresse IP, des identifiants de votre navigateur et les pages que vous consultez.</p>

      <h3>Transferts hors de la Commission européenne</h3>
      <p>Certains de ces prestataires sont établis aux États-Unis. Les transferts reposent sur la décision d'adéquation de la Commission européenne relative au cadre de protection des données UE-États-Unis (Data Privacy Framework, 10&nbsp;juillet 2023) pour les destinataires certifiés ou, à défaut, sur les clauses contractuelles types de la Commission européenne. Pour plus d'informations, consultez les politiques de confidentialité de Netlify, de Meta et de Google.</p>

      <h3>Vos droits</h3>
      <p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données, ainsi que du droit de retirer votre consentement à tout moment. Écrivez-nous à {M}&nbsp;: nous répondons dans un délai d'un mois.</p>

      <h3>Réclamation auprès d'une autorité de contrôle</h3>
      <p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une réclamation auprès de l'autorité de contrôle de votre choix, notamment l'Agencia Española de Protección de Datos (AEPD, aepd.es), dont relève Ecomtierra Group SL, ou l'autorité de votre pays&nbsp;: en France, la CNIL (cnil.fr)&nbsp;; en Belgique, l'Autorité de protection des données (autoriteprotectiondonnees.be)&nbsp;; au Luxembourg, la CNPD (cnpd.lu)&nbsp;; en Suisse, le Préposé fédéral à la protection des données et à la transparence (PFPDT, edoeb.admin.ch).</p>
    </section>

    <!-- ================= COOKIES ================= -->
    <section id="cookies">
      <h2>Cookies</h2>
      <p class="sub">Conformément à l'article&nbsp;82 de la loi française Informatique et Libertés et aux recommandations de la CNIL</p>
      <p>Ce site utilise des cookies et traceurs strictement nécessaires à son fonctionnement, qui ne demandent pas de consentement. Les cookies de mesure d'audience et de publicité ne sont déposés qu'avec votre consentement.</p>
      <table>
        <thead><tr><th>Finalité</th><th>Outil</th><th>Consentement</th></tr></thead>
        <tbody>
          <tr><td>Fonctionnement du site et mémorisation de votre choix</td><td>Stockage local de votre navigateur (clés mp_cookie_consent et mp_cookie_consent_ts)</td><td>Non requis</td></tr>
          <tr><td>Mesure d'audience</td><td>Google Analytics 4 (Google Ireland Ltd.)</td><td>Requis</td></tr>
          <tr><td>Mesure de nos annonces</td><td>pixel Meta (Meta Platforms Ireland Ltd.)</td><td>Requis</td></tr>
        </tbody>
      </table>
      <p>À votre première visite, un bandeau vous propose «&nbsp;Tout accepter&nbsp;» ou «&nbsp;Tout refuser&nbsp;», avec la même visibilité. Tant que vous n'avez pas choisi, aucun outil de mesure n'est chargé. Le site fonctionne de la même façon dans les deux cas.</p>
      <p>Nous conservons votre choix pendant 6&nbsp;mois dans votre navigateur, puis nous vous redemandons votre choix. Vous pouvez le modifier à tout moment avec le lien «&nbsp;Gestion des cookies&nbsp;» en bas de chaque page, en supprimant les données de ce site dans votre navigateur ou en nous écrivant à {M}.</p>
    </section>

    <!-- ================= CGV ================= -->
    <section id="cgv">
      <h2>Conditions générales de vente</h2>
      <p class="sub">Applicables à tous les devis et à toutes les livraisons aux clients professionnels</p>

      <h3>1. Champ d'application</h3>
      <p>Les présentes conditions s'appliquent à toutes les offres, maquettes, devis et contrats conclus entre Ecomtierra Group SL (Mediterrano Pilates) et des clients professionnels, tels que les studios de Pilates et de yoga. Nos produits et nos prix s'adressent aux entreprises et ne s'appliquent pas aux consommateurs. Sauf mention contraire, les prix indiqués s'entendent hors TVA.</p>

      <h3>2. Maquettes et devis</h3>
      <p>Les maquettes et les devis sont gratuits et sans engagement. La commande n'est ferme qu'après votre validation écrite (par e-mail) du visuel définitif et la confirmation de la commande.</p>

      <h3>3. Personnalisation et validation</h3>
      <p>Tous les produits sont fabriqués spécialement pour votre studio, avec votre logo et vos couleurs. En validant la maquette, vous acceptez le visuel, les couleurs et les spécifications. De légères différences de couleur peuvent exister entre l'écran et le produit fini. Dans une tolérance raisonnable, elles ne constituent pas un défaut&nbsp;; la correspondance Pantone permet de les réduire au minimum.</p>

      <h3>4. Prix, TVA et frais de douane</h3>
      <p>Les prix sont indiqués en euros, hors TVA. Pour les professionnels établis dans l'Union européenne et disposant d'un numéro de TVA intracommunautaire valide, la facture est établie hors TVA&nbsp;: la livraison est exonérée en Espagne et la TVA est autoliquidée par l'acheteur dans son pays. Sans numéro de TVA valide, la TVA espagnole (21&nbsp;%) est appliquée.</p>
      <p>Pour la Suisse, la facture est établie hors TVA. À l'importation, la TVA suisse et les éventuels frais de dédouanement sont à la charge du destinataire, sauf accord contraire indiqué dans le devis.</p>

      <h3>5. Pas de droit de rétractation pour les produits personnalisés</h3>
      <p><span class="hl">Les produits personnalisés ne sont ni repris ni échangés.</span> Chaque produit étant fabriqué selon vos spécifications et à votre logo, il ne peut être revendu à un tiers. Nos ventes sont par ailleurs conclues entre professionnels, auxquelles le droit de rétractation du consommateur ne s'applique pas.</p>

      <h3>6. Qualité et défauts</h3>
      <p>L'absence de droit de rétractation n'exclut pas la garantie. Vous recevez un produit présentant un défaut de fabrication, ou la livraison ne correspond pas à la maquette validée&nbsp;? Signalez-le-nous dans un délai de 14&nbsp;jours à compter de la livraison, photos à l'appui, à {M}. Nous y remédierons par un remplacement, une nouvelle livraison ou une compensation appropriée.</p>

      <h3>7. Livraison</h3>
      <p>Le délai de livraison indicatif est d'environ 4&nbsp;semaines après la validation de la maquette et le paiement. La livraison est gratuite dans toute l'Europe. Les délais sont donnés à titre indicatif&nbsp;; les retards indépendants de notre volonté (douane, transport) n'ouvrent droit ni à annulation ni à indemnisation, mais nous vous informons en temps utile. Les éventuels droits de douane et taxes à l'importation dans le pays de destination sont à la charge du client.</p>

      <h3>8. Paiement</h3>
      <p>Les conditions de paiement sont convenues à chaque commande et indiquées sur la facture. Pour les premières commandes, un paiement anticipé, total ou partiel, peut être demandé avant le début de la production. Tout retard de paiement entraîne de plein droit, sans mise en demeure préalable, des intérêts de retard au taux prévu par la loi espagnole 3/2004 ainsi qu'une indemnité forfaitaire de 40&nbsp;€ pour frais de recouvrement, conformément à la directive 2011/7/UE.</p>

      <h3>9. Responsabilité</h3>
      <p>Notre responsabilité est limitée au montant facturé de la commande concernée. Nous ne sommes pas responsables des dommages indirects, dans les limites permises par la loi,, tels que la perte de revenus ou de bénéfices.</p>

      <h3>10. Propriété intellectuelle</h3>
      <p>Vous garantissez détenir les droits d'utilisation du logo et des éléments de marque que vous nous fournissez. Votre logo reste votre propriété&nbsp;; nous l'utilisons exclusivement pour vos produits et, avec votre seul accord, comme référence dans notre portfolio.</p>

      <h3>11. Droit applicable et juridiction</h3>
      <p>Le droit espagnol s'applique à tous les contrats, sans préjudice des dispositions impératives en vigueur dans le pays du client. Tout litige qui ne peut être réglé à l'amiable relève des juridictions espagnoles.</p>

      <h3 id="contenu">12. Contenu informatif du site</h3>
      <p>Les informations publiées sur ce site (y compris le blog, les pages produits et les pages par secteur) ont un caractère général et informatif. Elles ne constituent pas un conseil juridique, fiscal, médical ou professionnel d'aucune sorte et ne remplacent pas l'avis de votre ordre professionnel, de votre fédération ou de votre conseiller. Lorsque nous évoquons une réglementation, nous le faisons selon notre propre lecture à la date de publication&nbsp;; elle peut évoluer et différer dans votre pays. Avant toute décision fondée sur ce contenu, confirmez-la auprès d'un professionnel qualifié. Ecomtierra Group SL décline toute responsabilité pour les décisions prises uniquement sur la base des informations de ce site.</p>

      <h3>13. Langues</h3>
      <p>Les présentes conditions sont disponibles en français, en espagnol, en anglais, en allemand et en néerlandais. En cas de divergence, la version espagnole fait foi.</p>

      <p class="note">Dernière mise à jour&nbsp;: octobre 2026. Une question sur ces conditions&nbsp;? Écrivez-nous à {M}.</p>
    </section>

    <footer>
      <p>Mediterrano Pilates · Une marque d'Ecomtierra Group SL · <a href="/fr/">mediterranopilates.com</a></p>
    </footer>
  </div>
</div>

</body>
</html>
"""
out = root / "site/fr/legal.html"
out.write_text(head + body, encoding="utf-8")
print("geschreven", out)
