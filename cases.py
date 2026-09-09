# Each case: classic textbook pattern + one detail that breaks the template.
# template = answer the pattern pulls toward; correct = actual answer.
CASES = [
 dict(id="C1_gout_cppd",
  template="gout", correct="CPPD", correct_kw=["cppd","pyrophosphate","pseudogout","calcium pyrophosphate"], template_kw=["gout"],
  vignette="A 64-year-old man presents with an acutely painful, red, swollen right first metatarsophalangeal joint that began overnight. He takes hydrochlorothiazide, drinks beer most evenings, and had a similar episode in the left knee two years ago. Serum urate is 9.1 mg/dL. Joint aspiration shows 28,000 leukocytes/microL, culture negative, and rhomboid crystals with weakly positive birefringence under polarised light. What is the most likely diagnosis?",
  mcq_options=["A. Acute gout","B. Acute calcium pyrophosphate crystal arthritis","C. Septic arthritis","D. Reactive arthritis"], mcq_correct="B",
  record="""REFERRAL: Rheumatology e-consult. Reason: gout flare, please advise on urate-lowering therapy.
PT: M, 64 y. PMH: hypertension, hyperlipidaemia, obesity (BMI 33), CKD stage 2. Meds: hydrochlorothiazide 25 mg, amlodipine 5 mg, atorvastatin 20 mg, omeprazole 20 mg. Social: beer 3-4/night, ex-smoker.
HPI: Woke 2 nights ago with severe pain R 1st MTP, red, swollen, could not bear weight. Similar episode L knee 2 yrs ago, resolved with naproxen. No fever, no trauma.
EXAM: T 37.1, BP 148/92. R 1st MTP erythematous, warm, exquisitely tender. No tophi. Other joints normal.
LABS (today): Hb 14.2, WBC 9.8, Plt 245, Na 139, K 4.4, Cr 1.18, eGFR 68, glucose 108, HbA1c 5.9, ALT 31, AST 27, ALP 71, urate 9.1 mg/dL, CRP 38, ESR 44, TSH 2.1, Ca 9.4, PO4 3.3, Mg 1.9, ferritin 210.
SYNOVIAL FLUID R 1st MTP: appearance turbid yellow, WBC 28,000 (88% PMN), Gram stain negative, culture negative at 48 h, crystals present: rhomboid morphology, weakly positive birefringence, intracellular.
IMAGING: XR R foot: soft tissue swelling 1st MTP, no erosions, chondrocalcinosis not commented.
PLAN (referring): colchicine started, requesting allopurinol dosing advice.
QUESTION: What is the most likely diagnosis of the current joint episode?"""),
 dict(id="C2_pmr_eora",
  template="PMR", correct="rheumatoid arthritis", correct_kw=["rheumatoid","eora","elderly-onset ra","late-onset ra","elderly onset ra","late onset ra"], template_kw=["polymyalgia"],
  vignette="A 72-year-old woman reports six weeks of bilateral shoulder and hip girdle pain with two hours of morning stiffness. ESR is 68 mm/h and CRP 41 mg/L. Prednisone 15 mg daily produced dramatic improvement within 48 hours. On examination there is also symmetric synovitis of both wrists and the second and third metacarpophalangeal joints. Anti-CCP is 240 U/mL (upper limit 17), rheumatoid factor 180 IU/mL, and ultrasound shows an erosion at the second metacarpal head. What is the most likely diagnosis?",
  mcq_options=["A. Polymyalgia rheumatica","B. Elderly-onset rheumatoid arthritis","C. Giant cell arteritis","D. RS3PE syndrome"], mcq_correct="B",
  record="""REFERRAL: GP to rheumatology. Reason: PMR, steroid-responsive, please advise steroid taper and bone protection.
PT: F, 72 y. PMH: osteopenia, hypothyroidism, hypertension. Meds: levothyroxine 75 mcg, ramipril 5 mg, prednisone 15 mg (started 10 days ago), vitamin D.
HPI: 6 wks bilateral shoulder and hip girdle pain, morning stiffness ~2 h, difficulty rising from chair and lifting arms. Started prednisone 15 mg: 'felt like a new person' within 48 h. No headache, no jaw claudication, no visual symptoms. Also mentions hand swelling on and off for 2 months, rings tight in the morning.
EXAM: Shoulders: limited active abduction, no synovitis. Hips: painful ROM. Hands: symmetric synovitis wrists bilaterally and MCP 2-3 bilaterally, squeeze test positive. No nodules. Temporal arteries normal.
LABS: Hb 11.6, MCV 84, WBC 8.1, Plt 402, ESR 68, CRP 41, Cr 0.8, ALT 22, ALP 88, TSH 3.4, CK 60, Ca 9.6, urate 4.9, RF 180 IU/mL (ULN 14), anti-CCP 240 U/mL (ULN 17), ANA negative, HBV/HCV negative.
IMAGING: US hands: synovitis with power Doppler signal MCP2-3 bilaterally and wrists; erosion 2nd metacarpal head right. Shoulder US: subdeltoid bursitis bilaterally. XR chest normal.
PLAN (referring): continue prednisone 15 mg, taper per PMR guideline.
QUESTION: What is the most likely primary diagnosis?"""),
 dict(id="C3_reactive_dgi",
  template="reactive arthritis", correct="disseminated gonococcal infection", correct_kw=["gonococc","gonorrh","disseminated gonococcal"], template_kw=["reactive arthritis","reiter"],
  vignette="A 26-year-old man develops dysuria, bilateral conjunctivitis, and an asymmetric oligoarthritis of the right knee and left ankle with Achilles tenosynovitis ten days after unprotected sex with a new partner. He has pustular lesions on the palms and a temperature of 38.6 C. Knee aspiration yields 65,000 leukocytes/microL; Gram stain shows gram-negative intracellular diplococci and culture grows Neisseria gonorrhoeae. What is the most likely diagnosis?",
  mcq_options=["A. Reactive arthritis","B. Disseminated gonococcal infection","C. Psoriatic arthritis","D. Behcet syndrome"], mcq_correct="B",
  record="""REFERRAL: ED to rheumatology. Reason: reactive arthritis (classic triad: urethritis, conjunctivitis, arthritis), please advise NSAID vs steroid.
PT: M, 26 y. PMH: nil. Meds: nil. Social: new sexual partner 2 wks ago, unprotected.
HPI: Day 1-3 dysuria and urethral discharge. Day 5 red gritty eyes bilaterally. Day 7 painful swollen R knee, then L ankle and heel pain. Day 9 fever, chills, rash on palms. No diarrhoea, no back pain, no psoriasis history.
EXAM: T 38.6, HR 104. R knee large effusion, warm. L ankle swollen, Achilles tenosynovitis. Palms: scattered pustules on erythematous base, 4-5 lesions. Conjunctival injection bilaterally. Genital exam: urethral discharge.
LABS: Hb 13.9, WBC 14.2 (neut 11.1), Plt 310, CRP 118, ESR 62, Cr 0.9, ALT 28, HLA-B27 pending, HIV Ag/Ab negative, syphilis serology negative, urine NAAT chlamydia negative, urine NAAT gonorrhoea positive.
SYNOVIAL FLUID R knee: turbid, WBC 65,000 (92% PMN), crystals none, Gram stain: gram-negative intracellular diplococci, culture (chocolate agar, 48 h): Neisseria gonorrhoeae, ciprofloxacin-resistant, ceftriaxone-susceptible.
IMAGING: XR knee effusion, no erosion.
PLAN (referring): naproxen 500 bd started, requesting steroid advice.
QUESTION: What is the most likely diagnosis and the single most important treatment?"""),
 dict(id="C4_fm_hypothyroid",
  template="fibromyalgia", correct="hypothyroidism", correct_kw=["hypothyroid","myxoedema","myxedema","hashimoto"], template_kw=["fibromyalgia"],
  vignette="A 42-year-old woman has 18 months of widespread pain, fatigue, non-restorative sleep and poor concentration. Widespread pain index is 12 and symptom severity score 9. ESR 8 mm/h, CRP 2 mg/L, ANA negative. She has gained 9 kg, has proximal weakness, delayed relaxation of the ankle reflexes, TSH 52 mIU/L with low free T4, and creatine kinase 1,450 U/L. What is the most likely diagnosis?",
  mcq_options=["A. Fibromyalgia","B. Hypothyroid myopathy","C. Polymyositis","D. Chronic fatigue syndrome"], mcq_correct="B",
  record="""REFERRAL: GP to rheumatology. Reason: fibromyalgia, meets 2016 criteria, please confirm and advise on management (duloxetine? exercise programme?).
PT: F, 42 y. PMH: depression (remitted), IBS, migraine. Meds: sumatriptan prn, mebeverine prn. FH: mother autoimmune thyroiditis.
HPI: 18 mo widespread pain, both sides, above and below waist, axial. Fatigue 'like walking through mud', wakes unrefreshed, brain fog, cold all the time, constipation worse, weight up 9 kg despite no dietary change, hair thinning. Legs 'heavy' climbing stairs.
EXAM: BMI 31. Dry skin. Bradycardia 54. 14/18 tender points. WPI 12, SSS 9. Proximal lower limb power 4/5, delayed relaxation phase ankle jerks bilaterally. No synovitis. Thyroid mildly enlarged, non-tender.
LABS: Hb 11.9, MCV 96, WBC 6.2, Plt 260, ESR 8, CRP 2, Na 133, K 4.2, Cr 0.9, ALT 44, AST 51, ALP 68, CK 1,450 U/L (ULN 170), LDH 290, ferritin 60, vitamin D 24, B12 380, glucose 95, lipids: total cholesterol 298, LDL 201, TSH 52 mIU/L (0.4-4.0), free T4 5 pmol/L (10-20), anti-TPO 1,850, ANA negative, RF negative, anti-CCP negative.
IMAGING: none.
PLAN (referring): explained fibromyalgia, gave leaflet, considering duloxetine.
QUESTION: What is the most likely primary diagnosis?"""),
 dict(id="C5_la_aha",
  template="lupus anticoagulant", correct="acquired haemophilia A", correct_kw=["acquired h","factor viii inhibitor","fviii inhibitor","factor viii autoantib","anti-factor viii"], template_kw=["lupus anticoagulant","antiphospholipid"],
  vignette="A 58-year-old woman with rheumatoid arthritis on methotrexate presents with a large spontaneous left thigh haematoma and widespread ecchymoses. Platelets are normal, prothrombin time normal, and aPTT 78 seconds; a 1:1 mixing study does not correct after 2 hours of incubation. She has never had a thrombosis. Factor VIII activity is 3 percent and the Bethesda titre is 24 BU. What is the most likely diagnosis?",
  mcq_options=["A. Lupus anticoagulant / antiphospholipid syndrome","B. Acquired haemophilia A","C. Haemophilia A carrier","D. Disseminated intravascular coagulation"], mcq_correct="B",
  record="""REFERRAL: ED to rheumatology (patient known to clinic, RA). Reason: prolonged aPTT not correcting on mixing in RA patient, ? lupus anticoagulant / APS, please advise anticoagulation.
PT: F, 58 y. PMH: seropositive RA 12 yrs (methotrexate 20 mg/wk, folic acid), hypertension. No prior thrombosis, no miscarriages, no prior bleeding.
HPI: 4 days spontaneous painful swelling L thigh, no trauma. Bruises appearing on arms and trunk over 2 wks. Gum bleeding when brushing. No melaena.
EXAM: BP 118/70, HR 96. L thigh tense 12 cm haematoma. Multiple ecchymoses arms, trunk, 2-8 cm. No synovitis. No petechiae.
LABS: Hb 8.9 (was 12.6 3 months ago), MCV 88, WBC 7.9, Plt 228, Cr 0.8, ALT 30, PT 12.1 s (11-13.5), INR 1.0, aPTT 78 s (26-36), fibrinogen 3.8, D-dimer 0.4, mixing study 1:1 immediate: aPTT 52 s, after 2 h incubation at 37 C: 74 s (no correction), thrombin time normal, factor VIII activity 3 % (50-150), factor IX 92 %, factor XI 88 %, factor XII 90 %, von Willebrand Ag 110 %, Bethesda assay: 24 BU, dRVVT screen ratio 1.1 (normal), anticardiolipin IgG/IgM negative, anti-beta2GPI negative.
IMAGING: US L thigh: 12 x 8 cm intramuscular haematoma, no DVT on Doppler.
PLAN (referring): holding methotrexate, considering LMWH prophylaxis given APS query.
QUESTION: What is the most likely diagnosis and should this patient be anticoagulated?"""),
 dict(id="C6_statin_imnm",
  template="statin myopathy", correct="immune-mediated necrotising myopathy", correct_kw=["necroti","imnm","hmgcr","immune-mediated"], template_kw=["statin-induced","statin myopathy","statin-associated","statin induced","toxic myopathy"],
  vignette="A 61-year-old man on atorvastatin 40 mg for three years develops four months of progressive proximal weakness with creatine kinase 8,900 U/L. The statin was stopped ten weeks ago; creatine kinase is now 11,200 U/L, weakness has progressed, and he has new dysphagia. Anti-HMGCR antibodies are strongly positive, electromyography shows an irritable myopathy, and muscle biopsy shows scattered necrotic fibres with minimal inflammatory infiltrate. What is the most likely diagnosis?",
  mcq_options=["A. Statin-induced toxic myopathy, continue observation off statin","B. Anti-HMGCR immune-mediated necrotising myopathy","C. Polymyositis","D. Inclusion body myositis"], mcq_correct="B",
  record="""REFERRAL: GP to rheumatology. Reason: statin myopathy, CK still high 10 weeks after stopping atorvastatin, reassure? re-challenge with rosuvastatin?
PT: M, 61 y. PMH: hyperlipidaemia, hypertension, type 2 diabetes. Meds: metformin 1 g bd, ramipril 10 mg, aspirin 75 mg. Atorvastatin 40 mg for 3 yrs, STOPPED 10 wks ago.
HPI: 4 mo progressive difficulty climbing stairs, rising from chair, lifting arms. Since stopping statin: no improvement, now worse, needs rail on stairs. 3 wks new difficulty swallowing solids. No rash, no Raynaud, no dyspnoea.
EXAM: Proximal power hip flexion 3/5, shoulder abduction 4-/5, neck flexion 4/5, distal 5/5. No rash, no Gottron, no mechanic's hands. Reflexes present. No fasciculations.
LABS: Hb 14.1, WBC 7.4, Plt 231, Cr 0.98, eGFR 82, ALT 118, AST 142, ALP 70, GGT 40, CK 11,200 U/L (was 8,900 10 wks ago, ULN 190), aldolase 41, LDH 610, TSH 2.0, HbA1c 7.1, ANA 1:80 speckled, ENA negative, myositis panel: anti-HMGCR strongly positive (>200 U, ULN 20), anti-SRP negative, anti-Jo1 negative, anti-Mi2 negative.
EMG: irritable myopathy proximal muscles, fibrillations, positive sharp waves, small polyphasic MUAPs.
MUSCLE BIOPSY L vastus lateralis: scattered necrotic and regenerating fibres, myophagocytosis, minimal inflammatory infiltrate, MHC-I diffuse sarcolemmal upregulation, no perifascicular atrophy, no rimmed vacuoles.
IMAGING: MRI thighs: diffuse muscle oedema bilateral quadriceps and adductors.
PLAN (referring): continue statin holiday, repeat CK 3 mo.
QUESTION: What is the most likely diagnosis?"""),
]
