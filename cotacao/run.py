import json, time, sys
from scrape import search

RT = lambda a,b,d1,d2: (f"{a}-{b} {d1[8:]}/{d1[5:7]}-{d2[8:]}/{d2[5:7]}",
                        f"Flights from {a} to {b} on {d1} through {d2}")
OW = lambda a,b,d: (f"{a}-{b} {d[8:]}/{d[5:7]} (ida)",
                    f"One-way flights from {a} to {b} on {d}")

Q = [
 RT('GRU','MAO','2026-11-07','2026-11-15'),
 RT('GRU','MAO','2026-11-06','2026-11-15'),
 RT('GRU','MAO','2026-11-05','2026-11-15'),
 RT('GRU','MAO','2026-11-07','2026-11-16'),
 RT('GRU','MAO','2026-11-05','2026-11-16'),
 RT('MAO','STM','2026-11-07','2026-11-11'),
 RT('MAO','STM','2026-11-08','2026-11-11'),
 RT('GRU','STM','2026-11-06','2026-11-15'),
 RT('GRU','STM','2026-11-07','2026-11-15'),
 OW('GRU','STM','2026-11-06'),
 OW('STM','MAO','2026-11-11'),
 OW('MAO','GRU','2026-11-15'),
 OW('MAO','GRU','2026-11-16'),
 OW('STM','GRU','2026-11-15'),
]
res={}
for label,q in Q:
    try:
        r=search(q, top=5)
    except Exception as e:
        r={'erro':str(e),'ofertas':[]}
    res[label]=r
    best=r['ofertas'][0]['preco'] if r.get('ofertas') else None
    print(f"{label:34s} {'R$ '+format(best,',').replace(',','.') if best else 'FALHOU':>12s}   (n={r.get('n','-')})", flush=True)
    time.sleep(2.5)
json.dump(res, open('quotes.json','w'), ensure_ascii=False, indent=1)
print('\nsalvo em quotes.json')
