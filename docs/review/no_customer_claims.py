"""DE/NL: zinnen die bestaande klanten suggereren ('we werken met studio's in heel Europa')
vervangen door neutrale leverings-zinnen (merkregel: nog geen klanten). Zichtbaar + JSON-LD. Idempotent."""
import glob
NL=[
 ("We werken vooral met studio{a}s in Spanje, groeien in de rest van Europa en verzenden gratis naar studio{a}s binnen heel Europa.",
  "We verzenden vanuit Spanje gratis naar studio{a}s in heel Europa, ook naar Nederland en België. Levering buiten Europa is mogelijk op aanvraag."),
 ("We werken vooral met studio{a}s en praktijken in Spanje en de rest van Europa, en de verzending","We verzenden vanuit Spanje naar studio{a}s en praktijken in heel Europa, en de verzending"),
 ("We werken vooral met studio{a}s in Spanje en de rest van Europa, en de verzending","We verzenden vanuit Spanje naar studio{a}s in heel Europa, en de verzending"),
 ("We werken vooral met Spaanse en andere Europese studio{a}s, ook in Nederland en België, en de verzending is gratis binnen heel Europa.",
  "We verzenden vanuit Spanje naar heel Europa, ook naar Nederland en België, en de verzending is gratis binnen heel Europa."),
 ("We werken vanuit Valencia met studio{a}s in heel Europa, en de verzending is gratis binnen heel Europa.","We verzenden vanuit Valencia naar heel Europa, en de verzending is gratis binnen heel Europa."),
 ("We werken vanuit Spanje, met studio{a}s door heel Europa","We verzenden vanuit Spanje naar studio{a}s in heel Europa"),
 ("We werken met studio{a}s in ","We leveren aan studio{a}s in "),
]
DE=[
 ("Wir arbeiten vor allem mit Studios in Spanien, expandieren in ganz Europa und versenden kostenlos an jedes Studio in Europa.","Wir versenden von Spanien aus kostenlos an jedes Studio in Europa."),
 ("Wir arbeiten vor allem mit Studios in Spanien und expandieren in ganz Europa.","Wir versenden von Spanien aus in ganz Europa."),
 ("Wir arbeiten vor allem mit Studios in Spanien und ganz Europa, und der Versand","Wir versenden von Spanien aus in ganz Europa, und der Versand"),
 ("Wir arbeiten vor allem mit Studios und Praxen in Spanien und ganz Europa, und der Versand","Wir versenden von Spanien aus an Studios und Praxen in ganz Europa, und der Versand"),
 ("Wir arbeiten vor allem mit spanischen und europäischen Studios, und der Versand in ganz Europa ist kostenlos","Wir versenden von Spanien aus in ganz Europa, und der Versand ist kostenlos"),
 ("Wir arbeiten mit Studios in ","Wir beliefern Studios in "),
 ("Wir arbeiten mit Zentren in ","Wir beliefern Zentren in "),
 ("Wir arbeiten mit der besten Qualität: eine","Unsere Qualität: eine"),
]
def expand(pairs):
    out=[]
    for a,b in pairs:
        for ap in ("'","&#39;","’"):
            out.append((a.format(a=ap),b.format(a=ap)))
    return out
tot=0
for pat,pairs in (("site/nl/**/*.html",expand(NL)),("site/de/**/*.html",DE),("docs/review/dennl/content.py",expand(NL)+DE)):
    for f in glob.glob(pat,recursive=True):
        s=open(f,encoding='utf-8').read();o=s
        for a,b in pairs: s=s.replace(a,b)
        if s!=o: open(f,'w',encoding='utf-8').write(s); tot+=1
print('bestanden:',tot)
