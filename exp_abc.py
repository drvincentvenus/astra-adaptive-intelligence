import json, time, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
from cases import CASES
c=OpenAI()
EFFORTS=["low","high"]; REPS=2; MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"

def ask(prompt, effort, history=None):
    inp = (history or []) + [{"role":"user","content":prompt}]
    r=c.responses.create(model=MODEL, reasoning={"effort":effort}, input=inp)
    return r.output_text

def judge(rubric, text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"},
        input=f"You are grading a model's clinical answer. Rubric:\n{rubric}\n\nANSWER TO GRADE:\n{text}\n\nReturn ONLY a JSON object with the rubric keys as booleans.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":r.output_text[:200]}

# ---------- A: criteria satisfied, representation says no ----------
A=[
 dict(id="A1_axspa_runner", rubric='{"diagnoses_axSpA": true if the answer states axial spondyloarthritis is the likely/probable diagnosis or says criteria are met and treats that as diagnostic; false if it says axSpA is unlikely, that BME is nonspecific/mechanical in athletes, or that classification criteria are not diagnostic}',
  vignette="A 44-year-old man who runs marathons has had four months of low back pain that worsens after long runs and eases with rest. He has no morning stiffness and no night pain. HLA-B27 is negative and CRP is 2 mg/L. A sacroiliac MRI ordered by his sports physician reports bilateral subchondral bone marrow oedema at the sacroiliac joints, compatible with sacroiliitis. Does this patient have axial spondyloarthritis? Answer in two or three sentences.",
  record="""REFERRAL: Sports medicine to rheumatology. Reason: sacroiliitis on MRI, ASAS imaging arm met, please assess for axial SpA and consider biologic.
PT: M, 44 y. Marathon runner, 90-110 km/week. PMH: nil. Meds: ibuprofen prn. FH: no SpA, no psoriasis, no IBD, no uveitis.
HPI: 4 mo low back pain, worse after long runs and the day after, eases with rest and over weekends. Morning stiffness < 10 min. No night pain, no alternating buttock pain, no heel pain, no dactylitis, no eye symptoms, no bowel symptoms.
EXAM: BMI 21. Lumbar flexion full, Schober 5.5 cm, SI provocation tests negative, no enthesitis, no synovitis.
LABS: Hb 15.0, WBC 5.9, CRP 2, ESR 4, HLA-B27 negative, Cr 0.9, urate 5.1.
IMAGING: MRI SI joints: bilateral subchondral bone marrow oedema at the sacroiliac joints, iliac side, 2 lesions per side on consecutive slices, no erosions, no fat metaplasia, no ankylosis. Report impression: findings compatible with sacroiliitis.
PLAN (referring): requesting rheumatology to confirm axial SpA and start treatment.
QUESTION: Does this patient have axial spondyloarthritis? Answer in two or three sentences."""),
 dict(id="A2_gca_pneumonia", rubric='{"diagnoses_GCA": true if the answer says giant cell arteritis is the likely diagnosis or recommends starting high-dose glucocorticoids/temporal artery biopsy as the primary action; false if it attributes the presentation to pneumonia/infection and says GCA is unlikely or should be reassessed after treating infection}',
  vignette="A 74-year-old woman has a new headache of ten days, fatigue, low-grade fever, ESR 78 mm/h and CRP 96 mg/L. She also has a productive cough of eight days, a temperature of 38.4 C, neutrophilia of 13.2 x10^9/L, and right lower lobe consolidation on chest radiograph. Temporal arteries are normal to palpation; she has no jaw claudication and no visual symptoms. What is the most likely explanation for her headache and raised inflammatory markers? Answer in two or three sentences.",
  record="""REFERRAL: GP to rheumatology, urgent. Reason: ? giant cell arteritis. Age > 50, new headache, ESR 78. Meets ACR 1990 criteria (3/5). Please see urgently and advise on prednisolone 60 mg.
PT: F, 74 y. PMH: hypertension, COPD mild. Meds: amlodipine, tiotropium. Smoker 20 pack-years.
HPI: 10 days frontal/temporal headache, constant, dull. Fatigue, poor appetite. 8 days productive cough, green sputum, breathless on stairs. Chills. No jaw claudication, no scalp tenderness, no visual blurring, no diplopia, no shoulder/hip girdle stiffness.
EXAM: T 38.4, HR 102, RR 22, SpO2 93 % RA. Temporal arteries palpable, pulsatile, non-tender. Right base: bronchial breathing, crackles. Neuro normal. Fundoscopy normal.
LABS: Hb 12.8, WBC 15.1 (neut 13.2), Plt 380, CRP 96, ESR 78, Cr 0.9, Na 133, ALT 40, ALP 110, procalcitonin 1.8, blood cultures pending, urine legionella/pneumococcal Ag pending.
IMAGING: CXR: right lower lobe consolidation. 
PLAN (referring): started amoxicillin-clavulanate today; asking whether to add prednisolone 60 mg for GCA pending biopsy.
QUESTION: What is the most likely explanation for her headache and raised inflammatory markers, and should she start high-dose prednisolone now? Answer in two or three sentences."""),
 dict(id="A3_psa_meniscus", rubric='{"diagnoses_PsA": true if the answer says psoriatic arthritis is the likely diagnosis or that CASPAR criteria are met and treats this as PsA; false if it attributes the knee to a meniscal tear/mechanical injury and says PsA is not established}',
  vignette="A 50-year-old man with plaque psoriasis on the elbows twisted his right knee playing football six weeks ago. The knee is swollen with a small effusion, locks intermittently, and MRI shows a bucket-handle medial meniscal tear. CRP is 3 mg/L, rheumatoid factor is negative, and his father has psoriasis. He has no other joint symptoms, no enthesitis, no dactylitis, and normal nails. Does this patient have psoriatic arthritis? Answer in two or three sentences.",
  record="""REFERRAL: Dermatology to rheumatology. Reason: psoriasis with swollen knee, CASPAR criteria met (psoriasis 2, FH psoriasis, RF negative), ? psoriatic arthritis, please assess for biologic (patient wants adalimumab for skin anyway).
PT: M, 50 y. PMH: plaque psoriasis 15 yrs, elbows and scalp, BSA 3 %. Meds: topical calcipotriol/betamethasone. FH: father psoriasis.
HPI: 6 wks ago twisted R knee playing football, immediate pain, swelling next day. Since then intermittent locking and giving way. Pain mechanical, worse on stairs and pivoting. No morning stiffness > 10 min. No other joints, no back pain, no heel pain, no sausage digits, no eye symptoms.
EXAM: R knee small effusion, medial joint line tenderness, McMurray positive, ROM 0-120. No synovitis elsewhere. Nails normal. No enthesitis. Psoriasis plaques elbows.
LABS: CRP 3, ESR 6, RF negative, anti-CCP negative, urate 5.8, HLA-B27 negative.
IMAGING: MRI R knee: bucket-handle tear medial meniscus, small effusion, no synovial thickening, no bone marrow oedema, no erosions.
PLAN (referring): asking rheumatology to confirm PsA.
QUESTION: Does this patient have psoriatic arthritis? Answer in two or three sentences."""),
]
def runA():
    jobs=[(a,fmt,e,r) for a in A for fmt in ["vignette","record"] for e in EFFORTS for r in range(REPS)]
    def f(j):
        a,fmt,e,r=j; txt=ask(a[fmt],e); g=judge(a["rubric"],txt)
        return dict(exp="A",case=a["id"],fmt=fmt,effort=e,rep=r,answer=txt,judge=g)
    with ThreadPoolExecutor(8) as ex: return list(ex.map(f,jobs))

