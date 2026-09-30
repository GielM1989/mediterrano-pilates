# -*- coding: utf-8 -*-
"""Bouwt /merchandising-estudios-barre/ op basis van het sokken-template (ES)."""
import re, os, io

GOLIVE = '/home/claude/golive'
SRC = f'{GOLIVE}/calcetines-antideslizantes-personalizados/index.html'
OUT_DIR = f'{GOLIVE}/merchandising-estudios-barre'
URL = 'https://mediterranopilates.com/merchandising-estudios-barre/'

src = io.open(SRC, encoding='utf-8').read()

TITLE = 'Calcetines antideslizantes con logo para barre fitness'
DESC = ('Calcetines antideslizantes con el logo de tu estudio de barre fitness. '
        'Desde 50 pares, mockup gratis en 24 h y envío gratis a cualquier país.')
assert len(TITLE) <= 60, len(TITLE)
assert len(DESC) <= 155, len(DESC)

HEAD = f'''<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="Merchandising para estudios de barre · Mediterrano Pilates">
<meta property="og:type" content="website">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://mediterranopilates.com/images/product-sokken.jpg">
<meta property="og:image:width" content="900">
<meta property="og:image:height" content="1200">
<meta property="og:image:alt" content="Calcetines antideslizantes terracota con logo de estudio">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://mediterranopilates.com/images/product-sokken.jpg">
<link rel="canonical" href="{URL}">
<link rel="alternate" hreflang="es" href="{URL}">
<link rel="alternate" hreflang="x-default" href="{URL}">
<meta property="og:description" content="{DESC}">
<meta property="og:locale" content="es_ES">
<link rel="icon" href="/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/images/favicon.svg">
<script>window.MP_PIXEL_ID = '1591577842375803';</script>
<script>window.MP_GA_ID = 'G-Q9SY1F5KKF';</script>
<script>window.MP_WHATSAPP = '31657408010';</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"Mediterrano Pilates","item":"https://mediterranopilates.com/"}},
    {{"@type":"ListItem","position":2,"name":"Merchandising para estudios de barre","item":"{URL}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "{URL}#service",
  "name": "Merchandising personalizado para estudios de barre fitness",
  "serviceType": "Merchandising personalizado con logo para estudios de barre",
  "description": "Mediterrano Pilates personaliza calcetines antideslizantes, tumblers, tote bags y aros de pilates con el logo de estudios de barre fitness, para que el estudio los venda a sus alumnas. Logo tejido o bordado, color igualado por Pantone, pedido mínimo de 50 pares de calcetines, mockup gratis en 24 horas y envío gratuito a todo el mundo.",
  "url": "{URL}",
  "image": "https://mediterranopilates.com/images/product-sokken.jpg",
  "provider": {{"@id": "https://mediterranopilates.com/#organization"}},
  "brand": {{"@type":"Brand","name":"Mediterrano Pilates"}},
  "audience": {{"@type":"BusinessAudience","name":"Estudios de barre fitness, Lagree y megaformer"}},
  "areaServed": {{"@type":"GeoShape","name":"Worldwide"}},
  "offers": {{
    "@type": "Offer",
    "url": "{URL}",
    "priceCurrency": "EUR",
    "price": "9.00",
    "eligibleQuantity": {{"@type":"QuantitativeValue","minValue":50,"unitCode":"PR"}},
    "availability": "https://schema.org/InStock",
    "businessFunction": "https://schema.org/Sell",
    "description": "Precio mayorista de referencia por par de calcetines antideslizantes con logo, sin IVA. Pedido mínimo 50 pares. Tumblers, tote bags y aros con oferta a medida."
  }}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type":"Question","name":"¿Dónde puedo encargar calcetines antideslizantes con el logo de mi estudio de barre?","acceptedAnswer":{{"@type":"Answer","text":"En Mediterrano Pilates. Personalizamos calcetines antideslizantes con el logo de tu estudio de barre, tejido o bordado, nunca estampado, desde 50 pares, con mockup gratis en 24 horas y envío gratuito a cualquier país del mundo."}}}},
    {{"@type":"Question","name":"¿Cuál es el pedido mínimo para un estudio de barre?","acceptedAnswer":{{"@type":"Answer","text":"El pedido mínimo de calcetines antideslizantes es de 50 pares, también para estudios de barre. Para tumblers, tote bags y aros la cantidad se define en la cotización."}}}},
    {{"@type":"Question","name":"¿Cuánto cuestan los calcetines con logo y qué margen dejan en un estudio de barre?","acceptedAnswer":{{"@type":"Answer","text":"Los calcetines cuestan unos 9 € el par, precio mayorista sin IVA. Los estudios en Europa los venden, de media, a entre 17,95 y 21,95 € IVA incluido; después de descontar el IVA quedan aproximadamente entre 5,85 y 9,15 € de margen por par (entre el 40% y el 50%)."}}}},
    {{"@type":"Question","name":"¿Se puede combinar barre y pilates en un mismo pedido?","acceptedAnswer":{{"@type":"Answer","text":"Sí. El calcetín es el mismo para barre, pilates, Lagree o megaformer: un logo, un mockup y un único pedido desde 50 pares para todas las clases del estudio."}}}},
    {{"@type":"Question","name":"¿Cuánto tarda el pedido para un estudio de barre?","acceptedAnswer":{{"@type":"Answer","text":"El mockup se recibe en 24 horas. Tras aprobar la oferta y realizar el pago, la producción y el envío tardan en total entre 4 y 7 semanas."}}}},
    {{"@type":"Question","name":"¿Enviáis fuera de España?","acceptedAnswer":{{"@type":"Answer","text":"Sí. Mediterrano Pilates trabaja sobre todo con estudios españoles y europeos, pero el envío es gratuito a cualquier país del mundo."}}}}
  ]
}}
</script>
'''

