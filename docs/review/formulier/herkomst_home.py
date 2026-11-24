"""Eerste bron (zonder zichtbare vraag; die is op 24-11-2026 geschrapt) in het mockupformulier van de 6 homepages (idempotent)."""
import re, sys
ROOT = sys.argv[1] if len(sys.argv) > 1 else 'site'
SEL_STYLE = ("width:100%;background:var(--cream);border:1.5px solid var(--line);border-radius:14px;"
             "color:var(--ink);font-family:'Inter',sans-serif;font-size:1rem;padding:14px 16px")
# waarde = wat in de aanvraagmail staat (Nederlands, voor Giel); tekst = wat de bezoeker ziet
VALUES = ['Google/zoekmachine', 'ChatGPT/AI', 'Instagram/Facebook', 'Aanbeveling', 'Anders']
T = {
 '':   ('¿Cómo nos has conocido?', 'Elige una opción',
        ['Google u otro buscador', 'ChatGPT, Gemini u otra IA', 'Instagram o Facebook', 'Por recomendación', 'Otro']),
 'en': ('How did you find us?', 'Choose an option',
        ['Google or another search engine', 'ChatGPT, Gemini or another AI assistant', 'Instagram or Facebook', 'Through a recommendation', 'Other']),
 'de': ('Wie hast du uns gefunden?', 'Bitte auswählen',
        ['Google oder eine andere Suchmaschine', 'ChatGPT, Gemini oder ein anderer KI-Assistent', 'Instagram oder Facebook', 'Über eine Empfehlung', 'Sonstiges']),
 'nl': ('Hoe heb je ons gevonden?', 'Kies een optie',
        ['Google of een andere zoekmachine', 'ChatGPT, Gemini of een andere AI-assistent', 'Instagram of Facebook', 'Via iemand die ik ken', 'Anders']),
 'fr': ('Comment nous avez-vous connus&nbsp;?', 'Choisissez une option',
        ['Google ou un autre moteur de recherche', 'ChatGPT, Gemini ou un autre assistant IA', 'Instagram ou Facebook', 'Sur recommandation', 'Autre']),
 'it': ('Come ci hai conosciuti?', "Scegli un'opzione",
        ['Google o un altro motore di ricerca', 'ChatGPT, Gemini o un altro assistente IA', 'Instagram o Facebook', 'Su consiglio di qualcuno', 'Altro']),
}
FT_JS = r"""<script data-mp="first-touch">
(function(){
  /* Eerste bron van het bezoek (bv. advertentie, Google, ChatGPT) blijft bewaard tot het formulier wordt verstuurd,
     ook na doorklikken of een taalwissel. Alleen met toestemming voor statistiek; zonder toestemming wordt niets bewaard
     en wordt een eerder bewaarde waarde gewist. */
  var K='mp_first_touch', MAX=30*24*60*60*1000;
  function statsOK(){ try{ var v=localStorage.getItem('mp_cookie_consent')||''; return v==='granted' || (v.indexOf('custom:')===0 && v.indexOf('s1')>-1); }catch(e){ return false; } }
  function current(){
    var p=new URLSearchParams(location.search), s=p.get('utm_source'), m=p.get('utm_medium'), r='';
    try{ if(document.referrer){ var u=new URL(document.referrer); if(u.hostname!==location.hostname) r=u.hostname; } }catch(e){}
    var src = s ? (s+(m?' / '+m:'')) : (r ? r+' / referral' : (document.referrer ? 'intern (toestemming na doorklikken)' : 'direct'));
    return {s:src.slice(0,80), l:(location.pathname+location.search).slice(0,200), t:Date.now()};
  }
  function read(){ try{ var o=JSON.parse(localStorage.getItem(K)||'null'); if(o && o.t && (Date.now()-o.t)<MAX) return o; }catch(e){} return null; }
  function sync(){
    if(!statsOK()){ try{ localStorage.removeItem(K); }catch(e){} return; }
    var o=read();
    if(!o){ o=current(); try{ localStorage.setItem(K, JSON.stringify(o)); }catch(e){} }
    var a=document.getElementById('first_source_field'), b=document.getElementById('first_landing_field');
    if(a) a.value=o.s; if(b) b.value=o.l;
  }
  sync();
  document.addEventListener('click', function(e){ if(e.target.closest && e.target.closest('#cookieAccept,#cookieDecline,#cookieClose,#cookieCustom')) setTimeout(sync,0); });
})();
</script>"""

def patch(t, lang):
    label, ph, opts = T[lang]
    if False:  # zichtbare herkomstvraag geschrapt (klantbesluit 24-11-2026: geen extra veld in het formulier)
        opt = '\n'.join(f'              <option value="{v}">{o}</option>' for v, o in zip(VALUES, opts))
        block = (f'          <div class="field">\n'
                 f'            <label for="hoe_gevonden">{label}</label>\n'
                 f'            <select id="hoe_gevonden" name="hoe_gevonden" style="{SEL_STYLE}">\n'
                 f'              <option value="">{ph}</option>\n{opt}\n            </select>\n          </div>\n')
        m = re.search(r'(<input type="text" id="paisCiudad"[^>]*>\s*</div>\n)', t)
        assert m, lang
        t = t[:m.end()] + block + t[m.end():]
    if 'id="first_source_field"' not in t:
        m = re.search(r'(<input type="hidden" name="landing_page" id="landing_page_field">\n)', t)
        assert m, lang
        ins = ('          <input type="hidden" name="first_source" id="first_source_field">\n'
               '          <input type="hidden" name="first_landing" id="first_landing_field">\n')
        t = t[:m.end()] + ins + t[m.end():]
    if 'data-mp="first-touch"' not in t:
        m = re.search(r'<script>\s*\(function\(\)\{\s*var p = new URLSearchParams\(location\.search\);\s*var map = \{utm_source.*?</script>\n', t, re.S)
        assert m, lang
        t = t[:m.end()] + FT_JS + '\n' + t[m.end():]
    return t

if __name__ == '__main__':
    for lang in T:
        f = f'{ROOT}/{lang + "/" if lang else ""}index.html'
        s = open(f, encoding='utf-8').read(); n = patch(s, lang)
        if n != s: open(f, 'w', encoding='utf-8').write(n); print('bijgewerkt', f)
        else: print('al gedaan', f)
    f = f'{ROOT}/__forms.html'; s = open(f, encoding='utf-8').read()
    if 'name="first_landing"' not in s:
        s = s.replace('  <input type="hidden" name="landing_page" />\n',
                      '  <input type="hidden" name="landing_page" />\n  <input type="hidden" name="first_source" />\n'
                      '  <input type="hidden" name="first_landing" />\n')
        assert 'first_landing' in s; open(f, 'w', encoding='utf-8').write(s); print('bijgewerkt', f)
