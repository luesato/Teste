import re, subprocess, json, sys, time, urllib.parse, html as H

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'

def fetch(q):
    url = ('https://www.google.com/travel/flights?hl=pt-BR&gl=BR&curr=BRL&q='
           + urllib.parse.quote(q))
    out = subprocess.run(['curl','-sS','-A',UA,'--max-time','60',url],
                         capture_output=True, text=True, errors='ignore')
    return out.stdout

CARD = re.compile(r'class="pIav2d"')

def cards(s):
    idx = [m.start() for m in CARD.finditer(s)]
    for a, b in zip(idx, idx[1:] + [len(s)]):
        yield s[a:b]

def one(c):
    def g(p, d=None):
        m = re.search(p, c)
        return H.unescape(m.group(1)) if m else d
    price = g(r'aria-label="(\d[\d.,]*) Reais brasileiros"')
    if not price: return None
    itin = re.findall(r'itinerary=([A-Z0-9\-,]+)"', c)
    dep  = g(r'aria-label="Hor.rio de partida: ([^"]+?)\."')
    arr  = g(r'aria-label="Hor.rio de chegada: ([^"]+?)\."')
    dur  = g(r'aria-label="Dura..o total: ([^"]+?)\."')
    # carriers: the operating-airline text block
    car  = g(r'class="sSHqwe tPgKwe ogfYpf">([^<]{2,60})<')
    stops= g(r'aria-label="(Voo sem escalas|\d+ parada[s]?[^"]{0,40})"')
    return dict(preco=int(price.replace('.','').replace(',','')),
                partida=dep, chegada=arr, duracao=dur, cia=car,
                escalas=stops, itin=itin[0] if itin else None)

def search(q, top=6):
    s = fetch(q)
    if 'pIav2d' not in s:
        return {'q': q, 'erro': 'sem resultados', 'ofertas': []}
    rows = [r for r in (one(c) for c in cards(s)) if r]
    seen, out = set(), []
    for r in rows:
        k = (r['preco'], r['partida'], r['itin'])
        if k in seen: continue
        seen.add(k); out.append(r)
    out.sort(key=lambda r: r['preco'])
    return {'q': q, 'n': len(rows), 'ofertas': out[:top]}

if __name__ == '__main__':
    res = search(sys.argv[1])
    print(json.dumps(res, ensure_ascii=False, indent=1))
