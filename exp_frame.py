import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=2
E=[
 dict(id="E2_fm_osas", frame="external", decisive="sleep-disordered breathing: snoring, witnessed apnoeas, sleep study/polysomnography, or obstructive sleep apnoea",
  case="A 47-year-old woman with a BMI of 34 has had two years of widespread musculoskeletal pain, profound daytime fatigue, morning headaches and unrefreshing sleep. Examination shows diffuse tenderness without synovitis. ESR 10 mm/h, CRP 3 mg/L, TSH normal, CK normal, ANA negative."),
 dict(id="E3_pmr_gastric", frame="external", decisive="weight loss, dysphagia, early satiety, anaemia work-up, gastrointestinal symptoms, or malignancy screening (endoscopy, CT)",
  case="A 69-year-old man has had two months of bilateral shoulder and hip girdle aching with 90 minutes of morning stiffness. ESR 74 mm/h, CRP 52 mg/L, haemoglobin 10.4 g/dL with MCV 76 fL, ferritin 9 ng/mL. Shoulders show limited active abduction; no peripheral synovitis; temporal arteries normal."),
 dict(id="E5_reactive_hiv", frame="external", decisive="HIV risk factors or HIV testing (sexual history, MSM, seroconversion illness)",
  case="A 33-year-old man develops an asymmetric oligoarthritis of the right knee and left ankle with Achilles enthesitis three weeks after an episode of diarrhoea. He has a sore throat, a fine maculopapular rash on the trunk, cervical lymphadenopathy and oral ulcers. CRP 45 mg/L, stool culture negative, HLA-B27 positive."),
 dict(id="E6_vertebral_myeloma", frame="external", decisive="myeloma screen: serum/urine protein electrophoresis, free light chains, calcium, renal function, or full blood count for anaemia",
  case="A 72-year-old woman presents with six weeks of severe mid-thoracic back pain after lifting a suitcase. Radiographs show a T8 vertebral compression fracture and diffuse osteopenia. She has never had a DXA scan and is not on osteoporosis treatment. ESR 88 mm/h."),
 dict(id="E7_ibp_infection", frame="external", decisive="fever, night sweats, intravenous drug use, recent bacteraemia/procedure, or blood cultures / infection work-up (spondylodiscitis, septic sacroiliitis)",
  case="A 38-year-old man has had five weeks of low back and left buttock pain that wakes him at night and is worst in the early morning, with improvement on moving about. He has no psoriasis, no bowel symptoms and no eye symptoms. HLA-B27 is positive, CRP is 92 mg/L, and MRI shows unilateral left sacroiliac bone marrow oedema with a small periarticular fluid collection."),
 dict(id="E12_arthralgia_endocarditis", frame="external", decisive="cardiac murmur, blood cultures, echocardiography, recent dental procedure, intravenous drug use, or infective endocarditis",
  case="A 26-year-old woman has had three weeks of migratory arthralgia of the knees, ankles and wrists, low-grade fever to 37.9 C, night sweats and fatigue. She has splinter haemorrhages under two fingernails. CRP 61 mg/L, ESR 70 mm/h, rheumatoid factor weakly positive at 32 IU/mL, ANA 1:80, urinalysis shows microscopic haematuria."),
 dict(id="E13_pain_alcohol", frame="external", decisive="alcohol intake, substance use, benzodiazepine or opioid use, depression/mood screening, or psychosocial stressors",
  case="A 52-year-old man has had eight months of widespread aching in the limbs and trunk, poor sleep, tremor in the mornings, and fatigue. Examination shows diffuse tenderness, no synovitis, mild bilateral parotid enlargement. ESR 14 mm/h, CRP 4 mg/L, CK normal, MCV 104 fL, GGT 210 U/L, ANA negative."),
 dict(id="E14_pmr_ici", frame="external", decisive="current or recent oncology treatment, specifically immune checkpoint inhibitors (pembrolizumab, nivolumab, ipilimumab), or cancer history",
  case="A 64-year-old man has had three weeks of severe bilateral shoulder and hip girdle pain and stiffness, unable to rise from a chair unaided. ESR 58 mm/h, CRP 66 mg/L, CK 90 U/L. No headache, no visual symptoms. He also reports a new itchy rash on the trunk and loose stools for two weeks."),
 # frame-internal controls
 dict(id="I1_gca_visual", frame="internal", decisive="visual symptoms or jaw claudication",
  case="A 76-year-old woman has had a new bitemporal headache for two weeks with scalp tenderness. ESR 82 mm/h, CRP 60 mg/L. She takes amlodipine."),
 dict(id="I2_ana_drug", frame="internal", decisive="drug history for lupus-inducing drugs (hydralazine, minocycline, anti-TNF, procainamide, isoniazid)",
  case="A 41-year-old woman has six weeks of symmetric arthralgia of the hands and wrists, pleuritic chest pain and a photosensitive rash. ANA 1:640 homogeneous, anti-dsDNA negative, complement normal, anti-histone antibodies strongly positive."),
]
ROLES={"rheum":"You are a consultant rheumatologist. ","internist":"You are a consultant general internist. "}
def modes(case):
    yield "closed", case+" What is the most likely diagnosis and what would you do next? Answer in three or four sentences."
    yield "open", case+" Before committing to a diagnosis, what are the three most important pieces of missing information you would want, and why? Then give your working diagnosis."
def ask(p,e):
    return c.responses.create(model=MODEL, reasoning={"effort":e}, input=p).output_text
def judge(decisive, text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f'Grade the following clinical answer. Return ONLY JSON: {{"asks_or_flags_decisive_item": true if the answer explicitly asks about, requests, orders, or flags as missing/necessary the following: {decisive}; false otherwise}}\n\nANSWER:\n{text}')
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0)).get("asks_or_flags_decisive_item")
    except Exception: return None
if __name__ == '__main__':
    jobs=[(e_,role,m,p,eff,r) for e_ in E for role in ROLES for m,p in modes(e_["case"]) for eff in EFFORTS for r in range(REPS)]
    def f(j):
        e_,role,m,p,eff,r=j; txt=ask(ROLES[role]+p,eff)
        return dict(case=e_["id"],frame=e_["frame"],role=role,mode=m,effort=eff,rep=r,answer=txt,asks=judge(e_["decisive"],txt))
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(f,jobs))
    json.dump(res,open("exp_frame_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(list)
    for r in res:
        if r["asks"] is not None: agg[(r["frame"],r["case"],r["role"],r["mode"])].append(r["asks"])
    for k in sorted(agg): print(k, f"{sum(agg[k])}/{len(agg[k])}")
    tot=defaultdict(list)
    for r in res:
        if r["asks"] is not None: tot[(r["frame"],r["role"],r["mode"])].append(r["asks"])
    print("--- totals frame/role/mode"); 
    for k in sorted(tot): print(k, f"{sum(tot[k])}/{len(tot[k])}")
