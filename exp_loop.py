import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); DOC="gpt-6-astra"; SIM="gpt-5.6-sol"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=2; MAXT=12
DOC_SYS="""Sei il medico di guardia in un Pronto Soccorso italiano. Hai davanti il paziente e il triage. Non hai altre informazioni: devi costruirle tu.
Ad ogni turno fai UNA sola cosa, in poche righe: una domanda al paziente, oppure una manovra di esame obiettivo specifica, oppure la richiesta di un esame/imaging, oppure una decisione terapeutica immediata. Il sistema ti risponde solo a quello che chiedi.
Quando hai abbastanza elementi, scrivi una riga che inizia con "DECISIONE FINALE:" seguita da diagnosi di lavoro, decisioni immediate e cosa NON fare (max 5 frasi). Hai al massimo 12 turni."""
SIM_SYS="""Simuli il paziente e il mondo del Pronto Soccorso. Hai una CARTELLA NASCOSTA con la verità. Regole:
- Se il medico fa una domanda al paziente, rispondi in prima persona come il paziente, in italiano colloquiale, 1-3 frasi, rivelando SOLO ciò che è stato chiesto e che è nella cartella. Se la domanda tocca un dato nella cartella, rivelalo con naturalezza. Non offrire spontaneamente informazioni non chieste. Il paziente non conosce i termini tecnici e può minimizzare.
- Se il medico esegue una manovra di esame obiettivo, rispondi con "EO: ..." riportando il reperto dalla cartella; se il reperto non è in cartella, "EO: nella norma".
- Se richiede un esame di laboratorio o imaging, rispondi con "RISULTATO: ..." dalla cartella; se non è in cartella, dai un valore normale plausibile.
- Se decide una terapia, rispondi "ESEGUITO." ed eventuale effetto se in cartella.
- Se fa più cose insieme, rispondi solo alla prima.
- Non fare mai diagnosi, non suggerire, non dare ipotesi.
CARTELLA NASCOSTA:
"""
CASES=[
 dict(id="L1_septic_vs_flare",
  triage="TRIAGE 03:40 codice VERDE. Uomo 57 aa. Motivo: 'ginocchio gonfio, ha l'artrite psoriasica, dice che è una riacutizzazione, chiede il cortisone'. PA 128/78 FC 104 T 38.1 SpO2 97% dolore 8/10.",
  hidden="""Uomo 57 aa. Artrite psoriasica dal 2015, in adalimumab dal 2022 (ultima dose 5 gg fa), MTX sospeso per transaminasi. Diabete tipo 2 in metformina. Ginocchio dx gonfio da 2 gg, "come le altre volte ma peggio", ibuprofene senza beneficio. Brividi scuotenti ieri sera (lo dice solo se chiesto di brividi/febbre). Pulizia dei denti 10 giorni fa (solo se chiesto di procedure/dentista/interventi recenti). Episodio simile 2 anni fa trattato con prednisone dal curante. Nega traumi, nega ferite. Nega altri sintomi.
EO ginocchio dx: caldo, versamento abbondante, ROM limitato dal dolore, cute integra. Altre articolazioni: nulla. Cuore: soffio sistolico 2/6 al focolaio aortico, non noto in precedenza (solo se ausculta il cuore). Torace nella norma. Addome nella norma. No porte d'ingresso cutanee.
Esami: GB 14.8 (N 88%), Hb 13.9, PLT 310, PCR 187 mg/L, PCT 1.9, creatinina 1.1, glicemia 214, urato 5.9, lattato 1.6. Emocolture: prelevate, in corso. ECG: sinusale 102. RX ginocchio: versamento, no lesioni ossee.
Artrocentesi (se richiesta): liquido torbido giallo, 68.000 GB/microL 92% PMN, Gram: cocchi Gram positivi in ammassi, nessun cristallo. Coltura in corso.
Ecocardiogramma TT (se richiesto): vegetazione 6 mm sul lembo aortico non coronarico, insufficienza aortica lieve.""",
  rubric='{"aspirated_joint_before_steroid": true if the doctor ordered joint aspiration and did not give steroids before it; "asked_chills_or_fever_history": true if asked about chills/fever; "auscultated_heart_or_found_murmur": true if the doctor examined the heart or the murmur was revealed; "asked_dental_or_procedures": true if asked about recent dental work/procedures; "ordered_echo": true if echocardiography was ordered; "held_adalimumab": true if adalimumab was held; "gave_steroids": true if any corticosteroid was given; "final_septic_arthritis": true if the final decision names septic arthritis as working diagnosis; "final_endocarditis_considered": true if the final decision mentions endocarditis; "final_empirical_antibiotics": true if the final decision includes IV antibiotics after cultures}'),
 dict(id="L2_pe_in_fm",
  triage="TRIAGE 14:05 codice VERDE. Donna 48 aa. Motivo: 'dolori dappertutto, fibromialgia nota, oggi anche al petto, ansiosa'. PA 118/74 FC 112 FR 22 T 36.9 SpO2 93% aa dolore 7/10. Accompagnata dal marito che dice che è sempre così quando è stressata.",
  hidden="""Donna 48 aa. Fibromialgia da 6 anni, depressione in sertralina, emicrania. Fumatrice 15/die. Contraccettivo orale estroprogestinico (solo se chiesto di farmaci/pillola). Rientrata 3 giorni fa da viaggio in auto di 11 ore (solo se chiesto di viaggi/immobilità). Dolore toracico dx da stamattina che aumenta con il respiro (se chiesto delle caratteristiche), fiato corto sulle scale e ora anche a riposo parlando. Gamba sx "un po' gonfia da qualche giorno, pensavo fosse il caldo" (solo se chiesto di gambe/gonfiore). Nega febbre, tosse, emottisi. Piange, è spaventata. Dice "il solito dolore ma questo al petto è diverso" solo se le si chiede se il dolore è come al solito.
EO: tachipnoica a riposo. Torace MV presente, no rumori aggiunti. Cuore: toni ritmici tachicardici, no soffi. Polpaccio sx circonferenza +2.5 cm rispetto al dx, dolente alla palpazione, lieve edema (solo se esamina gli arti inferiori). Tender points diffusi positivi.
Esami: GB 9.1, Hb 13.2, PLT 240, PCR 12, troponina hs 8, D-dimero 2.850 ng/mL, creatinina 0.8, EGA: pO2 66, pCO2 30, pH 7.47. ECG: tachicardia sinusale 110, S1Q3T3 dubbio. RX torace: nella norma.
Angio-TC polmonare (se richiesta): emboli bilaterali lobari e segmentari, rapporto VD/VS 1.1. Ecocolordoppler arti inferiori (se richiesto): trombosi poplitea-femorale sx.""",
  rubric='{"asked_chest_pain_characteristics_or_dyspnoea": true if asked about chest pain character/dyspnoea; "asked_vte_risk_factors": true if asked about pill/hormones, travel/immobility, smoking or previous thrombosis; "examined_legs_or_found_calf": true if the doctor examined the legs or calf swelling was revealed; "ordered_ddimer_or_ctpa": true if D-dimer, CTPA or leg Doppler was ordered; "anticoagulated": true if anticoagulation was started; "final_pe": true if the final decision names pulmonary embolism; "accepted_anxiety": true if the final decision attributes the presentation to anxiety/fibromyalgia}'),
 dict(id="L3_gca_in_pmr",
  triage="TRIAGE 20:15 codice VERDE. Donna 74 aa. Motivo: 'mal di testa da 4 giorni, ha la polimialgia, prende il cortisone'. PA 152/88 FC 78 T 37.2 SpO2 97% dolore 6/10. Accompagnata dalla figlia.",
  hidden="""Donna 74 aa. Polimialgia reumatica diagnosticata 7 mesi fa dal curante, prednisone 15 con ottima risposta, ora 5 mg da 3 settimane. Ipertensione in ramipril. Cefalea temporale bilaterale da 4 gg, "mai avuto mal di testa in vita mia". Stamattina per mezz'ora "vedevo annebbiato dall'occhio destro, poi è passato" (solo se chiesto di vista/occhi). "Mi fa male masticare, mi si stanca la mascella" (solo se chiesto di masticazione/mandibola/mangiare). Cuoio capelluto dolente a pettinarsi (solo se chiesto). Rigidità alle spalle tornata da una settimana (solo se chiesto di spalle/anche/polimialgia). La figlia dice che è confusa la sera (solo se chiesto). Nega traumi. Non prende antiaggreganti.
EO: arteria temporale dx ispessita, ipopulsante, dolente (solo se palpa le temporali). Acuità visiva 10/10 bilaterale ora. Fundus: non esplorabile stanotte, no oftalmologo. Neuro: nulla di focale. Spalle: dolore e limitazione attiva.
Esami: GB 10.2, Hb 11.4, PLT 480, PCR 96 mg/L, VES 88, creatinina 0.9, glicemia 118. TC cranio senza mdc: nella norma.
Ecografia temporali (se richiesta): non disponibile stanotte, disponibile domattina. Biopsia: prenotabile entro 3-5 gg.""",
  rubric='{"asked_visual_symptoms": true if asked about vision/eyes; "asked_jaw_claudication": true if asked about chewing/jaw; "palpated_temporal_arteries": true if temporal arteries were examined; "ordered_crp_or_esr": true if CRP/ESR ordered; "gave_high_dose_steroid_now": true if high-dose glucocorticoid was given tonight (IV methylprednisolone or prednisone >= 40-60 mg / 1 mg/kg); "final_gca": true if final decision names giant cell arteritis; "delayed_steroid_for_tests": true if the doctor explicitly deferred steroids until ultrasound/biopsy/ophthalmology; "accepted_tension_headache": true if final decision attributes to tension/hypertensive headache}'),
 dict(id="L5_pjp_on_mtx",
  triage="TRIAGE 11:20 codice VERDE. Donna 66 aa. Motivo: 'tosse e fiatone da 3 settimane, tampone COVID negativo dal curante, dice che è un virus che non passa. Ha l'artrite reumatoide, prende una pastiglia a settimana e delle punture'. PA 134/80 FC 98 FR 24 T 37.8 SpO2 91% aa dolore 2/10.",
  hidden="""Donna 66 aa. AR da 12 anni. Farmaci (solo se chiesto quali): metotrexato 20 mg sc una volta a settimana, etanercept 50 mg sc settimanale da 4 anni, prednisone 5 mg/die cronico, acido folico. Non fa profilassi per pneumocistite (solo se chiesto di profilassi/bactrim). Tosse secca da 3 settimane, fiatone in salita, peggiorato negli ultimi 4 gg, ora a riposo parlando. Febbricola serale 37.5-38. Amoxicillina 7 gg dal curante senza beneficio. Nega viaggi, nega contatti TB noti, ex fumatrice. Nega dolore toracico, nega edemi, nega emottisi.
EO: tachipnoica a riposo, SpO2 91% aa, 95% con O2 2 L. Crepitii fini bibasali. Cuore nella norma. No edemi. Articolazioni: nulla di attivo.
Esami: GB 6.9 (linfociti 0.6), Hb 12.8, PLT 260, PCR 68, LDH 480, creatinina 1.0, PCT 0.2, BNP 60, D-dimero 500. EGA aa: pO2 58, pCO2 33, pH 7.46. RX torace: tenue accentuazione interstiziale bilaterale, no addensamenti. Beta-D-glucano (se richiesto): 380 pg/mL (positivo). Antigene urinario legionella/pneumococco: negativi. HRCT (se richiesta): vetro smerigliato diffuso bilaterale a distribuzione centrale con risparmio subpleurico. BAL (se richiesto): prenotabile domani; PCR Pneumocystis jirovecii positiva (risultato in 24 h).""",
  rubric='{"asked_which_drugs": true if the doctor asked which specific drugs (revealing methotrexate/etanercept/prednisone); "asked_pjp_prophylaxis": true if asked about prophylaxis; "ordered_ega_or_sat_on_exertion": true if blood gas ordered; "ordered_hrct": true if HRCT chest ordered; "ordered_pjp_test_or_bal": true if beta-D-glucan, PJP PCR or BAL ordered; "started_empirical_cotrimoxazole": true if high-dose cotrimoxazole started; "held_mtx_biologic": true if methotrexate/etanercept were held; "final_pjp_or_mtx_pneumonitis": true if final decision names PJP and/or methotrexate pneumonitis; "discharged": true if final decision discharges the patient}'),
 dict(id="L7_tocilizumab_abdomen",
  triage="TRIAGE 09:50 codice VERDE. Uomo 71 aa. Motivo: 'mal di pancia da 2 giorni, ha l'artrite reumatoide, il curante ieri ha detto che gli esami del sangue sono buoni e di aspettare'. PA 122/76 FC 96 T 37.4 SpO2 98% dolore 5/10. Non sembra sofferente, chiacchiera.",
  hidden="""Uomo 71 aa. AR da 20 anni. Farmaci (solo se chiesto quali): tocilizumab sc settimanale da 3 anni ("la puntura per l'artrite, quella che comincia con t"), prednisone 4 mg/die cronico, ramipril. Diverticolosi nota alla colonscopia del 2023 (solo se chiesto di colonscopia/intestino/diverticoli). Dolore addominale sx da 2 gg, continuo, in aumento, ora in fossa iliaca sx e ipogastrio. Un episodio di vomito. Alvo chiuso a feci da ieri, gas passati. Nega sangue nelle feci. Nega febbre alta. Ha preso paracetamolo.
EO: addome trattabile ma dolente in FIS con reazione di difesa modesta, Blumberg dubbio, peristalsi torpida. Esplorazione rettale: ampolla vuota, no sangue.
Esami: GB 7.8 (N 72%), Hb 12.9, PLT 210, PCR 4 mg/L, creatinina 0.9, lipasi 40, lattato 1.4, esame urine nella norma. RX addome in bianco: qualche livello idroaereo, no aria libera evidente. Ecografia addome (se richiesta): ispessimento parietale sigma, falda liquida pericolica, no versamento libero. TC addome con mdc (se richiesta): diverticolite del sigma con perforazione coperta, ascesso pericolico 3.5 cm, bolle di aria extraluminale.""",
  rubric='{"asked_which_drugs": true if asked which specific drugs (revealing tocilizumab); "recognised_tocilizumab_crp_suppression": true if the doctor stated that tocilizumab/IL-6 blockade masks CRP/fever/leukocytosis; "ordered_ct_abdomen": true if contrast CT abdomen ordered; "surgical_consult": true if surgery consulted; "started_antibiotics": true if IV antibiotics started; "final_complicated_diverticulitis": true if final decision names complicated diverticulitis/perforation/abscess; "discharged_or_short_observation": true if final decision discharges or plans short observation and discharge; "reassured_by_normal_crp": true if the doctor treated the normal CRP as reassuring}'),
 dict(id="L8_atlantoaxial",
  triage="TRIAGE 17:30 codice VERDE. Donna 69 aa. Motivo: 'caduta in casa, ha battuto la nuca contro la vasca, dolore al collo, tipo colpo di frusta. Ha l'artrite reumatoide da una vita, mani deformate'. PA 140/85 FC 82 T 36.6 SpO2 98% GCS 15 dolore 6/10. Deambulante, collare non posizionato al triage.",
  hidden="""Donna 69 aa. AR da 35 anni, sieropositiva erosiva, leflunomide, anni di prednisone. Scivolata in bagno, caduta battendo la nuca contro il bordo della vasca, no perdita di coscienza. Dolore cervicale alto e occipitale. "Formicolio alle mani, ma le ho sempre un po' addormentate" (solo se chiesto di formicolii/sensibilità). Da alcuni mesi "sensazione che la testa cada in avanti" e "scosse elettriche lungo la schiena quando piego il collo" (solo se chiesto di sintomi precedenti al collo, scosse, debolezza, o se chiesto come stava prima della caduta). Non ha mai fatto RX cervicale (solo se chiesto). Deformità mani e piedi.
EO: dolore alla palpazione C1-C2, mobilizza il collo con cautela. Forza 4/5 agli arti superiori (solo se esamina la forza), riflessi vivaci ai 4 arti (solo se esamina i riflessi), Babinski dubbio a sx, Hoffmann positivo bilaterale (solo se cercati), marcia leggermente instabile (solo se osserva la marcia). Cranio: ematoma occipitale, no ferite.
Esami: nulla di rilevante. TC cranio: no emorragia, no fratture della teca. TC rachide cervicale (se richiesta): sublussazione atlanto-assiale anteriore, distanza atlanto-dentale 9 mm, erosione del dente dell'epistrofeo, impressione basilare iniziale, no fratture. RM cervicale (se richiesta): pannus retro-odontoideo con compressione midollare a livello C1-C2, iperintensità midollare intramidollare T2. RX dinamiche: se richieste, il radiologo chiede conferma per rischio.""",
  rubric='{"asked_prior_neck_symptoms_or_paresthesia": true if asked about paraesthesia, weakness, electric shocks, previous neck symptoms; "did_neuro_exam": true if the doctor examined strength, reflexes, Hoffmann/Babinski or gait; "immobilised_cervical_spine": true if a rigid collar/immobilisation was applied before imaging; "ordered_cervical_ct_or_mri": true if cervical CT or MRI was ordered; "ordered_dynamic_xray": true if flexion-extension radiographs were ordered; "neurosurgical_referral": true if neurosurgery/spinal surgery involved; "final_atlantoaxial_myelopathy": true if the final decision names atlantoaxial subluxation/cervical instability with myelopathy; "discharged_with_soft_collar": true if final decision discharges with soft collar}'),
]
def call(model, sysm, hist, effort):
    return c.responses.create(model=model, reasoning={"effort":effort}, instructions=sysm, input=hist).output_text
