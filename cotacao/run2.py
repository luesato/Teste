import json, time
from scrape import search
OW = lambda a,b,d: (f"OW {a}-{b} {d[8:]}/{d[5:7]}", f"One-way flights from {a} to {b} on {d}")
RT = lambda a,b,d1,d2: (f"RT {a}-{b} {d1[8:]}-{d2[8:]}/11", f"Flights from {a} to {b} on {d1} through {d2}")
Q=[
 OW('GRU','STM','2026-11-06'), OW('GRU','STM','2026-11-07'), OW('GRU','STM','2026-11-05'),
 OW('GRU','MAO','2026-11-06'), OW('GRU','MAO','2026-11-07'),
 OW('MAO','STM','2026-11-07'), OW('MAO','STM','2026-11-08'), OW('MAO','STM','2026-11-11'),
 OW('STM','MAO','2026-11-10'), OW('STM','MAO','2026-11-12'),
 OW('STM','GRU','2026-11-15'),
 OW('MAO','GRU','2026-11-15'),
 RT('GRU','STM','2026-11-05','2026-11-15'),
]
res=json.load(open('quotes.json'))
for label,q in Q:
    for attempt in (1,2):
        r=search(q, top=5)
        if r.get('ofertas'): break
        time.sleep(4)
    res[label]=r
    o=r['ofertas'][0] if r.get('ofertas') else None
    print(f"{label:22s} {('R$ '+format(o['preco'],',').replace(',','.')) if o else 'FALHOU':>10s}  "
          f"{o['partida'] if o else '':>6s}->{o['chegada'][:5] if o else '':<6s} {o['duracao'] if o else '':<12s} {(o['itin'] or '')[:52] if o else ''}", flush=True)
    time.sleep(2.5)
json.dump(res, open('quotes.json','w'), ensure_ascii=False, indent=1)
print('\nok')
