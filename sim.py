#!/usr/bin/env python3
"""World simulator CLI for the ED loop. Usage:
  python3 sim.py start <case_id> <run_id>      -> prints the triage
  python3 sim.py act <case_id> <run_id> "<one action>"  -> prints the world's response
  python3 sim.py final <case_id> <run_id> "<DECISIONE FINALE ...>" -> records and closes
Do NOT read any other file in this folder."""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from openai import OpenAI
from loop_cases import CASES
from exp_loop import SIM_SYS
c=OpenAI(); SIM="gpt-5.6-sol"; MAXT=12
cmd, cid, run = sys.argv[1], sys.argv[2], sys.argv[3]
case={x["id"]:x for x in CASES}[cid]
path=f"loop_sessions/{cid}_{run}.json"
st=json.load(open(path)) if os.path.exists(path) else {"case":cid,"run":run,"sim_hist":[],"transcript":[],"final":None}
if cmd=="start":
    print(case["triage"]+"\n\nIl paziente è davanti a te. Hai al massimo 12 azioni. Inizia.")
elif cmd=="act":
    if st["final"]: print("Sessione chiusa."); sys.exit()
    n=len([1 for a,_ in st["transcript"] if a=="MEDICO"])
    if n>=MAXT: print("Turni esauriti. Devi dare la DECISIONE FINALE con: python3 sim.py final ..."); sys.exit()
    action=sys.argv[4]; st["transcript"].append(("MEDICO",action)); st["sim_hist"].append({"role":"user","content":"MEDICO: "+action})
    r=c.responses.create(model=SIM, reasoning={"effort":"low"}, instructions=SIM_SYS+case["hidden"], input=st["sim_hist"]).output_text
    st["transcript"].append(("MONDO",r)); st["sim_hist"].append({"role":"assistant","content":r})
    print(r+f"\n[azioni usate: {n+1}/{MAXT}]")
elif cmd=="final":
    st["transcript"].append(("MEDICO",sys.argv[4])); st["final"]=sys.argv[4]; print("Decisione registrata. Sessione chiusa.")
json.dump(st,open(path,"w"),ensure_ascii=False,indent=1)
