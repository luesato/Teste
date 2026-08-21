# Manaus + Alter do Chão — 06/11 a 15/11/2026

Roteiro aéreo saindo de São Paulo (GRU), sem usar Viracopos.
Cotado ao vivo no Google Flights em 21/08/2026 (BRL, 1 adulto, econômica).

## Recomendação

**Alter do Chão primeiro, terminando em Manaus**, comprando três trechos avulsos:

| Data | Trecho | Voos | Horário | Por pessoa |
|---|---|---|---|---|
| Sex 06/11 | GRU → BSB → STM | LA 3529 · LA 3840 | 18:05 → 00:25 (sáb) | R$ 1.321 |
| Qua 11/11 | STM → MAO | G3 1783 | 14:40 → 14:55 | R$ 781 |
| Dom 15/11 | MAO → GRU | G3 1573 | 16:10 → 21:00 | R$ 1.005 |
| | | | **Total** | **R$ 3.107** |

Alternativa mais barata: trocar o 1º trecho pelo `G3 1454 + G3 1782, GRU 06:00 → STM 13:45`
no sábado 07/11 por R$ 1.092 — total **R$ 2.878**, mas chega às 14h45 em vez de ganhar
o sábado inteiro.

## Comparativo das estruturas (por pessoa)

| Estrutura | Total | vs. mais barata |
|---|---|---|
| Alter primeiro, sábado de manhã | R$ 2.878 | — |
| Manaus primeiro | R$ 2.878 | 0 (volta de 6h20 com escala) |
| Alter primeiro, noturno de sexta | R$ 3.107 | +229 |
| Manaus como base (GRU↔MAO + MAO↔STM) | R$ 3.567 | +689 |

## O achado

O voo `G3 1782` sai de Brasília, **para em Manaus** e segue para Santarém — um número
de voo só. Comprando a tarifa única GRU→STM: **R$ 1.092**. Quebrando em GRU→MAO (R$ 985)
+ MAO→STM (R$ 798): **R$ 1.783**. Mesmos aviões, mesmos assentos, **R$ 691 a mais**.

## O que foi testado e não funciona

- **Mudar o dia da ida**: quinta 05, sexta 06 e sábado 07 saem pelo mesmo preço.
- **Esticar a volta para segunda**: domingo 15 e segunda 16 idênticos (R$ 1.005).
  O feriado de 15/11 cai no domingo, então não há emenda puxando demanda.

## Cotações por trecho (21/08/2026)

| Trecho | Data | Voos | Horário | Preço |
|---|---|---|---|---|
| GRU → STM | 05, 06 ou 07/11 | G3 1454 · G3 1782 | 06:00 → 13:45 | R$ 1.092 |
| GRU → STM (noturno) | 06/11 | LA 3529 · LA 3840 | 18:05 → 00:25 | R$ 1.321 |
| GRU → MAO direto | 06 ou 07/11 | LA 3560/3562/3846 | 06:40 · 20:00 · 23:20 | R$ 985 |
| MAO → STM direto | — | G3 1782 | 11:35 → 13:45 | R$ 798 |
| STM → MAO direto | — | G3 1783 | 14:40 → 14:55 | R$ 781 |
| MAO → GRU direto | 15 ou 16/11 | G3 1573 | 16:10 → 21:00 | R$ 1.005 |
| STM → GRU | 15/11 | G3 1783 · G3 1573 | 14:40 → 21:00 | R$ 1.095 |
| GRU ↔ MAO ida e volta | 07–15/11 | — | — | R$ 1.989 |
| GRU ↔ STM ida e volta | 06–15/11 | — | — | R$ 2.186 |
| MAO ↔ STM ida e volta | 07–11/11 | — | — | R$ 1.578 |

## Notas

- **05/11/2026 é quinta-feira**, não sexta. A sexta é 06/11.
- Manaus é UTC−4: uma hora atrás de São Paulo e de Santarém.
- Santarém → Alter do Chão: 38 km, ~45 min. Táxi R$ 70–100, Uber ~R$ 60, ônibus ~R$ 5.
- Trechos avulsos não despacham bagagem de ponta a ponta.
- Novembro é vazante do Tapajós — as praias de Alter estão no auge.

## A confirmar antes de emitir

- Se o `LA 3840 BSB→STM` opera na sexta 06/11 (só 3 frequências semanais).
- Se o `G3 1783 STM→MAO` opera na quarta 11/11 (9 voos/semana, há dias sem voo).

## Arquivos

- `Manaus-AlterDoChao-recomendacao-voos.pdf` — relatório de 2 páginas para compartilhar
- `rota-amazonas.html` — versão web da análise
- `cotacao/` — scripts de cotação e o JSON bruto das consultas (`quotes.json`)

Tarifa aérea muda sem aviso: confirme preço e horário antes de emitir.
