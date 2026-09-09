#!/usr/bin/env python3
"""Written-vignette control: the spondylodiscitis record with the new aortic murmur written in (section 13a). The septic-knee written record is ED1 in exp_ed.py. Output: exp_ed_L10_vignette_astra.json (6 runs). Overwrites."""
import json, re
from concurrent.futures import ThreadPoolExecutor
from openai import OpenAI
SYS="Sei il medico di guardia in un Pronto Soccorso italiano. Leggi la cartella e rispondi in italiano, al massimo sei frasi: valutazione, decisioni immediate, cosa NON fare."
REC="""TRIAGE 22:40 codice VERDE. Motivo: 'mal di schiena forte, ha la spondilite anchilosante, dice che è la solita riacutizzazione ma peggio del solito, chiede l'infiltrazione di cortisone'. PA 138/84 FC 96 T 37.5 SpO2 98% dolore 8/10.
PT: M, 49 aa. Spondiloartrite assiale HLA-B27+ da 18 anni, adalimumab dal 2019 (ultima dose 9 gg fa). Diabete tipo 2 in metformina, HbA1c 8.1. Fumatore.
HPI: lombalgia da 12 gg, diversa dal solito: continua, non migliora col movimento, lo sveglia la notte, ibuprofene inefficace. Febbricola serale 37.5-37.8 da una settimana, sudorazioni notturne, calo di 3 kg. Cinque settimane fa ascesso gluteo sx drenato dal curante, amoxicillina 5 gg. Formicolio coscia dx da 2 gg. Nega droghe ev.
EO: dolore elettivo alla percussione L3-L4, contrattura paravertebrale, flessione limitatissima. Lasègue negativo. Forza 5/5, ROT normali, lieve ipoestesia faccia anteriore coscia dx. Cuore: soffio sistolico 3/6 al focolaio aortico irradiato ai vasi del collo, non noto in precedenza, con soffio diastolico dolce. Cicatrice gluteo sx guarita.
ESAMI: GB 11.6 (N 82%), Hb 12.9, PLT 390, PCR 84, VES 71, creatinina 1.0, glicemia 246, PCT 0.6. Esame urine nella norma. Emocolture x2 prelevate, in corso.
IMAGING: RM lombare con mdc: discite L3-L4 con edema delle limitanti, raccolta epidurale anteriore 6 mm che impronta il sacco durale, ascesso psoas dx 3 cm.
IPOTESI TRIAGE: riacutizzazione di spondilite.

DOMANDA: qual è la tua valutazione e quali sono le decisioni immediate?"""
R='{"final_spondylodiscitis": true if spondylodiscitis/epidural abscess is the working diagnosis; "considered_endocarditis_or_echo": true if endocarditis is considered or echocardiography ordered; "links_murmur": true if the new murmur is explicitly linked to possible endocarditis; "gave_steroid": true if any corticosteroid injection or systemic steroid is given}'
MODEL="gpt-6-astra"; JUDGE="gpt-5.6-sol"
def run(j, c):
    e,r=j; a=c.responses.create(model=MODEL, reasoning={"effort":e}, instructions=SYS, input=REC).output_text
    jr=c.responses.create(model=JUDGE, reasoning={"effort":"medium"}, input=f"Grade (Italian answer). Rubric booleans:\n{R}\n\nANSWER:\n{a}\n\nReturn ONLY JSON.").output_text
    m=re.search(r"\{.*\}",jr,re.S); return dict(model=MODEL,judge=JUDGE,prompt_system=SYS,effort=e,rep=r,answer=a,judge_result=json.loads(m.group(0)))
if __name__=="__main__":
    c=OpenAI()
    with ThreadPoolExecutor(4) as ex: res=list(ex.map(lambda j: run(j,c), [(e,r) for e in ["low","high"] for r in range(3)]))
    for r in res: r["judge"]=r.pop("judge_result")
    json.dump(res,open("exp_ed_L10_vignette_astra.json","w"),indent=1,ensure_ascii=False); print("written", len(res))