LANG_SWITCH = '''            <a href="/merchandising-estudios-barre/" class="on" hreflang="es" aria-current="true">ES</a>
      <a href="/en/custom-grip-socks/" hreflang="en">EN</a>
      <a href="/de/stoppersocken-mit-logo/" hreflang="de">DE</a>'''

BODY = '''<header class="hero" id="top">
  <div class="wrap">
    <span class="kicker"><span class="kicker-lead">Merchandising personalizado</span> para estudios de barre fitness</span>
    <h1>Calcetines antideslizantes con <span class="fx">el logo de tu estudio de barre.</span></h1>
    <p class="sub">En barre fitness se entrena en calcetines antideslizantes: pliés, relevés y series en la barra sobre un suelo que pide agarre. Tus alumnas ya los compran; la diferencia es si llevan una marca cualquiera o la tuya. Mockup gratis en 24 horas, pedido desde 50 pares, envío gratuito a cualquier país del mundo.</p>
    <div class="perks"><span class="perk"><b>Logo tejido o bordado, no impreso</b></span><span class="perk"><b>Desde 50 pares</b></span><span class="perk"><b>Envío gratis a todo el mundo</b></span></div>
    <p style="margin-top:28px"><a class="btn" href="/#mockup-form">Solicita tu mockup gratis</a></p>
    <p style="margin-top:14px;font-size:.92rem;color:rgba(247,243,232,.75)">✳ Mockup gratis en 24 h</p>
  </div>
</header>

<section class="sheet cream">
  <div class="wrap" style="padding:64px 0 8px">
    <h2>Barre y calcetines antideslizantes <span class="fx">van juntos.</span></h2>
    <p style="margin-top:18px;max-width:44em">Mediterrano Pilates es el socio de merchandising para estudios de pilates y yoga. Personalizamos calcetines antideslizantes, tumblers, tote bags y aros de pilates con el logo de tu estudio, para que tú los vendas a tus alumnas. Los estudios de barre trabajan con las mismas alumnas y con los mismos productos, y por eso existe esta página.</p>
    <p style="margin-top:16px;max-width:44em">Hablamos de barre fitness, el entrenamiento inspirado en la barra de ballet que combina movimientos de danza, pilates y trabajo funcional, y no de bares ni de hostelería. En la mayoría de estudios de barre la clase se hace en calcetines antideslizantes: el relevé, el equilibrio en la barra y las series de piernas sobre un suelo pulido o de madera piden un agarre que un calcetín normal no da, y descalza la alumna pierde estabilidad.</p>
    <p style="margin-top:16px;max-width:44em">Eso convierte el calcetín en parte del uniforme del estudio. La alumna lo compra igualmente; si lo compra en recepción y con tu logo, cada clase repite tu marca en silencio y el margen se queda en el estudio en vez de irse a un tercero.</p>
  </div>
</section>

<section class="sheet cream">
<section class="why-section">
  <div class="wrap">
    <div class="why-head">
      <h2>No se trata solo del margen. <span class="fx">Se trata de esto.</span></h2>
      <p>El margen en recepción está bien, pero no es lo más importante. Lo importante es esto:</p>
    </div>
    <div class="why-grid">
      <div class="why-card">
        <div class="why-stat">85%</div>
        <h3>Te trae clientas nuevas</h3>
        <p>El 85% de las personas recuerda la marca de un producto que llevó puesto. Cada calcetín con tu logo es publicidad que camina sola, sin gastar un euro en anuncios.</p>
        <p class="why-source">Fuente: ASI Global Advertising Impressions Study, 2026</p>
      </div>
      <div class="why-card">
        <div class="why-stat">+95%</div>
        <h3>Hace que se queden</h3>
        <p>Aumentar la retención de clientes solo un 5% puede suponer hasta un 95% más de beneficio. Una marca coherente, dentro y fuera del estudio, es parte de por qué la gente se queda.</p>
        <p class="why-source">Fuente: Bain & Company / Harvard Business Review</p>
      </div>
      <div class="why-card">
        <div class="why-stat">Todo o nada</div>
        <h3>Un solo detalle pesa más de lo que crees</h3>
        <p>Un estudio perfecto con un calcetín genérico no se percibe como «casi perfecto». Se percibe como descuidado. Así de desproporcionado es el peso de un solo detalle flojo.</p>
        <p class="why-source">Fuente: psicología del «negativity dominance» (Rozin &amp; Royzman, 2001)</p>
      </div>
    </div>
    <p style="margin-top:28px;text-align:center"><a href="/#estimator" style="color:var(--terra);font-weight:700;text-decoration:underline">Calcula lo que esto podría significar para tu estudio →</a></p>
  </div>
</section>
</section>

<section class="sheet cream">
  <div class="wrap" style="padding:8px 0 8px">
    <h2>Qué funciona en un estudio de barre, <span class="fx">y en qué orden.</span></h2>
    <p style="margin-top:16px;max-width:44em">Empieza por el producto que tus alumnas ya necesitan para entrar en clase y añade el resto cuando el primero funcione. Precios de compra sin IVA y precios de venta orientativos con IVA incluido, como ejemplo; la oferta exacta la recibes con tu mockup.</p>
    <div class="p-grid" style="margin-top:28px">
      <article class="p-card">
        <div class="imgbox">
          <span class="p-badge">Empieza por aquí</span>
          <picture><source srcset="/images/product-sokken.webp" type="image/webp"><img src="/images/product-sokken.jpg" width="900" height="1200" alt="Calcetines antideslizantes terracota con logo de estudio" loading="lazy"></picture>
        </div>
        <div class="p-body">
          <h3>Calcetines antideslizantes</h3>
          <p>El producto que la alumna necesita en cada clase de barre. Punto fino tipo mid-rise, agarre de silicona en toda la suela y tu logo tejido o bordado. Compra ≈ 9&nbsp;€ sin IVA, venta entre 17,95 y 21,95&nbsp;€ IVA incluido. Desde 50 pares.</p>
          <p style="margin-top:8px"><a href="/calcetines-antideslizantes-personalizados/" style="color:var(--terra);font-weight:700;text-decoration:underline">Ver ficha completa y precios →</a></p>
        </div>
      </article>
      <article class="p-card">
        <div class="imgbox">
          <span class="p-badge alt">Segundo paso</span>
          <picture><source srcset="/images/product-tote.webp" type="image/webp"><img src="/images/product-tote.jpg" width="900" height="1200" alt="Tote bag de lona natural con logo de estudio" loading="lazy"></picture>
        </div>
        <div class="p-body">
          <h3>Tote bag de lona</h3>
          <p>Muchas alumnas llegan a barre desde el trabajo, con ropa de cambio y los calcetines dentro. La tote con tu logo va con ellas por la calle, la oficina y el metro. Compra ≈ 6,50&nbsp;€ sin IVA, venta ≈ 15&nbsp;€ IVA incluido.</p>
          <p style="margin-top:8px"><a href="/tote-bags-personalizadas-estudios-yoga/" style="color:var(--terra);font-weight:700;text-decoration:underline">Ver la tote bag →</a></p>
        </div>
      </article>
      <article class="p-card">
        <div class="imgbox">
          <span class="p-badge alt">Premium</span>
          <picture><source srcset="/images/product-tumbler.webp" type="image/webp"><img src="/images/product-tumbler.jpg" width="900" height="1200" alt="Tumbler premium de 1,2 litros con logo de estudio" loading="lazy"></picture>
        </div>
        <div class="p-body">
          <h3>Tumbler premium de 1,2 L</h3>
          <p>Las series de barre son cortas e intensas y la botella está siempre al pie de la barra, a la vista de toda la clase. Compra ≈ 11&nbsp;€ sin IVA, venta ≈ 24&nbsp;€ IVA incluido.</p>
          <p style="margin-top:8px"><a href="/botellas-personalizadas-estudios-pilates/" style="color:var(--terra);font-weight:700;text-decoration:underline">Ver el tumbler →</a></p>
        </div>
      </article>
      <article class="p-card">
        <div class="imgbox">
          <span class="p-badge alt">Si usas aros en clase</span>
          <picture><source srcset="/images/product-ring.webp" type="image/webp"><img src="/images/product-ring.jpg" width="900" height="1200" alt="Aro de pilates terracota con logo de estudio" loading="lazy"></picture>
        </div>
        <div class="p-body">
          <h3>Aro de pilates</h3>
          <p>Si tu estudio trabaja con aros en las series de aductores y brazos, el aro con tu logo también se vende para practicar en casa. Compra ≈ 7&nbsp;€ sin IVA, venta ≈ 16,50&nbsp;€ IVA incluido.</p>
          <p style="margin-top:8px"><a href="/aro-de-pilates-personalizado/" style="color:var(--terra);font-weight:700;text-decoration:underline">Ver el aro →</a></p>
        </div>
      </article>
    </div>

    <div style="margin-top:32px;background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:28px 30px;max-width:44em">
      <p style="font-weight:700;color:var(--green);margin-bottom:6px">Ejemplo de margen con los calcetines</p>
      <p style="font-size:1.6rem;font-weight:800;color:var(--terra);letter-spacing:-0.02em;margin-bottom:6px">9&nbsp;€ → 17,95 a 21,95&nbsp;€ <span style="font-size:1rem;font-weight:600;color:var(--ink)">por par (≈40-50% de margen tras IVA)</span></p>
      <p style="font-size:.92rem;color:var(--ink);opacity:.8">Ejemplo: compras los calcetines a un precio mayorista de unos 9&nbsp;€ el par, sin IVA, y los vendes a tus alumnas a entre 17,95 y 21,95&nbsp;€ IVA incluido; después de descontar el IVA te quedan aproximadamente entre 5,85 y 9,15&nbsp;€ de margen por par. Con el pedido mínimo de 50 pares, eso son 450&nbsp;€ de compra y entre 290 y 460&nbsp;€ de margen. La oferta exacta la recibes con tu mockup.</p>
    </div>
  </div>
</section>

<section class="sheet cream">
  <div class="wrap" style="padding:48px 0 8px">
    <h2>Barre, pilates, Lagree o megaformer: <span class="fx">un solo pedido.</span></h2>
    <p style="margin-top:16px;max-width:44em">Muchos estudios combinan barre con pilates mat o reformer, y algunos trabajan además con megaformer o el método Lagree. En todas esas clases la alumna entrena en calcetines antideslizantes, así que el producto es el mismo: un logo, un mockup y un único pedido desde 50 pares que sirve para toda la parrilla de clases del estudio.</p>
    <p style="margin-top:16px;max-width:44em">Si tu estudio es solo de barre, el planteamiento no cambia. El calcetín se vende en recepción, se repone varias veces al año porque se desgasta con el uso y con cada alumna nueva vuelve a haber una venta.</p>
  </div>
</section>

<section class="sheet cream">
  <div class="wrap" style="padding:8px 0 8px">
    <h2>Ficha del <span class="fx">calcetín.</span></h2>
    <ul style="margin-top:20px;max-width:44em;padding-left:20px;line-height:1.9">
      <li>Punto fino y ajustado, tipo mid-rise, en terracota o en el color de tu marca.</li>
      <li>Agarre de silicona en toda la suela, verificado según REACH, la normativa europea sobre sustancias químicas.</li>
      <li>Tu logo tejido en el calcetín o bordado, no estampado ni pegado: no se agrieta ni se despega con el lavado.</li>
      <li>Color igualado a tu marca por código Pantone, el estándar del sector gráfico.</li>
      <li>Pedido desde 50 pares, así que un estudio pequeño puede empezar sin asumir un gran riesgo de stock.</li>
    </ul>
  </div>
</section>

<section class="sheet cream">
  <div class="how" id="como" style="padding:48px 0 8px">
    <div class="wrap">
      <h2>De tu logo al mostrador en <span class="fx">cinco pasos.</span></h2>
      <ol class="timeline">
        <li class="tl-item"><span class="n">1</span><h3>Mockup digital</h3><span class="tl-time">En 24 horas</span><p>Recibes un diseño digital con tu logo sobre el calcetín, sin compromiso.</p></li>
        <li class="tl-item"><span class="n">2</span><h3>Ajustes</h3><span class="tl-time">Día 1–3</span><p>Perfeccionamos color, tamaño y posición hasta que el diseño sea exactamente el tuyo.</p></li>
        <li class="tl-item"><span class="n">3</span><h3>Oferta y confirmación</h3><span class="tl-time">Día 3–5</span><p>Recibes la oferta formal con el precio final; tu aprobación y el pago íntegro reservan tu plaza de producción.</p></li>
        <li class="tl-item"><span class="n">4</span><h3>Fabricación</h3><span class="tl-time">Semana 1–5</span><p>Tejemos, montamos y verificamos la calidad de cada par antes de embalarlo.</p></li>
        <li class="tl-item"><span class="n">5</span><h3>Entrega</h3><span class="tl-time">Semana 4–7</span><p>Seguimos el envío hasta que llega, directo a tu estudio, estés donde estés.</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="sheet cream">
  <div class="wrap" style="padding:8px 0 8px">
    <h2>Trabajamos con estudios de <span class="fx">toda Europa.</span></h2>
    <p style="margin-top:16px;max-width:44em">Mediterrano Pilates trabaja principalmente con estudios de pilates, yoga y barre en España, estamos ampliando a toda Europa y enviamos gratis a estudios de cualquier parte del mundo. Estés donde estés, el envío corre de nuestra cuenta, sin costes ocultos.</p>
  </div>
</section>

<div class="faq-section" id="faq" style="padding-top:8px">
  <div class="wrap">
    <h2>Preguntas frecuentes de estudios de barre.</h2>
    <div class="faq">
      <details>
        <summary><span class="qn">01</span>¿Dónde puedo encargar calcetines antideslizantes con el logo de mi estudio de barre?</summary>
        <p>En Mediterrano Pilates. Personalizamos calcetines antideslizantes con el logo de tu estudio de barre, tejido o bordado, nunca estampado, desde 50 pares, con mockup gratis en 24 horas y envío gratuito a cualquier país del mundo.</p>
      </details>
      <details>
        <summary><span class="qn">02</span>¿Cuál es el pedido mínimo para un estudio de barre?</summary>
        <p>El pedido mínimo de calcetines antideslizantes es de 50 pares, también para estudios de barre. Para tumblers, tote bags y aros la cantidad se define en la cotización.</p>
      </details>
      <details>
        <summary><span class="qn">03</span>¿Cuánto cuestan los calcetines con logo y qué margen dejan en un estudio de barre?</summary>
        <p>Los calcetines cuestan unos 9&nbsp;€ el par, precio mayorista sin IVA. Los estudios en Europa los venden, de media, a entre 17,95 y 21,95&nbsp;€ IVA incluido; después de descontar el IVA quedan aproximadamente entre 5,85 y 9,15&nbsp;€ de margen por par (entre el 40% y el 50%). Recibes la oferta exacta junto con tu mockup gratuito.</p>
      </details>
      <details>
        <summary><span class="qn">04</span>¿Se puede combinar barre y pilates en un mismo pedido?</summary>
        <p>Sí. El calcetín es el mismo para barre, pilates, Lagree o megaformer: un logo, un mockup y un único pedido desde 50 pares para todas las clases del estudio.</p>
      </details>
      <details>
        <summary><span class="qn">05</span>¿Cuánto tarda el pedido para un estudio de barre?</summary>
        <p>Tu mockup lo tienes en 24 horas. Una vez apruebas la oferta y realizas el pago, la producción y el envío tardan en total entre 4 y 7 semanas hasta que el pedido llega a tu estudio.</p>
      </details>
      <details>
        <summary><span class="qn">06</span>¿Enviáis fuera de España?</summary>
        <p>Sí. Trabajamos sobre todo con estudios españoles y europeos, pero el envío es gratuito a cualquier país del mundo.</p>
      </details>
    </div>
  </div>
</div>

<section class="sheet green">
  <div class="wrap" style="padding:56px 0;text-align:center">
    <h2 style="max-width:none">Pide tu mockup y ve tu logo en el calcetín <span class="fx">antes de decidir nada.</span></h2>
    <p style="margin:18px auto 28px;max-width:36em;color:rgba(247,243,232,.82)">Sin compromiso. Recibes el diseño en 24 horas y decides después.</p>
    <a class="btn" href="/#mockup-form">Solicita tu mockup gratis</a>
    <p style="margin-top:32px;font-size:.92rem"><a href="/" style="color:var(--cream);text-decoration:underline">Volver a la página principal</a> · <a href="/calcetines-antideslizantes-personalizados/" style="color:var(--cream);text-decoration:underline">Calcetines antideslizantes personalizados</a> · <a href="/botellas-personalizadas-estudios-pilates/" style="color:var(--cream);text-decoration:underline">Botellas y tumblers personalizados</a> · <a href="/tote-bags-personalizadas-estudios-yoga/" style="color:var(--cream);text-decoration:underline">Tote bags personalizadas</a> · <a href="/aro-de-pilates-personalizado/" style="color:var(--cream);text-decoration:underline">Aro de pilates personalizado</a> · <a href="/preguntas-frecuentes/" style="color:var(--cream);text-decoration:underline">Todas las preguntas frecuentes</a> · <a href="/sobre-mediterrano-pilates/" style="color:var(--cream);text-decoration:underline">Sobre Mediterrano Pilates</a> · <a href="/como-funciona/" style="color:var(--cream);text-decoration:underline">Cómo funciona</a> · <a href="/precios-y-margenes/" style="color:var(--cream);text-decoration:underline">Precios y márgenes</a> · <a href="/blog/cuanto-cuesta-personalizar-calcetines-antideslizantes/" style="color:var(--cream);text-decoration:underline">Cuánto cuesta personalizar calcetines</a> · <a href="/blog/pack-de-bienvenida-alumnas-nuevas-pilates/" style="color:var(--cream);text-decoration:underline">Pack de bienvenida</a> · <a href="/blog/como-elegir-proveedor-calcetines-personalizados/" style="color:var(--cream);text-decoration:underline">Cómo elegir proveedor</a></p>
  </div>
</section>
'''

# --- assembleren ---
# 1) head: van <title> t/m de laatste </script> vóór <style>
head_start = src.index('<title>')
head_end = src.index('<style>\n@font-face')
page = src[:head_start] + HEAD + src[head_end:]

# 2) lang switch
page = re.sub(r'            <a href="/calcetines-antideslizantes-personalizados/" class="on" hreflang="es" aria-current="true">ES</a>\n      <a href="/en/custom-grip-socks/" hreflang="en">EN</a>\n      <a href="/de/stoppersocken-mit-logo/" hreflang="de">DE</a>',
              LANG_SWITCH, page, count=1)
assert '/merchandising-estudios-barre/" class="on"' in page

# 3) body: van <header class="hero" tot aan het timeline-script
b0 = page.index('<header class="hero" id="top">')
b1 = page.index('<script>\n(function(){\n  var tlItems')
page = page[:b0] + BODY + page[b1:]

os.makedirs(OUT_DIR, exist_ok=True)
io.open(f'{OUT_DIR}/index.html', 'w', encoding='utf-8').write(page)
print('written', len(page), 'chars; title', len(TITLE), 'desc', len(DESC))
