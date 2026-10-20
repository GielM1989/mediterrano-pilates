#!/bin/bash
# Bouwt alle Franse pagina's opnieuw uit de woordenboeken en toont per pagina het rapport (samengevat).
cd "$(dirname "$0")/../../.."
B="python3 docs/review/fr/build_fr.py"
D=docs/review/fr
run() { # es-pad fr-slug dict
  echo "=== /fr/$2/"; $B site/$1/index.html site/fr/$2/index.html /fr/$2/ $D/$3 | grep -v '^geschreven' | grep -E 'onvertaald|Spaanse|JSON-LD|FAQ|streepjes|WAARSCHUWING|MISMATCH|^    \(' ; }
run calcetines-antideslizantes-personalizados chaussettes-antiderapantes-personnalisees dict_socks.json
run precios-y-margenes prix-et-marges dict_precios-y-margenes.json
run preguntas-frecuentes faq dict_preguntas-frecuentes.json
run como-funciona comment-ca-marche dict_como-funciona.json
run mockup-gratis maquette-gratuite dict_mockup-gratis.json
run sobre-mediterrano-pilates a-propos-de-mediterrano-pilates dict_sobre-mediterrano-pilates.json
run botellas-personalizadas-estudios-pilates gourde-isotherme-personnalisee dict_gourde-isotherme-personnalisee.json
run tote-bags-personalizadas-estudios-yoga tote-bag-personnalise dict_tote-bag-personnalise.json
run aro-de-pilates-personalizado anneau-de-pilates-personnalise dict_anneau-de-pilates-personnalise.json
run merchandising-estudios-yoga produits-personnalises-studios-yoga dict_produits-personnalises-studios-yoga.json
run merchandising-estudios-barre produits-personnalises-studios-barre dict_produits-personnalises-studios-barre.json
run merchandising-clinicas-fisioterapia produits-personnalises-cabinets-kinesitherapie dict_produits-personnalises-cabinets-kinesitherapie.json
# Fase C: blog
run blog blog dict_blog_blog-index.json
run blog/regalos-de-navidad-alumnas-pilates blog/cadeaux-de-noel-eleves-pilates dict_blog_regalos.json
run blog/aumentar-ingresos-estudio-pilates-sin-stock blog/augmenter-chiffre-affaires-studio-pilates-sans-stock dict_blog_aumentar.json
run blog/fidelizar-alumnas-pilates-productos-marca blog/fideliser-eleves-pilates-produits-a-votre-logo dict_blog_fidelizar.json
run blog/como-elegir-proveedor-calcetines-personalizados blog/choisir-fournisseur-chaussettes-antiderapantes-personnalisees dict_blog_elegir.json
run blog/cuanto-cuesta-personalizar-calcetines-antideslizantes blog/prix-chaussettes-antiderapantes-personnalisees dict_blog_cuanto.json
run blog/pack-de-bienvenida-alumnas-nuevas-pilates blog/kit-de-bienvenue-nouveaux-eleves-pilates dict_blog_pack.json