def run(j):
    case,eff,rep=j
    doc_hist=[{"role":"user","content":case["triage"]+"\n\nIl paziente è davanti a te. Inizia."}]
    sim_hist=[]; transcript=[]; final=None
    for t in range(MAXT):
        d=call(DOC, DOC_SYS, doc_hist, eff); transcript.append(("MEDICO",d)); doc_hist.append({"role":"assistant","content":d})
        if "DECISIONE FINALE" in d.upper(): final=d; break
        sim_hist.append({"role":"user","content":"MEDICO: "+d})
        s=call(SIM, SIM_SYS+case["hidden"], sim_hist, "low"); transcript.append(("MONDO",s)); sim_hist.append({"role":"assistant","content":s})
        doc_hist.append({"role":"user","content":s})
    if final is None:
        doc_hist.append({"role":"user","content":"Turni esauriti. Scrivi ora la DECISIONE FINALE."})
        d=call(DOC, DOC_SYS, doc_hist, eff); transcript.append(("MEDICO",d)); final=d
    tx="\n".join(f"{a}: {b}" for a,b in transcript)
    jr=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this ED consultation transcript (Italian). The doctor's lines are 'MEDICO', the patient/world lines are 'MONDO'. Rubric (booleans):\n{case['rubric']}\n\nTRANSCRIPT:\n{tx}\n\nReturn ONLY the JSON object.").output_text
    m=re.search(r"\{.*\}", jr, re.S)
    try: jd=json.loads(m.group(0))
    except Exception: jd={"parse_error":True}
    return dict(case=case["id"],effort=eff,rep=rep,turns=len([1 for a,_ in transcript if a=="MEDICO"]),transcript=transcript,judge=jd)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser(description="Interactive ED loop with the doctor model (default: the six original scenarios L1-L8). Every run overwrites --out.")
    ap.add_argument("--cases", default="", help="comma-separated case ids from loop_cases.py (e.g. L9_dactylitis_vs_trauma,L10_spondylodiscitis_vs_flare); default = the six built-in cases")
    ap.add_argument("--out", default="exp_loop_results.json"); ap.add_argument("--reps", type=int, default=REPS)
    a=ap.parse_args()
    if a.cases:
        from loop_cases import CASES as ALL
        CASES=[c for c in ALL if c["id"] in a.cases.split(",")]
    REPS=a.reps
    jobs=[(cs,e,r) for cs in CASES for e in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,jobs))
    json.dump(res,open(a.out,"w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(lambda: defaultdict(list)); turns=defaultdict(list)
    for r in res:
        turns[r["case"]].append(r["turns"])
        for k,v in r["judge"].items():
            if isinstance(v,bool): agg[r["case"]][k].append(v)
    for k in sorted(agg): print(k, "turns",turns[k], {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
    x=[r for r in res if r["case"]=="L1_septic_vs_flare" and r["effort"]=="high"][0]
    print("\n===== L1 high rep0 transcript"); 
    for a,b in x["transcript"]: print(f"[{a}] {b[:400]}")
