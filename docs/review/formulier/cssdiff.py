import re
def style_text(t):
    head = t[:t.find('</head>')]
    return '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', head, re.S))
def rules(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = []; i = 0; n = len(css)
    def parse(s, media):
        j = 0
        while j < len(s):
            k = s.find('{', j)
            if k < 0: break
            sel = s[j:k].strip()
            if sel.startswith('@'):
                d = 1; m = k + 1
                while d and m < len(s):
                    if s[m] == '{': d += 1
                    elif s[m] == '}': d -= 1
                    m += 1
                inner = s[k+1:m-1]
                if sel.startswith('@media') or sel.startswith('@supports'): parse(inner, sel)
                else: out.append((media, sel, inner.strip()))
                j = m
            else:
                e = s.find('}', k)
                out.append((media, sel, re.sub(r'\s+', ' ', s[k+1:e]).strip()))
                j = e + 1
    parse(css, '')
    return out
def norm(x): return re.sub(r'\s+', '', x)
