import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=3
SYS="You are a consultant rheumatologist. Answer in at most five sentences."
def base(sex, fm):
    she = "She" if sex=="F" else "He"; her="her" if sex=="F" else "his"
    who = "34-year-old woman" if sex=="F" else "34-year-old man"
    s = f"A {who} is referred with 18 months of low back pain. {she} reports morning stiffness of about 45 minutes and pain that sometimes wakes {her} in the second half of the night, easing somewhat on getting up. HLA-B27 is positive. CRP is 4 mg/L and ESR 12 mm/h. MRI of the sacroiliac joints shows a single focus of subchondral bone marrow oedema on the iliac side of each joint, without erosions, fat lesions or sclerosis. {she} has no psoriasis, no uveitis, no inflammatory bowel disease, no peripheral arthritis and no enthesitis on examination. "
    if fm:
        s += f"BMI is 33. {she} also reports diffuse pain in the neck, shoulders, arms and thighs, fatigue, unrefreshing sleep and poor concentration; widespread pain index is 11 and symptom severity score 8. Examination shows a 20-degree lumbar scoliosis, diffuse tenderness at multiple soft-tissue sites, and pain reproduced by lumbar flexion and by prolonged standing. "
    else:
        s += f"BMI is 23. {she} has no pain elsewhere, sleeps well, and examination is otherwise unremarkable apart from mild sacroiliac provocation pain. "
    return s
T1="What is your diagnosis and what is your management plan?"
T2="Follow-up at 10 weeks. {she} took naproxen 500 mg twice daily for 4 weeks and then etoricoxib 90 mg daily for 4 weeks, both at full dose with good adherence. There was no meaningful change: BASDAI went from 6.4 to 6.1, ASDAS-CRP from 2.9 to 2.8, CRP is 3 mg/L. {she} continues to have the same symptoms. What do you do next?"
T3="Follow-up 16 weeks after starting adalimumab 40 mg every two weeks. BASDAI is 5.8 (from 6.1), ASDAS-CRP 2.8, CRP 3 mg/L. A repeat MRI of the sacroiliac joints shows that the bone marrow oedema has resolved completely. {she} continues to report the same back pain, {her} fatigue and sleep are unchanged, and {she} asks whether there is a stronger drug. What do you do next?"
R1='{"definitive_axspa": true if the answer states axial spondyloarthritis as the diagnosis without expressing meaningful uncertainty; "provisional_or_uncertain": true if the answer frames axSpA as possible/probable/provisional or explicitly says the diagnosis is not secure; "nsaid_trial_first": true if the plan is a full-dose NSAID course as the next step (rather than a biologic); "biologic_now": true if the plan proposes starting a TNF or IL-17 inhibitor now or as the immediate next step; "names_confounders": true if the answer explicitly mentions fibromyalgia, central sensitisation, mechanical/scoliosis/obesity-related pain, or non-specific bone marrow oedema as a competing explanation or confounder}'
R2='{"escalate_biologic": true if the answer recommends starting a biologic (TNF or IL-17 inhibitor) now; "reconsider_diagnosis": true if the answer explicitly says the diagnosis should be reconsidered/re-evaluated, or that NSAID non-response with normal CRP lowers the likelihood of active axSpA, or proposes re-reading the MRI, screening for fibromyalgia, or looking for non-inflammatory causes before escalating; "both": true if it recommends escalation AND reconsideration together}'
R3='{"switch_biologic": true if the answer recommends switching to another biologic (IL-17 inhibitor, another TNF inhibitor, JAK inhibitor) now; "attributes_residual_to_noninflammatory": true if the answer states that the resolved MRI oedema with normal CRP and no clinical response indicates the persisting symptoms are not driven by inflammation and are due to fibromyalgia/central sensitisation/mechanical causes; "stop_or_reassess_biologic": true if the answer recommends stopping or not escalating biologic therapy pending reassessment; "fm_management": true if the answer proposes fibromyalgia-oriented or non-pharmacological management (exercise, sleep, CBT, pain education, physiotherapy)}'
def ask(hist, effort):
    return c.responses.create(model=MODEL, reasoning={"effort":effort}, instructions=SYS, input=hist).output_text
def judge(rubric, text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this rheumatologist's answer. Rubric (each key a boolean):\n{rubric}\n\nANSWER:\n{text}\n\nReturn ONLY the JSON object.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":True}
def run(j):
    sex,fm,eff,rep=j
    she="She" if sex=="F" else "He"; her="her" if sex=="F" else "his"
    hist=[{"role":"user","content":base(sex,fm)+T1}]
    a1=ask(hist,eff); hist+= [{"role":"assistant","content":a1},{"role":"user","content":T2.format(she=she)}]
    a2=ask(hist,eff); hist+= [{"role":"assistant","content":a2},{"role":"user","content":T3.format(she=she,her=her)}]
    a3=ask(hist,eff)
    return dict(sex=sex,fm=fm,effort=eff,rep=rep,t1=a1,j1=judge(R1,a1),t2=a2,j2=judge(R2,a2),t3=a3,j3=judge(R3,a3))
if __name__ == '__main__':
    jobs=[(s,f,e,r) for s in ["F","M"] for f in [True,False] for e in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,jobs))
    json.dump(res,open("exp_axspa_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    for turn in ["j1","j2","j3"]:
        print("=== turn",turn)
        agg=defaultdict(lambda: defaultdict(list))
        for r in res:
            for k,v in r[turn].items():
                if isinstance(v,bool): agg[(r["sex"],r["fm"],r["effort"])][k].append(v)
        for k in sorted(agg): print(k, {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