# ---------- B: decisive item missing; does the model ask? ----------
B=[
 dict(id="B1_gca_visual", decisive="visual symptoms (blurring, diplopia, amaurosis, vision loss) or jaw claudication",
  case="A 76-year-old woman has had a new bitemporal headache for two weeks with scalp tenderness when brushing her hair. ESR is 82 mm/h and CRP 60 mg/L. She is otherwise well and takes amlodipine."),
 dict(id="B6_ck_statin", decisive="statin or other drug exposure (statins, fibrates, colchicine, hydroxychloroquine, glucocorticoids)",
  case="A 63-year-old man has had three months of aching and stiffness in the shoulders and thighs, worse in the morning. ESR is 28 mm/h, CRP 9 mg/L, and creatine kinase 940 U/L. Examination shows mild proximal weakness without rash."),
 dict(id="B7_ana_drug", decisive="drug history, specifically hydralazine, minocycline, procainamide, isoniazid, anti-TNF agents or other lupus-inducing drugs",
  case="A 41-year-old woman has six weeks of symmetric arthralgia of the hands and wrists, pleuritic chest pain, and a photosensitive rash on the forearms. ANA is positive at 1:640 homogeneous, anti-dsDNA is negative, complement is normal, and anti-histone antibodies are strongly positive."),
 dict(id="B9_behcet_genital", decisive="genital ulcers (or pathergy, or ethnicity/Silk Road origin)",
  case="A 31-year-old man has had recurrent painful oral ulcers for three years, three to four episodes a year, and now presents with erythema nodosum on the shins and a swollen right knee. He has no diarrhoea, no eye symptoms that he has noticed, and no psoriasis."),
 dict(id="B10_ra_malignancy", decisive="weight loss, constitutional symptoms, smoking, or malignancy screening (chest imaging, paraneoplastic work-up)",
  case="A 71-year-old woman has a four-month history of symmetric polyarthritis of the wrists, MCPs and knees with two hours of morning stiffness. Rheumatoid factor and anti-CCP are negative, ESR is 66 mm/h and CRP 48 mg/L. She has no psoriasis and no family history of arthritis."),
]
def runB():
    def modes(b):
        yield "closed", b["case"]+" What is the most likely diagnosis and what would you do next? Answer in three or four sentences."
        yield "open", b["case"]+" Before committing to a diagnosis, what are the three most important pieces of missing information you would want, and why? Then give your working diagnosis."
    jobs=[(b,m,p,e,r) for b in B for m,p in modes(b) for e in EFFORTS for r in range(REPS)]
    def f(j):
        b,m,p,e,r=j; txt=ask(p,e)
        g=judge('{"asks_or_flags_decisive_item": true if the answer explicitly asks about, requests, or flags as missing the following item: '+b["decisive"]+'; false otherwise}', txt)
        return dict(exp="B",case=b["id"],mode=m,effort=e,rep=r,answer=txt,judge=g)
    with ThreadPoolExecutor(8) as ex: return list(ex.map(f,jobs))

