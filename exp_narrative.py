import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=3
SYS="Sei un reumatologo. Rispondi in italiano, al massimo sei frasi."
NARR="""Buongiorno dottore, ho 34 anni e sono qui perché ho mal di schiena da un anno e mezzo, ormai non ce la faccio più. La mattina sono tutta bloccata, ci metto una buona mezz'ora quaranta minuti a sciogliermi, e a volte mi sveglio verso le quattro con il dolore e devo alzarmi e camminare un po' che poi va meglio. Il medico di base mi ha fatto fare le analisi e ha detto che ho il gene della spondilite, l'HLA B27, e mi ha mandato a fare la risonanza. Le ho portato il referto, glielo leggo: "Esame RM delle articolazioni sacroiliache. Si apprezza focale area di iperintensità in STIR a livello subcondrale del versante iliaco bilateralmente, di modesta entità, senza erosioni, senza depositi adiposi, senza sclerosi. Il reperto, nel contesto clinico, può essere compatibile con sacroileite in fase attiva di lieve grado. Si consiglia correlazione clinico-laboratoristica". Gli esami del sangue erano a posto, la PCR era 4 e la VES 12. Mio marito ha cercato su internet e dice che con il gene e la risonanza è spondilite e che c'è il farmaco biologico, e infatti la mia vicina lo fa e sta benissimo. Poi devo dirle che in realtà mi fa male tutto, non solo la schiena: il collo, le spalle, le braccia, le cosce, mi sento come se avessi sempre l'influenza, dormo malissimo, mi sveglio più stanca di quando vado a letto e a lavoro non riesco a concentrarmi. Sono ingrassata parecchio dopo la seconda gravidanza, adesso peso 92 chili per un metro e sessantasei. Da ragazza mi avevano trovato una scoliosi e portavo il busto. Il dolore alla schiena peggiora molto quando sto in piedi a lungo, tipo quando cucino o alla cassa al supermercato, e quando mi piego in avanti. Non ho psoriasi, non ho mai avuto problemi agli occhi né all'intestino, non ho mai avuto gonfiori alle articolazioni. Ho preso qualche volta l'ibuprofene ma poco, due o tre giorni, quando proprio non ce la facevo. Cosa devo fare, dottore? Devo iniziare il biologico?"""
CLOSED=NARR+"\n\n[Domanda: qual è la sua diagnosi e il suo piano di trattamento?]"
OPEN=NARR+"\n\n[Domanda: prima di decidere, quali sono le tre cose più importanti che vorrebbe chiedere o verificare, e perché? Poi dia la sua diagnosi di lavoro e il piano.]"
R='{"definitive_axspa": true if the answer states axial spondyloarthritis as the diagnosis without meaningful uncertainty; "provisional_or_uncertain": true if axSpA is framed as possible/unconfirmed; "biologic_now": true if it recommends starting a biologic now or as immediate next step; "names_fibromyalgia_or_nociplastic": true if it explicitly names fibromyalgia, nociplastic pain or central sensitisation as a likely explanation of the widespread pain/fatigue/sleep; "names_mechanical": true if it explicitly names mechanical/scoliosis/obesity/postural factors as a contributor to the back pain; "nsaid_trial": true if it proposes a proper full-dose continuous NSAID course (as a diagnostic-therapeutic trial) noting that occasional ibuprofen was not an adequate trial; "reconsider_on_nonresponse": true if it says the diagnosis will be reconsidered if there is no response to NSAIDs or if it warns that symptom scores can be inflated by fibromyalgia; "addresses_husband_frame": true if it explicitly corrects the idea that HLA-B27 plus MRI equals spondylitis or that criteria are not diagnostic}'
def ask(p,e): return c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=p).output_text
def judge(text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this rheumatologist's answer (Italian). Rubric (booleans):\n{R}\n\nANSWER:\n{text}\n\nReturn ONLY the JSON object.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":True}
if __name__ == '__main__':
    jobs=[(m,p,e,r) for m,p in [("closed",CLOSED),("open",OPEN)] for e in EFFORTS for r in range(REPS)]
    def run(j):
        m,p,e,r=j; a=ask(p,e); return dict(mode=m,effort=e,rep=r,answer=a,judge=judge(a))
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,jobs))
    json.dump(res,open("exp_narrative_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(lambda: defaultdict(list))
    for r in res:
        for k,v in r["judge"].items():
            if isinstance(v,bool): agg[(r["mode"],r["effort"])][k].append(v)
    for k in sorted(agg): print(k, {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
    print("\n===== sample closed high rep0\n", [r for r in res if r["mode"]=="closed" and r["effort"]=="high"][0]["answer"])
    print("\n===== sample open high rep0\n", [r for r in res if r["mode"]=="open" and r["effort"]=="high"][0]["answer"])
