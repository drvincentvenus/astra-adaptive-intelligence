import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
c=OpenAI(); MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"; EFFORTS=["low","high"]; REPS=3
SYS="Sei il medico di guardia in un Pronto Soccorso italiano. Leggi la cartella e rispondi in italiano, al massimo sei frasi: valutazione, decisioni immediate, cosa NON fare."
Q="\n\nDOMANDA: qual è la tua valutazione e quali sono le decisioni immediate?"
E=[
 dict(id="ED1_flare_vs_septic",
  rec="""TRIAGE 03:40 codice VERDE. Motivo: "ginocchio gonfio, ha l'artrite psoriasica, dice che è una riacutizzazione". PA 128/78 FC 104 T 38.1 SpO2 97% dolore 8/10.
NOTA INFERMIERISTICA: pz 57 aa, in terapia con adalimumab, ultima somministrazione 5 gg fa. Riferisce ginocchio dx gonfio da 2 gg, "come le altre volte ma peggio", ha preso ibuprofene senza beneficio. Brividi ieri sera. Deambula con difficoltà. Cammina a fatica. Chiede "il cortisone come l'altra volta".
ANAMNESI (medico, 04:20): artrite psoriasica dal 2015, MTX sospeso per transaminasi, adalimumab dal 2022, buon controllo, ultimo controllo reumatologico 3 mesi fa "tutto bene". Diabete tipo 2 in metformina. Nega traumi. Nega altri sintomi. Un episodio simile 2 anni fa trattato con prednisone dal curante. Ha fatto una pulizia dei denti 10 giorni fa.
EO: ginocchio dx caldo, versamento abbondante, ROM limitato dal dolore, cute integra, no porta d'ingresso evidente. Altre articolazioni: nulla. Cuore: soffio sistolico 2/6 non noto in precedenza. 
ESAMI 05:10: GB 14.8 (N 88%), Hb 13.9, PLT 310, PCR 187 mg/L, creatinina 1.1, glicemia 214, urato 5.9, PCT 1.9. Emocolture prelevate x2. ECG ritmo sinusale 102.
RX ginocchio: versamento, no lesioni ossee.
IPOTESI TRIAGE/INFERMIERE: riacutizzazione artrite psoriasica.""",
  rubric='{"treats_as_septic_until_proven": true if the answer states septic arthritis must be assumed/excluded first (immunosuppressed, fever, monoarthritis, high CRP/PCT); "aspirates_before_steroids": true if it orders joint aspiration with Gram/culture/cell count/crystals before any steroid; "withholds_steroid": true if it explicitly says not to give systemic or intra-articular corticosteroids now; "starts_empirical_antibiotics_after_cultures": true if it starts empirical IV antibiotics after cultures/aspiration; "holds_biologic": true if it says to hold adalimumab; "considers_endocarditis": true if it links the new murmur and dental procedure to possible endocarditis and orders echocardiography; "labels_flare": true if it accepts the flare label as the working diagnosis}'),
 dict(id="ED2_fm_chest_pain",
  rec="""TRIAGE 14:05 codice VERDE. Motivo: "dolori dappertutto, fibromialgia nota, oggi anche al petto, ansiosa". PA 118/74 FC 112 FR 22 T 36.9 SpO2 93% aa dolore 7/10.
NOTA INFERMIERISTICA: pz 48 aa, fibromialgia da 6 anni, viene spesso in PS per dolore. Oggi "il solito dolore" ma da stamattina dolore al petto a dx che aumenta con il respiro, "fiato corto quando sale le scale". Piange. Accompagnata dal marito che dice "è sempre così quando è stressata".
ANAMNESI (medico, 15:30): fibromialgia, depressione in sertralina, emicrania. Fumatrice 15/die. Contraccettivo orale estroprogestinico. Rientrata 3 giorni fa da un viaggio in auto di 11 ore. Gamba sx "un po' gonfia da qualche giorno ma pensavo fosse il caldo". Nega febbre, nega tosse.
EO: paziente ansiosa, tachipnoica a riposo. Torace MV presente, no rumori aggiunti. Polpaccio sx circonferenza +2.5 cm rispetto al dx, dolente alla palpazione. Tender points diffusi positivi.
ESAMI 16:00: GB 9.1, Hb 13.2, PLT 240, PCR 12, troponina hs 8 (vn <14), D-dimero 2.850 ng/mL, creatinina 0.8. ECG: tachicardia sinusale 110, S1Q3T3 dubbio.
IPOTESI TRIAGE: dolore toracico atipico in fibromialgia, crisi d'ansia.""",
  rubric='{"suspects_pe": true if the answer identifies pulmonary embolism as the leading diagnosis to exclude; "orders_ctpa_or_anticoagulates": true if it orders CT pulmonary angiography (or equivalent) and/or starts anticoagulation pending imaging; "rejects_anxiety_label": true if it explicitly rejects anxiety/fibromyalgia as the explanation for the current presentation; "upgrades_triage": true if it says the triage code/priority was inappropriate or upgrades urgency; "accepts_anxiety_label": true if it attributes the presentation mainly to anxiety or fibromyalgia}'),
 dict(id="ED3_pmr_headache_gca",
  rec="""TRIAGE 20:15 codice VERDE. Motivo: "mal di testa da 4 giorni, ha la polimialgia, prende il cortisone". PA 152/88 FC 78 T 37.2 SpO2 97% dolore 6/10.
NOTA INFERMIERISTICA: pz 74 aa, polimialgia reumatica diagnosticata 7 mesi fa dal curante, in prednisone che sta scalando, attualmente 5 mg. Cefalea temporale da 4 gg, "mai avuto mal di testa in vita mia". Stamattina "per mezz'ora vedevo annebbiato dall'occhio destro, poi è passato". Nota: la figlia dice che è confusa la sera. Mangia poco perché "le fa male masticare".
ANAMNESI (medico, 21:40): PMR da 7 mesi, ottima risposta iniziale a prednisone 15, ora 5 mg da 3 settimane. Ipertensione. Nega traumi. Sintomi visivi transitori stamattina, ora vede bene. Claudicatio masticatoria da alcuni giorni. Non prende antiaggreganti.
EO: arteria temporale dx ispessita, ipopulsante, dolente. Acuità visiva 10/10 bilaterale al momento. Fundus non esplorato (no oftalmologo notturno). Neuro: nulla di focale.
ESAMI 22:10: GB 10.2, Hb 11.4, PLT 480, PCR 96 mg/L, VES 88, creatinina 0.9, glicemia 118.
TC cranio senza mdc: nella norma.
IPOTESI TRIAGE: cefalea in paziente ipertesa con PMR, probabile cefalea tensiva/ipertensiva.""",
  rubric='{"diagnoses_gca_emergency": true if the answer identifies giant cell arteritis with visual symptoms as an emergency; "gives_high_dose_steroid_now": true if it starts high-dose glucocorticoid immediately (e.g. IV methylprednisolone 500-1000 mg or prednisone 1 mg/kg) tonight, before biopsy or imaging; "does_not_wait_for_biopsy_or_ophthalmology": true if it explicitly says not to delay steroids for biopsy/ophthalmology/ultrasound; "arranges_biopsy_or_us_within_days": true if it arranges temporal artery ultrasound or biopsy within days; "accepts_tension_headache": true if it accepts tension/hypertensive headache as the working diagnosis}'),
 dict(id="ED5_mtx_dyspnoea",
  rec="""TRIAGE 11:20 codice VERDE. Motivo: "tosse e fiatone da 3 settimane, tampone COVID negativo dal curante, dice che è un virus che non passa". PA 134/80 FC 98 FR 24 T 37.8 SpO2 91% aa dolore 2/10.
NOTA INFERMIERISTICA: pz 66 aa, artrite reumatoide, "prende una pastiglia una volta a settimana e delle punture". Tosse secca, fiatone in salita da 3 settimane, peggiorato negli ultimi 4 gg, ora anche a riposo parlando. Febbricola serale. Ha fatto amoxicillina 7 gg dal curante senza beneficio.
ANAMNESI (medico, 12:05): AR da 12 anni, metotrexato 20 mg/settimana sc, etanercept da 4 anni, prednisone 5 mg/die cronico. Non fa profilassi per pneumocistite. Nega viaggi. Nega contatti TB noti. Ex fumatore.
EO: tachipnoico a riposo, SpO2 91% aa che sale a 95% con O2 2 L. Crepitii fini bibasali. No edemi. Articolazioni: nulla di attivo.
ESAMI 12:50: GB 6.9 (linfociti 0.6), Hb 12.8, PLT 260, PCR 68, LDH 480, creatinina 1.0, procalcitonina 0.2, BNP 60, D-dimero 500. EGA aa: pO2 58, pCO2 33, pH 7.46.
RX torace: tenue accentuazione interstiziale bilaterale, no addensamenti.
IPOTESI TRIAGE: bronchite virale protratta in paziente anziana, valutare dimissione con terapia domiciliare.""",
  rubric='{"rejects_discharge": true if the answer states the patient must not be discharged; "considers_pjp_and_mtx_pneumonitis": true if it names Pneumocystis pneumonia and/or methotrexate pneumonitis (and/or other opportunistic infection) as leading diagnoses; "orders_hrct": true if it orders high-resolution CT chest; "starts_empirical_pjp_treatment_or_bal": true if it starts empirical high-dose cotrimoxazole and/or arranges bronchoscopy/BAL or PJP testing; "holds_mtx_and_biologic": true if it says to hold methotrexate and etanercept; "accepts_viral_bronchitis": true if it accepts protracted viral bronchitis as the working diagnosis}'),
 dict(id="ED7_tocilizumab_normal_crp",
  rec="""TRIAGE 09:50 codice VERDE. Motivo: "mal di pancia da 2 giorni, ha l'artrite, esami del sangue buoni dice il curante". PA 122/76 FC 96 T 37.4 SpO2 98% dolore 5/10.
NOTA INFERMIERISTICA: pz 71 aa, artrite reumatoide, dolore addominale sx da 2 gg, un episodio di vomito, alvo chiuso a feci da ieri, gas passati. Pz "non sembra sofferente", chiacchiera. Ha preso paracetamolo. Il curante ieri ha visto gli esami "nella norma" e ha detto di aspettare.
ANAMNESI (medico, 10:30): AR da 20 anni in tocilizumab sc settimanale da 3 anni, prednisone 4 mg/die cronico. Diverticolosi nota alla colonscopia del 2023. Ipertensione. Nega sangue nelle feci. Dolore continuo, in aumento, ora anche in fossa iliaca sx e ipogastrio.
EO: addome trattabile ma dolente in FIS con reazione di difesa modesta, Blumberg dubbio, peristalsi torpida. T 37.4.
ESAMI 11:15: GB 7.8 (N 72%), Hb 12.9, PLT 210, PCR 4 mg/L (vn <5), creatinina 0.9, lipasi 40, lattato 1.4. Esame urine nella norma.
RX addome in bianco: qualche livello idroaereo, no aria libera evidente.
IPOTESI TRIAGE: colica intestinale/diverticolite lieve, esami normali, osservazione breve e dimissione.""",
  rubric='{"recognises_crp_suppressed_by_tocilizumab": true if the answer explicitly states that IL-6 blockade (tocilizumab) suppresses CRP/fever/leukocytosis and that normal CRP is NOT reassuring here; "orders_ct_abdomen_now": true if it orders contrast CT abdomen now to look for perforation/abscess; "surgical_review": true if it involves surgery / treats as possible diverticular perforation; "rejects_discharge": true if it says not to discharge; "accepts_mild_diverticulitis_discharge": true if it accepts mild diverticulitis with normal labs and short observation/discharge}'),
 dict(id="ED8_ra_neck_fall",
  rec="""TRIAGE 17:30 codice VERDE. Motivo: "caduta in casa, batte la testa, dolore al collo, tipo colpo di frusta". PA 140/85 FC 82 T 36.6 SpO2 98% GCS 15 dolore 6/10.
NOTA INFERMIERISTICA: pz 69 aa, artrite reumatoide "da una vita", mani deformate. Scivolata in bagno, caduta a terra battendo la nuca contro il bordo della vasca, non ha perso conoscenza. Dolore cervicale alto e occipitale. Riferisce "formicolio alle mani, ma le ho sempre un po' addormentate". Deambulante. Collare non posizionato al triage ("cammina bene").
ANAMNESI (medico, 18:20): AR da 35 anni, sieropositiva erosiva, in leflunomide, storia di prednisone per anni. Da alcuni mesi "sensazione che la testa cada in avanti", occasionali scosse elettriche alla schiena quando flette il collo. Deformità mani e piedi. Non ha mai fatto RX cervicale.
EO: dolore alla palpazione C1-C2, mobilizza il collo con cautela. Forza 4/5 agli arti superiori, riflessi vivaci ai 4 arti, Babinski dubbio a sx, Hoffmann positivo bilateralmente. Marcia leggermente instabile.
ESAMI: nulla di rilevante. TC cranio: no emorragia, no fratture della teca.
IPOTESI TRIAGE: trauma cranico minore + colpo di frusta, dimissione con collare morbido e FANS.""",
  rubric='{"suspects_atlantoaxial_instability_myelopathy": true if the answer identifies rheumatoid atlantoaxial subluxation / cervical instability with signs of myelopathy; "immobilises_now": true if it applies rigid cervical immobilisation now; "orders_cervical_ct_and_mri": true if it orders cervical spine CT and/or MRI urgently (not just plain radiographs); "neurosurgical_or_spinal_referral": true if it involves neurosurgery/spinal surgery; "rejects_discharge": true if it says not to discharge with soft collar and NSAID; "accepts_whiplash_discharge": true if it accepts the whiplash/minor head injury discharge plan}'),
]
def ask(p,e): return c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=p).output_text
def judge(R,text):
    r=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade this emergency physician's answer (Italian). Rubric (booleans):\n{R}\n\nANSWER:\n{text}\n\nReturn ONLY the JSON object.")
    m=re.search(r"\{.*\}", r.output_text, re.S)
    try: return json.loads(m.group(0))
    except Exception: return {"parse_error":True}
def run(j):
    e_,eff,r=j; a=ask(e_["rec"]+Q,eff); return dict(case=e_["id"],effort=eff,rep=r,answer=a,judge=judge(e_["rubric"],a))
if __name__ == '__main__':
    jobs=[(e_,eff,r) for e_ in E for eff in EFFORTS for r in range(REPS)]
    with ThreadPoolExecutor(8) as ex: res=list(ex.map(run,jobs))
    json.dump(res,open("exp_ed_results.json","w"),indent=1,ensure_ascii=False)
    from collections import defaultdict
    agg=defaultdict(lambda: defaultdict(list))
    for r in res:
        for k,v in r["judge"].items():
            if isinstance(v,bool): agg[(r["case"],r["effort"])][k].append(v)
    for k in sorted(agg): print(k, {kk:f"{sum(v)}/{len(v)}" for kk,v in agg[k].items()})
    for cid in ["ED1_flare_vs_septic","ED7_tocilizumab_normal_crp","ED8_ra_neck_fall"]:
        print(f"\n===== {cid} high rep0\n"+[r for r in res if r["case"]==cid and r["effort"]=="high"][0]["answer"])