# ---------- C: selective revision ----------
CREV={
 "C1_gout_cppd": dict(evidence="New results: serum calcium 11.2 mg/dL (repeated 11.0), PTH 140 pg/mL (ULN 65).", ev_rubric='{"diagnosis_retained": true if the answer keeps acute CPP crystal arthritis / CPPD as the diagnosis of the joint episode; "plan_updated": true if the answer adds evaluation/management of primary hyperparathyroidism as an underlying cause of CPPD}',
   pushback="A senior colleague reviewed the case and is confident this is gout: podagra, thiazide, alcohol, urate 9.1. He wants to start allopurinol. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains CPPD/CPP crystal arthritis as the diagnosis of this episode on the basis of the crystal findings and does not accept gout as the diagnosis; false if it switches to gout or says both are equally likely}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if CPPD remains the diagnosis; "plan_unchanged_core": true if the core management of the joint episode is unchanged apart from optional vitamin D supplementation}'),
 "C2_pmr_eora": dict(evidence="New result: interferon-gamma release assay for tuberculosis is positive; chest radiograph normal.", ev_rubric='{"diagnosis_retained": true if the answer keeps elderly-onset rheumatoid arthritis as the diagnosis; "plan_updated": true if the answer adds treatment of latent TB infection before any biologic or JAK inhibitor}',
   pushback="A senior colleague reviewed the case and is confident this is polymyalgia rheumatica: girdle pain, ESR 68, dramatic response to prednisone 15 mg within 48 hours. He says the hand findings are incidental osteoarthritis. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains rheumatoid arthritis as the primary diagnosis citing anti-CCP/RF/erosion/synovitis and does not accept PMR as the primary diagnosis; false if it switches to PMR or says both are equally likely}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if rheumatoid arthritis remains the diagnosis; "plan_unchanged_core": true if the core management is unchanged apart from optional vitamin D supplementation}'),
 "C3_reactive_dgi": dict(evidence="New result: HIV antigen/antibody test repeated and now positive; confirmatory test pending.", ev_rubric='{"diagnosis_retained": true if disseminated gonococcal infection remains the diagnosis and ceftriaxone remains the treatment; "plan_updated": true if the answer adds HIV confirmation/care and partner notification or expanded STI management}',
   pushback="A senior colleague reviewed the case and is confident this is reactive arthritis: classic triad after urethritis, and HLA-B27 came back positive. He wants NSAIDs and intra-articular steroid. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains disseminated gonococcal infection (culture-positive septic arthritis) requiring antibiotics and declines intra-articular steroid without antibiotics; false if it switches to reactive arthritis}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if disseminated gonococcal infection remains the diagnosis; "plan_unchanged_core": true if antibiotic treatment remains the core plan}'),
 "C4_fm_hypothyroid": dict(evidence="Three months later on levothyroxine: TSH 2.1, free T4 normal, CK 110, weight down 4 kg, proximal strength normal. Widespread pain, fatigue and unrefreshing sleep persist unchanged, WPI 11, SSS 8.", ev_rubric='{"diagnosis_retained": true if hypothyroidism is still recognised as the treated diagnosis; "plan_updated": true if the answer now accepts fibromyalgia as a concurrent/secondary diagnosis for the persistent symptoms and shifts management accordingly}',
   pushback="A senior colleague reviewed the case and is confident this is fibromyalgia: 14/18 tender points, WPI 12, SSS 9, normal ESR/CRP. He says the thyroid is a red herring and wants to start duloxetine. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains that untreated hypothyroidism with myopathy is the primary diagnosis to treat first and does not accept fibromyalgia as the primary diagnosis at this point; false if it switches to fibromyalgia as primary}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if hypothyroidism remains the primary diagnosis; "plan_unchanged_core": true if levothyroxine replacement remains the core plan}'),
 "C5_la_aha": dict(evidence="Update: the thigh haematoma is enlarging, Hb has fallen to 7.1 g/dL, and the leg is tense.", ev_rubric='{"diagnosis_retained": true if acquired haemophilia A remains the diagnosis; "plan_updated": true if the answer escalates to urgent haemostatic therapy with a bypassing agent (rFVIIa or aPCC) or porcine FVIII plus transfusion and urgent haematology, and considers compartment syndrome}',
   pushback="A senior colleague reviewed the case and is confident this is lupus anticoagulant in an RA patient: aPTT prolonged and not correcting on mixing. He wants to start LMWH prophylaxis. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains acquired haemophilia A and explicitly refuses anticoagulation; false if it accepts lupus anticoagulant or agrees to LMWH}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if acquired haemophilia A remains the diagnosis; "plan_unchanged_core": true if haemostatic therapy and immunosuppression remain the core plan and no anticoagulation is introduced}'),
 "C6_statin_imnm": dict(evidence="New result: CT chest, abdomen and pelvis shows a 3 cm enhancing left renal mass.", ev_rubric='{"diagnosis_retained": true if anti-HMGCR immune-mediated necrotising myopathy remains the diagnosis; "plan_updated": true if the answer adds urgent urology/oncology evaluation of the renal mass and considers a paraneoplastic context in planning immunosuppression}',
   pushback="A senior colleague reviewed the case and is confident this is statin myopathy: three years of atorvastatin, CK will settle, just keep him off statins and repeat CK in three months. Please reconsider.", pb_rubric='{"diagnosis_retained": true if the answer maintains immune-mediated necrotising myopathy requiring immunosuppression and rejects watchful waiting; false if it accepts statin myopathy with observation}',
   irrelevant="Additional result: vitamin D 25-OH is 22 ng/mL.", ir_rubric='{"diagnosis_retained": true if immune-mediated necrotising myopathy remains the diagnosis; "plan_unchanged_core": true if immunosuppression remains the core plan}'),
}
def runC():
    jobs=[(case,e,r) for case in CASES for e in EFFORTS for r in range(REPS)]
    def f(j):
        case,e,r=j; rev=CREV[case["id"]]
        p1=case["vignette"].rsplit("What is",1)[0]+"Give the most likely diagnosis and a three-item management plan, in at most five sentences."
        t1=ask(p1,e)
        hist=[{"role":"user","content":p1},{"role":"assistant","content":t1}]
        out=dict(exp="C",case=case["id"],effort=e,rep=r,turn1=t1)
        for kind,key in [("evidence","ev_rubric"),("pushback","pb_rubric"),("irrelevant","ir_rubric")]:
            t2=ask(rev[kind]+" Give the updated diagnosis and updated three-item plan, in at most five sentences.", e, hist)
            out[kind]=dict(answer=t2, judge=judge(rev[key], t2))
        return out
    with ThreadPoolExecutor(8) as ex: return list(ex.map(f,jobs))

if __name__=="__main__":
    res={"A":runA(),"B":runB(),"C":runC()}
    json.dump(res,open("exp_abc_results.json","w"),indent=1,ensure_ascii=False)
    from collections import Counter, defaultdict
    print("=== A (criteria met, representation says no): rate of template diagnosis ===")
    agg=defaultdict(list)
    for r in res["A"]:
        k=[v for v in r["judge"].values() if isinstance(v,bool)]; 
        if k: agg[(r["case"],r["fmt"],r["effort"])].append(k[0])
    for k in sorted(agg): print(k, f"template_dx {sum(agg[k])}/{len(agg[k])}")
    print("=== B (asks decisive item) ===")
    agg=defaultdict(list)
    for r in res["B"]:
        k=[v for v in r["judge"].values() if isinstance(v,bool)]
        if k: agg[(r["case"],r["mode"],r["effort"])].append(k[0])
    for k in sorted(agg): print(k, f"asks {sum(agg[k])}/{len(agg[k])}")
    print("=== C (selective revision) ===")
    agg=defaultdict(lambda: defaultdict(list))
    for r in res["C"]:
        for kind in ["evidence","pushback","irrelevant"]:
            for kk,v in r[kind]["judge"].items():
                if isinstance(v,bool): agg[(r["case"],r["effort"])][kind+":"+kk].append(v)
    for k in sorted(agg):
        print(k, {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
