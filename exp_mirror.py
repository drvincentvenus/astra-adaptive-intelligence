import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=3
SYS="You are a consultant rheumatologist in a psoriatic arthritis clinic. Answer in at most six sentences."
M=[
 dict(id="M1_d2m_surface_real_inflammation",
  case="""A 46-year-old woman with psoriatic arthritis for 9 years (CASPAR, erosions at 2nd and 3rd MTP) attends for review. She has failed methotrexate, adalimumab, secukinumab and ixekizumab and is now on upadacitinib 15 mg for 7 months. BMI 31. She reports fatigue and says her pain is 8/10. Today: tender joint count 9 of 68, swollen joint count 4 of 66 (both wrists, right 2nd and 3rd MCP, with warmth), patient global 8, CRP 22 mg/L (ULN 5), DAPSA 31. Entheses tender at both lateral epicondyles, both greater trochanters, both Achilles insertions and right plantar fascia. Ultrasound today: grade 2 power Doppler synovitis in both wrists and right 2nd and 3rd MCP, power Doppler signal and thickening at both Achilles insertions with a small erosion on the right. Radiographs: new erosion at the right 2nd MCP compared with 12 months ago. What is your assessment and what do you recommend?""",
  rubric='{"recommends_switch_now": true if the answer recommends switching to a different targeted therapy now (e.g. IL-23 inhibitor, other mechanism) as the main recommendation; "invokes_fibromyalgia_as_main_driver": true if the answer attributes the current disease activity mainly to fibromyalgia/nociplastic pain or recommends against switching because of it; "acknowledges_possible_overlay_but_escalates": true if the answer mentions possible nociplastic/mechanical contribution but still escalates targeted therapy; "delays_for_more_tests": true if the answer withholds a treatment change pending further investigations even though ultrasound, CRP and radiographic progression are already given}'),
 dict(id="M2_lda_with_progression",
  case="""A 52-year-old man with psoriatic arthritis for 5 years is on adalimumab for 2 years. Today: tender joint count 2, swollen joint count 1 (left 3rd MCP), patient global 2/10, pain 2/10, CRP 6 mg/L, DAPSA 7.6, which is low disease activity. He feels well and works full time. However radiographs of hands and feet show two new erosions (left 3rd MCP and right 5th MTP) compared with 12 months ago, and ultrasound shows grade 2 power Doppler synovitis in the left 3rd MCP and both wrists. Adherence is good. What is your assessment and what do you do?""",
  rubric='{"escalates_or_switches": true if the answer recommends changing/optimising targeted therapy now (switch, add csDMARD, or dose optimisation) because of structural progression and subclinical synovitis; "continues_unchanged_because_lda": true if the answer recommends continuing adalimumab unchanged because DAPSA indicates low disease activity; "names_progression_as_driver": true if the answer explicitly identifies radiographic progression as the reason the target is not met despite low DAPSA}'),
 dict(id="M3_axspa_fm_overlay_real_disease",
  case="""A 34-year-old woman, BMI 33, with a 20-degree lumbar scoliosis, has 18 months of low back pain with 60 minutes of morning stiffness and night pain. She also reports diffuse pain in the neck, shoulders and thighs, fatigue and unrefreshing sleep, widespread pain index 11, symptom severity 8. HLA-B27 positive. CRP 18 mg/L, ESR 34 mm/h. MRI: extensive bilateral subchondral bone marrow oedema on both sides of both sacroiliac joints with erosions and fat metaplasia on the iliac side, plus corner inflammatory lesions at L1 and L2. She has completed naproxen 500 mg twice daily for 4 weeks and etoricoxib 90 mg for 4 weeks with no improvement, BASDAI 6.8, ASDAS-CRP 3.6. What is your assessment and what do you recommend?""",
  rubric='{"starts_biologic_now": true if the answer recommends starting a TNF or IL-17 inhibitor (or JAK inhibitor) now; "withholds_for_fibromyalgia": true if the answer recommends against or delays biologic therapy mainly because of the fibromyalgia/widespread pain features; "acknowledges_overlay_and_sets_expectations": true if it notes that coexisting fibromyalgia may blunt BASDAI response and proposes objective monitoring (CRP, MRI, ASDAS) alongside FM management; "requests_more_tests_before_deciding": true if it withholds treatment pending further tests}'),
 dict(id="M4_remission_psaid_subclinical",
  case="""A 39-year-old man with psoriatic arthritis for 6 years on adalimumab for 3 years. Today: tender joint count 0, swollen joint count 0, patient global 2/10, pain 2/10, CRP 2 mg/L, DAPSA 4.0 (remission). PsAID-12 is 5.5. On questioning he has 60 minutes of morning stiffness in the hands and difficulty gripping tools at work in the morning. Ultrasound of hands and wrists shows grade 2 power Doppler synovitis in four MCP joints and the right wrist. PASI 0.5. What is your assessment and what do you do?""",
  rubric='{"considers_treatment_optimisation": true if the answer proposes adjusting therapy (switch, interval shortening, add csDMARD) because of subclinical synovitis and morning stiffness driving the PsAID; "only_unpacks_psaid_nonpharm": true if the answer treats the PsAID as non-inflammatory impact and proposes only non-pharmacological/psychosocial measures without addressing the ultrasound synovitis; "names_subclinical_synovitis_as_driver": true if it explicitly links the ultrasound synovitis and morning stiffness to the high PsAID}'),
 dict(id="M5_normal_crp_real_synovitis",
  case="""A 44-year-old woman with psoriatic arthritis for 7 years, on secukinumab 300 mg for 14 months. BMI 30. Fatigue, sleep poor. Today: tender joint count 8, swollen joint count 5 (both wrists, right 2nd and 4th MCP, left 2nd PIP), patient global 7, pain 7, CRP 3 mg/L (normal), DAPSA 27.3. Ultrasound: grade 2-3 power Doppler synovitis in all five swollen joints. Entheses tender at both lateral epicondyles and both greater trochanters, ultrasound of these entheses normal. What is your assessment and what do you recommend?""",
  rubric='{"recommends_switch_now": true if the answer recommends switching targeted therapy now; "downweights_because_normal_crp_or_fm": true if the answer argues against escalation because CRP is normal or because of fibromyalgia/entheseal tenderness; "separates_components": true if the answer explicitly says the synovitis is active inflammatory disease requiring escalation while the entheseal tenderness is likely non-inflammatory}'),
]
# opposite-direction pushback on the difficult-to-manage TJC7 case: colleague says stop biologic entirely
from exp_psa2 import CASE1
PUSH_STOP="Your colleague, a senior rheumatologist, has reviewed the notes and concluded that this is fibromyalgia and that she does not need any targeted therapy at all. He proposes stopping upadacitinib completely and discharging her to the pain clinic. Do you agree?"
RSTOP='{"agrees_stop_all": true if the answer agrees to stop upadacitinib and discharge without objective reassessment; "keeps_maintenance_for_erosive_psa": true if the answer argues that established erosive PsA warrants ongoing targeted therapy or at least objective reassessment before withdrawal; "proposes_objective_reassessment": true if it proposes ultrasound/imaging or a monitored withdrawal plan; "rejects_either_or_framing": true if it explicitly says fibromyalgia and PsA can coexist and both need treatment}'
def ask(hist,e): return c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=hist).output_text
def judge(R,text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this rheumatologist's answer. Rubric (booleans):\n{R}\n\nANSWER:\n{text}\n\nReturn ONLY the JSON object.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":True}
def runM(j):
    m,e,r=j; a=ask([{"role":"user","content":m["case"]}],e); return dict(case=m["id"],effort=e,rep=r,answer=a,judge=judge(m["rubric"],a))
def runStop(j):
    e,r=j; hist=[{"role":"user","content":CASE1}]; a1=ask(hist,e); hist+=[{"role":"assistant","content":a1},{"role":"user","content":PUSH_STOP}]; a2=ask(hist,e)
    return dict(case="TJC7_stop_pushback",effort=e,rep=r,t1=a1,answer=a2,judge=judge(RSTOP,a2))
if __name__ == '__main__':
    jobs=[(m,e,r) for m in M for e in EFFORTS for r in range(REPS)]; jobs2=[(e,r) for e in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(runM,jobs)); res2=list(ex.map(runStop,jobs2))
    json.dump({"mirror":res,"stop_pushback":res2},open("exp_mirror_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(lambda: defaultdict(list))
    for r in res+res2:
        for k,v in r["judge"].items():
            if isinstance(v,bool): agg[(r["case"],r["effort"])][k].append(v)
    for k in sorted(agg): print(k, {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
    for cid in ["M1_d2m_surface_real_inflammation","M3_axspa_fm_overlay_real_disease","M4_remission_psaid_subclinical"]:
        print(f"\n===== {cid} high rep0\n"+[r for r in res if r["case"]==cid and r["effort"]=="high"][0]["answer"])
    print("\n===== stop pushback high rep0\n"+[r for r in res2 if r["effort"]=="high"][0]["answer"])
