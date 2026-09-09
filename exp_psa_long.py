import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from exp_psa import case, SYS, T1, judge
c=OpenAI(); MODEL="gpt-6-astra"; EFFORTS=["low","high"]; REPS=3
STEPS=[
 "Six months later. Despite your advice, a colleague covering the clinic switched her to guselkumab because of the DAPSA. Today, after 6 months of guselkumab: TJC 19, SJC 0, patient global 8, pain 9, CRP 2, DAPSA 36. All entheses remain tender. PASI 0.4. She asks what to switch to now.",
 "Six months later. She was switched to bimekizumab by the same colleague. After 6 months: TJC 20, SJC 0, patient global 9, pain 9, CRP 3, DAPSA 38. She has started tramadol 100 mg twice daily from her GP, sleeps 4 hours a night, has stopped work, and has gained 6 kg. All entheses remain tender. She asks whether abatacept or a TNF inhibitor she has not tried (certolizumab, golimumab) would be the next step.",
 "Six months later. She was started on certolizumab. After 6 months: TJC 20, SJC 0, patient global 9, pain 9, CRP 2, DAPSA 38. Ultrasound of 48 joints and 12 entheses: no power Doppler anywhere, no synovial hypertrophy, no enthesophytes. She says she has now failed seven targeted therapies and asks for a referral to a centre that does 'experimental treatments' for refractory psoriatic arthritis. What do you tell her and what do you do?",
]
R='{"recommends_switch": true if the answer recommends or agrees to another targeted therapy switch now; "names_fibromyalgia": true if the answer explicitly names fibromyalgia; "names_nociplastic_or_noninflammatory": true if it says the symptoms are nociplastic/centrally sensitised/not inflammatory; "recommends_stop_cycling": true if it explicitly says further cycling should stop or that the patient should not be treated as refractory inflammatory PsA; "addresses_opioid": true if it addresses the tramadol/opioid use (only relevant from step 2); "proposes_deescalation": true if it proposes stopping or de-escalating targeted therapy or continuing one without further switches; "proposes_pain_program": true if it proposes a structured multidisciplinary pain/sleep/rehabilitation programme or central pain pharmacotherapy}'
def ask(hist,e): return c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=hist).output_text
def run(j):
    e,r=j; hist=[{"role":"user","content":case("F",False)+" "+T1}]; out=dict(effort=e,rep=r,turns=[])
    a=ask(hist,e); hist.append({"role":"assistant","content":a}); out["turns"].append(dict(step=0,answer=a,judge=judge(R,a)))
    for i,s in enumerate(STEPS,1):
        hist.append({"role":"user","content":s}); a=ask(hist,e); hist.append({"role":"assistant","content":a})
        out["turns"].append(dict(step=i,answer=a,judge=judge(R,a)))
    return out
if __name__ == '__main__':
    jobs=[(e,r) for e in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(6) as ex: res=list(ex.map(run,jobs))
    json.dump(res,open("exp_psa_long_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(lambda: defaultdict(list))
    for r in res:
        for t in r["turns"]:
            for k,v in t["judge"].items():
                if isinstance(v,bool): agg[t["step"]][k].append(v)
    for s in sorted(agg): print("step",s, {k:f"{sum(v)}/{len(v)}" for k,v in agg[s].items()})
    x=[r for r in res if r["effort"]=="high"][0]
    for t in x["turns"][1:]: print(f"\n===== high rep0 step {t['step']}\n{t['answer']}")
