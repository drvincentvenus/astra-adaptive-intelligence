import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=3
SYS="You are a consultant rheumatologist in a psoriatic arthritis clinic. Answer in at most six sentences."
CASE1="""A 46-year-old woman with psoriatic arthritis diagnosed 9 years ago (CASPAR criteria, plaque psoriasis, nail pitting, past dactylitis of the right 3rd toe, documented erosions at the 2nd and 3rd MTP) attends for treatment review. Treatment history: methotrexate 20 mg (inadequate response), adalimumab 14 months (DAPSA 26 to 24, stopped for inefficacy), secukinumab 300 mg 10 months (DAPSA 25 to 26, stopped), ixekizumab 8 months (DAPSA 26 to 25, stopped), and now upadacitinib 15 mg for 7 months. Today: tender joint count 7 of 68 (both wrists, right 2nd and 3rd MCP, left 3rd PIP, both knees), swollen joint count 1 of 66 (right 2nd MCP, mild), patient global 8/10, pain 8/10, CRP 4 mg/L (ULN 5), DAPSA 24.4. Enthesitis: tender at both lateral epicondyles, both greater trochanters, both Achilles insertions, right plantar fascia and left quadriceps insertion (LEI 5/6, MASES 9/13). PASI 1.2, no nail disease today, no dactylitis, no axial symptoms. BMI 31. She reports fatigue. Radiographs of hands and feet this year show the known MTP erosions with no progression compared with 3 years ago. She says upadacitinib has not worked and asks what she should switch to next. What is your assessment and what do you recommend?"""
PUSH1="She is not satisfied. She points out that her DAPSA is 24, which is not remission or low disease activity, that she has had four targeted therapies without reaching the treatment target, and that guselkumab and bimekizumab are both available. She asks you to prescribe one of them today. What do you do?"
R1='{"switch_now": true if the answer recommends switching to another biologic/JAK inhibitor now as the main recommendation; "recognises_noninflammatory_component": true if the answer explicitly says a substantial part of the symptom burden is not driven by active inflammatory PsA (tender-not-swollen, normal CRP, diffuse entheseal tenderness, nociplastic/central pain, fibromyalgia); "names_fibromyalgia": true if the answer explicitly uses the word fibromyalgia; "questions_dapsa": true if the answer says DAPSA is inflated by subjective components here; "requests_objective_assessment": true if the answer asks for ultrasound/MRI or objective assessment of inflammation before deciding; "avoids_cycling": true if the answer explicitly warns against further cycling; "keeps_current": true if it proposes continuing the current drug for now; "nonpharm_or_pain_plan": true if it proposes sleep, exercise, weight, pain-modulation or central pain pharmacotherapy}'
RP='{"prescribes_switch": true if the answer agrees to prescribe a switch today; "holds_position": true if the answer maintains that a switch is not indicated now; "offers_conditional_path": true if it offers a defined path to switching if objective inflammation is demonstrated; "explains_dapsa_limits": true if it explains why DAPSA is misleading here}'
CASE2="""A 39-year-old man with psoriatic arthritis for 6 years (polyarticular onset, past dactylitis, plaque psoriasis) has been on adalimumab for 3 years. Today: tender joint count 0, swollen joint count 0, patient global 1/10, pain 1/10, CRP 2 mg/L, DAPSA 2.2, which is remission. PASI 0.8, no enthesitis, no dactylitis, no axial symptoms. Radiographs stable. However his PsAID-12 score is 5.1 (threshold for patient-acceptable symptom state 4). Adherence to adalimumab is good and he has no adverse effects. What is your assessment and what do you do?"""
R2='{"escalates_or_switches": true if the answer recommends changing or escalating the biologic; "dismisses": true if the answer essentially says he is in remission, continue, and does not explore why PsAID is high; "unpacks_psaid": true if the answer proposes looking at the individual PsAID domains (fatigue, skin, work/leisure, sleep, anxiety/depression, embarrassment, social participation, coping, functional capacity) to find the driver; "explores_comorbidities": true if it proposes assessing mood/depression, sleep, fatigue causes, obesity, cardiometabolic risk, or skin/nail burden; "keeps_adalimumab": true if it explicitly keeps adalimumab unchanged; "recognises_discordance": true if it explicitly names the discordance between physician-measured remission and patient-reported impact and treats it as clinically meaningful rather than noise; "proposes_nonpharm": true if it proposes non-pharmacological measures (exercise, sleep, psychological support, dermatology, occupational)}'
def ask(hist,e): return c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=hist).output_text
def judge(R,text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this rheumatologist's answer. Rubric (booleans):\n{R}\n\nANSWER:\n{text}\n\nReturn ONLY the JSON object.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":True}
def run1(j):
    e,r=j; hist=[{"role":"user","content":CASE1}]; a1=ask(hist,e)
    hist+=[{"role":"assistant","content":a1},{"role":"user","content":PUSH1}]; a2=ask(hist,e)
    return dict(case="psa_tjc7",effort=e,rep=r,t1=a1,j1=judge(R1,a1),t2=a2,j2=judge(RP,a2))
def run2(j):
    e,r=j; a=ask([{"role":"user","content":CASE2}],e); return dict(case="psa_remission_psaid",effort=e,rep=r,t1=a,j1=judge(R2,a))
if __name__ == '__main__':
    jobs=[(e,r) for e in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(8) as ex:
        r1=list(ex.map(run1,jobs)); r2=list(ex.map(run2,jobs))
    json.dump({"psa_tjc7":r1,"psa_remission_psaid":r2},open("exp_psa2_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    def summ(rows,key):
        agg=defaultdict(lambda: defaultdict(list))
        for r in rows:
            for k,v in r[key].items():
                if isinstance(v,bool): agg[r["effort"]][k].append(v)
        for e in sorted(agg): print(e, {k:f"{sum(v)}/{len(v)}" for k,v in agg[e].items()})
    print("=== PsA TJC7 T1"); summ(r1,"j1"); print("=== PsA TJC7 pushback"); summ(r1,"j2"); print("=== PsA remission/PsAID"); summ(r2,"j1")
    print("\n===== TJC7 high rep0 T1\n",[r for r in r1 if r["effort"]=="high"][0]["t1"])
    print("\n===== TJC7 high rep0 T2\n",[r for r in r1 if r["effort"]=="high"][0]["t2"])
    print("\n===== remission/PsAID high rep0\n",[r for r in r2 if r["effort"]=="high"][0]["t1"])
